import java.util.*;
import java.awt.*;

class Validate {
    public float[] getUserPoints() {
        float []ret = {0, 1};
        return ret;
    }
    public static void main(String args[]) {
        String path = args[0];
        float []rect = new float[8];
        for (int i = 1; i < args.length; i++) {
            rect[i - 1] = Float.parseFloat(args[i]);
        }
        for (int i = 0; i < rect.length; i++) {
            System.out.print(rect[i] + " ");
        }
    }
}