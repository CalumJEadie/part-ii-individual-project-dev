package shaders;

import javax.media.opengl.GL;

import com.benton.framework.mesh.Mesh;



public class GoochRenderer extends ShaderRenderer {
  
  public GoochRenderer(Torus torus, Mesh teapot) {
    super(torus, teapot);
  }

  public void init(final GL gl) {
    super.init(gl, "gooch-vs.glsl", "gooch-fs.glsl");
    gl.glLineWidth(4);
    gl.glEnable(GL.GL_CULL_FACE);
    gl.glEnable(GL.GL_VERTEX_PROGRAM_TWO_SIDE);
    gl.glPolygonMode(GL.GL_FRONT, GL.GL_FILL);
    gl.glPolygonMode(GL.GL_BACK, GL.GL_LINE);
  }
  
  public void displayTorus(final GL gl) {
    gl.glCullFace(GL.GL_FRONT);
    super.displayTorus(gl);
    gl.glCullFace(GL.GL_BACK);
    super.displayTorus(gl);
  }
  
  public void displayTeapot(final GL gl) {
    gl.glCullFace(GL.GL_FRONT);
    super.displayTeapot(gl);
    gl.glCullFace(GL.GL_BACK);
    super.displayTeapot(gl);
  }

  public void disable(final GL gl) {
    gl.glPolygonMode(GL.GL_FRONT, GL.GL_FILL);
    gl.glPolygonMode(GL.GL_BACK, GL.GL_FILL);
    super.disable(gl);
  }
}
