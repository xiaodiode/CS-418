#version 300 es

in vec4 color;

out vec2 fragmentPos;
out vec4 vColor;


void main() {
    vColor = color;

    /* initializes position coordinates based on VertexID without
    breaking warp parallelism */
    vec2 temp = (gl_VertexID == 0) ? vec2(-1, -1) :
                    (gl_VertexID == 1) ? vec2( 1, -1) :
                    (gl_VertexID == 2) ? vec2(1, 1) :
                    (gl_VertexID == 3) ? vec2(-1, -1) :
                    (gl_VertexID == 4) ? vec2( -1, 1) :
                    vec2(1, 1);
    gl_Position = vec4(temp, 0, 1);

    fragmentPos = temp;
}