from collections import  deque
import numpy as np
import time
#import imutils
import cv2
#�趨��ɫ��ֵ��HSV�ռ�
redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])
#��ʼ��׷�ٵ���б�
mybuffer = 16
pts = deque(maxlen=mybuffer)
counter = 0
#������ͷ
camera = cv2.VideoCapture(0)
#�ȴ�����
time.sleep(3)
#����ÿһ֡������ɫƿ��
while True:
    #��ȡ֡
    (ret, frame) = camera.read()
    #�ж��Ƿ�ɹ�������ͷ
    if not ret:
        print 'No Camera'
        break
    #frame = imutils.resize(frame, width=600)
    #ת��HSV�ռ�
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #������ֵ������Ĥ
    mask = cv2.inRange(hsv, redLower, redUpper)
    #��ʴ����
    mask = cv2.erode(mask, None, iterations=2)
    #���Ͳ�������ʵ�ȸ�ʴ�����͵�Ч���ǿ����㣬ȥ�����
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #��ʼ��ƿ��Բ����������
    center = None
    #�����������
    if len(cnts) > 0:
        #�ҵ������������
        c = max(cnts, key = cv2.contourArea)
        #ȷ������������������Բ
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #���������ľ�
        M = cv2.moments(c)
        #��������
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        #ֻ�е��뾶����10ʱ����ִ�л�ͼ
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #��������ӵ�pts�У���������ӵ��б����
            pts.appendleft(center)
    else:#���ͼ����û�м�⵽ƿ�ǣ������pts��ͼ���ϲ���ʾ�켣��
        pts.clear()
    
    for i in xrange(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        #��������С�߶εĴ�ϸ
        thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
        #����С�߶�
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        #�ж��ƶ�����
        if counter >= 10 and i == 1 and len(pts) >= 10:
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")
            
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"
            
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"
            
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)
            else:
                direction = dirX if dirX != "" else dirY
        
            cv2.putText(frame, direction, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 
                        (0, 255, 0), 3)
            cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
    cv2.imshow('Frame', frame)
    #���̼�⣬��⵽esc���˳�
    k = cv2.waitKey(1)&0xFF
    counter += 1
    if k == 27:
        break
#����ͷ�ͷ�
camera.release()
#�������д���
cv2.destroyAllWindows()
