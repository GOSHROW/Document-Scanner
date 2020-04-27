import cv2
from tkinter import Tk, filedialog, Label, Button
import numpy as np
from imutils import grab_contours
from PIL import Image
import os
import subprocess

class Scanner: 
    
    def __init__(self):
        self.path = ''

    def IMGinput(self):
        root = Tk()
        f = filedialog.askopenfilename(
            parent = root, initialdir = '/',
            title = 'Choose Document Image',
            filetypes = [('jpg images', '.jpg'), ('png images', '.png'), ('gif images', '.gif'), ('jpeg images', '.jpeg')]
            )
        root.destroy()
        self.path = f
        return cv2.imread(f)

    def EdgeDetector(self):
        img = self.IMGinput()
        img = cv2.resize(img, dsize = (1000, 1000), interpolation = cv2.INTER_AREA)
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
        contours = grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        c = contours[0]
        M = cv2.moments(c)
        cX = int(M["m10"] / (M["m00"] + 1))
        cY = int(M["m01"] / (M["m00"] + 1))
        return (img, contours, c)
        
    def getPoints(self, pts):
        rect = np.zeros((4, 2), dtype = "float32")
        s = pts.sum(axis = 1)
        rect[2] = pts[np.argmax(s)]
        rect[0] = pts[np.argmin(s)]
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def changePerspective(self, image, pts):
        rect = self.getPoints(pts)
        print(rect)
        r = rect
        print(r)
        rectStr = ''
        for i in rect:
            for j in i:
                rectStr += str(j) + ' '
        command = "javac Validate.java; java Validate " + self.path + " " + rectStr
        retVal = subprocess.check_output(command, shell = True) 
        retVal = retVal.decode("utf-8")
        retVal = [float(x) for x in retVal.split()]
        rect = np.append([[retVal[0], retVal[1]], [retVal[2], retVal[3]]], [[retVal[4], retVal[5]], [retVal[6], retVal[7]]], axis=0)
        print(rect)
        print(rect == r)
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))   
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def Warp(self):
        img, contours, contour= self.Contours()
        copied = img.copy()
        if len(contours) != 0:
            cv2.drawContours(copied, contours, -1, 255, 3)
        c = max(contours, key = cv2.contourArea)
        approx = cv2.approxPolyDP(c, 0.1*cv2.arcLength(c, True), True)
        warped = self.changePerspective(img, approx.sum(axis = 1))
        return warped

    def getPDF(self):
        image = self.Warp()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        img.save(r'./newScan.pdf')

Scanner().getPDF()