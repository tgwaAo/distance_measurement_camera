#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 00:05:52 2019

Test tracking of an arrow pointing up.

@author: me
"""

import cv2
import numpy as np
import _pickle
import support_functions as sf

WIDTH = 640
HEIGHT = 480
shape_ref = np.load("shape_reference.npy")
cam_data = np.loadtxt("cam_data.txt")

cv2.namedWindow("Camera",cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT);

if (not cap.isOpened()):
    print("Camera not found.")
else:
    with open("sign_ai.pkl","rb") as f:
        ai = _pickle.load(f)
    
    while (True):
        ret, frame = cap.read()
        
        con = sf.find_contours(frame)
        
        for i in range(len(con)):
            points,x_c,y_c = sf.get_shape(con[i])

            if (len(points) == sf.NUM_POINTS):
                ranges,angles,r_sum = sf.get_ranges_and_angles(points,x_c,y_c)
                ranges = sf.ranges_in_percentage(ranges,r_sum)
                dist,alpha,x_m,y_m = sf.data_between_nearest(points,x_c,y_c)
    
                if (dist > 25):
                    angles, ranges = sf.sort_angles(angles,ranges,alpha)
                    hsv = sf.get_color_in_hsv(frame,con[i])
                    similarity = np.float(cv2.matchShapes(con[i],shape_ref,cv2.CONTOURS_MATCH_I2,0))
                    
                    data = np.zeros((1,sf.NUM_FEATURES))
                    data[0,:] = np.concatenate((angles,ranges,[dist],[alpha], hsv[0,0,1:],[similarity]))

                    ans = ai.predict(data)
            
                    if (ans == 1 ):
                        d = cam_data[0]*cam_data[1] / (dist*10)

                        for j in range(len(points)):
                            cv2.line( frame,(points[j,0,0],points[j,0,1]),(points[j,0,0],points[j,0,1]),(0,0,255),10)
                            
                        cv2.drawContours( frame,con,i,(255,0,0),2)
                        cv2.line( frame,(x_c,y_c),(x_c,y_c),(255,255,0),20)
                        cv2.line( frame,(x_m,y_m),(x_m,y_m),(0,255,0),15)
                        cv2.putText(frame, "{:.0f}".format(d)+" cm", (10,  frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX,1.5,(255, 255, 0), 2)    
                        break
                    
        cv2.imshow("Camera",frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
    cap.release()
    cv2.destroyAllWindows()
    print("done")