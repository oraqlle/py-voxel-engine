import settings as cfg
import numpy as np
from world_objects.chunk import Chunk
from voxel_hander import VoxelHandler


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(cfg.WORLD_VOL)]
        self.voxels = np.empty([cfg.WORLD_VOL, cfg.CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        for x in range(cfg.WORLD_W):
            for y in range(cfg.WORLD_H):
                for z in range(cfg.WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + cfg.WORLD_W * z + cfg.WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunks voxels in seperate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
