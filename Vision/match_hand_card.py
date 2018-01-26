# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import cv2
import numpy as np
def get_number_templates():
    Num_Templates_Path = thisPath + "\\hand_template\\number_templates"
    number_A = (cv2.imread(Num_Templates_Path+'\A.png',0),'A')
    number_2 = (cv2.imread(Num_Templates_Path+'\\2.png',0),'2')
    number_3 = (cv2.imread(Num_Templates_Path+'\\3.png',0),'3')
    number_4 = (cv2.imread(Num_Templates_Path+'\\4.png',0),'4')
    number_5 = (cv2.imread(Num_Templates_Path+'\\5.png',0),'5')
    number_6 = (cv2.imread(Num_Templates_Path+'\\6.png',0),'6')
    number_7 = (cv2.imread(Num_Templates_Path+'\\7.png',0),'7')
    number_8 = (cv2.imread(Num_Templates_Path+'\\8.png',0),'8')
    number_9 = (cv2.imread(Num_Templates_Path+'\\9.png',0),'9')
    number_10 = (cv2.imread(Num_Templates_Path+'\\10.png',0),'10')
    number_J = (cv2.imread(Num_Templates_Path+'\\J.png',0),'J')
    number_Q = (cv2.imread(Num_Templates_Path+'\\Q.png',0),'Q')
    number_K = (cv2.imread(Num_Templates_Path+'\\K.png',0),'K')
    number_templates = [number_A,number_2,number_3,number_4,number_5,number_6,number_7,number_8,number_9,number_10,number_J,number_Q,number_K]
    return number_templates
  
def get_Suit_templates():
    Suit_Templates_Path = thisPath + "\\Vision\\hand_template\\suit_templates"
    suit_Spade = (cv2.imread(Suit_Templates_Path+'\Spade.png',0),'Spade')
    suit_Heart = (cv2.imread(Suit_Templates_Path+'\Heart.png',0),'Heart')
    suit_Diamond = (cv2.imread(Suit_Templates_Path+'\Diamond.png',0),'Diamond')
    suit_Club = (cv2.imread(Suit_Templates_Path+'\Club.png',0),'Club')
    Suit_templates = [suit_Spade,suit_Heart,suit_Diamond,suit_Club]
    return Suit_templates
 
def Identify_number(img_rgb):
    number_templates = get_number_templates()
    number_res = img_rgb.copy()
    numbers = []
    for template in number_templates:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template[0].shape[::-1]
        res = cv2.matchTemplate(img_gray,template[0],cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(number_res, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            #print (pt)
            number = (pt[0],template[1])
            #print (number)
            numbers.append(number)
    cv2.imwrite(thisPath + '\\Vision\\result\\hand_number_res.png',number_res)
    numbers = list(set(numbers))
    numbers.sort(key=lambda x:x[0])
    
    identify_number = []
    #去掉误差重复牌号
    pre_row_index = -3
    for number in numbers:
        if (number[0]-2) > pre_row_index:
            pre_row_index = number[0]
            identify_number.append(number[1])
            #print (number[1])
    return identify_number

def Identify_suit(img_rgb):
    Suit_templates = get_Suit_templates()
    suit_res = img_rgb.copy()
    suits = []
    for template in Suit_templates:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template[0].shape[::-1]    
        res = cv2.matchTemplate(img_gray,template[0],cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(suit_res, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            #print (pt)
            suit = (pt[0],template[1])
            #print (number)
            suits.append(suit)
    cv2.imwrite(thisPath + '\\Vision\\result\\hand_suit_res.png',suit_res)        
    suits = list(set(suits))
    suits.sort(key=lambda x:x[0])
    
    identify_suit = []
    #去掉误差重复花色
    pre_row_index = -3
    for suit in suits:
        if (suit[0]-2) > pre_row_index:
            pre_row_index = suit[0]
            identify_suit.append(suit[1])
            #print (suit[1])
    return identify_suit
            
            
def crob_img(img_rgb):
    #截图的宽高
    h = 150
    w = 230
    height,width,rgb = img_rgb.shape
    
    #坐标
    crob_height_l = int(357*height/576)
    crob_height_r = crob_height_l+h
    
    crob_width_l = int(512*width/1024)
    crob_width_r = crob_width_l+w
    
    crobed_img = img_rgb[crob_height_l:crob_height_r, crob_width_l:crob_width_r]
    return  crobed_img       
 
def get_hand_card(img_rgb):
    crobed_img = crob_img(img_rgb)
    #cv2.imwrite('res22.png',crobed_img)
    
    identify_number = Identify_number(crobed_img)
    identify_suit = Identify_suit(crobed_img)
    identify_result = [identify_number,identify_suit]
    hand_card = []
    for r in zip(*identify_result):
        hand_card.append(r)
    return hand_card
'''
img_rgb = cv2.imread('C:\Poke\\Snapshot\\20170713150825.png')
crobed_img = crob_img(img_rgb)
#cv2.imwrite('res22.png',crobed_img)

identify_number = Identify_number(crobed_img)
identify_suit = Identify_suit(crobed_img)
identify_result = [identify_number,identify_suit]
for r in zip(*identify_result):
    print (r)
'''
'''
img_rgb = cv2.imread('C:\\Users\\bowei\\Desktop\\PokerGame\\Vision\\Snapshot\\20170713150825.png')
hand_card = get_hand_card(img_rgb)
'''