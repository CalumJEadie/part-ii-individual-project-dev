package blobby;

import internals.AppletContainer;

public class BlobbyApplet extends AppletContainer {

  private static final long serialVersionUID = -1822473974167496654L;

  public void init() {
    super.setup(new BlobbyDemo());
  }
}