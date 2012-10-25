package blobby;

import internals.GLRenderer;

import java.awt.event.KeyEvent;
import java.util.LinkedList;
import java.util.Queue;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;


import com.benton.framework.math.M3d;
import com.benton.framework.mesh.metaballs.ImplicitSurface;
import com.benton.framework.mesh.metaballs.MetaBall;
import com.sun.opengl.util.GLUT;

public class BlobbyDemo extends GLRenderer {

  boolean showFps = false;
  boolean paused = false;
  double d = 0;
  ImplicitSurface surface;
  ImplicitSurfaceRenderer surfaceRenderer;
  MetaBall mover;
  GL gl;

  @Override
  public String getTitle() {
    return "Blobby Demo";
  }

  public void init(GLAutoDrawable glDrawable) {
    super.init(glDrawable);

    gl = glDrawable.getGL();
    
    gl.glEnable(GL.GL_POLYGON_OFFSET_LINE);
    gl.glPolygonOffset(0, -100);

    showAxes = false;
    cameraDistance = 12;
    
    surface = new ImplicitSurface(new M3d(-10,-10,-10), new M3d(10,10,10), 5);
    surface.addForce(mover = new MetaBall(0,0,0,1.0));
    surface.addForce(new MetaBall(-4,0,0,1.0));

    surfaceRenderer = new ImplicitSurfaceRenderer(surface);
  }

  public void keyPressed(KeyEvent e) {
    switch (e.getKeyCode()) {
    case KeyEvent.VK_SPACE:
      paused = !paused;
      break;
    case KeyEvent.VK_B:
      surfaceRenderer.setShowBoxes(!surfaceRenderer.getShowBoxes());
      break;
    case KeyEvent.VK_E:
      surfaceRenderer.setShowEdges(!surfaceRenderer.getShowEdges());
      break;
    case KeyEvent.VK_F:
      showFps = !showFps;
      break;
    case KeyEvent.VK_1:
      surface.setTargetLevel(1);
      break;
    case KeyEvent.VK_2:
      surface.setTargetLevel(2);
      break;
    case KeyEvent.VK_3:
      surface.setTargetLevel(3);
      break;
    case KeyEvent.VK_4:
      surface.setTargetLevel(4);
      break;
    case KeyEvent.VK_5:
      surface.setTargetLevel(5);
      break;
    case KeyEvent.VK_6:
      surface.setTargetLevel(6);
      break;
    case KeyEvent.VK_7:
      surface.setTargetLevel(7);
      break;
    case KeyEvent.VK_8:
      surface.setTargetLevel(8);
      break;
    default: super.keyPressed(e);
      break;
    }
  }
  
  long then = 0;
  Queue<Long> times = new LinkedList<Long>();
  public void display(GLAutoDrawable glDrawable) {
    long now = System.currentTimeMillis();

    if (then == 0) {
      then = now;
    }
    preDisplay(glDrawable);
    if (!paused) {
      mover.setX(4*Math.cos(d));
      d += ((now-then) * 15.0 / 1000.0) * 3.141592/64.0;
      surface.reset();
      surface.refine();
    }
    then = now;
    surfaceRenderer.render(gl);

    // Track our timing
    times.add(now);
    while (now - times.peek() > 2500) {
      times.remove();
    }
    if (showFps) {
      float fps = ((float) times.size()) / 2.5f;
      glPrint(gl, 0, 3.3f, 0, GLUT.STROKE_MONO_ROMAN, fps + " fps");
    }
    
    postDisplay(glDrawable);
  }
}
