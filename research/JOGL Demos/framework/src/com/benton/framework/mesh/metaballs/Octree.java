package com.benton.framework.mesh.metaballs;

import java.util.LinkedList;
import java.util.List;

import com.benton.framework.math.M3d;
import com.benton.framework.mesh.SimpleMesh;



/*      010----------110          --------------          2------------6  
 *     /|           /|           /|           /|         /|           /|      
 *    / |          / |          / |   2      / |        / |          / |      
 *   /  |         /  |         /  |     5   /  |       /  |         /  |      
 *  011-----------111|        |-------------|  |      3-------------7  |      
 *  |   |         |  |        | 1 |         |4 |      |   |         |  |      
 *  |   000-------|--100      |   |---------|--|      |   0---------|--4      
 *  |  /          |  /        |  /  0       |  /      |  /          |  /      
 *  | /           | /         | /     3     | /       | /           | /       
 *  |/            |/          |/            |/        |/            |/        
 *  001-----------101         |-------------/         1-------------5         
 *    Vertex codes              Face indices           Vertex indices
 */

@SuppressWarnings("serial")
public class Octree extends SimpleMesh {
  
  private static final int[][][] tetrahedra = {
    { {0,0,0}, {0,1,1}, {1,0,1}, {1,1,0} },
    { {0,0,0}, {0,0,1}, {1,0,1}, {0,1,1} },
    { {1,1,0}, {0,1,1}, {1,0,1}, {1,1,1} },
    { {0,0,0}, {0,1,1}, {0,1,0}, {1,1,0} },
    { {0,0,0}, {1,0,0}, {1,0,1}, {1,1,0} },
  };
  
  private static final int[][][] faces = {
    { {0,0,1}, {1,0,1}, {1,1,1}, {0,1,1} },
    { {0,1,0}, {0,0,0}, {0,0,1}, {0,1,1} },
    { {0,1,1}, {1,1,1}, {1,1,0}, {0,1,0} },
    { {0,0,1}, {1,0,1}, {1,0,0}, {0,0,0} },
    { {1,0,1}, {1,0,0}, {1,1,0}, {1,1,1} },
    { {1,0,0}, {0,0,0}, {0,1,0}, {1,1,0} },
  };
  
  private static final int[][][] edges = {
    { {0,0,0}, {1,0,0} },
    { {1,0,0}, {1,1,0} },
    { {1,1,0}, {0,1,0} },
    { {0,1,0}, {0,0,0} },
    { {0,0,1}, {1,0,1} },
    { {1,0,1}, {1,1,1} },
    { {1,1,1}, {0,1,1} },
    { {0,1,1}, {0,0,1} },
    { {0,0,0}, {0,0,1} },
    { {1,0,0}, {1,0,1} },
    { {1,1,0}, {1,1,1} },
    { {0,1,0}, {0,1,1} },
  };
  
  private int level;
  private M3d[][][] corners;
  private LinkedList<M3d> targets;
  private Octree[][][] children;
  private ImplicitSurface surface;
  
  Octree(ImplicitSurface surface, int level, M3d[][][] coords, int x, int y, int z, List<M3d> possibleTargets) {
    boolean isOdd = (((x+y+z)&1) != 0);
    this.surface = surface;
    this.level = level;
    this.corners = new M3d[2][2][2];
    this.targets = new LinkedList<M3d>();

    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 2; k++) {
          corners[i][j][k] = coords[x+i][y+j][z+k];
        }
      }
    }
    
    for (M3d pt : possibleTargets) {
      if (encloses(pt)) {
        addTarget(pt);
      }
    }

    if (this.level == surface.getTargetLevel()) {
      polygonalize(isOdd);
    }
  }
  
  void polygonalize(boolean isOdd) {
    for (int i = 0; i < tetrahedra.length; i++) {
      int crossings = 0;
      OctTreeEdge[] arr = { null, null, null, null };
      int[][] tet = tetrahedra[i];

      for (int j = 0; j < tet.length; j++) {
        for (int k = j+1; k < tet.length; k++) {
          M3d A = corners [tet[j][0]] [isOdd ? (1-tet[j][1]) : tet[j][1]] [tet[j][2]];
          M3d B = corners [tet[k][0]] [isOdd ? (1-tet[k][1]) : tet[k][1]] [tet[k][2]];
          
          if (surface.isHot(A) != surface.isHot(B)) {
            arr[crossings++] = surface.getEdge(level, A, B, null);
          }
        }
      }

      if (crossings == 4) {
        boolean zeroOneAdjacent = arr[0].hasSharedEndPoint(arr[1]); 
        OctTreeEdge a = arr[0];
        OctTreeEdge b = zeroOneAdjacent ? arr[1] : arr[2];
        OctTreeEdge c = zeroOneAdjacent ? arr[2] : arr[1];
        OctTreeEdge d = arr[3];
        
        addPolyWithOrientation(
            a.getInterpolatedCrossing(), 
            b.getInterpolatedCrossing(), 
            c.getInterpolatedCrossing(), 
            arr[0].getNormalDir());
        addPolyWithOrientation(
            b.getInterpolatedCrossing(), 
            c.getInterpolatedCrossing(), 
            d.getInterpolatedCrossing(), 
            arr[0].getNormalDir());
      } else if (crossings == 3) {
        addPolyWithOrientation(
            arr[0].getInterpolatedCrossing(), 
            arr[1].getInterpolatedCrossing(), 
            arr[2].getInterpolatedCrossing(), 
            arr[0].getNormalDir());
      }
    }
  }
  
  void addTarget(M3d pt) {
    targets.add(pt);
  }
  
  void addSelfToOctreeEdges() {
    for (int i = 0; i < 12; i++) {
      OctTreeEdge edge = surface.getEdge(
          level,
          corners[edges[i][0][0]][edges[i][0][1]][edges[i][0][2]],
          corners[edges[i][1][0]][edges[i][1][1]][edges[i][1][2]],
          null);
      if (edge.isInteresting()) {
        edge.add(this);
      }
    }
  }
  
  boolean encloses(M3d pt) {
    return pt.getX() >= corners[0][0][0].getX() && pt.getX() <= corners[1][1][1].getX()
        && pt.getY() >= corners[0][0][0].getY() && pt.getY() <= corners[1][1][1].getY()
        && pt.getZ() >= corners[0][0][0].getZ() && pt.getZ() <= corners[1][1][1].getZ();
  }
  
  boolean isInteresting() {
    if (!targets.isEmpty()) {
      return true;
    } else {
      boolean first = surface.isHot(corners[0][0][0]);
      
      for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
          for (int k = 0; k < 2; k++) {
            if (surface.isHot(corners[i][j][k]) != first) {
              return true;
            }
          }
        }
      }
      return false;
    }
  }

  boolean hasInterestingFace(int faceIndex, OctTreeEdge edge) {
    int [] firstFaceCorner = faces[faceIndex][0];
    boolean first = surface.isHot(corners[firstFaceCorner[0]][firstFaceCorner[1]][firstFaceCorner[2]]);
    boolean interested = false;
    
    for (int i = 1; i < 4 && !interested; i++) {
      int []corner = faces[faceIndex][i];
      if (edge.hasEndPoint(corners[corner[0]][corner[1]][corner[2]])) {
        interested = true;
      }
    }

    if (interested) {
      for (int i = 1; i<4; i++) {
        int []corner = faces[faceIndex][i];
        if (surface.isHot(corners[corner[0]][corner[1]][corner[2]]) != first) {
          return true;
        }
      }
    }
    return false;
  }
  
  M3d getPointJustBeyondFace(int faceIndex) {
    M3d faceCenter = new M3d();
    M3d center = corners[0][0][0].plus(corners[1][1][1]).times(0.5);
    
    for (int i = 0; i<4; i++) {
      int []corner = faces[faceIndex][i];
      M3d pt = corners[corner[0]][corner[1]][corner[2]];
      
      faceCenter = faceCenter.plus(pt);
    }
    faceCenter = faceCenter.times(0.25);
    return center.plus(faceCenter.minus(center).times(1.1));
  }
  
  M3d[][][] makeSubCorners() {
    M3d[][][] subCorners = new M3d[3][3][3];
    
    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 2; k++) {
          subCorners[i*2][j*2][k*2] = corners[i][j][k];
        }
      }
    }
    
    for (int i = 0; i <= 2; i+=2) {
      for (int j = 0; j <= 2; j+=2) {
        subCorners[1][i][j] = surface.subdivideEdge(level, subCorners[0][i][j], subCorners[2][i][j], null);
        subCorners[i][1][j] = surface.subdivideEdge(level, subCorners[i][0][j], subCorners[i][2][j], null);
        subCorners[i][j][1] = surface.subdivideEdge(level, subCorners[i][j][0], subCorners[i][j][2], null);
      }
    }
    
    for (int i = 0; i <= 2; i+=2) {
      subCorners[i][1][1] = surface.subdivideFace(
          level, 
          subCorners[i][0][1], subCorners[i][2][1], 
          subCorners[i][1][0], subCorners[i][1][2]);
      subCorners[1][i][1] = surface.subdivideFace(
          level, 
          subCorners[0][i][1], subCorners[2][i][1], 
          subCorners[1][i][0], subCorners[1][i][2]);
      subCorners[1][1][i] = surface.subdivideFace(
          level, 
          subCorners[1][0][i], subCorners[1][2][i], 
          subCorners[0][1][i], subCorners[2][1][i]);
    }
    
    subCorners[1][1][1] = surface.subdivideCube(
        level, 
        subCorners[0][1][1], subCorners[2][1][1],
        subCorners[1][0][1], subCorners[1][2][1],
        subCorners[1][1][0], subCorners[1][1][2]);
    
    return subCorners;
  }
  
  int getLevel() {
    return level;
  }
  
  public M3d[][][] getCorners() {
    return corners;
  }
  
  Octree[][][] getChildOctrees() {
    return children;
  }
  
  void refine() {
    M3d[][][] subCorners = makeSubCorners();

    if (children == null) {
      children = new Octree[2][2][2];
    }

    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 2; k++) {
          if (children[i][j][k] == null) {
            Octree child = new Octree(surface, level+1, subCorners, i, j, k, targets);
            if (child.isInteresting()) {
              if (child.getLevel() == surface.getTargetLevel()) {
                child.addSelfToOctreeEdges();
              }
              children[i][j][k] = child;
            }
          }
        }
      }
    }
  }
}