package raytracer;

import internals.AppContainer;

public class RayTracerMain {
  public static void main(String[] args) {
    AppContainer.go(new RayTracerDemo().withAutoResizeRequested());
  }
}
