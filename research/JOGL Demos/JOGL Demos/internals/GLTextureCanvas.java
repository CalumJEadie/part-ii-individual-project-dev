package internals;

import static java.lang.Math.max;
import static java.lang.Math.min;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.media.opengl.GL;
import javax.media.opengl.GLException;

import com.benton.framework.math.M3d;
import com.benton.framework.ui.RGBCanvas;
import com.sun.opengl.util.texture.Texture;
import com.sun.opengl.util.texture.TextureCoords;
import com.sun.opengl.util.texture.TextureData;
import com.sun.opengl.util.texture.TextureIO;


public class GLTextureCanvas implements RGBCanvas {

  BufferedImage image;
  Graphics2D imageAccessor;
  Texture texture = null;
  TextureCoords frame;
  
  public GLTextureCanvas(int width, int height) {
    image = new BufferedImage(width, height, BufferedImage.TYPE_3BYTE_BGR);
    imageAccessor = image.createGraphics();
  }

  @Override
  public void fill(double x, double y, double dx, double dy, M3d color) {
    float r = max(min((float)color.get(0), 1), 0);
    float g = max(min((float)color.get(1), 1), 0);
    float b = max(min((float)color.get(2), 1), 0);
    
    imageAccessor.setColor(new Color(r, g, b));
    imageAccessor.fillRect((int)x, (int)y, (int)dx, (int)dy);
  }

  public void clear() {
    imageAccessor.setColor(new Color(1,1,1));
    imageAccessor.fillRect(0, 0, image.getWidth(), image.getHeight());
  }

  @Override
  public int getWidth() {
    return image.getWidth();
  }

  @Override
  public int getHeight() {
    return image.getHeight();
  }
  
  public void render(GL gl) {
    if (texture == null) {
      gl.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR);
      texture = TextureIO.newTexture(image, false);
      texture.bind();
      texture.enable();
      frame = texture.getImageTexCoords();
    } else {
      texture.updateImage(new TextureData(0,0,false,image));
    }

    gl.glBegin(GL.GL_QUADS);
      gl.glTexCoord2f(frame.left(), frame.top());
      gl.glVertex3f(-0.5f, -0.5f, 0.0f);
      
      gl.glTexCoord2f(frame.left(), frame.bottom());
      gl.glVertex3f(-0.5f, 0.5f, 0.0f);
      
      gl.glTexCoord2f(frame.right(), frame.bottom());
      gl.glVertex3f(0.5f, 0.5f, 0.0f);
      
      gl.glTexCoord2f(frame.right(), frame.top());
      gl.glVertex3f(0.5f, -0.5f, 0.0f);
    gl.glEnd();
  }
  
  public void write(GL gl, String filename) {
    try {
      TextureIO.write(texture, new File(filename));
    } catch (GLException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
