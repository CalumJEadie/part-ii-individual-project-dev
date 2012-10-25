package com.benton.raytrace.engine;

import com.benton.framework.math.M3d;

public class Material {

  protected M3d color;
  protected double reflectivity;
  protected double transparency;
  protected double ka, kd, ks;
  protected double specularShininess;
  protected double refractiveIndex;
  
  public Material() {
    color = new M3d(1,1,1);
    reflectivity = 0;
    transparency = 0;
    specularShininess = 1;
    ka = 0.2;
    kd = 0.6;
    ks = 0.2;
    refractiveIndex = 1.0;
  }
  
  public Material(Material src) {
    this.color = src.color;
    this.reflectivity = src.reflectivity;
    this.specularShininess = src.specularShininess;
    this.transparency = src.transparency;
    this.ka = src.ka;
    this.kd = src.kd;
    this.ks = src.ks;
    this.refractiveIndex = src.refractiveIndex;
  }

  public M3d getColor() {
    return color;
  }

  public void setColor(M3d color) {
    this.color = color;
  }

  public double getReflectivity() {
    return reflectivity;
  }

  public void setReflectivity(double reflectivity) {
    this.reflectivity = reflectivity;
  }

  public double getTransparency() {
    return transparency;
  }

  public void setTransparency(double transparency) {
    this.transparency = transparency;
  }

  public double getSpecularShininess() {
    return specularShininess;
  }

  public void setSpecularShininess(double shininess) {
    this.specularShininess = shininess;
  }

  public double getRefractiveIndex() {
    return refractiveIndex;
  }

  public void setRefractiveIndex(double refractiveIndex) {
    this.refractiveIndex = refractiveIndex;
  }

  public double getKa() {
    return ka;
  }

  public void setKa(double ka) {
    this.ka = ka;
  }

  public double getKd() {
    return kd;
  }

  public void setKd(double kd) {
    this.kd = kd;
  }

  public double getKs() {
    return ks;
  }

  public void setKs(double ks) {
    this.ks = ks;
  }
  
  public void setLightingCoefficients(double ka, double kd, double ks, double specularShininess) {
    this.ka = ka;
    this.kd = kd;
    this.ks = ks;
    this.specularShininess = specularShininess;
  }
}
