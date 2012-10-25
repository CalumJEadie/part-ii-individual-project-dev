package shaders;

import internals.AppContainer;

public class ShaderMain {

  public static void main(String[] args) {
    AppContainer.dx = 413 * 3 / 2;
    AppContainer.dy = 442 * 3 / 2;
    AppContainer.go(new ShaderDemo());
  }
}
