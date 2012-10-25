package com.benton.raytrace.engine;

import static java.lang.Math.acos;
import static java.lang.Math.asin;
import static java.lang.Math.max;
import static java.lang.Math.pow;
import static java.lang.Math.sin;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.benton.framework.math.Ray;
import com.benton.framework.ui.RGBCanvas;

public class RayTracer {
  
  public static final double MIN_TRAVEL = 0.001;
  public static final int NUM_REFLECTIONS = 3;
  public static final boolean SHADOWS = false;
  public static final M3d GRAY = new M3d(0.5, 0.5, 0.5);
  public static final M3d BLACK = new M3d(0, 0, 0);
  
  private Scene scene;
  private RGBCanvas canvas;
  private Camera camera;

  float pixelSize;
  boolean recalculate;
  boolean renderInProgress = false;
  int pos = 0, stop = 1;
  float w, h, sx, sy;
  
  public static String rgbToString(M3d color) {
    return "#" + hexIntColor(color.getX())
        + hexIntColor(color.getY())
        + hexIntColor(color.getZ());
  }
  
  public static M3d secondaryRay(Scene scene, Ray ray, int numLevels) {
    HitList hits = new HitList();
    
    if (scene.traceRay(ray, hits)) {
      return illuminate(scene, ray, hits.get(0), numLevels+1);
    } else {
      return GRAY;
    }
  }
  
  public static M3d illuminate(Scene scene, Ray eyeRay, RayCollision hit, int numReflectionBounces) {
    final Material hitMaterial = hit.material;
    double diffuseSum = 0;
    double specularSum = 0;
    M3d normal = (hit.normal.dot(eyeRay.direction) > 0) ? hit.normal.times(-1) : hit.normal;
    M3d nVDotN = normal.times(normal.dot(eyeRay.direction));
    M3d reflectedColor = new M3d(0,0,0);
    M3d transparencyColor = new M3d(0,0,0);
    M3d baseColor = hitMaterial.getColor();
    
    for (M3d light : scene.getLights()) {
      // Shadow test
      HitList hits = new HitList();
      Ray shadowRay = new Ray(hit.point, light.minus(hit.point).normalized());
      boolean shadowed = SHADOWS ? scene.traceRay(shadowRay, hits) : false;
      
      if (!shadowed) {
        // Diffuse
        diffuseSum += normal.dot(light.minus(hit.point).normalized());
      
        // Specular
        M3d N = normal;
        M3d L = light.minus(hit.point).normalized();
        M3d R = N.times(2*(L.dot(N))).minus(L); 
        M3d E = eyeRay.direction.times(-1);
  
        specularSum += pow(max(R.dot(E), 0), hitMaterial.getSpecularShininess());
      }
    }
    
    // Reflection
    if (numReflectionBounces < NUM_REFLECTIONS && hitMaterial.getReflectivity() > 0) {
      M3d reflection = eyeRay.direction.minus(nVDotN.times(2)).normalized();
      Ray eyeRayReflected = new Ray(hit.point, reflection);
      
      reflectedColor = secondaryRay(scene, eyeRayReflected, numReflectionBounces);
      reflectedColor = reflectedColor.times(hitMaterial.getReflectivity());
    }
    
    // Transparency
    if (numReflectionBounces < NUM_REFLECTIONS && hitMaterial.getTransparency() > 0) {
      Ray eyeRayPassedThrough;
      
      if (hitMaterial.getRefractiveIndex() == 1.0 || eyeRay.direction.times(-1).dot(normal) > 0.99999) {
        eyeRayPassedThrough = new Ray(hit.point, eyeRay.direction);
      } else {
        double nOne = (hit.normal.dot(eyeRay.direction) >  0) ? hitMaterial.getRefractiveIndex() : 1.0;
        double nTwo = (hit.normal.dot(eyeRay.direction) <= 0) ? hitMaterial.getRefractiveIndex() : 1.0;
        double thetaOne = acos(normal.dot(eyeRay.direction.times(-1)));
        double thetaTwo = asin(sin(thetaOne) * nOne / nTwo);
        M3d axis = normal.times(-1).cross(eyeRay.direction);
        M4x4 bend = M4x4.rotation(axis, thetaTwo);
        
        eyeRayPassedThrough = new Ray(hit.point, bend.times(normal.times(-1)));
      }
      transparencyColor = secondaryRay(scene, eyeRayPassedThrough, numReflectionBounces);
      transparencyColor = transparencyColor.times(hitMaterial.getTransparency());
    }
    
    double localLighting = hitMaterial.getKa() + 
      diffuseSum * hitMaterial.getKd() + 
      specularSum * hitMaterial.getKs();
    M3d localColor = baseColor.times(localLighting).times(1-Math.max(hitMaterial.getReflectivity(), hitMaterial.getTransparency()));
    M3d totalColor = localColor.plus(reflectedColor).plus(transparencyColor);
    return totalColor;
  }

  //////////////////////////////////////
  
  public RayTracer(Scene scene, RGBCanvas canvas, Camera camera) {
    this.scene = scene;
    this.canvas = canvas;
    this.camera = camera;

    pixelSize = Math.max(canvas.getWidth(), canvas.getHeight()) / 4f;
    findProgressiveRenderConstants();
    renderInProgress = true;
  }

  public void fireRay(int x, int y, float w, float h, float sx, float sy) {
    float cellLeft = (camera.viewWidth/2) * ((x - (w/2)) / w);
    float cellRight = (camera.viewWidth/2) * (((x+1) - (w/2)) / w);
    float cellTop = (camera.viewHeight/2) * ((y - (h/2)) / h);
    float cellBottom = (camera.viewHeight/2) * (((y+1) - (h/2)) / h);
    float cellX = (cellLeft + cellRight) / 2;
    float cellY = (cellTop + cellBottom) / 2;
    
    M3d interceptRight = camera.right.times(cellX);
    M3d interceptUp = camera.up.times(cellY);
    M3d intercept = camera.position.plus(camera.direction.times(camera.distanceToViewingPlane)).plus(interceptUp).plus(interceptRight);
    Ray ray = new Ray(camera.position, intercept.minus(camera.position).normalized());
    HitList hits = new HitList();
    
    if (scene.traceRay(ray, hits)) {
      canvas.fill(sx*x,sy*y,sx,sy, illuminate(scene, ray, hits.get(0), 0));
    } else {
      canvas.fill(sx*x,sy*y,sx,sy, GRAY);
    }
  }
  
  private void findProgressiveRenderConstants() {
    w = canvas.getWidth() / pixelSize;
    h = canvas.getHeight() / pixelSize;
    sx = canvas.getWidth() / (float)w;
    sy = canvas.getHeight() / (float)w;
    pos = 0;
    stop = ((int) h) * ((int) w);
    recalculate = false;
  }
  
  public void renderScene() {
    pixelSize = 1;
    recalculate = true;
    while (renderInProgress) {
      renderSceneProgressively();
    }
  }
  
  public boolean renderSceneProgressively() {
    if (recalculate) {
      findProgressiveRenderConstants();
    }

    if (renderInProgress) {
      for (int counter = 0; counter < 64 && pos < stop; counter++) {
        int x = pos % ((int)w);
        int y = pos / ((int)h);
  
        fireRay(x, y, w, h, sx, sy);
        pos++;
      }
  
      if (pos < stop) {
        int y = pos / ((int)h);
        canvas.fill(0,sy*(y+1),canvas.getWidth(),sy, BLACK);
      } else {
        if (pixelSize > 1) {
          pixelSize = pixelSize / 4;
          if (pixelSize < 1) {
            pixelSize = 1;
          }
          recalculate = true;
        } else {
          renderInProgress = false;
        }
      }
    }
    
    return renderInProgress;
  }
  
  public boolean getRenderInProgress() {
    return renderInProgress;
  }
  
  public void resetProgressiveRender() {
    pixelSize = Math.max(canvas.getWidth(), canvas.getHeight()) / 4f;
    recalculate = true;
    renderInProgress = true;
  }
  
  private static String hexIntColor(double f) {
    String hex = Integer.toHexString(Math.max(Math.min((int)(f*255), 255), 0));
    
    if(hex.length() < 2) {
      return "0" + hex;
    } else {
      return hex;
    }
  }
}
