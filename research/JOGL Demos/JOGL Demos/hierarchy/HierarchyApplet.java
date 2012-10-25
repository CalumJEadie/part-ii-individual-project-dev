package hierarchy;

import internals.AppletContainer;

public class HierarchyApplet extends AppletContainer {
  private static final long serialVersionUID = 1812754336586895622L;

  public void init() {
    super.setup(new HierarchyDemo());
  }
}
