vec3 SurfaceColor = vec3(0.75, 0.75, 0.75);
vec3 WarmColor    = vec3(0.1, 0.4, 0.8);
vec3 CoolColor    = vec3(0.6, 0.0, 0.0);
float DiffuseWarm = 0.45;
float DiffuseCool = 0.045;

varying float NdotL;
varying vec3 ReflectVec;
varying vec3 ViewVec;

void main() {
  vec3 kcool    = min(CoolColor + DiffuseCool * vec3(gl_Color), 1.0);
  vec3 kwarm    = min(WarmColor + DiffuseWarm * vec3(gl_Color), 1.0);
  vec3 kfinal   = mix(kcool, kwarm, NdotL) * gl_Color.a;

  vec3 nreflect = normalize(ReflectVec);
  vec3 nview    = normalize(ViewVec);

  float spec    = max(dot(nreflect, nview), 0.0);
  spec          = pow(spec, 32.0);

  gl_FragColor = vec4(min(kfinal + spec, 1.0), 1.0);
}