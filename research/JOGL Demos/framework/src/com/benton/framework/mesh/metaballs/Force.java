package com.benton.framework.mesh.metaballs;

import com.benton.framework.math.M3d;

public interface Force {

  public double F(M3d v);

  public boolean isIn(M3d minCorner, M3d maxCorner);
}
