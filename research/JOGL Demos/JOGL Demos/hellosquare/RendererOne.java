package hellosquare;

import javax.media.opengl.GL;

public class RendererOne extends SimpleRendererBase {

  public void render(GL gl) {
    gl.glBegin(GL.GL_QUADS);
      gl.glVertex3f(-1, -1,  0);
      gl.glVertex3f( 1, -1,  0);
      gl.glVertex3f( 1,  1,  0);
      gl.glVertex3f(-1,  1,  0);
    gl.glEnd();
  }
}
