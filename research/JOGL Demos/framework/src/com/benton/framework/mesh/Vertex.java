package com.benton.framework.mesh;

import java.util.HashMap;
import java.util.Map;

import com.benton.framework.math.M3d;

public class Vertex extends M3d {

  Map<Face, Integer> faces = new HashMap<Face, Integer>();
  public M3d normal = new M3d();

  public Vertex(M3d src) {
    super(src);
  }
  
  public Vertex(double x, double y, double z) {
    super(x, y, z);
  }
  
  public void addFace(Face face, int index) {
    faces.put(face, index);
  }
  
  public void computeNormal() {
    normal = new M3d();
    for (Face face : faces.keySet()) {
      normal = normal.plus(face.getNormal().times(face.getFaceAngle(this)));
    }
    normal = normal.normalized();
  }
  
  int getFaceIndex(Face f) {
    return faces.get(f);
  }
  
  public M3d getNormal() {
    return normal;
  }
}