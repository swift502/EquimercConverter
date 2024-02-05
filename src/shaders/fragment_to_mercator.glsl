#version 330
in vec2 fragCoord;
out vec4 fragColor;
uniform sampler2D texture;

#define M_PI 3.1415926535897932384626433832795
#define M_E 2.7182818284590452353602874713527

float remap(float value, float oldMin, float oldMax, float newMin, float newMax)
{
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
}

vec2 merc_to_equi(float u, float v)
{
    // uv to mercator
    float lat = remap(u, 0, 1, 0, 2 * M_PI);
    float lon = remap(v, 0, 1, -M_PI, M_PI);

    // mercator to equirectangular
    float x = lat;
    float y = 2 * atan(pow(M_E, lon)) - M_PI * 0.5;

    // equirectangular to uv
    x = remap(x, 0, 2 * M_PI, 0, 1);
    y = remap(y, -M_PI * 0.5, M_PI * 0.5, 0, 1);

    return vec2(x, y);
}

void main()
{
    vec2 uv = merc_to_equi(fragCoord.x, fragCoord.y);
    fragColor = texture2D(texture, uv);
}