package morph;

import internals.AppletContainer;

public class MorphApplet extends AppletContainer {
  private static final long serialVersionUID = -8331325495251738456L;

  public void init() {
    super.setup(new MorphingSurface());
  }
}
