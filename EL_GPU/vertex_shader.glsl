#version 300 es

layout(location=0) in vec4 position;
layout(location=1) in vec4 color;

uniform float seconds;

out vec4 vColor;

void main() {
    vColor = color;

    /* Constants to use for warping the logo */
    float warpFactor = 0.13;
    float scale = 0.6;
    float warpSpeed = 2000.0;
    float vertexDistortion = 150.0;

    /* Combine all the warp components into one variable */
    float warp = scale + warpFactor*sin(radians(vertexDistortion*float(gl_VertexID) + warpSpeed*seconds)); 

    /* Update the new positions with warp effect */
    vec2 newPos;
    newPos.x = position.x*warp; 
    newPos.y = position.y*warp; 

    /* Scales and transforms the xy coordinates, zw remain the same */
    gl_Position = vec4(
        newPos, 
        position.zw
    );
    
    
}
