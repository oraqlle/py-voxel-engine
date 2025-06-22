import moderngl as mgl
import glm


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.ctx = app.ctx

        # -------- shaders -------- #
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
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

    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)

    def get_program(self, shader_name: str) -> mgl.Program:
        with open(f'shaders/{shader_name}.vert') as vert:
            vertex_shader = vert.read()

        with open(f'shaders/{shader_name}.frag') as frag:
            fragment_shader = frag.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
