package com.benton.raytrace.primitives;

import static com.benton.raytrace.engine.RayTracer.MIN_TRAVEL;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.RayCollision;

public abstract class Primitive {
  
  private M4x4 l2p = new M4x4();
  private M4x4 l2p4Normals = new M4x4();
  private M4x4 p2l = new M4x4();

  public M4x4 getLocalToParent() {
    return l2p;
  }
  
  public M4x4 getParentToLocal() {
    return p2l;
  }
  
  public void setLocalTransform(M4x4 l2p) {
    this.l2p = l2p;
    this.l2p4Normals = l2p.extract3x3().inverted().transposed();
    this.p2l = l2p.inverted();
  }

  protected M3d getNormal(M3d point) {
    return new M3d(0,0,0);
  }
  
  protected RayCollision recordCollision(double t, Ray ray, HitList collisions) {
    if (t >= MIN_TRAVEL) {
      RayCollision hit = new RayCollision();
      
      hit.t = t;
      hit.point = ray.at(t);
      hit.normal = getNormal(hit.point);
      collisions.insert(hit);
      return hit;
    } else {
      return null;
    }
  }
  
  public boolean traceRay(Ray ray, HitList collisions) {
    Ray transformedRay = ray.transformedBy(p2l);
    HitList hits = new HitList();
    
    if (testLocalRay(transformedRay, hits)) {
      for (RayCollision collision : hits) {
/*
        // Work it all out
        M3d notTheNormal = (Math.abs(collision.normal.getX()) < 0.9) ? new M3d(1, 0, 0) : new M3d(0, 1, 0);
        M3d A = collision.normal.cross(notTheNormal);
        M3d B = collision.normal.cross(A);
        M3d ptA = collision.point.plus(A);
        M3d ptB = collision.point.plus(B);
        M3d ptAP = l2p.times(ptA);
        M3d ptBP = l2p.times(ptB);
        M3d AD = ptAP.minus(l2p.times(collision.point));
        M3d BD = ptBP.minus(l2p.times(collision.point));
        collision.normal = AD.cross(BD).normalized();
        
        // Or...
*/
        collision.normal = l2p4Normals.times(collision.normal).normalized();
        collision.point = l2p.times(collision.point);
        collision.t = ray.origin.minus(collision.point).length();
        collisions.insert(collision);
      }
      return true;
    } else {
      return false;
    }
  }
  
  public abstract boolean testLocalRay(Ray ray, HitList collisions);
}
