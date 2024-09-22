#version 330
in vec3 position;
in vec3 color;

uniform mat4 translate;
uniform mat4 scale;

out vec3 fragColor;

void main()
{
    fragColor = color;
    gl_Position = translate * scale * vec4(position, 1.0f);
}