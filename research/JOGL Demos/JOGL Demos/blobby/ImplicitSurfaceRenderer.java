package blobby;

import java.util.ArrayList;
import java.util.LinkedList;

import javax.media.opengl.GL;

import com.benton.framework.math.M3d;
import com.benton.framework.mesh.metaballs.ImplicitSurface;
import com.benton.framework.mesh.metaballs.Octree;


public class ImplicitSurfaceRenderer {
  
  private ImplicitSurface surface;
  private boolean showEdges = true;
  private boolean showBoxes = false;

  public ImplicitSurfaceRenderer(ImplicitSurface surface) {
    this.surface = surface;
  }
  
  private void renderOctrees(GL gl, LinkedList<Octree> L, boolean normals) {
    for (Octree octree : L) {
      for (ArrayList<M3d> poly : octree) {
        if (normals) {
          gl.glNormal3dv(poly.get(2).minus(poly.get(1)).cross(poly.get(0).minus(poly.get(1))).normalized().get(), 0);
        }
        for (M3d pt : poly) {
          gl.glVertex3dv(pt.get(), 0);
        }
      }
    }
  }
  
  private void renderOctreeBoxes(GL gl, LinkedList<Octree> L, boolean normals) {
    for (Octree octree : L) {
      for (int x = 0; x<2; x++) {
        for (int y = 0; y<2; y++) {
          for (int z = 0; z<2; z++) {
            if (x > 0) {
              gl.glVertex3dv(octree.getCorners()[0][y][z].get(), 0);
              gl.glVertex3dv(octree.getCorners()[1][y][z].get(), 0);
            }
            if (y > 0) {
              gl.glVertex3dv(octree.getCorners()[x][0][z].get(), 0);
              gl.glVertex3dv(octree.getCorners()[x][1][z].get(), 0);
            }
            if (z > 0) {
              gl.glVertex3dv(octree.getCorners()[x][y][0].get(), 0);
              gl.glVertex3dv(octree.getCorners()[x][y][1].get(), 0);
            }
          }
        }
      }
    }
  }
  
  public boolean getShowBoxes() {
    return showBoxes;
  }
  
  public void setShowBoxes(boolean boxes) { 
    this.showBoxes = boxes;
  }

  public boolean getShowEdges() {
    return showEdges;
  }
  
  public void setShowEdges(boolean edges) { 
    this.showEdges = edges;
  }

  public void render(GL gl) {
    gl.glDisable(GL.GL_LIGHTING);    

    if (showEdges) {
      gl.glColor3f(0,0,0);
      gl.glPolygonMode(GL.GL_FRONT, GL.GL_LINE);
      gl.glBegin(GL.GL_TRIANGLES);
      renderOctrees(gl, surface.getFinished(), false);
      gl.glEnd();
    }
    
    if (showBoxes) {
      gl.glColor3f(0.5f,0.5f,0.5f);
      gl.glBegin(GL.GL_LINES);
      renderOctreeBoxes(gl, surface.getFinished(), false);
      gl.glEnd();
    }

    gl.glEnable(GL.GL_LIGHTING);

    gl.glColor3f(1,1,1);
    gl.glPolygonMode(GL.GL_FRONT, GL.GL_FILL);
    gl.glBegin(GL.GL_TRIANGLES);
    renderOctrees(gl, surface.getFinished(), true);
    gl.glEnd();
  }
}
