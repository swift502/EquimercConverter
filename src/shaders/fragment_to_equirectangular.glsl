#version 330
in vec2 fragCoord;
out vec4 fragColor;
uniform sampler2D texture;

#define M_PI 3.1415926535897932
#define M_E 2.7182818284590452
#define M_MAX 1.4844222297453324

float remap(float value, float oldMin, float oldMax, float newMin, float newMax)
{
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
}

vec2 equi_to_merc(float u, float v)
{
    // uv to equirectangular
    float lon = remap(v, 0, 1, -M_MAX, M_MAX);

    // equirectangular to mercator
    float y = log(tan(M_PI / 4 + lon / 2));

    // mercator to uv
    y = remap(y, -M_PI, M_PI, 0, 1);

    return vec2(u, y);
}

void main()
{
    vec2 uv = equi_to_merc(fragCoord.x, fragCoord.y);
    fragColor = texture2D(texture, uv);
}