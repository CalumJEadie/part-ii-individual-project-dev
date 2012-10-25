package com.benton.framework.mesh.metaballs;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M3dPair;


public class ImplicitSurface {
  
  @SuppressWarnings("serial")
  class EdgeMap extends HashMap<M3dPair, OctTreeEdge> { }

  private double cutoff = 0.5;
  private int targetLevel = 4;
  private M3d min;
  private double scale;
  private int fx, fy, fz;
  private LinkedList<Force> forces = new LinkedList<Force>();
  private HashMap<M3d, Double> samples;
  private LinkedList<Octree> inProgress;
  private LinkedList<Octree> finished;
  private LinkedList<Octree> roots;
  private EdgeMap[] edgeMapArray;

  ////////////////////////////////////////
  
  public ImplicitSurface(M3d min, M3d max, int targetLevel) {
    double dx = max.getX() - min.getX();
    double dy = max.getY() - min.getY();
    double dz = max.getZ() - min.getZ();

    this.min = min;
    this.targetLevel = targetLevel;
    if (dx < dy && dx < dz) {
      scale = dx;
    } else if (dy < dx && dy < dz) {
      scale = dy;
    } else {
      scale = dz;
    }
    fx = (int)Math.ceil(dx / scale);
    fy = (int)Math.ceil(dy / scale);
    fz = (int)Math.ceil(dz / scale);
    
    reset();
  }
  
  public void reset() {
    M3d[][][] coords = new M3d[fx+1][fy+1][fz+1];
    List<M3d> targets = new LinkedList<M3d>();

    samples = new HashMap<M3d, Double>();
    inProgress = new LinkedList<Octree>();
    finished = new LinkedList<Octree>();
    roots = new LinkedList<Octree>();
    edgeMapArray = new EdgeMap[10];
    for (Force f : forces) {
      if (f instanceof M3d) {
        targets.add((M3d)f);
      }
    }
    for (int x = 0; x <= fx; x++) {
      for (int y = 0; y <= fy; y++) {
        for (int z = 0; z <= fz; z++) {
          coords[x][y][z] = new M3d(
              min.getX() + x * scale, 
              min.getY() + y * scale, 
              min.getZ() + z * scale);
        }
      }
    }
    for (int x = 0; x < fx; x++) {
      for (int y = 0; y < fy; y++) {
        for (int z = 0; z < fz; z++) {
          inProgress.add(new Octree(this, 0, coords, x, y, z, targets));
        }
      }
    }
    roots.addAll(inProgress);
  }
  
  private List<Octree> findContainer(M3d pt, Octree parent) {
    List<Octree> ret = new LinkedList<Octree>();
    boolean addedChild = false;
    Octree[][][] kids = parent.getChildOctrees();
    
    if (parent.encloses(pt)) {
      if (kids != null) {
        for (int i = 0; i < 2; i++) {
          for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
              if (kids[i][j][k] != null) {
                List<Octree> containingKids = findContainer(pt, kids[i][j][k]);
                
                if (!containingKids.isEmpty()) {
                  ret.addAll(containingKids);
                  addedChild = true;
                }
              }
            }
          }
        }
      }

      if (!addedChild) {
        ret.add(parent);
      }
    }
    
    return ret;
  }

  private List<Octree> findContainer(M3d pt) {
    List<Octree> ret = new LinkedList<Octree>();
    
    for (Octree root : roots) {
      if (root.encloses(pt)) {
        ret.addAll(findContainer(pt, root));
      }
    }
    return ret;
  }
  
  private Octree findUniqueContainer(M3d pt) {
    List<Octree> containers = findContainer(pt);
    
    if (containers.size()==1) {
      return containers.get(0);
    } else {
      return null;
    }
  }

  public double getCutoff() {
    return cutoff;
  }

  public void setCutoff(double cutoff) {
    this.cutoff = cutoff;
  }

  public int getTargetLevel() {
    return targetLevel;
  }

  public void setTargetLevel(int targetLevel) {
    this.targetLevel = targetLevel;
    reset();
  }

  public LinkedList<Octree> getInProgress() {
    return inProgress;
  }
  
  public LinkedList<Octree> getFinished() {
    return finished;
  }
  
  double sumForces(M3d v) {
    double sum = 0;
    
    if (!samples.containsKey(v)) {
      for (Force f : forces) {
        sum += f.F(v);
      }
      samples.put(v, sum);
    }
    else {
      sum = samples.get(v);
    }

    return sum;
  }
  
  boolean isHot(M3d v) {
    return sumForces(v) > cutoff;
  }
  
  public void addForce(Force f) {
    forces.add(f);
  }
  
  public boolean addInterpolants(OctTreeEdge edge) {
    M3d a = edge.getEndPt(0);
    M3d b = edge.getEndPt(1);
    double ta = sumForces(a);
    double tb = sumForces(b);
    double t;

    if (ta<=cutoff && tb>cutoff) {
      t = (cutoff-ta) / (tb-ta);
      edge.setCrossingData(new M3d(a.plus(b.minus(a).times(t))), 
          a.minus(b).normalized());
      return true;
    } else if (tb<=cutoff && ta>cutoff) {
      t = (cutoff-tb) / (ta-tb);
      edge.setCrossingData(new M3d(b.plus(a.minus(b).times(t))), 
          b.minus(a).normalized());
      return true;
    }
    return false;
  }

  public EdgeMap getEdgeMap(int level) {
    if (edgeMapArray.length <= level) {
      EdgeMap[] temp = edgeMapArray;
      
      edgeMapArray = new EdgeMap[level + 5];
      for (int i = 0; i < temp.length; i++) {
        edgeMapArray[i] = temp[i];
      }
    }
    if (edgeMapArray[level] == null) {
      edgeMapArray[level] = new EdgeMap();
    }
    return edgeMapArray[level];
  }
  
  public OctTreeEdge getEdge(int level, M3d a, M3d b, M3d precomputedMidPt) {
    EdgeMap map = getEdgeMap(level);
    M3dPair pair = new M3dPair(a,b);
    OctTreeEdge edge;

    if (map.containsKey(pair)) {
      edge = map.get(pair);
    } else {
      edge = new OctTreeEdge(null, a, b, precomputedMidPt);
      addInterpolants(edge);
      map.put(new M3dPair(a,b), edge);
    }
    return edge;
  }
  
  public M3d subdivideEdge(int level, M3d a, M3d b, M3d precomputedMidPt) {
    OctTreeEdge edge = getEdge(level, a, b, precomputedMidPt);

    for (int i = 0; i<2; i++) {
      if (edge.getChild(i) == null) {
        edge.setChild(i, getEdge(level + 1, edge.getEndPt(i), edge.getMidPt(), null)); 
      }
    }
    return edge.getMidPt();
  }
  
  public M3d subdivideFace(int level, M3d a, M3d b, M3d alpha, M3d beta) {
    return subdivideEdge(level, alpha, beta, subdivideEdge(level, a, b, null));
  }
  
  public M3d subdivideCube(int level, M3d a, M3d b, M3d alpha, M3d beta, M3d alef, M3d bet) {
    return subdivideEdge(level, alef, bet, subdivideEdge(level, alpha, beta, subdivideEdge(level, a, b, null)));
  }

  public void refine() {
    while (!inProgress.isEmpty()) {
      Octree T = inProgress.remove();
      Octree[][][] children;
      
      T.refine();
      children = T.getChildOctrees();
      if (children != null) {
        for (int i = 0; i < 2; i++) {
          for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
              Octree t = children[i][j][k];
              
              if (t != null) {
                if (t.getLevel() < targetLevel) {
                  inProgress.addLast(t);
                }
                else if (!t.isEmpty()){
                  finished.add(t);
                }
              }
            }
          }
        }
      }
    }

    HashMap<M3dPair, OctTreeEdge> map = getEdgeMap(getTargetLevel());
    for (OctTreeEdge edge : map.values()) {
      if (edge.isInteresting()) {
        if (edge.size() > 0 && edge.size() < 4) {
          for (Octree o : edge) {
            for (int i = 0; i<6; i++) {
              if (o.hasInterestingFace(i, edge)) {
                M3d pt = o.getPointJustBeyondFace(i);
                Octree op = findUniqueContainer(pt);

                if (op.getLevel() < targetLevel) {
                  op.addTarget(pt);
                  inProgress.addLast(op);
                }
              }
            }
          }
        }
      }
    }

    if (!inProgress.isEmpty()) {
      refine();
    }
  }
}
