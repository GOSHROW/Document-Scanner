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
            filetypes = [('jpg images', '.jpg'), ('png images', '.png'), ('gif images', '.gif'), ('jpeg images', '.jpeg')]
            )
        root.destroy()
        return cv2.imread(f)

    def EdgeDetector(self):
        img = self.IMGinput()
        ratio = (img.shape[0] / 500.0, img.shape[1] / 500.0)
        img = cv2.resize(img, dsize = (500, 500), interpolation = cv2.INTER_AREA)
        bounds = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bounds = cv2.GaussianBlur(bounds, (5, 5), 7)
        v = np.median(img)
        sigma = 0.33
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        bounds = cv2.Canny(bounds, lower, upper)
        return (img, bounds, ratio)

    def Contours(self):
        img, edges, ratio = self.EdgeDetector()
        contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        c = contours[0]
        M = cv2.moments(c)
        cX = int(M["m10"] / (M["m00"] + 1))
        cY = int(M["m01"] / (M["m00"] + 1))
        return (img, contours, c, ratio)
        
    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype = "float32")
        s = pts.sum(axis = 1)
        rect[2] = pts[np.argmax(s)]
        rect[0] = pts[np.argmin(s)]
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
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
        img, contours, contour, ratio = self.Contours()
        copied = img.copy()
        if len(contours) != 0:
            cv2.drawContours(copied, contours, -1, 255, 3)
        c = max(contours, key = cv2.contourArea)
        approx = cv2.approxPolyDP(c, 0.1*cv2.arcLength(c, True), True)

        warped = self.four_point_transform(img, approx.sum(axis = 1))
        warped = cv2.resize(warped, (int(500 * ratio[0]), int(500 * ratio[1])))
        cv2.imshow("", warped)
        cv2.waitKey(0)

Scanner().Warp()