#version 330 core

layout (location = 0) out vec4 fragColour;

in vec3 voxel_colour;

void main() {
    fragColour = vec4(voxel_colour, 1);
}

