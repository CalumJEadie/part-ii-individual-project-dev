package com.benton.framework.mesh;


import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

import com.benton.framework.math.M3d;

@SuppressWarnings("serial")
public class Mesh extends LinkedList<Face> {
  
  //////////////////////////////////////////////
  
  public Mesh() {
  }
  
  public void computeAllNormals() {
    Map<Vertex, Integer> visited = new HashMap<Vertex, Integer>();
    
    for (Face face : this) {
      for (Vertex v : face.getVertices()) {
        if (!visited.containsKey(v)) {
          visited.put(v, 1);
          v.computeNormal();
        }
      }
    }
  }
  
  public Mesh scaled(M3d scale) {
    Mesh newMesh = new Mesh();
    Map<Vertex, Vertex> newVerts = new HashMap<Vertex, Vertex>();
    
    for (Face face : this) {
      for (Vertex v : face.getVertices()) {
        if (!newVerts.containsKey(v)) {
          newVerts.put(v, new Vertex(new M3d(v.getX() * scale.getX(), v.getY() * scale.getY(), v.getZ() * scale.getZ())));
        }
      }
    }
    
    for (Face face : this) {
      int n = face.getVertices().length;
      Vertex arr[] = new Vertex[n];
      
      for (int i = 0; i < n; i++) {
        arr[i] = newVerts.get(face.getVertices()[i]);
      }
      
      newMesh.add(new Face(arr));
    }
    newMesh.computeAllNormals();
    return newMesh;
  }
  
  public Mesh flipped() {
    Mesh newMesh = new Mesh();
    Map<Vertex, Vertex> newVerts = new HashMap<Vertex, Vertex>();
    
    for (Face face : this) {
      for (Vertex v : face.getVertices()) {
        if (!newVerts.containsKey(v)) {
          newVerts.put(v, new Vertex(v));
        }
      }
    }
    
    for (Face face : this) {
      int n = face.getVertices().length;
      Vertex arr[] = new Vertex[n];
      
      for (int i = 0; i < n; i++) {
        arr[n-1-i] = newVerts.get(face.getVertices()[i]);
      }
      
      newMesh.add(new Face(arr));
    }
    newMesh.computeAllNormals();
    return newMesh;
  }
}
