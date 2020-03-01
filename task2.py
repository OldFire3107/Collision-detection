import cv2
import numpy as np

def calculateDistance(x1,y1,x2,y2):
    # print(x1, x2,y1, y2)
    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist 

image = 'task2.png'

img = cv2.imread(image, 0)
edges = cv2.Canny(img, 20, 60, apertureSize=3)
img = cv2.medianBlur(img, 5)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, 50, 20)
cimg = cv2.imread(image, 1)

cueX1, cueY1, cueX2, cueY2 = (0, 0, 0, 0)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10, param1=100, param2=20, minRadius=0, maxRadius=0)

if lines is not None:
    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            # draw the line
            cv2.line(cimg, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cueX1 = x1
            cueY1 = y1
            cueX2 = x2
            cueY2 = y2

else:
    print('No cue found! Exiting....')
    cv2.imshow("Canny", edges)
    cv2.waitKey(0)
    exit()

small = np.inf
c = 0
X = []
Y = []

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0,255,0), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0,0,255), 3)

        X.append(float(i[0]))
        Y.append(float(i[1]))
        c += 1

        global index

        d = calculateDistance(i[0], i[1], cueX1, cueY1)
        if d < small :
            small = d
            index = i
        d = calculateDistance(i[0], i[1], cueX2, cueY2)
        if d < small :
            small = d
            temp = cueX1
            cueX1 = cueX2
            cueX2 = temp
            temp = cueY1
            cueY1 = cueY2
            cueY2 = temp 
            index = i

else:
    print('No balls found! Exiting...')
    exit()

dist = calculateDistance(cueX1, cueY1, cueX2, cueY2)
velX = (cueX1 - cueX2)/dist
velY = (cueY1 - cueY2)/dist

print(cueX1, cueY1, velX, velY, index)

cv2.imshow('detected circles', cimg)

maxCollisions = int(input('Enter the maximum number of collisions you want to see:'))
collisions = 0

Xpos = float(index[0])
Ypos = float(index[1])

while collisions < maxCollisions:
    col = np.zeros(cimg.shape, dtype=np.uint8)

    if Xpos <= index[2] or col.shape[1] - Xpos <= index[2]:
        velX = -1*velX
        
    if Ypos <= index[2] or col.shape[0] - Ypos <= index[2]:
        velY = -1*velY

    Xpos = Xpos + velX
    Ypos = Ypos + velY
    c = 0

    for i in circles[0,:]:
        i[0] = int(X[c])
        i[1] = int(Y[c])

        cv2.circle(col, (i[0], i[1]), i[2], (0,255,0), 2)
        cv2.circle(col, (i[0], i[1]), 2, (0,0,255), 3)
        
        comp = index == i
        if comp.all():
            X[c] = Xpos
            Y[c] = Ypos
            i[0] = int(X[c])
            i[1] = int(Y[c])
            index = i 
        else:
            dist = calculateDistance(Xpos, Ypos, X[c], Y[c])
            if dist <= float(i[2] + index[2]):
                index = i
                Xpos = X[c]
                Ypos = Y[c]
                print(index)
                collisions = collisions + 1

        c += 1
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:
        break
    cv2.imshow('collisions', col)

cv2.destroyAllWindows()
