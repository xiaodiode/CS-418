#version 300 es
precision highp float;

in vec4 vColor;

uniform float seconds;

out vec4 fragColor;

void main() {
    /* rgba values remain consistent with geom color in "attributes" */
    fragColor = vec4(
        vColor.r,
        vColor.g,
        vColor.b,
        vColor.a
    );
}