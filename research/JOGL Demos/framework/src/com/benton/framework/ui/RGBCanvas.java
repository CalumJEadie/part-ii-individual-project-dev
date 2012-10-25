package com.benton.framework.ui;

import com.benton.framework.math.M3d;

public interface RGBCanvas {

  public int getWidth();
  public int getHeight();
  public void fill(double x, double y, double dx, double dy, M3d color);
}
