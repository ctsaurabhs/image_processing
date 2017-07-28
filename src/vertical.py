import cv2
import numpy as np
import math

# jain constant
offset = 60 

#img = cv2.imread('dave.jpg')
img = cv2.imread('out_image_2.jpg')
frame = cv2.medianBlur(img,7)
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize = 3)
edges = cv2.Canny(gray,180, 200)
cv2.imwrite('canny.jpg',edges)

rows = img.shape[0]
columns = img.shape[1]
print img.shape 
minLineLength=columns

#lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=1000, minLineLength=minLineLength,maxLineGap=10)
#lines = cv2.HoughLinesP(edges,0.02,np.pi/180,300,minLineLength,100)

#lines = cv2.HoughLinesP(edges,1, np.pi/180, 100, 100, 12)
lines = cv2.HoughLinesP(edges,1, np.pi/180, 100, 100, 10)
#print lines
print "++++++++++++++++++++++++++"
#print lines.sort()
listElem = []
a,b,c = lines.shape
for x in range(0, len(lines)):
    #print lines[x] 
    listElem.append(lines[x].tolist())
    for x1,y1,x2,y2 in lines[x]:
        if y1 == y2:
            continue
     #   print "(", x1, ",", y1, ")", "(", x2,",", y2,")"    
#        new_x1 = x1 - x1 + offset 
#	new_x2 = x2 - x2 + (columns - offset)
#        print math.atan2(y2 - y1, new_x2 - new_x1) * 180.0 / np.pi 
#        cv2.line(img,(new_x1,y1),(new_x2,y2),(0,0,255),2, cv2.LINE_AA)

        new_y1 = y1 - y1 + offset
        new_y2 = y2 - y2 + (rows - offset)

        cv2.line(img,(x1,new_y1),(x2,new_y2),(0,255,0),2, cv2.LINE_AA)
        #cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2, cv2.LINE_AA)

print listElem[0][0][0]

# Dictionary to hold index and listElem items
lineDict = {}
finalList = []
for index in range(0, len(listElem)):
    lineDict[index] = listElem[index][0][1] 

finalList = lineDict.values()
finalList.sort()

closeInd = []
discard = 0
'''
for ind in range(0, len(finalList)):
    check_ind = finalList[ind]
    for val in range(ind, len(finalList)-1):
        print "val to check", finalList[val], "::", check_ind
        if finalList[val] <= check_ind + 30:
            continue
        else:
            closeInd.append(finalList[val])
'''     
     
        
#print closeInd
cv2.imwrite('hough_2.jpg',img)

'''
minLineLength = 10000
maxLineGap = 0 
lines = cv2.HoughLinesP(edges,1,np.pi/90,15,minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)


lines = cv2.HoughLines(edges,5,np.pi/180,2000)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)
'''
