#version 330 core

layout(location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float time;
uniform bool waveEnabled;

void main()
{
    vec3 pos = aPos;
    if (waveEnabled) {
        pos.z += time;
    }
    gl_Position = projection * view * model * vec4(pos, 1.0);
}
