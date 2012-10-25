package com.benton.raytrace.engine;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;

public class Camera {
  public M3d position;
  public M3d direction;
  public M3d up;
  public M3d right;
  public float distanceToViewingPlane;
  public float viewWidth, viewHeight;
  
  public Camera(M3d pos) {
    position = pos;
    direction = position.times(-1).normalized();
    right = direction.cross(new M3d(0,1,0)).normalized();
    up = right.cross(direction).normalized();
    distanceToViewingPlane = 1;
    viewWidth = 0.25f;
    viewHeight = 0.25f;
  }
  
  public void pivot(double x, double y) {
    M4x4 T = M4x4.rotation(new M3d(0,1,0), x);
    
    position = T.times(position);
    direction = T.times(direction);
    right = T.times(right);
    T = M4x4.rotation(right, y);
    position = T.times(position);
    direction = T.times(direction);
    up = right.cross(direction).normalized();
  }
}
