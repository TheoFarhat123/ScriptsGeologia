# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:48:48 2023

@author: theocf
"""

import cv2 
from PIL import Image
import os





def crop_images(FileName, OutputName):

    img = Image.open(FileName)
    width, height = img.size
    
    left = int(0.12 * width)
    top = int(0.12 * height)
    right = int(0.88 * width)
    bottom = int(0.88 * height)
    
    cropped = img.crop((left, top, right, bottom))
    
    cropped.save(OutputName)
    
    


def resize_images(FileName, OutputName):

    img = cv2.imread(FileName)
    
    img = cv2.resize(img, None, fx=0.10, fy=0.10)

    cv2.imwrite(OutputName, img)

    
    return OutputName
   


def main():
    
    PATH = 'C:/Users/theocf/Documents/Theo-Tarefas/DeePore/Resultados_Sapinhoa/Sapinhoa/JPEG'
    
    
    subdirectories = [os.path.join(PATH, d) for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]

    for subdirectory in subdirectories:
        
        image_files = [f for f in os.listdir(subdirectory) if f.endswith('.jpg')]
        
        if len(image_files) >= 1:
            for image_file in image_files:
                input_file = os.path.join(subdirectory, image_file)
                output_file_cropped = os.path.join(subdirectory, image_file.replace('.jpg', '_CROPPED.png'))
                
                img = resize_images(input_file, output_file_cropped)
                crop_images(img, output_file_cropped)
            
            
if __name__=="__main__":
    main()