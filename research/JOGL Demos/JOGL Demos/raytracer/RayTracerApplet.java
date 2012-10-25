package raytracer;

import internals.AppletContainer;

public class RayTracerApplet extends AppletContainer {
  private static final long serialVersionUID = -8331325495251738456L;

  public void init() {
    super.setup(new RayTracerDemo());
  }
}
