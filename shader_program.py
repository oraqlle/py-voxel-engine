import moderngl as mgl
import glm
from settings import (
    BG_COLOUR,
    CENTER_XZ,
    WATER_LINE,
    WATER_AREA,
    CLOUD_SCALE,
)


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.ctx = app.ctx

        # -------- shaders -------- #
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
        self.water = self.get_program(shader_name='water')
        self.clouds = self.get_program(shader_name='clouds')
        # ------------------------- #

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        # chunk
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_array_0'] = 1

        # marker
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0

        # water
        self.water['m_proj'].write(self.player.m_proj)
        self.water['u_texture_0'] = 2
        self.water['water_area'] = WATER_AREA
        self.water['water_line'] = WATER_LINE

        # clouds
        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center'] = CENTER_XZ
        self.clouds['bg_color'].write(BG_COLOUR)
        self.clouds['cloud_scale'] = CLOUD_SCALE

    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.water['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)

    def get_program(self, shader_name: str) -> mgl.Program:
        with open(f'shaders/{shader_name}.vert') as vert:
            vertex_shader = vert.read()

        with open(f'shaders/{shader_name}.frag') as frag:
            fragment_shader = frag.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
