#version 330

in vec2 fragCoord;
out vec4 fragColor;
uniform sampler2D textureSampler;

uniform sampler2D tDiffuse;
uniform vec2 resolution;
varying vec2 vUv;

#define EDGE_STEP_COUNT 10
#define EDGE_GUESS 8.0
#define EDGE_STEPS 1.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.0
const float edgeSteps[EDGE_STEP_COUNT] = float[EDGE_STEP_COUNT]( EDGE_STEPS );

float _ContrastThreshold = 0.0312;
float _RelativeThreshold = 0.063;
float _SubpixelBlending = 1.0;

vec4 Sample(sampler2D  tex2D, vec2 uv)
{
    return texture(tex2D, uv);
}

float SampleLuminance(sampler2D tex2D, vec2 uv)
{
    return dot(Sample(tex2D, uv).rgb, vec3(0.3, 0.59, 0.11));
}

float SampleLuminance(sampler2D tex2D, vec2 texSize, vec2 uv, float uOffset, float vOffset)
{
    uv += texSize * vec2(uOffset, vOffset);
    return SampleLuminance(tex2D, uv);
}

struct LuminanceData
{
    float m, n, e, s, w;
    float ne, nw, se, sw;
    float highest, lowest, contrast;
};

LuminanceData SampleLuminanceNeighborhood(sampler2D tex2D, vec2 texSize, vec2 uv)
{
    LuminanceData l;
    l.m = SampleLuminance(tex2D, uv);
    l.n = SampleLuminance(tex2D, texSize, uv,  0.0,  1.0);
    l.e = SampleLuminance(tex2D, texSize, uv,  1.0,  0.0);
    l.s = SampleLuminance(tex2D, texSize, uv,  0.0, -1.0);
    l.w = SampleLuminance(tex2D, texSize, uv, -1.0,  0.0);

    l.ne = SampleLuminance(tex2D, texSize, uv,  1.0,  1.0);
    l.nw = SampleLuminance(tex2D, texSize, uv, -1.0,  1.0);
    l.se = SampleLuminance(tex2D, texSize, uv,  1.0, -1.0);
    l.sw = SampleLuminance(tex2D, texSize, uv, -1.0, -1.0);

    l.highest = max(max(max(max(l.n, l.e), l.s), l.w), l.m);
    l.lowest = min(min(min(min(l.n, l.e), l.s), l.w), l.m);
    l.contrast = l.highest - l.lowest;
    return l;
}

bool ShouldSkipPixel(LuminanceData l)
{
    float threshold = max(_ContrastThreshold, _RelativeThreshold * l.highest);
    return l.contrast < threshold;
}

float DeterminePixelBlendFactor(LuminanceData l)
{
    float f = 2.0 * (l.n + l.e + l.s + l.w);
    f += l.ne + l.nw + l.se + l.sw;
    f *= 1.0 / 12.0;
    f = abs(f - l.m);
    f = clamp(f / l.contrast, 0.0, 1.0);

    float blendFactor = smoothstep(0.0, 1.0, f);
    return blendFactor * blendFactor * _SubpixelBlending;
}

struct EdgeData
{
    bool isHorizontal;
    float pixelStep;
    float oppositeLuminance, gradient;
};

EdgeData DetermineEdge(vec2 texSize, LuminanceData l)
{
    EdgeData e;
    float horizontal =
        abs(l.n + l.s - 2.0 * l.m) * 2.0 +
        abs(l.ne + l.se - 2.0 * l.e) +
        abs(l.nw + l.sw - 2.0 * l.w);
    float vertical =
        abs(l.e + l.w - 2.0 * l.m) * 2.0 +
        abs(l.ne + l.nw - 2.0 * l.n) +
        abs(l.se + l.sw - 2.0 * l.s);
    e.isHorizontal = horizontal >= vertical;

    float pLuminance = e.isHorizontal ? l.n : l.e;
    float nLuminance = e.isHorizontal ? l.s : l.w;
    float pGradient = abs(pLuminance - l.m);
    float nGradient = abs(nLuminance - l.m);

    e.pixelStep = e.isHorizontal ? texSize.y : texSize.x;
    
    if (pGradient < nGradient)
    {
        e.pixelStep = -e.pixelStep;
        e.oppositeLuminance = nLuminance;
        e.gradient = nGradient;
    }
    else
    {
        e.oppositeLuminance = pLuminance;
        e.gradient = pGradient;
    }

    return e;
}

float DetermineEdgeBlendFactor(sampler2D  tex2D, vec2 texSize, LuminanceData l, EdgeData e, vec2 uv)
{
    vec2 uvEdge = uv;
    vec2 edgeStep;
    if (e.isHorizontal)
    {
        uvEdge.y += e.pixelStep * 0.5;
        edgeStep = vec2(texSize.x, 0.0);
    }
    else
    {
        uvEdge.x += e.pixelStep * 0.5;
        edgeStep = vec2(0.0, texSize.y);
    }

    float edgeLuminance = (l.m + e.oppositeLuminance) * 0.5;
    float gradientThreshold = e.gradient * 0.25;

    vec2 puv = uvEdge + edgeStep * edgeSteps[0];
    float pLuminanceDelta = SampleLuminance(tex2D, puv) - edgeLuminance;
    bool pAtEnd = abs(pLuminanceDelta) >= gradientThreshold;

    for (int i = 1; i < EDGE_STEP_COUNT && !pAtEnd; i++)
    {
        puv += edgeStep * edgeSteps[i];
        pLuminanceDelta = SampleLuminance(tex2D, puv) - edgeLuminance;
        pAtEnd = abs(pLuminanceDelta) >= gradientThreshold;
    }

    if (!pAtEnd)
    {
        puv += edgeStep * EDGE_GUESS;
    }

    vec2 nuv = uvEdge - edgeStep * edgeSteps[0];
    float nLuminanceDelta = SampleLuminance(tex2D, nuv) - edgeLuminance;
    bool nAtEnd = abs(nLuminanceDelta) >= gradientThreshold;

    for (int i = 1; i < EDGE_STEP_COUNT && !nAtEnd; i++)
    {
        nuv -= edgeStep * edgeSteps[i];
        nLuminanceDelta = SampleLuminance(tex2D, nuv) - edgeLuminance;
        nAtEnd = abs(nLuminanceDelta) >= gradientThreshold;
    }

    if (!nAtEnd)
    {
        nuv -= edgeStep * EDGE_GUESS;
    }

    float pDistance, nDistance;
    if (e.isHorizontal)
    {
        pDistance = puv.x - uv.x;
        nDistance = uv.x - nuv.x;
    }
    else
    {
        pDistance = puv.y - uv.y;
        nDistance = uv.y - nuv.y;
    }

    float shortestDistance;
    bool deltaSign;
    if (pDistance <= nDistance)
    {
        shortestDistance = pDistance;
        deltaSign = pLuminanceDelta >= 0.0;
    }
    else
    {
        shortestDistance = nDistance;
        deltaSign = nLuminanceDelta >= 0.0;
    }

    if (deltaSign == (l.m - edgeLuminance >= 0.0))
    {
        return 0.0;
    }

    return 0.5 - shortestDistance / (pDistance + nDistance);
}

vec4 ApplyFXAA(sampler2D  tex2D, vec2 texSize, vec2 uv)
{
    LuminanceData l = SampleLuminanceNeighborhood(tex2D, texSize, uv);
    if (ShouldSkipPixel(l))
    {
        return Sample(tex2D, uv);
    }

    float pixelBlend = DeterminePixelBlendFactor(l);
    EdgeData e = DetermineEdge(texSize, l);
    float edgeBlend = DetermineEdgeBlendFactor(tex2D, texSize, l, e, uv);
    float finalBlend = max(pixelBlend, edgeBlend);

    if (e.isHorizontal)
    {
        uv.y += e.pixelStep * finalBlend;
    }
    else
    {
        uv.x += e.pixelStep * finalBlend;
    }

    return Sample(tex2D, uv);
}

void main()
{
    vec2 texSize = 1.0 / vec2(1920, 1080);
    fragColor = ApplyFXAA(textureSampler, texSize, fragCoord);
}

// const float M_PI = 3.1415926535897932;
// const float M_E = 2.7182818284590452;

// // Max longitude in the equirectangular projection (2*atan(e^pi)-pi/2)
// const float EQUI_LON = 1.4844222297453324;

// float remap(float value, float oldMin, float oldMax, float newMin, float newMax)
// {
//     return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
// }

// vec2 equi_to_merc(float u, float v)
// {
//     // uv to equirectangular
//     float lon = remap(v, 0, 1, -EQUI_LON, EQUI_LON);

//     // equirectangular to mercator
//     float y = log(tan(M_PI / 4 + lon / 2));

//     // mercator to uv
//     y = remap(y, -M_PI, M_PI, 0, 1);

//     return vec2(u, y);
// }

// void main()
// {
//     vec2 uv = equi_to_merc(fragCoord.x, fragCoord.y);
//     fragColor = texture(textureSampler, uv);
// }