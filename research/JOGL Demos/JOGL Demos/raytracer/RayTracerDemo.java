package raytracer;

import static java.lang.Math.PI;
import internals.GLRenderer;
import internals.GLTextureCanvas;

import java.awt.Frame;
import java.awt.event.KeyEvent;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.benton.raytrace.engine.Camera;
import com.benton.raytrace.engine.RayTracer;
import com.benton.raytrace.engine.Scene;
import com.benton.raytrace.primitives.Plane;
import com.benton.raytrace.primitives.Sphere;

public class RayTracerDemo extends GLRenderer {
  
  Camera camera;
  Scene scene;
  GLTextureCanvas canvas;
  RayTracer raytracer;
  boolean autoResizeRequested = false;
  
  Sphere S;
  int frame = 0;
  long tick = 0;
  
  public static final int IMAGE_WIDTH = 512;
  public static final int IMAGE_HEIGHT = 512;
  
  public String getTitle() {
    return "Ray Tracer";
  }
  
  public RayTracerDemo() {
    canvas = new GLTextureCanvas(IMAGE_WIDTH, IMAGE_HEIGHT);
    cameraDistance = 1;
    showAxes = false;

    camera = new Camera(new M3d(6,6,10).times(4));
    scene = new Scene();
    scene.addLight(new M3d(20,20,0));

    Plane P = new Plane(new M3d(1,1,1));
    P.setLocalTransform(M4x4.translation(new M3d(0,-1.5,0)));
    P.getMaterial().setLightingCoefficients(1, 0.4, 0.4, 5);
    scene.add(P);

    S = new Sphere(new M3d(0.2, 0.6, 0.8));
    S.getMaterial().setLightingCoefficients(1, 0.4, 0.4, 5);
    S.getMaterial().setTransparency(0.4);
    S.getMaterial().setRefractiveIndex(1.0);
    S.setLocalTransform(M4x4.scale(new M3d(1.4,1.4,1.4)));
    scene.add(S);

    raytracer = new RayTracer(scene, canvas, camera);
  }
  
  public RayTracerDemo withAutoResizeRequested() {
    autoResizeRequested = true;
    return this;
  }

  public void keyPressed(KeyEvent e) {
    switch (e.getKeyCode()) {
    default:
      super.keyPressed(e);
      break;
    case KeyEvent.VK_1:
      cameraDistance = 1;
      cameraTransform = new M4x4();
      break;
    case KeyEvent.VK_2:
      cameraDistance = 2;
      cameraTransform = M4x4.rotation(new M3d(0,1,0), -PI/8.0);
      cameraTransform.rotate(new M3d(1,0,-1), PI/8.0);
      cameraTransform.rotate(new M3d(0,0,1), 5*PI/64.0);
      break;
    }
  }
  
  public void preDisplay(GLAutoDrawable glDrawable) {
    if (autoResizeRequested) {
      autoResizeRequested = false;
      Frame.getFrames()[0].setSize(512, 512);
    }
    super.preDisplay(glDrawable);
  }

  @Override
  public void display(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();

    preDisplay(glDrawable);
    raytracer.renderScene();
    canvas.render(gl);
    
    if (frame < 500) {
      frame++;
      canvas.write(gl, "output/Frame" + frame + ".PNG");

      long tock = System.currentTimeMillis();
      if (tick != 0) {
        System.out.println(frame + ": " + (tock - tick) + "ms");
      }
      tick = tock;
      
      S.getMaterial().setRefractiveIndex(1.0 + (0.001 * frame));
      raytracer.resetProgressiveRender();
    }
    
    postDisplay(glDrawable);
  }
}
