# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 18:15:31 2021

@author: DFTF@PConsole#

"""


import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import math


## 2.
def lerImagem(nome):
    img = mpimg.imread(nome)
    return img


## 3.
def visualizarImagem(img):
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    # abrir janela: %matplotlib


## 4.
def realcarVermelho(img, fator):
    img = np.array(img, np.int32)
    canalR = np.array(img[:,:,0], np.int32) * fator
    canalR[(255 < canalR).nonzero()] = 255
    img[:, :, 0] = canalR
    return img


## 5.
def efeitoMosaico(img, W):
    lenLinhas = img.shape[0]
    lenColunas = img.shape[1]
    lenRgb = img.shape[2]
    
    imgFinal = np.ones((lenLinhas, lenColunas, lenRgb), img.dtype)
    
    for l in range(0, lenLinhas, W):
            
        if l + math.floor(W/2) < lenLinhas:
            lPixel = l + math.floor(W/2)
        else:
            lPixel = l + math.floor( (lenLinhas - l) /2)
                
        for c in range(0, lenColunas, W):
                
            if c + math.floor(W/2) < lenColunas:
                cPixel = c + math.floor(W/2)
            else:
                cPixel = c + math.floor( (lenColunas - c) /2)
                
            if l + W < lenLinhas:
                lLimite = l + W
            else :
                lLimite = lenLinhas
                    
            if c + W < lenColunas:
                cLimite = c + W
            else :
                cLimite = lenColunas
                
            imgFinal[ l:lLimite , c:cLimite , : ] = img[ lPixel, cPixel, : ]
    
    return imgFinal


## 6.
def converterCinza(img):
    lenLinhas = img.shape[0]
    lenColunas = img.shape[1]
    lenRgb = img.shape[2]
    
    imgCinza = np.ones((lenLinhas, lenColunas, lenRgb), img.dtype)
    
    imgCinza[:, :, 2] = imgCinza[:, :, 1] = imgCinza[:, :, 0] = (0.2978 * img[ :, :, 0 ]) + (0.5870 * img[ :, :, 1 ]) + (0.1140 * img[ :, :, 2 ])
    
    return imgCinza
    

## 7.
def binariza(imgCinza, limiar):
    lenLinhas = imgCinza.shape[0]
    lenColunas = imgCinza.shape[1]
    lenRgb = imgCinza.shape[2]
    
    imgBin = np.ones((lenLinhas, lenColunas, lenRgb), imgCinza.dtype)
    
    imgBin[(imgCinza < limiar).nonzero()] = 0
    imgBin[(imgCinza >= limiar).nonzero()] = 255
    
    return imgBin


## 8.
def contorno(imgBin):
    lenLinhas = imgBin.shape[0]
    lenColunas = imgBin.shape[1]
    lenRgb = imgBin.shape[2]
    
    imgContorno = np.zeros((lenLinhas, lenColunas, lenRgb), imgBin.dtype)
    
    for l in range(0, lenLinhas-1, 1):
        for c in range(0, lenColunas-1, 1):
                
            if (imgBin[l, c, 0] == 0 and imgBin[l, c+1, 0] == 255) or (imgBin[l, c, 0] == 255 and imgBin[l, c+1, 0] == 0) or (imgBin[l, c, 0] == 0 and imgBin[l+1, c, 0] == 255) or (imgBin[l, c, 0] == 255 and imgBin[l+1, c, 0] == 0):
                imgContorno[l, c, :] = 255
    
    return imgContorno


## 9.
def gravarImagem(nomeFich, imgArray):
    mpimg.imsave(nomeFich, imgArray)


## Main
if __name__ == "__main__":
    plt.close('all')
    
    nome = 'image008.jpg'
    
    img = lerImagem(nome)
    
    visualizarImagem(img)
    
    imgVermelho = realcarVermelho(img, 2)
    visualizarImagem(imgVermelho)
    
    W1 = 11
    W2 = 25
    W3 = 35
    imgMosaico1 = efeitoMosaico(img, W1)
    visualizarImagem(imgMosaico1)
    imgMosaico2 = efeitoMosaico(img, W2)
    visualizarImagem(imgMosaico2)
    imgMosaico3 = efeitoMosaico(img, W3)
    visualizarImagem(imgMosaico3)
    
    imgCinza = converterCinza(img)
    visualizarImagem(imgCinza)
    
    imgBin = binariza(imgCinza, 100)
    visualizarImagem(imgBin)
    
    imgContorno = contorno(imgBin)
    visualizarImagem(imgContorno)
    
    gravarImagem('gravacao1.bmp', imgContorno)
    
    
    