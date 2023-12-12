/**
 * Compiles the vertex and fragment shaders, which are then
 * attached to a program and linked to be returned
 * 
 * @param {*} vs_source The source code for vertex shader
 * @param {*} fs_source The source code for fragment shader
 * @returns The program linked with the vs and fs shaders
 */
function compileShader(vs_source, fs_source) {
    const vs = gl.createShader(gl.VERTEX_SHADER)
    gl.shaderSource(vs, vs_source)
    gl.compileShader(vs)
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(vs))
        throw Error("Vertex shader compilation failed")
    }

    const fs = gl.createShader(gl.FRAGMENT_SHADER)
    gl.shaderSource(fs, fs_source)
    gl.compileShader(fs)
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(fs))
        throw Error("Fragment shader compilation failed")
    }

    const program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
    
    // loop through all uniforms in the shader source code
    // get their locations and store them in the GLSL program object for later use
    const uniforms = {}
    for(let i=0; i<gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS); i+=1) {
        let info = gl.getActiveUniform(program, i)
        uniforms[info.name] = gl.getUniformLocation(program, info.name)
    }
    program.uniforms = uniforms

    return program
}

/**
 * 
 * @param {*} geom Contains data for "triangles" (lists the vertices of each triangle)
 *                  and "attributes" (lists the positions of each vertex and respective color)
 * @returns an object with four keys:
 *  - mode = the 1st argument for gl.drawElements
 *  - count = the 2nd argument for gl.drawElements
 *  - type = the 3rd argument for gl.drawElements
 *  - vao = the vertex array object for use with gl.bindVertexArray
 */
function setupGeomery(geom) {
    var triangleArray = gl.createVertexArray()
    gl.bindVertexArray(triangleArray)

    for(let i=0; i<geom.attributes.length; i+=1) {
        let buf = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, buf)
        let f32 = new Float32Array(geom.attributes[i].flat())
        gl.bufferData(gl.ARRAY_BUFFER, f32, gl.STATIC_DRAW)
        
        gl.vertexAttribPointer(i, geom.attributes[i][0].length, gl.FLOAT, false, 0, 0)
        gl.enableVertexAttribArray(i)
    }

    var indices = new Uint16Array(geom.triangles.flat())
    var indexBuffer = gl.createBuffer()
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer)
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW)

    return {
        mode: gl.TRIANGLES,
        count: indices.length,
        type: gl.UNSIGNED_SHORT,
        vao: triangleArray
    }
}
/**
 * Draws one frame
 * @param {*} milliseconds 
 */
function draw(milliseconds) {
    gl.clear(gl.COLOR_BUFFER_BIT) 
    gl.useProgram(program)
    
    // values that do not vary between vertexes or fragments are called "uniforms"
    gl.uniform1f(program.uniforms.seconds, milliseconds/1000)
    
    gl.bindVertexArray(geom.vao)
    gl.drawElements(geom.mode, geom.count, geom.type, 0)
}

/**
 * Calls the draw function to draw elements each frame
 * @param {*} milliseconds 
 */
function tick(milliseconds) {
    draw(milliseconds)
    requestAnimationFrame(tick) // asks browser to call tick before next frame
}

window.addEventListener('load', async (event) => {
    window.gl = document.querySelector('canvas').getContext('webgl2')
    let vs = await fetch('vertex_shader.glsl').then(res => res.text())
    let fs = await fetch('fragment_shader.glsl').then(res => res.text())
    window.program = compileShader(vs,fs)
    let data = await fetch('geometry.json').then(r=>r.json())
    window.geom = setupGeomery(data)
    requestAnimationFrame(tick) // asks browser to call tick before first frame
})