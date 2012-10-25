package com.benton.framework.mesh.metaballs;

import java.util.LinkedList;

import com.benton.framework.math.M3d;


@SuppressWarnings("serial")
public class OctTreeEdge extends LinkedList<Octree> {
  
  M3d a, b;
  M3d midPt;
  M3d normalDir;
  M3d interpolatedCrossing;
  OctTreeEdge parent;
  OctTreeEdge childA, childB;

  OctTreeEdge(OctTreeEdge parent, M3d a, M3d b, M3d precomputedMidPt) {
    this.parent = parent;
    this.a = a;
    this.b = b;
    this.interpolatedCrossing = null;
    this.normalDir = null;
    this.midPt = (precomputedMidPt == null) ? 
        a.plus(b).times(0.5) : 
        precomputedMidPt;
  }
  
  boolean hasEndPoint(M3d pt) {
    return (a == pt) || (b == pt);
  }
  
  boolean hasSharedEndPoint(OctTreeEdge e) {
    return (a == e.a) || (b == e.b) || (a == e.b) || (b == e.a);
  }
  
  boolean isInteresting() {
    return interpolatedCrossing != null;
  }
  
  void setMidPt(M3d midPt) {
    this.midPt = midPt;
  }
  
  void setCrossingData(M3d interpolatedCrossing, M3d normalDir) {
    this.interpolatedCrossing = interpolatedCrossing;
    this.normalDir = normalDir;
  }

  public OctTreeEdge getParent() {
    return parent;
  }

  public M3d getMidPt() {
    return midPt;
  }
  
  public M3d getNormalDir() {
    return normalDir;
  }
  
  public M3d getEndPt(int which) {
    return (which==0) ? a : b;
  }
  
  public OctTreeEdge getChild(int which) {
    return (which==0) ? childA : childB;
  }

  public void setChild(int which, OctTreeEdge child) {
    if (which==0) {
      this.childA = child;
    } else {
      this.childB = child;
    }
  }

  public M3d getInterpolatedCrossing() {
    return interpolatedCrossing;
  }
}
