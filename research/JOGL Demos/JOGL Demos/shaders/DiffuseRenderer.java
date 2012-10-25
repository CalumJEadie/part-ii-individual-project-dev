package shaders;

import javax.media.opengl.GL;

import com.benton.framework.mesh.Mesh;



public class DiffuseRenderer extends ShaderRenderer {
  
  public DiffuseRenderer(Torus torus, Mesh teapot) {
    super(torus, teapot);
  }

  public void init(final GL gl) {
    super.init(gl, "diffuse-vs.glsl", "diffuse-fs.glsl");
  }
}
