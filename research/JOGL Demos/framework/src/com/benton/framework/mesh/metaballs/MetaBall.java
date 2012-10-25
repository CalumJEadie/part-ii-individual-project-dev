package com.benton.framework.mesh.metaballs;

import com.benton.framework.math.M3d;

public class MetaBall extends M3d implements Force {
  
  double strength;
  
  public MetaBall(double x, double y, double z, double strength) {
    super(x,y,z);
    this.strength = strength;
  }
  
  // The Wyvill Brothers' "soft object" function
   @Override
  public double F(M3d v) {
    double a = strength;
    double b = 5;
    double r = this.minus(v).length();
    double f;
    
    if (r < b/3.0) {
      f = a * (1 - ((3 * r * r) / (b*b)));
    } else if (r >= b/3.0 && r < b) {
      f = a * 1.5 * (1-(r/b)) * (1-(r/b));
    } else {
      f = 0;
    }

    return f;
  }

   public boolean isIn(M3d minCorner, M3d maxCorner) {
     return getX() >= minCorner.getX() && getX() <= maxCorner.getX()
         && getY() >= minCorner.getY() && getY() <= maxCorner.getY()
         && getZ() >= minCorner.getZ() && getZ() <= maxCorner.getZ();
   }
}
