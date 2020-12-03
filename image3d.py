import numpy as np
import argparse
import math
import cv2
import sys
import os

# Parameters:
#     image_path: the path of image that you want rotated
#     shape     : the ideal shape of input image, None for original size.
#     alpha     : rotation around the x axis
#     beta       : rotation around the y axis
#     gamma     : rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image
# 
class ImageTransformer(object):
    """ Perspective transformation class for image
        with shape (height, width, #channels) """

    def __init__(self, image_path, shape):
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print("Err: can't open image file.")
            sys.exit()

        if shape is not None:
            img = cv2.resize(img, shape)

        # the size of the original image: height, width, channels
        h, w, c = img.shape

        # calculate the border size
        hw = math.ceil(math.sqrt(h ** 2 + w ** 2)) #+ 25

        bg_img = np.zeros((hw, hw, c), dtype=np.uint8)

        rows, cols = img.shape[:2]
        roi = bg_img[0:rows, 0:cols ]
        dst = cv2.addWeighted(img, 1, roi, 0, 0)
        #add_img = timg.copy()
        topH = int ((hw - h) / 2 )
        topW = int ((hw - w) / 2)
        bg_img[topH:topH+rows, topW:topW+cols] = dst

        self.image = bg_img
        self.height = hw
        self.width = hw
        self.num_channels = c

        #print("h, w, c: ", self.height, self.width, self.num_channels)

    """ set the source image """
    def set_img(self, img):
        self.image=img

    def get_img(self, img):
        return self.image

    def get_rad(self, alpha, beta, gamma):
        return (self.deg_to_rad(alpha),
                self.deg_to_rad(beta),
                self.deg_to_rad(gamma))

    def get_deg(self, alpha, beta, gamma):
        return (self.rad_to_deg(alpha),
                self.rad_to_deg(beta),
                self.rad_to_deg(gamma))

    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0

    def rad_to_deg(self, rad):
        return rad * 180.0 / math.pi

    """ Wrapper of Rotating a Image """
    def rotate_along_axis(self, alpha=0, beta=0, gamma=0, dx=0, dy=0, dz=0):
        
        # Get radius of rotation along 3 axes
        alpha, beta, gamma = self.get_rad(alpha, beta, gamma)
        
        # Get ideal focal length on z axis
        # NOTE: Change this section to other axis if needed
        d = np.sqrt(self.height**2 + self.width**2)
        self.focal = d / (0.4 * np.sin(gamma) if np.sin(gamma) != 0 else 1)
        dz = self.focal
        #print(dx, dy, dz, self.focal, np.sin(gamma))

        # Get projection matrix
        mat = self.get_M(alpha, beta, gamma, dx, dy, dz)
        
        return cv2.warpPerspective(self.image.copy(), mat, (self.width, self.height))


    """ Get Perspective Projection Matrix """
    def get_M(self, alpha, beta, gamma, dx, dy, dz):
        
        w = self.width
        h = self.height
        f = self.focal

        # Projection 2D -> 3D matrix
        A1 = np.array([ [1, 0, -w/2],
                        [0, 1, -h/2],
                        [0, 0, 0],
                        [0, 0, 1]])
        
        # Rotation matrices around the X, Y, and Z axis
        RX = np.array([ [1, 0, 0, 0],
                        [0, np.cos(alpha), -np.sin(alpha), 0],
                        [0, np.sin(alpha), np.cos(alpha), 0],
                        [0, 0, 0, 1]])
        
        RY = np.array([ [np.cos(beta), 0, -np.sin(beta), 0],
                        [0, 1, 0, 0],
                        [np.sin(beta), 0, np.cos(beta), 0],
                        [0, 0, 0, 1]])
        
        RZ = np.array([ [np.cos(gamma), -np.sin(gamma), 0, 0],
                        [np.sin(gamma), np.cos(gamma), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # Composed rotation matrix with (RZ, RY, RX)
        R = np.dot(np.dot(RZ, RY), RX)

        # Translation matrix
        T = np.array([  [1, 0, 0, dx],
                        [0, 1, 0, dy],
                        [0, 0, 1, dz],
                        [0, 0, 0, 1]])

        # Projection 3D -> 2D matrix
        A2 = np.array([ [f, 0, w/2, 0],
                        [0, f, h/2, 0],
                        [0, 0, 1, 0]])

        # Final transformation matrix
        return np.dot(A2, np.dot(T, np.dot(R, A1)))


def main():
    parser = argparse.ArgumentParser(description='Rotate a image to generate multiple rotated images')
    parser.add_argument('image_file', help='image file to be rotated')
    parser.add_argument('-x', type=int, metavar="axisX", dest="rx", default=0, help='the angle of rotate around X axis')
    parser.add_argument('-y', type=int, metavar="axisY", dest="ry", default=0, help='the angle of rotate around Y axis')
    parser.add_argument('-z', type=int, metavar="axisz", dest="rz", default=0, help='the angle of rotate around Z axis')
    parser.add_argument('-f', type=int, metavar="frame number", dest="fm", default=1, help='the frame number')
    parser.add_argument('-s', type=int, metavar=("scaleHeight,", "scaleWidth"), dest="size", nargs=2, help='the scaled height/width of image')
    parser.add_argument('-o', type=str, metavar="the output directory", dest="output", default="output", help='the directory of output image')

    args = parser.parse_args()
    img_path = args.image_file
    rx = args.rx
    ry = args.ry
    rz = args.rz
    frameNum = args.fm
    if frameNum == 0:
        print("Frame number can't be zero")
        sys.exit()

    if args.size is None:
        img_shape = None
    else:
        img_shape = (args.size[0], args.size[1])

    outdir = args.output

    #print(args)

    # Instantiate the class
    it = ImageTransformer(img_path, img_shape)

    # Make output dir
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    angx = rx / frameNum
    angy = ry / frameNum
    angz = rz / frameNum
 
    dx = 0
    dy = 0
    dz = 0
    # Iterate through rotation range
    for ang in range(0, frameNum):
        axisx = angx * ang
        axisy = angy * ang
        axisz = angz * ang

        rotated_img = it.rotate_along_axis(axisx, axisy, axisz, dx, dy, dz)

        #cv2.namedWindow("image",0);
        #cv2.resizeWindow("image", 400, 400);
        cv2.imwrite(outdir+'/{}.png'.format(str(ang).zfill(3)), rotated_img)
        #cv2.imshow('image', rotated_img)
        #cv2.waitKey(100)
        #cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
