package com.benton.framework.math;

import static java.lang.Math.PI;
import static java.lang.Math.abs;
import static java.lang.Math.acos;
import static java.lang.Math.cos;
import static java.lang.Math.pow;
import static java.lang.Math.sqrt;

/**
 * Code from Graphics Gems
 *
 * http://tog.acm.org/GraphicsGems/gems/Roots3And4.c
 */
public class MathUtil {

  public static boolean IsZero(double r) {
    return abs(r) <= 0.000001;
  }
  
  public static double cbrt(double x) {
    return ((x) > 0.0 ? pow(x, 1.0/3.0) : 
           ((x) < 0.0 ? -pow(-x, 1.0/3.0) : 0.0));
  }
  
  public static double sqr(double x) {
    return pow(x, 2);
  }
  
  public static int SolveQuadric(double[/*3*/] c, double[/*2*/] s) {
    double p, q, D;
  
    /* normal form: x^2 + px + q = 0 */
  
    p = c[ 1 ] / (2 * c[ 2 ]);
    q = c[ 0 ] / c[ 2 ];
  
    D = p * p - q;
  
    if (IsZero(D))
    {
      s[ 0 ] = - p;
      return 1;
    }
    else if (D < 0)
    {
      return 0;
    }
    else /* if (D > 0) */
    {
      double sqrt_D = sqrt(D);
      
      s[ 0 ] =   sqrt_D - p;
      s[ 1 ] = - sqrt_D - p;
      return 2;
    }
  }
  
  public static int SolveCubic(double[/*4*/] c, double[/*3*/] s) {
  int     i, num;
  double  sub;
  double  A, B, C;
  double  sq_A, p, q;
  double  cb_p, D;

  /* normal form: x^3 + Ax^2 + Bx + C = 0 */

  A = c[ 2 ] / c[ 3 ];
  B = c[ 1 ] / c[ 3 ];
  C = c[ 0 ] / c[ 3 ];

  /*  substitute x = y - A/3 to eliminate quadric term:
      x^3 +px + q = 0 */

  sq_A = A * A;
  p = 1.0/3 * (- 1.0/3 * sq_A + B);
  q = 1.0/2 * (2.0/27 * A * sq_A - 1.0/3 * A * B + C);

  /* use Cardano's formula */

  cb_p = p * p * p;
  D = q * q + cb_p;

  if (IsZero(D))
  {
    if (IsZero(q)) /* one triple solution */
    {
      s[ 0 ] = 0;
      num = 1;
    }
    else /* one single and one double solution */
    {
      double u = cbrt(-q);
      s[ 0 ] = 2 * u;
      s[ 1 ] = - u;
      num = 2;
    }
  }
  else if (D < 0) /* Casus irreducibilis: three real solutions */
  {
    double phi = 1.0/3 * acos(-q / sqrt(-cb_p));
    double t = 2 * sqrt(-p);
    
    s[ 0 ] =   t * cos(phi);
    s[ 1 ] = - t * cos(phi + PI / 3);
    s[ 2 ] = - t * cos(phi - PI / 3);
    num = 3;
  }
  else /* one real solution */
  {
    double sqrt_D = sqrt(D);
    double u = cbrt(sqrt_D - q);
    double v = - cbrt(sqrt_D + q);
    
    s[ 0 ] = u + v;
    num = 1;
  }

  /* resubstitute */

  sub = 1.0/3 * A;

  for (i = 0; i < num; ++i) {
    s[ i ] -= sub;
  }
  
  return num;
}
  
  public static int SolveQuartic(double[/*5*/] c, double[/*4*/] s) {
    double[] coeffs = new double[4];
    double  z, u, v, sub;
    double  A, B, C, D;
    double  sq_A, p, q, r;
    int     i, num;
  
    /* normal form: x^4 + Ax^3 + Bx^2 + Cx + D = 0 */
  
    A = c[ 3 ] / c[ 4 ];
    B = c[ 2 ] / c[ 4 ];
    C = c[ 1 ] / c[ 4 ];
    D = c[ 0 ] / c[ 4 ];
  
    /*  substitute x = y - A/4 to eliminate cubic term:
        x^4 + px^2 + qx + r = 0 */
  
    sq_A = A * A;
    p = - 3.0/8 * sq_A + B;
    q = 1.0/8 * sq_A * A - 1.0/2 * A * B + C;
    r = - 3.0/256*sq_A*sq_A + 1.0/16*sq_A*B - 1.0/4*A*C + D;
  
    if (IsZero(r))
    {
      /* no absolute term: y(y^3 + py + q) = 0 */
      
      coeffs[ 0 ] = q;
      coeffs[ 1 ] = p;
      coeffs[ 2 ] = 0;
      coeffs[ 3 ] = 1;
      
      num = SolveCubic(coeffs, s);
      
      s[ num++ ] = 0;
    }
    else
    {
      /* solve the resolvent cubic ... */
      
      coeffs[ 0 ] = 1.0/2 * r * p - 1.0/8 * q * q;
      coeffs[ 1 ] = - r;
      coeffs[ 2 ] = - 1.0/2 * p;
      coeffs[ 3 ] = 1;
      
      SolveCubic(coeffs, s);
      
      /* ... and take the one real solution ... */
      
      z = s[ 0 ];
      
      /* ... to build two quadric equations */
      
      u = z * z - r;
      v = 2 * z - p;
      
      if (IsZero(u)) {
        u = 0;
      } else if (u > 0) {
        u = sqrt(u);
      } else {
        return 0;
      }
      
      if (IsZero(v)) {
        v = 0;
      } else if (v > 0) {
        v = sqrt(v);
      } else {
        return 0;
      }
      
      coeffs[ 0 ] = z - u;
      coeffs[ 1 ] = q < 0 ? -v : v;
      coeffs[ 2 ] = 1;
      
      num = SolveQuadric(coeffs, s);
      
      coeffs[ 0 ]= z + u;
      coeffs[ 1 ] = q < 0 ? v : -v;
      coeffs[ 2 ] = 1;
      double[] s2 = new double[2];
      int n2;
      
      n2 = SolveQuadric(coeffs, s2);
      for (int j = 0; j<n2; j++) {
        s[num+j] = s2[j];
      }
      num += n2;
    }
  
    /* resubstitute */
  
    sub = 1.0/4 * A;
  
    for (i = 0; i < num; ++i) {
      s[ i ] -= sub;
    }
  
    return num;
  } 

  public static M3d intersectPlane(M3d linePtOne, M3d linePtTwo, M3d planePtOne, M3d planePtTwo, M3d planePtThree) {
    M3d N = planePtTwo.minus(planePtOne).cross(planePtThree.minus(planePtOne)).normalized();
    M3d D = linePtTwo.minus(linePtOne).normalized();
    
    if (N.dot(D)==0) {
      return null;
    } else {
      double t = (N.dot(planePtOne) - N.dot(linePtOne)) / N.dot(D);
      
      return linePtOne.plus(D.times(t));
    }
  }
}
