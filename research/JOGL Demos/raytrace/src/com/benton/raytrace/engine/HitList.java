package com.benton.raytrace.engine;

import java.util.ArrayList;

public class HitList extends ArrayList<RayCollision> {

  private static final long serialVersionUID = -4701611749512115215L;

  public void insert(RayCollision toAdd) {
    int i = 0;
    for (RayCollision hit : this) {
      if (toAdd.t < hit.t) {
        add(i, toAdd);
        return;
      } else {
        i++;
      }
    }
    add(toAdd);
  }
}
