import cv2
from tkinter import Tk
from tkinter import filedialog
import numpy as np
import imutils

class Scanner:   
    
    def IMGinput(self):
        root = Tk()
        f = filedialog.askopenfilename(
            parent = root, initialdir = '/',
            title = 'Choose Document Image',
            filetypes = [('png images', '.png'), ('gif images', '.gif'), ('jpg images', '.jpg'), ('jpeg images', '.jpeg')]
            )
        root.destroy()
        return cv2.imread(f)

    def EdgeDetector(self):
        img = self.IMGinput()
        img = cv2.resize(img, dsize = (500, 500), interpolation = cv2.INTER_AREA)
        bounds = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bounds = cv2.GaussianBlur(bounds, (5, 5), 7)
        v = np.median(img)
        sigma = 0.33
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        bounds = cv2.Canny(bounds, lower, upper)
        return (img, bounds)

    def Contours(self):
        img, edges = self.EdgeDetector()
        contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
        for e in contours:
            approx = cv2.approxPolyDP(e, 0.02 * cv2.arcLength(e, True), True)
            if len(approx) == 4:
                screenCnt = approx
                break
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Contour Established", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

Scanner().Contours()