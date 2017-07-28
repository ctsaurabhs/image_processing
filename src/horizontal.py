import cv2
import numpy as np
import math

# jain constant
offset = 60 

img = cv2.imread('test_1.JPG')
#img = cv2.imread('dave.jpg')
frame = cv2.medianBlur(img,7)
img23 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img23,cv2.COLOR_RGB2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize = 3)
edges = cv2.Canny(gray,180, 200)
cv2.imwrite('canny.jpg',edges)
cv2.imwrite('xxcanny.jpg',img23)

columns = img.shape[1]
print img.shape 
minLineLength=columns

#lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=1000, minLineLength=minLineLength,maxLineGap=10)
lines = cv2.HoughLinesP(edges,0.02,np.pi/180,300,minLineLength,100)

#print lines
print "++++++++++++++++++++++++++"
#print lines.sort()

listElem = []
a,b,c = lines.shape
for x in range(0, len(lines)):
    #print lines[x] 
    listElem.append(lines[x].tolist())
    for x1,y1,x2,y2 in lines[x]:
        if x1 == x2:
            continue
     #   print "(", x1, ",", y1, ")", "(", x2,",", y2,")"    
        new_x1 = x1 - x1 + offset 
	new_x2 = x2 - x2 + (columns - offset)
        #print math.atan2(y2 - y1, new_x2 - new_x1) * 180.0 / np.pi 
#        cv2.line(img,(new_x1,y1),(new_x2,y2),(0,0,255),2, cv2.LINE_AA)

# Dictionary to hold index and listElem items
lineDict = {}
finalList = []
for index in range(0, len(listElem)):
    lineDict[index] = listElem[index][0][1] 

finalList = lineDict.values()
finalList.sort()

closeInd = []
discard = 0
print lines
print "FinalList : ", finalList

# Calculate max gap between consecutive lines
maxGap = 0
for indFin in range(0, len(finalList)-1):
    diff = finalList[indFin + 1] - finalList[indFin]
    if maxGap < diff: 
        maxGap = diff 
    else:
        continue
   
print "maxGap::", maxGap

ind = 0
while ind <= len(finalList):
    checkVal = finalList[ind]
#    print "checking for::", checkVal
    if ind == 0:
        closeInd.append(finalList[ind])
    if ind == len(finalList)-1:
        closeInd.append(finalList[ind])
        break
    for val in range(ind + 1, len(finalList)):
#        print "Iterating val :", finalList[val] 
        if finalList[val] == finalList[-1]:
#            print "Equal", finalList[val] 
            ind = val
            break
        elif finalList[val] <= checkVal + maxGap/10:
            continue
        else:
            closeInd.append(finalList[val])
            ind = val
            break

print "Close List: ", closeInd
print lineDict
print "++++++++++++++++++"

# List to contain final lines - after removing false positives
resultLines = []
indelemClose = 0

for elemClose in closeInd:
#    print "closexnd:", elemClose
    if elemClose in finalList:
        for k, v in lineDict.items():
            if str(elemClose) in str(v):
#                print "key::", k, lines[k][0]
                resultLines.append(lines[k][0])

                b = 0
                g = 0
                r = 0

                for x1,y1,x2,y2 in lines[k]:
                    if x1 == x2:
                        continue
                    if y1 > y2 and y1-y2 > maxGap/10:
                        continue 
                    if y2 > y1 and y2-y1 > maxGap/10:
                        continue 
     #   print "(", x1, ",", y1, ")", "(", x2,",", y2,")"    
                    new_x1 = x1 - x1 + offset 
	            new_x2 = x2 - x2 + (columns - offset)
        #print math.atan2(y2 - y1, new_x2 - new_x1) * 180.0 / np.pi 
                    if indelemClose == 0:
                        r = 255
                        b = 0
                        g = 0
                    if indelemClose == 1:
                        r = 0 
                        b = 255
                        g = 0
                    if indelemClose == 2:
                        r = 0 
                        b = 0 
                        g = 255 
                    if indelemClose == 3:
                        r = 100 
                        b = 100 
                        g = 0 
 
                    #cv2.line(img,(new_x1,y1),(new_x2,y2),(b,g,r),2, cv2.LINE_AA)
                    cv2.line(img,(new_x1,y1),(new_x2,y2),(0,0,255),2, cv2.LINE_AA)
                    indelemClose += 1
                break

     #    finalList.index(elemClose) 

print resultLines
new_elemList = []
for elem_res in resultLines:
    if elem_res[0] == elem_res[2]:
        continue
    else:
        new_elemList.append(elem_res)


elem_cnt = 0
for nelem in new_elemList:
    ex1 = nelem[0] 
    ey1 = nelem[1] 
    ex2 = nelem[2] 
    ey2 = nelem[3] 
    print "ccordinates::", ex1, ":", ey1, ":", ex2, ":", ey2
    elem_cnt += 1

val = img[81:564, 0:3264]
imgName = "out_image.jpg"
cv2.imwrite(imgName,val)

val = img[564:1202, 0:3264]
imgName = "out_image_2.jpg"
cv2.imwrite(imgName,val)

#cv2.rectangle(img, (724,630), (2801,1121), (0,255,0), 5)
    
cv2.imwrite('hough_11.jpg',img)
