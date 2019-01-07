import cv2

imagepath = "captcha1.png"
gray = cv2.imread(imagepath, 0)

height, width = gray.shape
print(height)
for i in range(width):
    gray[0, i] = 255
    gray[height-1, i] = 255
for j in range(height):
    gray[j, 0] = 255
    gray[j, width-1] =255
    
    
blur = cv2.medianBlur(gray, 3)  # 模板大小3*3
ret, thresh1 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
image, contours, hierarchy = cv2.findContours(thresh1, 2, 2)
flag = 1


for cnt in contours:
    # 最小的外接矩形
    x, y, w, h = cv2.boundingRect(cnt)
    if x != 0 and y != 0 and w*h >= 100:
        print((x,y,w,h))
        # 显示图片
        cv2.imwrite('char%s.jpg'%flag, thresh1[y:y+h, x:x+w])
        flag += 1
