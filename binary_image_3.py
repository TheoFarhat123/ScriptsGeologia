# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:25:15 2023

@author: theocf
"""

import cv2
import numpy as np

# Nome dos arquivos de entrada e saída
input_file = 'C:/Users/theocf/Documents/Theo-Tarefas/DeePore/Resultados_Sapinhoa/results/9-BRSA-928-SPS_5008.05/9-BRSA-928-SPS_5008.05_x10_PP_CROPPED.png'
output_file = 'Output_resized_1.png'

# Limiar de crominância CB
threshold = 140

# Carrega a imagem
im = cv2.imread(input_file)

# Redimensiona a imagem para 256 x 256
im = cv2.resize(im, (256, 256))

# Converte a imagem para o espaço de cores YCbCr
ycbcr = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)

# Obtém as dimensões da imagem
s1, s2, _ = im.shape

# Inicializa uma matriz de zeros para armazenar a imagem binária
BW = np.zeros((s1, s2), dtype=np.uint8)

# Calcula a imagem binária com base no limiar de crominância CB
for I in range(s1):
    for J in range(s2):
        if ycbcr[I, J, 2] > threshold:
            BW[I, J] = 255  # Define pixels acima do limiar como brancos (porosos)

# Calcula a porosidade
inverted_BW = cv2.bitwise_not(BW)
porosity = round(sum(sum(inverted_BW))/(s1*s2)*100)

# Salva a imagem binária
cv2.imwrite(output_file, inverted_BW)

# Exibe a imagem original e a imagem binária
cv2.imshow('Imagem Original', im)
cv2.imshow('Imagem Binária', inverted_BW)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Exibe a porosidade
print(f'Porosidade Visual = {porosity} %')
