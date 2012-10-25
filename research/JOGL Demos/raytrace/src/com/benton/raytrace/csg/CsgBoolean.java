package com.benton.raytrace.csg;

import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.RayCollision;
import com.benton.raytrace.primitives.Primitive;

public abstract class CsgBoolean extends Primitive {

  protected static final HitList NONE = new HitList();
  protected Primitive A;
  protected Primitive B;

  public CsgBoolean(Primitive A, Primitive B) {
    this.A = A;
    this.B = B;
  }

  protected HitList push(RayCollision toAdd, HitList hits) {
    HitList result = new HitList();
    
    result.add(toAdd);
    for (RayCollision hit : hits) {
      result.add(hit);
    }
    return result;
  }

  protected HitList pop(HitList hits) {
    HitList result = new HitList();
    
    for (int i = 1; i<hits.size(); i++) {
      result.add(hits.get(i));
    }
    return result;
  }
  
  boolean mergeHitLists(boolean inA, HitList hitsA, boolean inB, HitList hitsB, HitList collisions) {
    int a = 0, b = 0;
    int initialSize = collisions.size();
    
    while (a < hitsA.size() && b < hitsB.size()) {
      if (hitsA.get(a).t < hitsB.get(b).t) {
        if (op(inA, !inA, inB, inB)) {
          collisions.insert(hitsA.get(a));
        }
        a++;
        inA = !inA;
      } else {
        if (op(inA, inA, inB, !inB)) {
          collisions.insert(hitsB.get(b));
        }
        b++;
        inB = !inB;
      }
    }
    while (a < hitsA.size()) {
      if (op(inA, !inA, inB, inB)) {
        collisions.insert(hitsA.get(a));
      }
      a++;
      inA = !inA;
    }
    while (b < hitsB.size()) {
      if (op(inA, inA, inB, !inB)) {
        collisions.insert(hitsB.get(b));
      }
      b++;
      inB = !inB;
    }
    return initialSize != collisions.size();
  }

  public boolean testLocalRay(Ray ray, HitList collisions) {
    HitList hitsA = new HitList();
    HitList hitsB = new HitList();
    boolean inA, inB;
    
    A.traceRay(ray, hitsA);
    B.traceRay(ray, hitsB);
    inA = hitsA.isEmpty() ? false : (hitsA.get(0).normal.dot(ray.direction) > 0);
    inB = hitsB.isEmpty() ? false : (hitsB.get(0).normal.dot(ray.direction) > 0);

    return mergeHitLists(inA, hitsA, inB, hitsB, collisions);
  }

  abstract boolean op(boolean wasInA, boolean isInA, boolean wasInB, boolean isInB);
}