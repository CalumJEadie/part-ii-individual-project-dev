package shaders;

import static java.lang.Math.PI;

import internals.GLRenderer;

import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;

import com.benton.framework.math.M3d;
import com.benton.framework.mesh.Mesh;
import com.benton.framework.mesh.OFFReader;



public class ShaderDemo extends GLRenderer {
  
  static final double closestApproach = 6.5;
  static final double defaultFarDist = 15.0;
  static final double defaultNearDist = 6.25;

  boolean paused = true;
  boolean showTeapot = false;
  double d = 0;
  long tick = 0;
  ShaderRenderer shaderRenderer;
  ShaderRenderer nextShader = null;
  Torus torus;
  Mesh teapot;

  public ShaderDemo() {
    torus = new Torus();
    teapot = OFFReader.parse(loadFile("teapot.off")).scaled(new M3d(2.75, 2.75, 2.75));
    shaderRenderer = new BasicRenderer(torus, teapot);
  }
  
  @Override
  public String getTitle() {
    return "Shader Demo";
  }
  
  @Override
  public void init(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();
    
    super.init(glDrawable);
    showAxes = false;
    cameraDistance = defaultFarDist;
    shaderRenderer.init(gl);
  }
  
  public void keyPressed(KeyEvent e) {
    switch (e.getKeyCode()) {
    case KeyEvent.VK_SPACE:
      paused = !paused;
      break;
    case KeyEvent.VK_A:
      nextShader = new BasicRenderer(torus, teapot);
      break;
    case KeyEvent.VK_B:
      nextShader = new DiffuseRenderer(torus, teapot);
      break;
    case KeyEvent.VK_C:
      nextShader = new GoochRenderer(torus, teapot);
      break;
    case KeyEvent.VK_D:
      nextShader = new MandelbrotRenderer(torus, teapot);
      break;
    case KeyEvent.VK_T:
      showTeapot = !showTeapot;
      break;
    case KeyEvent.VK_PAGE_DOWN:
      if (cameraDistance - closestApproach < 0.001) {
        cameraDistance = closestApproach + 0.001;
      } else {
        cameraDistance = (cameraDistance - closestApproach) * (1.0 / 0.9) + closestApproach;
      }
      break;
    case KeyEvent.VK_PAGE_UP:
      cameraDistance = (cameraDistance - closestApproach) * 0.9 + closestApproach;
      break;
    default: super.keyPressed(e);
      break;
    }
  }

  public double getMouseSpeed() {
    return Math.pow((cameraDistance - defaultNearDist) / (defaultFarDist - defaultNearDist), 1.6);
  }
  
  public void display(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();

    if (nextShader != null) {
      shaderRenderer.disable(gl);
      shaderRenderer = nextShader;
      shaderRenderer.init(gl);
      nextShader = null;
    }
    
    if (!paused) {
      long now = System.currentTimeMillis();

      if (tick == 0) {
        tick = now;
      }
      cameraTransform.rotate(new M3d(0,1,0), ((now - tick) / 1000.0) * PI / 4.0);
      
      tick = now;
    }
    
    preDisplay(glDrawable);
    if (!showTeapot) {
      shaderRenderer.displayTorus(gl);
    } else {
      shaderRenderer.displayTeapot(gl);
    }
    postDisplay(glDrawable);
  }
  
  private String loadFile(String filename) {
    BufferedReader brv;
    String line;
    StringBuffer buffer = new StringBuffer();
    
    try {
      brv = new BufferedReader(new FileReader(filename));
      while ((line=brv.readLine()) != null) {
        buffer.append(line);
        buffer.append("\n");
      }
    } catch (IOException e) {
      System.out.println("IOException: " + e.getMessage());
      System.exit(-1);
      return null;
    }
    return buffer.toString();
  }
}
