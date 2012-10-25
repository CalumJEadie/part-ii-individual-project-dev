package abnormals;

import internals.AppletContainer;

public class NormalsApplet extends AppletContainer {
  private static final long serialVersionUID = 5512765204804841640L;

  public void init() {
    super.setup(new NormalsAnimation());
  }
}
