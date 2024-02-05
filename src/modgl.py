import moderngl
import numpy as np
from PIL import Image
import shaders

# Create a moderngl context
ctx = moderngl.create_standalone_context()

# Load the input image
input_image_path = "./data/M2.png"
input_image = Image.open(input_image_path)
input_image = input_image.resize((input_image.width, input_image.height * 2), Image.Resampling.NEAREST)

# Create a shader program
prog = ctx.program(vertex_shader=shaders.vertex_shader, fragment_shader=shaders.to_equi_fragment_shader)

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
output_image.save("output_image_rendered2.png")
