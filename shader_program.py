import moderngl as mgl
import glm


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.ctx = app.ctx

        # -------- shaders -------- #
        self.quad = self.get_program(shader_name='quad')
        # ------------------------- #

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        self.quad['m_proj'].write(self.player.m_proj)
        self.quad['m_model'].write(glm.mat4())

    def update(self):
        self.quad['m_view'].write(self.player.m_view)

    def get_program(self, shader_name: str) -> mgl.Program:
        with open(f'shaders/{shader_name}.vert') as vert:
            vertex_shader = vert.read()

        with open(f'shaders/{shader_name}.frag') as frag:
            fragment_shader = frag.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
