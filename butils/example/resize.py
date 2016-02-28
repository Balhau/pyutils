import cv
original= cv.LoadImageM('resources/img1.jpg')
thumb=cv.CreateMat(original.rows/10,original.cols/10,cv.CV_8UC3)
cv.Resize(original,thumb)
cv.SaveImage('res.jpg',thumb)
