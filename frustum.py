import glm
import math
from settings import NEAR, FAR, V_FOV, H_FOV, CHUNK_SPHERE_RADIUS


class Frustum:
    def __init__(self, camera):
        self.cam = camera

        self.factor_y = 1.0 / math.cos(half_y := V_FOV * 0.5)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV * 0.5)
        self.tan_x = math.tan(half_x)

    def is_on_frustum(self, chunk) -> bool:
        # vector to sphere center
        sphere_vec = chunk.center - self.cam.position

        # check if outside the NEAR and FAR planes
        sz = glm.dot(sphere_vec, self.cam.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        # check if outside TOP and BOTTOM planes
        sy = glm.dot(sphere_vec, self.cam.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y

        if not (-dist <= sy <= dist):
            return False

        # check if outside LEFT and RIGHT planes
        sx = glm.dot(sphere_vec, self.cam.up)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x

        if not (-dist <= sx <= dist):
            return False

        return True
