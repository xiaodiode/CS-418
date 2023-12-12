#version 300 es
precision highp float;

in vec4 vColor;
in vec2 fragmentPos;

uniform float seconds;

out vec4 fragColor;

void main() {
    float x = fragmentPos.x;
    float y = fragmentPos.y;
    
    float density = 3.0; // how dense the curves fill up screen
    float speed = 3.0;   // how fast the curves move

    float freq1 = 8.0;  
    float amp1 = 0.5;
    float curve1 = amp1*sin(x*freq1);

    float freq2 = 8.0;
    float amp2 = 0.7;
    float curve2 = amp2*cos(y*freq2);

    float freq3 = 12.0;
    float amp3 = 0.2;
    float curve3 = amp3*sin((x + y) * freq3);

    float pattern1 = smoothstep(0.1, 0.15, mod(x*density + seconds*speed + curve1 + curve2 + curve3, 1.0));
    float pattern2 = smoothstep(0.1, 0.15, mod(y*density + seconds*speed + curve1 + curve2 + curve3, 1.0));
    float pattern3 = smoothstep(0.1, 0.15, mod((x+y)*density + seconds*speed + curve1 + curve2 + curve3, 1.0));

    float density2 = 0.05;
    float speed2 = 0.9;
    float pattern4 = smoothstep(0.1, 0.15, mod(x*density2 + seconds*speed2, 1.0));

    float density3 = 0.2;
    float speed3 = 1.2;
    float pattern5 = smoothstep(0.1, 0.15, mod(y*density3 + seconds*speed3, 1.0));

    float colorInterval = 4.0; // Adjust the interval for color change
    vec3 color1 = vec3(0.8, 0.2, 0.2); // Red
    vec3 color2 = vec3(0.45f, 0.53f, 0.24f); // Green
    vec3 color3 = vec3(0.2, 0.2, 0.8); // Blue

    float interpVal = mod(seconds, colorInterval) / colorInterval;
    vec3 final1 = mix(color1, mix(color2, color3, interpVal), pattern1 + pattern4);
    vec3 final2 = mix(color1, mix(color2, color3, interpVal), pattern2 + pattern5);
    vec3 final3 = mix(color1, mix(color2, color3, interpVal), pattern3);

    fragColor = vec4(final1 + final2 + final3, vColor.a);
}
