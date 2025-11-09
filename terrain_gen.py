import math
import settings as cfg
from noise import noise2, noise3
from random import random
from numba import njit


@njit
def get_height(x, z):
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - cfg.CENTER_XZ, z - cfg.CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = cfg.CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height, 1)
    height *= island

    return int(height)


@njit
def get_index(x, y, z):
    return x + cfg.CHUNK_SIZE * z + cfg.CHUNK_AREA * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = 0

    if wy < world_height - 1:
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and
                noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = 0
        else:
            voxel_id = cfg.STONE
    else:
        rnd = int(7 * random())
        ry = wy - rnd

        if cfg.SNOW_LVL <= ry < world_height:
            voxel_id = cfg.SNOW
        elif cfg.STONE_LVL <= ry < cfg.SNOW_LVL:
            voxel_id = cfg.STONE
        elif cfg.DIRT_LVL <= ry < cfg.STONE_LVL:
            voxel_id = cfg.DIRT
        elif cfg.GRASS_LVL <= ry < cfg.DIRT_LVL:
            voxel_id = cfg.GRASS
        else:
            voxel_id = cfg.SAND

    voxels[get_index(x, y, z)] = voxel_id

    # place tree
    if wy < cfg.DIRT_LVL:
        place_tree(voxels, x, y, z, voxel_id)


@njit
def place_tree(voxels, x, y, z, voxel_id):
    rnd = random()

    if voxel_id != cfg.GRASS or rnd > cfg.TREE_PROB:
        return None

    if y + cfg.TREE_HEIGHT >= cfg.CHUNK_SIZE:
        return None

    if x - cfg.TREE_H_WIDTH < 0 or x + cfg.TREE_H_WIDTH >= cfg.CHUNK_SIZE:
        return None

    if z - cfg.TREE_H_WIDTH < 0 or z + cfg.TREE_H_WIDTH >= cfg.CHUNK_SIZE:
        return None

    # dirt under tree
    voxels[get_index(x, y, z)] = cfg.DIRT

    # leaves
    m = 0
    for n, iy in enumerate(range(cfg.TREE_H_HEIGHT, cfg.TREE_HEIGHT - 1)):
        k = iy % 2
        rnd2 = int(random() * 2)
        for ix in range(-cfg.TREE_H_WIDTH + m, cfg.TREE_H_WIDTH - m * rnd2):
            for iz in range(-cfg.TREE_H_WIDTH + m * rnd2, cfg.TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = cfg.LEAVES

            m += 1 if n > 0 else 3 if n > 1 else 0

    # trunk
    for iy in range(1, cfg.TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = cfg.WOOD

    # top
    voxels[get_index(x, y + cfg.TREE_HEIGHT - 2, z)] = cfg.LEAVES
