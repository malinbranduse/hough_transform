import cv2 as cv
import math
import matplotlib.pyplot as plt
import numpy as np


class HoughTransformer:
    def hough_transform(self, img, threshold, rho_step=1, theta_step=math.pi / 180):
        self.img = img
        self.threshold = threshold
        self.rho_step = rho_step
        self.theta_step = theta_step

        # theta is calculated from -90 to 90 degrees
        min_theta = -np.pi / 2
        max_theta = np.pi / 2

        self.min_theta = min_theta
        self.max_theta = max_theta

        h, w = img.shape

        # maximum and minimum values for rho
        # could also calculated as the diagonal of the image
        max_rho = int(round(math.sqrt(w * w + h * h)))
        min_rho = -max_rho

        # number of values for rho and theta based on input params
        num_angle = int(np.floor((max_theta - min_theta) / theta_step) + 1)
        num_rho = int(round((max_rho - min_rho + 1) / rho_step))

        self.num_angle = num_angle
        self.num_rho = num_rho

        rho_offset = (num_rho - 1) / 2
        self.rho_offset = rho_offset

        # accumulator matrix sized larger with 2 to allow calculation of neighbors in the local maximum step
        accum = np.zeros((num_rho + 2, num_angle + 2), int)
        # calculate values for accumulator
        for i in range(h):
            for j in range(w):
                # skip black pixels
                if img[i, j] == 0:
                    continue
                # iterate each angle from -90 to 90
                for n in range(num_angle):
                    # theta angle in radians
                    angle = min_theta + n * theta_step
                    # Rho formula based on theory in hough space
                    r = round(j * math.cos(angle) + i * math.sin(angle))
                    # Move to center
                    r += int(rho_offset)
                    # increment accumulator
                    accum[r, n] += 1

        self.accumulator = accum

        return self.extractLinesFromAccumulator(threshold)

    def hough_transform_cv(self, img, threshold, rho_step=1, theta_step=math.pi / 180):
        lines = cv.HoughLines(img, rho_step, theta_step, threshold)
        lines = lines if lines is not None else np.array([])
        return lines

    def extractLinesFromAccumulator(self, threshold):
        # find local maximums
        maximums = []

        accum = self.accumulator

        # compare each value in accumulator with the threshold and the neighbors
        # if the value is a maximum, the numeric rho,theta pair is saved
        for r in range(1, self.num_rho):
            for n in range(1, self.num_angle):
                current = accum[r, n]
                neighbors = np.array(
                    [accum[r, n - 1], accum[r, n + 1], accum[r - 1, n], accum[r + 1, n]]
                )
                if current > threshold and (current > neighbors).all():
                    maximums.append((r, n))

        # sort maximums by accumulator value
        maximums.sort(key=lambda rho_theta: accum[rho_theta[0]][rho_theta[1]])

        # create list of lines
        # map the numeric rho,theta pairs back into actual pixels and radians
        lines = []
        for i in range(len(maximums)):
            r, th = maximums[i]
            rho = (r - self.rho_offset) * self.rho_step
            angle = self.min_theta + th * self.theta_step
            lines.append([(rho, angle)])

        return lines

    def plotAccumulator(self):
        plt.figure(figsize=(10, 10))
        ah, aw = self.accumulator.shape
        x_repeat = ah / aw
        accum_resize = np.repeat(self.accumulator, x_repeat, axis=1)
        plt.imshow(accum_resize)
        plt.show()

    def plotLinesToImage(self, output_image, lines, line_width=2, color=(255, 0, 0)):
        # reverse hough transform - from rho and theta, compute x and y
        # scalar is used to properly set the length of the line
        scalar = 1e5
        for i in range(len(lines)):
            rho, theta = lines[i][0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + scalar * (-b)), int(y0 + scalar * (a)))
            pt2 = (int(x0 - scalar * (-b)), int(y0 - scalar * (a)))
            cv.line(output_image, pt1, pt2, color, line_width, cv.LINE_AA)

        return output_image
