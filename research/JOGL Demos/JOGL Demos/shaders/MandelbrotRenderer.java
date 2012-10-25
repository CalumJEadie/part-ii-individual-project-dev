package shaders;

import static java.lang.Math.floor;
import static shaders.Torus.di;
import static shaders.Torus.dj;

import javax.media.opengl.GL;

import com.benton.framework.mesh.Mesh;
import com.benton.framework.mesh.Vertex;



public class MandelbrotRenderer extends ShaderRenderer {

  static final double numUSteps = 8;
  static final double numVSteps = 3;
  
  public MandelbrotRenderer(Torus torus, Mesh teapot) {
    super(torus, teapot);
  }

  public void init(final GL gl) {
    super.init(gl, "mandelbrot-vs.glsl", "mandelbrot-fs.glsl");
//    gl.glEnable(GL.GL_CULL_FACE);
//    gl.glEnable(GL.GL_VERTEX_PROGRAM_TWO_SIDE);
  }
  
  protected void preVertex(GL gl, Vertex vert) {
    gl.glTexCoord2d(-vert.getX() / 2.0, vert.getY() / 2.0);
  }
  
  protected void vertex(GL gl, int i, int j) {
    double u = (double)i / (double)(di-1);
    double v = (double)j / (double)(dj-1);

    u = ((u * numUSteps) - floor(u * numUSteps));
    v = ((v * numVSteps) - floor(v * numVSteps));
    u = u * 8 - 4;
    v = v * 8 - 4;
    gl.glTexCoord2d(u, v);
    super.vertex(gl, i, j);
  }

  public void displayTeapot(final GL gl) {
    gl.glCullFace(GL.GL_BACK);
    super.displayTeapot(gl);
  }
  
}
