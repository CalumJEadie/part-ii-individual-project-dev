package com.benton.raytrace.csg;

import com.benton.raytrace.primitives.Primitive;


public class Union extends CsgBoolean {
  
  public Union(Primitive A, Primitive B) {
    super(A,B);
  }
  
  boolean op(boolean wasInA, boolean isInA, boolean wasInB, boolean isInB) {
    return ((wasInA != isInA) && (!isInB) && (!wasInB)) ||
           ((wasInB != isInB) && (!isInA) && (!wasInA));
  }
}
