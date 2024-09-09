#version 330

in vec2 fragCoord;
out vec4 fragColor;
uniform sampler2D textureSampler;

const float M_PI = 3.1415926535897932;
const float M_E = 2.7182818284590452;

// Max longitude in the equirectangular projection
// 2*atan(e^pi)-pi/2
const float EQUI_LON = 1.4844222297453324;

float remap(float value, float oldMin, float oldMax, float newMin, float newMax)
{
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
}

vec2 merc_to_equi(float u, float v)
{
    // uv to mercator
    float lon = remap(v, 0, 1, -M_PI, M_PI);

    // mercator to equirectangular
    float y = 2 * atan(pow(M_E, lon)) - M_PI * 0.5;

    // equirectangular to uv
    y = remap(y, -EQUI_LON, EQUI_LON, 0, 1);

    return vec2(u, y);
}

void main()
{
    vec2 uv = merc_to_equi(fragCoord.x, fragCoord.y);
    fragColor = texture(textureSampler, uv);
}