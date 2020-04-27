import java.awt.*;
import java.awt.event.*;  
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.*;

class GUI{

    String path;
    float rect[];

    GUI (String path, float []rect) {
        this.path = path;
        this.rect = rect;
    }

    public class ImageCanvas extends Canvas {

        private BufferedImage img;

        public ImageCanvas() {
            try {
                img = ImageIO.read(new File(path));
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        @Override
        public Dimension getPreferredSize() {
            return img == null ? new Dimension(200, 200) : new Dimension(img.getWidth(), img.getHeight());
        }
        @Override
        public void paint(Graphics g) {
            super.paint(g);
            if (img != null) {
                int x = (getWidth() - img.getWidth()) / 2;
                int y = (getHeight() - img.getHeight()) / 2;
                g.drawImage(img, x, y, this);
            }
        }
    }
    
    public float[] getUserPoints() {
        JFrame f = new JFrame();  
        f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        f.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });  
        f.setLayout(null);  
        f.setTitle("GOSHROW Document Scanner");
        f.setLocationRelativeTo(null);
        f.setVisible(true); 
        f.getContentPane().add(new ImageCanvas());
        Button button = new Button("Submit"); 
        f.getContentPane().add(button); 
        f.setSize(500, 500);
        f.setLocationRelativeTo(null);
        f.setVisible(true);
        f.validate();
        return new float[2];
    }
}



class Validate {
    public static void main(String args[]) {
        String path = args[0];
        float []rect = new float[8];
        for (int i = 1; i < args.length; i++) {
            rect[i - 1] = Float.parseFloat(args[i]);
        }
        GUI gui = new GUI(path, rect);
        float []ret = gui.getUserPoints();
        for (int i = 0; i < rect.length; i++) {
            System.out.print(rect[i] + " ");
        }
    }
}