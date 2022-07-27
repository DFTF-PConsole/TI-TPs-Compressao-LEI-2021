# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 12:51:06 2021

@author: DFTF@PConsole#
"""


from scipy.io import wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np


## 2.
def leitura(nomeFicheiro):
    print("\n *** Ex 2 *** \n")
    
    [fs, data] = wavfile.read(nomeFicheiro)
    return fs, data


## 3.
def reproduzir(fs, data):
    print("\n *** Ex 3 *** \n")
    
    sd.play(data, fs)
    status = sd.wait()
    print(status)


## 4.
def apresentarInfo(nomeFicheiro, fs, nrBitsQuant):
    print("\n *** Ex 4 *** \n")
    
    print("Informação sobre o ficheiro")
    print("Nome do ficheiro: " + nomeFicheiro)
    print("Taxa de amostragem: " + str(fs) + " kHz")
    print("Quantização: " + str(nrBitsQuant) + " bits")


## 5.
### 5.1.
### 5.2.
def visualizacaoGrafica(sinal, fs, *args):
    # *args
    # sinal, fs, tIni, tFim
    
    print("\n *** Ex 5 *** \n")
    
    ts = 1/fs       # intervalo de amostragem
    nrAmostras = sinal.shape[0]
    duracao = nrAmostras * ts
    if len(sinal.shape) == 1:
        canais = 1
    else:
        canais = sinal.shape[1]
    
    sinal = np.array(sinal, float) / (float(pow(2, int(str(sinal.dtype)[3:]) - 1)) + 1)

    if len(args) == 0:
        print("Sem restrição no tempo")
        tIni = 0
        tFim = duracao
        
    elif len(args) == 1:
        print("Com restrição no tempo: tIni")
        tIni = args[0]
        tFim = duracao
        
    elif len(args) == 2:
        print("Com restrição no tempo: tIni e tFim")
        tIni = args[0]
        tFim = args[1]
        
    else:
        print("Erro nos args")
        return
    
    tempo = np.array(np.arange(0, duracao, ts), float)
    
    plt.figure()
    
    if canais == 1:
        print("Mono")
        
        plt.subplot(1,1,1)
        plt.plot(tempo, sinal[:],'g')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Mono')
        plt.ylim(-1, 1)
        plt.xlim(tIni, tFim)
        
    elif canais == 2:
        print("Stereo")
        
        plt.subplot(2,1,1)
        plt.plot(tempo, sinal[:,0],'b')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Esquerdo')
        plt.ylim(-1, 1)
        plt.xlim(tIni, tFim)
        
        plt.subplot(2,1,2)
        plt.plot(tempo, sinal[:,1],'r')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Direito')
        plt.ylim(-1, 1)
        plt.xlim(tIni, tFim)
    

## 6.
def visualizacaoGrafica2(sinal, fs, *args):
    # *args
    # sinal, fs, tIni, tFim
    
    print("\n *** Ex 6 *** \n")
    
    ts = 1/fs       # intervalo de amostragem
    nrAmostras = sinal.shape[0]
    duracao = nrAmostras * ts
    if len(sinal.shape) == 1:
        canais = 1
    else:
        canais = sinal.shape[1]
    
    sinal = np.array(sinal, float) / (float(pow(2, int(str(sinal.dtype)[3:]) - 1)) + 1)

    if len(args) == 0:
        print("Sem restrição no tempo")
        tIni = 0
        tFim = duracao
        
    elif len(args) == 1:
        print("Com restrição no tempo: tIni")
        tIni = args[0]
        tFim = duracao
        
    elif len(args) == 2:
        print("Com restrição no tempo: tIni e tFim")
        tIni = args[0]
        tFim = args[1]
        
    else:
        print("Erro nos args")
        return
    
    tempo = np.array(np.arange(0, duracao, ts), float)
    
    plt.figure()
    
    if canais == 1:
        print("Mono")
        
        plt.subplot(1,1,1)
        plt.plot(tempo, sinal[:],'y')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Mono')
        plt.axis([tIni, tFim, -1, 1])
        
    elif canais == 2:
        print("Stereo")
        
        plt.subplot(2,1,1)
        plt.plot(tempo, sinal[:,0],'c')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Esquerdo')
        plt.axis([tIni, tFim, -1, 1])
        
        plt.subplot(2,1,2)
        plt.plot(tempo, sinal[:,1],'m')
        plt.xlabel('Tempo (seg)')
        plt.ylabel('Amplitude [-1:1]')
        plt.title('Canal Direito')
        plt.axis([tIni, tFim, -1, 1])


## 7.
def ruido(sinal, amplitudeRuido):
    print("\n *** Ex 7 *** \n")
    
    nrAmostras = sinal.shape[0]
    if len(sinal.shape) == 1:
        canais = 1
    else:
        canais = sinal.shape[1]
    aleatorio = -amplitudeRuido + ( np.random.rand(nrAmostras, canais) * (2 * amplitudeRuido) )
    sinalRuidoso = sinal + aleatorio
    return sinalRuidoso


## 8.
def calcEnergia(sinal):
    print("\n *** Ex 8 *** \n")
    
    energia = np.sum(sinal.astype(np.float32)**2, axis=0)   # axis=0 -> coluna a coluna
    return energia
    

## 9.
### 9.1.
### 9.2.
### 9.3.
def substituirCanal(sinalOriginal1, nomeFichSinalOriginal2, tIni):
    print("\n *** Ex 9.1 *** \n")
    
    fsOriginal2, sinalOriginal2 = leitura(nomeFichSinalOriginal2)
    
    if len(sinalOriginal1.shape) == 1:
        canalL = sinalOriginal1[:]
    else:
        canalL = sinalOriginal1[:, 0]
        
    if len(sinalOriginal2.shape) == 1:
        canalR = sinalOriginal2[:]
    else:
        canalR = sinalOriginal2[:, 0]
        
    ts = 1.0/ float(fsOriginal2)       # intervalo de amostragem
    nrAmostrasCanalL = len(canalL)
    nrAmostrasCanalR = len(canalR)
    nrAmostrasZerosInicioCanalR = int ( float(tIni) / ts )
    
    if nrAmostrasCanalR + nrAmostrasZerosInicioCanalR > nrAmostrasCanalL:
        nrAmostrasZerosFinalCanalL = nrAmostrasCanalR + nrAmostrasZerosInicioCanalR - nrAmostrasCanalL
        nrAmostrasZerosFinalCanalR = 0
    else:
        nrAmostrasZerosFinalCanalL = 0
        nrAmostrasZerosFinalCanalR = nrAmostrasCanalL - nrAmostrasCanalR - nrAmostrasZerosInicioCanalR
        
    linhasTotal = nrAmostrasCanalR + nrAmostrasZerosInicioCanalR + nrAmostrasZerosFinalCanalR
    sinalResultante = np.zeros((linhasTotal, 2), sinalOriginal1.dtype)
    
    sinalResultante[ : nrAmostrasCanalL , 0] = canalL[:]
    sinalResultante[ nrAmostrasZerosInicioCanalR : nrAmostrasZerosInicioCanalR + nrAmostrasCanalR  , 1] = canalR[:] 
    
    return sinalResultante


### 9.4.
#### 9.4.1.
#### 9.4.2.
def misturarCanais(sinalOriginal1, nomeFichSinalOriginal2, tIni):
    print("\n *** Ex 9.4 *** \n")
    
    sinalIntermedio = substituirCanal(sinalOriginal1, nomeFichSinalOriginal2, tIni)
    
    sinalResultante = np.array(np.sum(sinalIntermedio, axis=1), sinalOriginal1.dtype)   # axis=1 -> linha a linha
    
    return sinalResultante


## 10.
### 10.1.
### 10.2.
### 10.3.
#### 10.3.1.
#### 10.3.2.
#### 10.3.3.
def contornoAmplitude(x, W):
    print("\n *** Ex 10 *** \n")
    
    if len(x.shape) == 1:
        xr = np.array(x[:], x.dtype)
    else:
        xr = np.array(x[:, 0], x.dtype)
        
    enerigaX = calcEnergia(xr)
    
    xr[(xr < 0).nonzero()] = 0
    
    ca = np.zeros((len(xr), 1), xr.dtype)
    
    iInicial = 0
    iFinal = len(ca)
    
    for i in range(iInicial, iFinal):
        a = i - np.floor(W/2)
        if a < iInicial:
            a = iInicial
            
        b = i + np.floor(W/2)
        if b >= iFinal:
            b = iFinal -1
            
        ca[i] = np.mean(xr[ int(a) : int(b) ])
    
    enerigaCA = calcEnergia(ca)
    fator = int (enerigaX / enerigaCA)
    
    ca = ca * fator
    
    return ca


def visualizacaoGraficaMonfonico(sinal, fs, ca):
    print("\n *** Ex 10 Grafico *** \n")
    
    ts = 1/fs       # intervalo de amostragem
    nrAmostras = sinal.shape[0]
    duracao = nrAmostras * ts
    if len(sinal.shape) == 1:
        sinal = np.array(sinal[:], sinal.dtype)
    else:
        sinal = np.array(sinal[:, 0], sinal.dtype)
    
    sinal = np.array(sinal, float) / (float(pow(2, int(str(sinal.dtype)[3:]) - 1)) + 1)
    
    ca = np.array(ca, ca.dtype)
    ca = np.array(ca, float) / (float(pow(2, int(str(ca.dtype)[3:]) - 1)) + 1)

    tIni = 0
    tFim = duracao
    
    tempo = np.array(np.arange(0, duracao, ts), float)
    
    plt.figure()
        
    plt.subplot(2,1,1)
    plt.plot(tempo, sinal,'y')
    plt.xlabel('Tempo (seg)')
    plt.ylabel('Amplitude [-1:1]')
    plt.title('Canal Esquerdo')
    plt.ylim(-1, 1)
    plt.xlim(tIni, tFim)
        
    plt.subplot(2,1,2)
    plt.plot(tempo, ca,'y')
    plt.xlabel('Tempo (seg)')
    plt.ylabel('Amplitude [0:1]')
    plt.title('Sinal Monfónico')
    plt.ylim(0, 1)
    plt.xlim(tIni, tFim)


## Main
if __name__ == "__main__":
    nomeFicheiro = 'saxriff.wav'
    
    fs, data = leitura(nomeFicheiro)
    #print(fs)
    #print(data)
    #print(data.dtype)
    
    #"""
    
    #reproduzir(fs, data)
    
    apresentarInfo(nomeFicheiro, fs, str(data.dtype)[3:])
    
    visualizacaoGrafica(data[:,0], fs)  # Exemplo Canal Mono
    
    visualizacaoGrafica(data, fs)   # Exemplo Sem Limitacao de Tempo
    
    visualizacaoGrafica(data, fs, 1.6)     # Exemplo Com Limitacao de Tempo
    
    visualizacaoGrafica(data, fs, 1.55, 1.57)     # Exemplo Com Limitacao de Tempo
    
    visualizacaoGrafica2(data, fs)  # Com Axis
    
    sinalRuidoso = ruido(data, 0.5)
    #reproduzir(fs, sinalRuidoso)
    
    eneriga = calcEnergia(data)
    print("Energia Esquerda: " + str(eneriga[0]))
    print("Energia Direita: " + str(eneriga[1]))
    
    sinalResultanteSetereoSubstituido = substituirCanal(data, 'beats.wav', 3)
    #reproduzir(fs, sinalResultanteSetereoSubstituido)
    visualizacaoGrafica(sinalResultanteSetereoSubstituido, fs)
    
    sinalResultanteMonoMisturado = misturarCanais(data, 'beats.wav', 3)
    #reproduzir(fs, sinalResultanteMonoMisturado)
    visualizacaoGrafica(sinalResultanteMonoMisturado, fs)
    
    #"""
    
    ca1 = contornoAmplitude(data, 5)
    visualizacaoGraficaMonfonico(data, fs, ca1)
    
    #ca2 = contornoAmplitude(data, 7)
    #visualizacaoGraficaMonfonico(data, fs, ca2)
    
    ca3 = contornoAmplitude(data, 21)
    visualizacaoGraficaMonfonico(data, fs, ca3)
    
    #ca4 = contornoAmplitude(data, 25)
    #visualizacaoGraficaMonfonico(data, fs, ca4)
    
    ca5 = contornoAmplitude(data, 75)
    visualizacaoGraficaMonfonico(data, fs, ca5)
    
    ca6 = contornoAmplitude(data, 255)
    visualizacaoGraficaMonfonico(data, fs, ca6)
    
    ca7 = contornoAmplitude(data, 355)
    visualizacaoGraficaMonfonico(data, fs, ca7)
    
    
    #"""
    
    
