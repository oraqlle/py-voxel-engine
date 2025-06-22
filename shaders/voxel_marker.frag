#version 330 core

layout (location = 0) out vec4 fragColour;

in vec3 marker_colour;
in vec2 uv;

uniform sampler2D u_texture_0;

void main() {
    fragColour = texture(u_texture_0, uv);
    fragColour.rgb += marker_colour;
    fragColour.a = (fragColour.r + fragColour.b > 1.0) ? 0.0 : 1.0;
}
