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
void main() {
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
void main() {
    fragColor = texture2D(texture, fragCoord);
}
"""

# Load the input image
input_image_path = "./data/equi.png"
input_image = Image.open(input_image_path)

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
output_image = Image.frombytes('RGBA', (width, height), pixels)
# output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM)
output_image.save("output_image_rendered.png")
