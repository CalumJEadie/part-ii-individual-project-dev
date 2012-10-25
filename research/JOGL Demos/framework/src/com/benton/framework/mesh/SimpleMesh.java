package com.benton.framework.mesh;

import java.util.ArrayList;
import java.util.LinkedList;

import com.benton.framework.math.M3d;

@SuppressWarnings("serial")
public class SimpleMesh extends LinkedList<ArrayList<M3d>> {
  
  public ArrayList<M3d> addPoly(M3d a, M3d b, M3d c) {
    ArrayList<M3d> poly = new ArrayList<M3d>();
    
    poly.add(a);
    poly.add(b);
    poly.add(c);
    add(poly);
    return poly;
  }
  
  public ArrayList<M3d> addPolyWithOrientation(M3d a, M3d b, M3d c, M3d normal) {
    M3d n = c.minus(b).cross(a.minus(b));
    
    if (n.dot(normal) > 0) {
      return addPoly(a, b, c);
    } else {
      return addPoly(a, c, b);
    }
  }
  
  public void addMesh(SimpleMesh mesh) {
    for (ArrayList<M3d> poly : mesh) {
      add(poly);
    }
  }
}
