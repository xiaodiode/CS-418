#version 300 es

layout(location=0) in vec4 position;
layout(location=1) in vec4 color;

uniform float seconds;

out vec4 vColor;

void main() {
    vColor = color;
    /* Scales and transforms the xy coordinates, zw remain the same */
    gl_Position = vec4(
        position.xy*abs(cos(seconds*0.1)) + cos(seconds*0.9),
        position.zw
    );
}