package com.benton.framework.mesh;

import static java.lang.Math.acos;

import com.benton.framework.math.M3d;

public class Face {

  Vertex[] arrVerts = null;
  M3d normal;
  
  public Face(Vertex... verts) {
    arrVerts = verts;
    for (int i = 0; i <arrVerts.length; i++) {
      arrVerts[i].addFace(this, i);
    }
    normal = getVertex(1).minus(getVertex(0)).cross(getVertex(-1).minus(getVertex(0))).normalized();
  }

  public M3d getNormal() {
    return normal;
  }
  
  public int getNumVerts() {
    return arrVerts.length;
  }
  
  public Vertex getVertex(int i) {
    while (i < 0) {
      i += arrVerts.length;
    }
    return arrVerts[i % arrVerts.length];
  }
  
  public Vertex[] getVertices() {
    return arrVerts;
  }
  
  public double getFaceAngle(Vertex v) {
    int i = v.getFaceIndex(this);
    
    return acos(getVertex(i-1).minus(v).normalized().dot(getVertex(i+1).minus(v).normalized()));
  }
}