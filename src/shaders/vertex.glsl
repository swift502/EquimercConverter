#version 330
in vec2 in_vert;
out vec2 fragCoord;
void main()
{
    gl_Position = vec4(in_vert, 0.0, 1.0);
    fragCoord = (in_vert + 1) / 2;
}