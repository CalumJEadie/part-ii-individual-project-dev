// Vertex Shader

varying vec3 Norm;
varying vec3 ToLight;

void main()
{
  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
  Norm        = gl_NormalMatrix * gl_Normal; 
  ToLight     = vec3(gl_LightSource[0].position - (gl_ModelViewMatrix * gl_Vertex));
} 
