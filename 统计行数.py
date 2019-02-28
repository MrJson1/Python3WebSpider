import numpy as np
import tensorflow as tf
import random
import os
from PIL import Image
import cv2
import  requests
import time

def gen_captchas(filepath = "./datas/"):
    pathDir = os.listdir(filepath)
    list = []
    count = 0
    for allDir in pathDir:
        dict = {}
        filename_child = os.path.join('%s/%s' % (filepath, allDir))
        print(filename_child)
        for index, line in enumerate(open(filename_child, 'r')):
            count += 1
        print(count)
        text = allDir.replace(".text","")
        # print(text)
        dict["text"] = text
        list.append(text)
    print(len(list))
    print("最后统计的是：",count)
    return list

list = gen_captchas()

