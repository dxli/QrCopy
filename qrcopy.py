#!/usr/bin/env python

"""
Copy a qr code
"""
import cv2
import numpy as np
import os
import sys

"""
@brief  -   Decode a QR code from a given image
"""
class QrDecoder:
    def __init__(self, img):
        qcd = cv2.QRCodeDetector()
        retval, info, points, coded = qcd.detectAndDecodeMulti(img)
        self.valid = retval
        if not retval:
            return
        # corner points in the source image
        pts = points[0]
        # coded QR used to duplicate the QR
        self.code = coded[0]
        # bounding box
        self.min = pts[3].copy()
        self.max = pts[3].copy()
        for p in pts:
            self.min = (int(min(self.min[0], p[0])), int(min(self.min[1], p[1])))
            self.max = (int(max(self.max[0], p[0])), int(max(self.max[1], p[1])))
    """
    @brief - extract the QR 
    """
    def extract(self, outputImage):
        if not self.valid:
            return
        codedInfo=self.code
        # QR block sizes
        ht, wt = codedInfo.shape
        # approximate color block size in the original image
        n0 = int((self.max[0] - self.min[0])/wt)
        if n0 < 10:
            n0 = 10
        height = n0*ht
        width = n0*wt
        # with a border or 2 blocks each side
        qrCopy = np.zeros(((ht + 4)*n0, (wt + 4)*n0, 3), np.uint8)
        qrCopy.fill(255)
        # fill blocks
        xT = [(i+2)*n0 for i in range(wt+1)]
        for yi in range(ht):
           for xi in range(wt):
              if codedInfo[yi, xi] == 0:
                  qrCopy = cv2.rectangle(qrCopy, (xT[xi], xT[yi]), (xT[xi+1], xT[yi+1]), color=(0, 0, 0), thickness=-1)
        # write the QR image
        cv2.imwrite(outputImage, qrCopy)
        print('Extract QR code to image {f}'.format(f=outputImage))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('extract qr code from an image file')
        print('usage:: <img-file> <qr-code-image>')
        exit(0)
    img = cv2.imread(sys.argv[1])
    if img is None :
        if not os.path.isfile(sys.argv[1]):
            print('Expected image file "{f}": file doesn\'t exist'.format(f=sys.argv[1]))
        print('Cannot read image file "{f}"'.format(f=sys.argv[1]))
        exit(0)
    decoder = QrDecoder(img)
    # extract the qr code to a file
    decoder.extract(sys.argv[2])
