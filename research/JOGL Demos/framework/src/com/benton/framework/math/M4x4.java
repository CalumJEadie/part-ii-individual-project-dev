package com.benton.framework.math;


/*
 * Math3d - The 3D Computer Graphics Math Library
 * Copyright (C) 1996-2000 by J.E. Hoffmann <je-h@gmx.net>
 * All rights reserved.
 * 
 * This program is  free  software;  you can redistribute it and/or modify it
 * under the terms of the  GNU Lesser General Public License  as published by 
 * the  Free Software Foundation;  either version 2.1 of the License,  or (at 
 * your option) any later version.
 *
 * This  program  is  distributed in  the  hope that it will  be useful,  but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or  FITNESS FOR A  PARTICULAR PURPOSE.  See the  GNU Lesser General Public  
 * License for more details.
 *
 * You should  have received  a copy of the GNU Lesser General Public License
 * along with  this program;  if not, write to the  Free Software Foundation,
 * Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 * $Id: m4x4.cpp,v 1.1 2005/09/09 13:42:14 pb355 Exp $
 */
public class M4x4 {
  
  double data[] = new double[16];

  public M4x4() {
    for (int i = 0; i<16; i++) {
      data[i] = (((i/4) == (i%4)) ? 1 : 0);
    }
  }

  public M4x4(double[][] A) {
    for (int row = 0; row<4; row++) {
      for (int col = 0; col<4; col++) {
        data[row*4+col] = A[row][col];
      }
    }
  }

  public M4x4(M4x4 A) {
    for (int i = 0; i<16; i++) {
      data[i] = A.data[i];
    }
  }
  
  public double[] getData() {
    return data;
  }

  public void identity() {
    for (int i = 0; i<16; i++) {
      data[i] = (((i/4) == (i%4)) ? 1 : 0);
    }
  }

  public boolean isIdentity() {
    for (int i = 0; i<16; i++) {
      if (data[i] != (((i/4) == (i%4)) ? 1 : 0)) {
        return false;
      }
    }
    return true;
  }

  public M4x4 plus(M4x4 A) {
    M4x4 M = new M4x4();

    for (int i = 0; i<16; i++) {
      M.data[i] = data[i] + A.data[i];
    }
    return M;
  }

  public M4x4 minus(M4x4 A) {
    M4x4 M = new M4x4();

    for (int i = 0; i<16; i++) {
      M.data[i] = data[i] - A.data[i];
    }
    return M;
  }

  public M4x4 neg() {
    M4x4 M = new M4x4();

    for (int i = 0; i<16; i++) {
      M.data[i] = -data[i];
    }
    return M;
  }

  public M4x4 times(M4x4 A)
  {
    M4x4 M = new M4x4();

    for (int j=0; j<4; j++) {
      for (int i=0; i<4; i++) {
        double ab=0.0f;
        for (int k=0; k<4; k++) 
          ab+=data[k*4+i]*A.data[j*4+k];
        M.data[j*4+i]=ab;
      }
    }
    return M;
  }

  public M4x4 times(double k) {
    M4x4 M = new M4x4();

    for (int i = 0; i<16; i++) {
      M.data[i] = data[i]*k;
    }
    return M;
  }

  public M4x4 transposed() {
    M4x4 M = new M4x4();
    double swp;

    for (int j=0; j<4; j++) {
      for (int i=j+1; i<4; i++) {
        swp=data[j*4+i];
        M.data[j*4+i]=data[i*4+j];
        M.data[i*4+j]=swp;
      }
    }
    return M;
  }
  
  double cell(int col, int row) {
    return data[col*4+row];
  }
  
  void setCell(int col, int row, double value) {
    data[col*4+row] = value;
  }

  private boolean inverse(final double A[][], double AI[][])
  {
    int n = A.length;
    int row[] = new int[n];
    int col[] = new int[n];
    double temp[] = new double[n];
    int hold , I_pivot , J_pivot;
    double pivot, abs_pivot;

    if(A[0].length!=n || AI.length!=n || AI[0].length!=n)
    {
      return false;
    }
    for(int i=0; i<n; i++)
      for(int j=0; j<n; j++)
        AI[i][j] = A[i][j];

    // set up row and column interchange vectors
    for(int k=0; k<n; k++)
    {
      row[k] = k ;
      col[k] = k ;
    }
    // begin main reduction loop
    for(int k=0; k<n; k++)
    {
      // find largest element for pivot
      pivot = AI[row[k]][col[k]] ;
      I_pivot = k;
      J_pivot = k;
      for(int i=k; i<n; i++)
      {
        for(int j=k; j<n; j++)
        {
          abs_pivot = Math.abs(pivot) ;
          if(Math.abs(AI[row[i]][col[j]]) > abs_pivot)
          {
            I_pivot = i ;
            J_pivot = j ;
            pivot = AI[row[i]][col[j]] ;
          }
        }
      }
      if(Math.abs(pivot) < 1.0E-15)
      {
        return false;
      }
      hold = row[k];
      row[k]= row[I_pivot];
      row[I_pivot] = hold ;
      hold = col[k];
      col[k]= col[J_pivot];
      col[J_pivot] = hold ;
       // reduce about pivot
      AI[row[k]][col[k]] = 1.0 / pivot ;
      for(int j=0; j<n; j++)
      {
        if(j != k)
        {
          AI[row[k]][col[j]] = AI[row[k]][col[j]] * AI[row[k]][col[k]];
        }
      }
      // inner reduction loop
      for(int i=0; i<n; i++)
      {
        if(k != i)
        {
          for(int j=0; j<n; j++)
          {
            if( k != j )
            {
              AI[row[i]][col[j]] = AI[row[i]][col[j]] - AI[row[i]][col[k]] * AI[row[k]][col[j]] ;
            }
          }
          AI[row[i]][col [k]] = - AI[row[i]][col[k]] * AI[row[k]][col[k]] ;
        }
      }
    }
    // end main reduction loop

    // unscramble rows
    for(int j=0; j<n; j++)
    {
      for(int i=0; i<n; i++)
      {
        temp[col[i]] = AI[row[i]][j];
      }
      for(int i=0; i<n; i++)
      {
        AI[i][j] = temp[i] ;
      }
    }
    // unscramble columns
    for(int i=0; i<n; i++)
    {
      for(int j=0; j<n; j++)
      {
        temp[row[j]] = AI[i][col[j]] ;
      }
      for(int j=0; j<n; j++)
      {
        AI[i][j] = temp[j] ;
      }
    }
    return true;
  }
  
  public M4x4 inverted() {
    double[][] input = new double[4][4];
    double[][] output = new double[4][4];
    
    for (int row = 0; row<4; row++) {
      for (int col = 0; col<4; col++) {
        input[row][col] = cell(row, col);
        output[row][col] = 0;
      }
    }
    
    if (!inverse(input, output)) {
      throw new IllegalArgumentException("Could not invert matrix" + this);
    } else {
      return new M4x4(output); 
    }
  }
  
  public static M4x4 translation(M3d t) {
    M4x4 M = new M4x4();
    
    for (int i=0; i<3; i++) {
      M.data[3*4+i] = t.get(i);
    }
    return M;
  }

  public static M4x4 scale(M3d t) {
    M4x4 M = new M4x4();
    
    for (int i=0; i<3; i++) {
      M.data[i*4+i] = t.get(i);
    }
    return M;
  }

  public void translate(M3d t) {
    for (int i=0; i<3; i++) {
      data[3*4+i] += data[0*4+i]*t.get(0) + data[1*4+i]*t.get(1) + data[2*4+i]*t.get(2);
    }
  }

  public static M4x4 rotation(M3d axis, double phi) {
    double c = Math.cos(phi);
    double s = Math.sin(phi);
    double t = 1-c;
    double x, y, z;
    M4x4 M = new M4x4();
    double data[] = M.getData();
    
    axis = axis.normalized();
    x = axis.getX();
    y = axis.getY();
    z = axis.getZ();
    data[0*4+0] = t*x*x+c;   data[0*4+1] = t*x*y+s*z; data[0*4+2] = t*x*z-s*y; data[0*4+3] = 0;
    data[1*4+0] = t*x*y-s*z; data[1*4+1] = t*y*y+c;   data[1*4+2] = t*y*z+s*x; data[1*4+3] = 0;
    data[2*4+0] = t*x*z+s*y; data[2*4+1] = t*y*z-s*x; data[2*4+2] = t*z*z+c;   data[2*4+3] = 0;
    data[3*4+0] = 0;         data[3*4+1] = 0;         data[3*4+2] = 0;         data[3*4+3] = 1;
    return M;
  }
  
  public void rotate(M3d axis, double phi) {
    data = this.times(rotation(axis,phi)).getData();
  }

  public M3d getCol(int col) {
    return new M3d(data[col*4+0], data[col*4+1], data[col*4+2]);
  }

  public M3d getRow(int row) {
    return new M3d(data[0*4+row], data[1*4+row], data[2*4+row]);
  }

  public M3d times(M3d C)
  {
    double a,b,c;

    a = data[0*4+0]*C.get(0) + data[1*4+0]*C.get(1) + data[2*4+0]*C.get(2) + data[3*4+0];
    b = data[0*4+1]*C.get(0) + data[1*4+1]*C.get(1) + data[2*4+1]*C.get(2) + data[3*4+1];
    c = data[0*4+2]*C.get(0) + data[1*4+2]*C.get(1) + data[2*4+2]*C.get(2) + data[3*4+2];
    return new M3d(a,b,c);
  }

  public M4x4 extract3x3() {
    M4x4 M = new M4x4();
    double d[] = M.getData();
    
    for (int i = 0; i<4; i++) {
      for (int j = 0; j<4; j++) {
        if (i < 3) {
          d[i*4+j] = data[i*4+j]; 
        } else if (i==j) {
          d[i*4+j] = 1;
        } else {
          d[i*4+j] = 0;
        }
      }
    }
    return M;
  }

  public String toString() {
    String str = new String();
    
    for (int i = 0; i<16; i++) {
      str += data[i];
      if (i<15) {
        str += ", ";
      }
    }
    return str.toString();
  }
}
