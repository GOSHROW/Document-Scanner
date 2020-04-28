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

    class CustomPanel extends JPanel
    {
        private BufferedImage image;

        public CustomPanel()
        {
            setOpaque(true);
            setBorder(BorderFactory.createLineBorder(Color.BLACK, 5));
            try
            {
                image = ImageIO.read(new File(path));
            }
            catch(IOException ioe)
            {
                System.out.println("Unable to fetch image.");
                ioe.printStackTrace();
            }
        }

        @Override
        public Dimension getPreferredSize()
        {
            return (new Dimension(image.getWidth(), image.getHeight()));
        }

        @Override
        protected void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            g.drawImage(image, 0, 0, this);
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
        f.setContentPane(new CustomPanel());
        f.pack();
        Button button = new Button("Submit"); 
        f.add(button);
        f.pack();
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
        for (int i = 0; i < ret.length; i++) {
            System.out.print(ret[i] + " ");
        }
        for (int i = 0; i < rect.length; i++) {
            System.out.print(rect[i] + " ");
        }
    }
}