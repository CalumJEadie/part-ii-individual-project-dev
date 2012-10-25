package internals;

import java.awt.BorderLayout;

import javax.media.opengl.GLCanvas;
import javax.swing.JApplet;

import com.sun.opengl.util.Animator;
import com.sun.opengl.util.FPSAnimator;

@SuppressWarnings("serial")
public abstract class AppletContainer extends JApplet {
  private Animator animator;
  GLCanvas canvas;
  
  public void setup(GLRenderer renderMe) {
    setLayout(new BorderLayout());
    canvas = new GLCanvas();
    canvas.addGLEventListener(renderMe);
    canvas.setSize(getSize());
    add(canvas, BorderLayout.CENTER);
    canvas.requestFocus();
    animator = new FPSAnimator(canvas, 60);
  }
  
  public void start() {
    animator.start();
  }
  
  public void stop() {
    animator.stop();
  }
}