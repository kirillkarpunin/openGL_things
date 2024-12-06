from OpenGL import GL as gl


def readShader(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def createShader(shader_type, file):
    shader = gl.glCreateShader(shader_type)
    source = readShader(file)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    # Проверка на ошибки компиляции
    result = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if not result:
        error = gl.glGetShaderInfoLog(shader)
        shader_type_str = "VERTEX" if shader_type == gl.GL_VERTEX_SHADER else "FRAGMENT"
        print(f"Ошибка компиляции {shader_type_str} шейдера {file}: {error.decode()}")
        gl.glDeleteShader(shader)
        raise RuntimeError(f"Ошибка компиляции {shader_type_str} шейдера {file}: {error.decode()}")

    return shader


def createShaderProgram():
    vertex_shader = createShader(gl.GL_VERTEX_SHADER, 'vertex_shader.vert')
    fragment_shader = createShader(gl.GL_FRAGMENT_SHADER, 'fragment_shader.frag')
    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)

    # Проверка на ошибки линковки
    result = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if not result:
        error = gl.glGetProgramInfoLog(program)
        print(f"Ошибка линковки программы шейдера: {error.decode()}")
        gl.glDeleteProgram(program)
        raise RuntimeError(f"Ошибка линковки программы шейдера: {error.decode()}")

    # Удаление шейдеров после линковки
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return program
