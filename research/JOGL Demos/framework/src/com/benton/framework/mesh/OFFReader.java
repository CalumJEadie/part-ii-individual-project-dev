package com.benton.framework.mesh;

import com.benton.framework.math.M3d;

public class OFFReader {
  
  private static class StringTokenizer {
    private String buffer;
    private int offset = 0;
    
    StringTokenizer(String val) {
      buffer = val;
      offset = 0;
    }
    
    boolean isspace(char c) {
      return (c == ' ') || (c == '\n') || (c == '\t');
    }
    
    String next(char token) {
      String ret = new String();
      
      while (isspace(buffer.charAt(offset)) || buffer.charAt(offset) == '#') {
        while (offset < buffer.length() && isspace(buffer.charAt(offset))) {
          offset++;
        }
        if (offset < buffer.length() && buffer.charAt(offset) == '#') {
          while (offset < buffer.length() && buffer.charAt(offset) != '\n') {
            offset++;
          }
        }
      }
      
      while (offset < buffer.length() && buffer.charAt(offset) != token) {
        ret = ret + buffer.charAt(offset++);
      }
      if (offset < buffer.length()) {
        offset++;
      }
      return ret.trim();
    }
  }

  public static Mesh parse(String data) {
    String chunk;
    StringTokenizer tokenizer, tokie;
    int nVerts, nFaces;
    Mesh mesh = new Mesh();

    tokenizer = new StringTokenizer(data);
    chunk = tokenizer.next('\n');
    if (chunk.compareTo("OFF") != 0) {
      throw new UnsupportedOperationException("Ill-formatted OFF data read: " + chunk);
    }

    tokie = new StringTokenizer(tokenizer.next('\n'));
    nVerts = Integer.valueOf(tokie.next(' '));
    nFaces = Integer.valueOf(tokie.next(' '));
    
    Vertex verts[] = new Vertex[nVerts];

    for (int i = 0; i < nVerts; i++)
    {
      tokie = new StringTokenizer(tokenizer.next('\n'));
      double x = Double.valueOf(tokie.next(' '));
      double y = Double.valueOf(tokie.next(' '));
      double z = Double.valueOf(tokie.next(' '));

      verts[i] = new Vertex(new M3d(x, y, z));
    }
    for (int i = 0; i<nFaces; i++)
    {
      tokie = new StringTokenizer(tokenizer.next('\n'));
      int n = Integer.valueOf(tokie.next(' '));
      Vertex faceVerts[] = new Vertex[n];
      
      for (int j = 0; j < n; j++) {
        faceVerts[j] = verts[Integer.valueOf(tokie.next(' '))];
      }
      mesh.add(new Face(faceVerts));
    }

    mesh.computeAllNormals();
    return mesh;
  }
}
