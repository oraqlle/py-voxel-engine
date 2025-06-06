from settings import *
import moderngl as mgl


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # -------- shaders -------- #
        self.quad = self.get_program(shader_name='quad')
        # ------------------------- #

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        pass

    def update(self):
        pass

    def get_program(self, shader_name: str) -> mgl.Program:
        with open(f'shaders/{shader_name}.vert') as vert:
            vertex_shader = vert.read()

        with open(f'shaders/{shader_name}.frag') as frag:
            fragment_shader = frag.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

