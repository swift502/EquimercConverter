import moderngl
import numpy
from PIL import Image
from .enums import CONVERSION, SAMPLING

def load_glsl(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def render(image: Image.Image, conversion: CONVERSION, sampling: SAMPLING):
    # Shaders
    vertex_shader = load_glsl("./src/shaders/vertex.glsl")
    if conversion == CONVERSION.TO_MERCATOR:
        fragmentShader = load_glsl("./src/shaders/fragment_to_mercator.glsl")
    else:
        fragmentShader = load_glsl("./src/shaders/fragment_to_equirectangular.glsl")

    # Setup
    ctx = moderngl.create_standalone_context()
    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragmentShader)
    quad = numpy.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype='f4')
    vbo = ctx.buffer(quad)
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

    # Texture
    texture = ctx.texture((image.width, image.height), len(image.mode), image.tobytes())
    texture.use()

    # Sampler
    sampler = ctx.sampler(repeat_x=False, repeat_y=False)
    if sampling == SAMPLING.LINEAR:
        sampler.filter = (moderngl.LINEAR, moderngl.LINEAR)
    else:
        sampler.filter = (moderngl.NEAREST, moderngl.NEAREST)
    sampler.use()

    # Framebuffer
    if conversion == CONVERSION.TO_MERCATOR:
        newImage = Image.new(image.mode, (image.width, 2 * image.height))
    else:
        newImage = Image.new(image.mode, (2 * image.width, image.height))
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((newImage.width, newImage.height), 4)])
    fbo.use()
    ctx.clear()

    # Render
    vao.render(moderngl.TRIANGLE_STRIP)
    pixels = fbo.read(components=len(newImage.mode), alignment=1)
    ctx.release()

    return Image.frombytes(newImage.mode, (newImage.width, newImage.height), pixels)