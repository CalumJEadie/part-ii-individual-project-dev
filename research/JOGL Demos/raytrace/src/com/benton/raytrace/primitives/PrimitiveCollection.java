package com.benton.raytrace.primitives;

import java.util.ArrayList;
import java.util.List;

import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;

public class PrimitiveCollection extends Primitive {

  protected List<Primitive> primitives;

  public PrimitiveCollection() {
    primitives = new ArrayList<Primitive>();
  }
  
  public Primitive add(Primitive sceneElement) {
    primitives.add(sceneElement);
    return sceneElement;
  }
  
  public Primitive remove(Primitive sceneElement) {
    primitives.remove(sceneElement);
    return sceneElement;
  }
  
  public List<Primitive> getPrimitives() {
    return primitives;
  }
  
  public boolean testLocalRay(Ray ray, HitList collisions) {
    boolean success = false;
    
    for (Primitive sceneElement : primitives) {
      success |= sceneElement.traceRay(ray, collisions);
    }
    return success;
  }
  
}
