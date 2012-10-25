package shaders;

import javax.media.opengl.GL;

import com.benton.framework.mesh.Mesh;



public class BasicRenderer extends ShaderRenderer {
  
  public BasicRenderer(Torus torus, Mesh teapot) {
    super(torus, teapot);
  }

  public void init(final GL gl) {
    super.init(gl, "basic-vs.glsl", "basic-fs.glsl");
  }
}
