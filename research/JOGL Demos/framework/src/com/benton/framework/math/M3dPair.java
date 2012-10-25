package com.benton.framework.math;

public class M3dPair {
  private M3d A, B;
  
  public M3dPair(M3d A, M3d B) {
    this.A = A;
    this.B = B;
  }

  @Override
  public int hashCode() {
    return A.hashCode() + B.hashCode();
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    M3dPair other = (M3dPair) obj;
    if (A.equals(other.A)) {
      return B.equals(other.B);
    } else if (A.equals(other.B)) {
      return B.equals(other.A);
    } else {
      return false;
    }
  }
}

