package shaders;

import static shaders.Torus.di;
import static shaders.Torus.dj;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import javax.media.opengl.GL;

import com.benton.framework.math.M3d;
import com.benton.framework.mesh.Face;
import com.benton.framework.mesh.Mesh;
import com.benton.framework.mesh.Vertex;



public abstract class ShaderRenderer {
  
  protected int vShader;
  protected int fShader;
  protected int shaderProgram;
  private Torus torus;
  private Mesh teapot;
  
  public ShaderRenderer(Torus torus, Mesh teapot) {
    this.torus = torus;
    this.teapot = teapot;
  }

  protected String[] readShader(String name) {
    List<String> lines = new LinkedList<String>();
    BufferedReader brv = null;
    String line;

    try {
      brv = new BufferedReader(new FileReader("shaders/" + name));
      while ((line=brv.readLine()) != null) {
        lines.add(line + "\n");
      }
      String[] ret = new String[lines.size()];
      int i = 0;
      for (String s : lines) {
        ret[i++] = s;
      }
      return ret;
    } catch (IOException e) {
      System.out.println("IOException: " + e.getMessage());
      System.exit(-1);
      return null;
    }
  }
  
  protected int[] lineLengths(String[] lines) {
    int[] ret = new int[lines.length];
    
    for (int i = 0; i < lines.length; i++) {
      ret[i] = lines[i].length();
    }
    return ret;
  }
  
  public void checkVersion(final GL gl) {
    System.out.println("GL version: " + gl.glGetString(GL.GL_VERSION));
    System.out.println("GL shading language version: " + gl.glGetString(GL.GL_SHADING_LANGUAGE_VERSION));
    System.out.println("GL shading language version (ARB): " + gl.glGetString(GL.GL_SHADING_LANGUAGE_VERSION));
  }

  public void checkShader(final GL gl, int shader, String filename) {
    int[] check = new int[1];
    gl.glGetShaderiv(shader, GL.GL_INFO_LOG_LENGTH, check, 0);
    int logLength = check[0];
    byte[] compilecontent = new byte[logLength+1];
    gl.glGetShaderInfoLog(shader, logLength, check, 0, compilecontent, 0);
    if (logLength > 1) {
      String infolog = new String(compilecontent);
      if (infolog.trim().compareTo("No errors.") != 0) {
        checkVersion(gl);
        System.out.println("Info log for shader '" + filename + "' (ID " + shader + "):");
        System.out.println(infolog);
        System.exit(-1);
      }
    }
  }
  
  public void checkProgram(final GL gl, int program) {
    int[] check = new int[1];

    gl.glGetProgramiv(program, GL.GL_INFO_LOG_LENGTH, check, 0);
    int logLength = check[0];
    byte[] compilecontent = new byte[logLength+1];
    gl.glGetProgramInfoLog(program, logLength, check, 0, compilecontent, 0);
    String infolog = new String(compilecontent);
    if (logLength > 1) {
      if (!infolog.trim().isEmpty()) {
        checkVersion(gl);
        System.out.println("Info Log of Program Object ID: " + program);
        System.out.println(infolog);
        gl.glGetProgramiv(program, GL.GL_VALIDATE_STATUS, check, 0);
        System.out.println("Status: " + check[0]);
        System.exit(-1);
      }
    }
  }

  public abstract void init(final GL gl);
  
  protected void init(final GL gl, String vertexShader, String fragmentShader) {
    vShader = gl.glCreateShader(GL.GL_VERTEX_SHADER);
    String[] vsrc = readShader(vertexShader);
    gl.glShaderSource(vShader, vsrc.length, vsrc, lineLengths(vsrc), 0);
    gl.glCompileShader(vShader);

    checkShader(gl, vShader, vertexShader);
    
    fShader = gl.glCreateShader(GL.GL_FRAGMENT_SHADER);
    String[] fsrc = readShader(fragmentShader);
    gl.glShaderSource(fShader, fsrc.length, fsrc, lineLengths(fsrc), 0);
    gl.glCompileShader(fShader);

    checkShader(gl, fShader, fragmentShader);
    
    shaderProgram = gl.glCreateProgram();
    gl.glAttachShader(shaderProgram, vShader);
    gl.glAttachShader(shaderProgram, fShader);
    gl.glLinkProgram(shaderProgram);

    gl.glValidateProgram(shaderProgram);
    checkProgram(gl, shaderProgram);

    gl.glUseProgram(shaderProgram);
  }

  public void disable(final GL gl) {
    gl.glDeleteProgram(shaderProgram);
  }
  
  protected void preVertex(GL gl, Vertex v) {
    // Do nothing
  }
  
  protected void vertex(GL gl, int i, int j) {
    M3d normal = torus.getNormal(i, j);
    M3d vertex = torus.getVertex(i, j);
    
    gl.glNormal3dv(normal.get(), 0);
    gl.glVertex3dv(vertex.get(), 0);
  }

  public void displayTorus(final GL gl) {
    gl.glBegin(GL.GL_QUADS);
    for (int i = 0; i<di; i++) {
      for (int j = 0; j<dj; j++) {
        vertex(gl, i, j);
        vertex(gl, i+1, j);
        vertex(gl, i+1, j+1);
        vertex(gl, i, j+1);
      }
    }
    gl.glEnd();
  }

  public void displayTeapot(final GL gl) {
    for (Face face : teapot) {
      gl.glBegin(GL.GL_POLYGON);
      for (int i = 0; i < face.getNumVerts(); i++) {
        Vertex v = face.getVertex(i);

        preVertex(gl, v);
        gl.glNormal3dv(v.getNormal().get(), 0);
        gl.glVertex3dv(v.get(), 0);
      }
      gl.glEnd();
    }
  }
}
