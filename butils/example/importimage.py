import cv

im=LoadImageM('resources/img1.jpg')
print type(im)
cv.SaveImage('resources/img1.png',im)