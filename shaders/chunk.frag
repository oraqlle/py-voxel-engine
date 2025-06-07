#version 330 core

layout (location = 0) out vec4 fragColour;

uniform sampler2D u_texture_0;

in vec3 voxel_colour;
in vec2 uv;

void main() {
    vec3 tex_col = texture(u_texture_0, uv).rgb;
    fragColour = vec4(tex_col, 1);
}

