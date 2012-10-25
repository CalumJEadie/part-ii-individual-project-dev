package com.benton.raytrace.csg;

import com.benton.raytrace.primitives.Primitive;


public class Difference extends CsgBoolean {
  
  public Difference(Primitive A, Primitive B) {
    super(A,B);
  }
  
  boolean op(boolean wasInA, boolean isInA, boolean wasInB, boolean isInB) {
    return ((wasInA != isInA) && (!isInB) && (!wasInB)) || 
           ((wasInB != isInB) && (wasInA || isInA));
  }
}
