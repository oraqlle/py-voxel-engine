#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_colour;

out vec3 colour;

void main() {
    colour = in_colour;
    gl_Position = vec4(in_position, 1.0);
}
