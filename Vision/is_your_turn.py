# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:24:02 2017

@author: admin
"""
import cv2
import sys
import numpy as np
thisPath = sys.path[0]
def get_template():
    template = cv2.imread(thisPath + '\\Vision\\action_template\\your_turn.png',0)
    return template
    
def crob_img(img_rgb):
    #截图的宽高
    h = 100
    w = 210
    height,width,rgb = img_rgb.shape
    
    #坐标
    crob_height_l = int(495*height/576)
    crob_height_r = crob_height_l+h
    
    crob_width_l = int(819*width/1024)
    crob_width_r = crob_width_l+w
    
    crobed_img = img_rgb[crob_height_l:crob_height_r, crob_width_l:crob_width_r]
    return  crobed_img
    
def match(img_rgb):
    template = get_template()
    is_your_turn_res = img_rgb.copy()
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(is_your_turn_res, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        #print (pt)
    cv2.imwrite(thisPath + '\\Vision\\result\\is_your_turn_res.png',is_your_turn_res)
    if loc[0].any():
        return True
    else:
        return False

def is_your_turn(img_rgb):
    crobed_img = crob_img(img_rgb)
    #cv2.imwrite('res22.png',crobed_img)
    your_turn = match(crobed_img)
    return your_turn
