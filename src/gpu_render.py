import moderngl
import numpy as np
from PIL import Image

def load_glsl(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def render(image: Image.Image):
    # Create a moderngl context
    ctx = moderngl.create_standalone_context()

    # Resize image
    input_image = input_image.resize((input_image.width, input_image.height * 2), Image.Resampling.NEAREST)

    vertex_shader = load_glsl("./src/shaders/vertex.glsl")

    # Create a shader program
    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=shaders.to_equi_fragment_shader)

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
    return Image.frombytes(mode, (width, height), pixels)