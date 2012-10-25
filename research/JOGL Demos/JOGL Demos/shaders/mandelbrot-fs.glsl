varying vec2 position;
varying float numSteps;

void main() {
	vec2 z;
	vec2 tempZ = position * position;
	float i = 0.0;

	while (i <= numSteps && (tempZ.x + tempZ.y) <= 4.0) {
    z = vec2(tempZ.x - tempZ.y, 2.0 * z.x * z.y) + position;
    tempZ = z * z;
    i += 1.0;    
	}
	if (i <= numSteps) {
	  float color = i / numSteps;
	  gl_FragColor = vec4(color, color, 1.0, 1.0);
  } else {
		gl_FragColor = vec4(numSteps, 1.0, 1.0, 1.0);
  }
}