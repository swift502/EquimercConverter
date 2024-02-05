import moderngl
import numpy as np
from PIL import Image

# Create a moderngl context
ctx = moderngl.create_standalone_context()

# Vertex shader
vertex_shader = """
#version 330
in vec2 in_vert;
out vec2 fragCoord;
void main()
{
    gl_Position = vec4(in_vert, 0.0, 1.0);
    fragCoord = (in_vert + 1) / 2;
}
"""

# Fragment shader
fragment_shader = """
#version 330
in vec2 fragCoord;
out vec4 fragColor;
uniform sampler2D texture;

#define M_PI 3.1415926535897932384626433832795
#define M_E 2.7182818284590452353602874713527
//#define M_MMAX 1.48442223358

float remap(float value, float oldMin, float oldMax, float newMin, float newMax)
{
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
}

vec2 equi_to_merc(float u, float v)
{
    // uv to equirectangular
    float lat = remap(u, 0, 1, 0, 2 * M_PI);
    float lon = remap(v, 0, 1, -M_PI * 0.5, M_PI * 0.5);

    // equirectangular to mercator
    float x = lat;
    //lon = clamp(lon, -M_MMAX, M_MMAX);
    float y = log(tan(M_PI / 4 + lon / 2));

    // mercator to uv
    x = remap(x, 0, 2 * M_PI, 0, 1);
    y = remap(y, -M_PI, M_PI, 0, 1);

    // clamp
    x = clamp(x, 0, 1);
    y = clamp(y, 0, 1);

    return vec2(x, y);
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

    // clamp
    x = clamp(x, 0, 1);
    y = clamp(y, 0, 1);

    return vec2(x, y);
}

void main()
{
    vec2 uv = merc_to_equi(fragCoord.x, fragCoord.y);
    //vec2 uv = equi_to_merc(fragCoord.x, fragCoord.y);
    fragColor = texture2D(texture, uv);
}
"""

# Load the input image
input_image_path = "./data/equi.png"
input_image = Image.open(input_image_path)
input_image = input_image.resize((input_image.width, input_image.height * 2), Image.Resampling.NEAREST)

# Create a shader program
prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

# Create a fullscreen quad
quad = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype='f4')
vbo = ctx.buffer(quad)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

# Create a texture from the input image
width, height = input_image.size
mode = input_image.mode
channels = len(mode)
texture = ctx.texture((width, height), channels, input_image.tobytes())
texture.use()

# Set the texture uniform in the shader
prog['texture'].value = 0  # 0 corresponds to the texture unit

# Create a framebuffer
fbo = ctx.framebuffer(color_attachments=[ctx.texture((width, height), 4)])

# Use the framebuffer
fbo.use()

# Clear the framebuffer
ctx.clear()

# Draw the fullscreen quad with the input image texture
vao.render(moderngl.TRIANGLE_STRIP)

# Read the pixel data from the framebuffer
pixels = fbo.read(components=channels, alignment=1)

# Close the context
ctx.release()

# Save the result as a PNG file
output_image = Image.frombytes(mode, (width, height), pixels)
# output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM)
output_image.save("output_image_rendered.png")
