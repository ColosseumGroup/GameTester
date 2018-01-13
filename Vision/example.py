# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 19:46:56 2017

@author: admin
"""

import cv2
import numpy as np
from match_hand_card import get_hand_card
from match_public_card import get_public_card
from is_your_turn import is_your_turn


img_rgb = cv2.imread('C:\Poke\\Snapshot\\20170713153303.png')
hand_card = get_hand_card(img_rgb)
public_card = get_public_card(img_rgb)
your_turn = is_your_turn(img_rgb)

print (hand_card)