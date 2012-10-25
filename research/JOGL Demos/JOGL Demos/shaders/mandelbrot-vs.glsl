varying vec2 position;
varying float numSteps;

void main() {
  vec3 ecPos    = vec3(gl_ModelViewMatrix * gl_Vertex);
  
  gl_Position = ftransform();
  position = vec2(gl_MultiTexCoord0);
  numSteps = max(10.0, 150.0 - 14.0 * distance(ecPos, vec3(0.0)));
}