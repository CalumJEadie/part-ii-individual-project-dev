package com.benton.raytrace.csg;

import com.benton.raytrace.primitives.Primitive;


public class Intersection extends CsgBoolean {
  
  public Intersection(Primitive A, Primitive B) {
    super(A,B);
  }
  
  boolean op(boolean wasInA, boolean isInA, boolean wasInB, boolean isInB) {
    return (wasInA || isInA) && (wasInB || isInB);
  }
}
