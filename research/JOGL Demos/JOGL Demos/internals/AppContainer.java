package internals;

import java.awt.Frame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.media.opengl.GLCanvas;

public class AppContainer implements Runnable {
  private static Thread displayT;
  private static GLRenderer toRender;
  private static boolean bQuit = false;
  
  public static int dx = 640, dy = 480;
  
  public static void go(GLRenderer renderMe) {
    toRender = renderMe;
    displayT = new Thread(new AppContainer());
    displayT.start();
  }
  
  public void run() {
    Frame frame = new Frame(toRender.getTitle());
    GLCanvas canvas = new GLCanvas();
    canvas.addGLEventListener(toRender);
    frame.add(canvas);
    frame.setSize(dx, dy);
    frame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
        bQuit = true;
        System.exit(0);
      }
    });
    frame.setVisible(true);
    canvas.requestFocus();
    while( !bQuit ) {
      canvas.display();
    }
  }
}