# -*- coding: utf-8 -*-

"""
    Trabalho Pratico n. 1 - Entropia, Redundancia e Informacao Mutua

    PL2 / Prof. Rui Paiva
    5 de novembro de 2021

    Autores (Grupo 9):
        > João Ricardo Botelho, n. 2019155348, uc2019155348@student.uc.pt
        > Guilherme Branco, n. 2020216924, mbranco@student.dei.uc.pt
        > Dario Felix, n. 2018275530, dario@student.dei.uc.pt

"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.io.wavfile as spiowf
import numpy as np
import string
from huffmancodec import *


# Alínea 1. (histograma)
def histograma(data, fname):
    if np.issubdtype(data.dtype, np.integer):
        data, count = alphabet(data)
    elif np.issubdtype(data.dtype, np.str_):
        data, count = alphabet_text(data)
    else:
        return None

    plt.figure()
    hist = plt.bar(data, count, edgecolor='black', linewidth=0.3)

    plt.title("Ocorrências dos símbolos de " + fname[5:])
    plt.xlabel("Símbolos")
    plt.ylabel("Ocorrências")

    return hist


# AUXILIAR: Alfabeto para arrays numericas
def alphabet(data):
    if data.dtype == np.uint8:
        size = 8
    else:
        size = int(str(data.dtype)[-2:])
    output = np.arange(0, pow(2, size))
    count = np.zeros((pow(2, size)), dtype=np.float64)
    for element in data:
        count[element] += 1
    return output, count


# AUXILIAR: Alfabeto para texto
def alphabet_text(data):
    output = np.array([c for c in string.ascii_letters], dtype='<U1')
    output.sort()
    count = np.zeros((len(output)), dtype=np.float32)
    for element in data:
        count[np.where(output == element)] += 1
    return output, count


# Alínea 2. (limite mínimo teórico para o número médio de bits por símbolo)
def entropia(lista_ocorrencias):
    lista_prob = np.array(lista_ocorrencias, float) / np.sum(lista_ocorrencias)
    lista_prob = lista_prob[(lista_prob > 0.0)]

    entrp = np.sum(lista_prob * np.log2(1 / lista_prob))

    return entrp


# AUXILIAR: Leitura do ficheiro de som, imagem e texto
def get_data(fname):
    if fname[-4:] == ".wav":
        sf, sig = spiowf.read(fname)  # devolve a frequência de amostragem (fs) e um array sig com os dados da onda
        if len(sig.shape) > 1:
            sig = sig[:, 0]  # only uses first sound channel
        return sig, sf

    elif fname[-4:] == ".bmp":
        img = mpimg.imread(fname)
        return img

    elif fname[-4:] == ".txt":
        with open(fname) as f:
            text = f.read()
        return np.array([char for char in text if char.isalpha()], dtype='<U1')

    else:
        print("Cannot get data from ", fname)
        return None


# Alínea 4. (codificação de Huffman: determine o número médio de bits por símbolo + variância dos comprimentos dos códigos resultantes)
def huffman_media_variancia(data, lista_ocorrencias):
    codec = HuffmanCodec.from_data(data)
    symbols, lenghts = codec.get_code_len()

    n_total_simbolos = np.sum(lista_ocorrencias)
    lista_prob = np.array(lista_ocorrencias, float) / n_total_simbolos
    lista_prob = lista_prob[(lista_prob > 0.0)]

    media = np.average(lenghts, weights=lista_prob)

    variancia = np.average(np.power(lenghts - media, 2), weights=lista_prob)
    # variancia = np.sum(np.power(lenghts - media, 2) * lista_prob) # Alternativa

    return media, variancia


# Alínea 5. (alínea 3. aplicando agrupamentos de símbolos)
def grouping(data):
    if len(data) % 2 != 0:
        data = data[:-1]
    res_data = data.reshape(len(data) // 2, 2)
    count = np.unique(res_data, axis=0, return_counts=True)[1].astype(np.float64) / (len(data) / 2)
    entrp = np.sum(count * np.log2(1 / count)) / 2
    return entrp


# ALTERNATIVA: Alínea 5. (alínea 3. aplicando agrupamentos de símbolos)
def grouping_without_np(data):
    if len(data) % 2 != 0:
        data = data[:-1]
    res_data = np.array([data[i] * len(data) + data[i + 1] for i in range(0, len(data), 2)])
    count = np.unique(res_data, return_counts=True)[1].astype(np.float64)
    entrp = entropia(count) / 2
    return entrp


# Alínea 6. a) (vector de valores de informação mútua em cada janela)
def shazam(query, target, alpha, step):
    return [mutualInfo(query, target[i: i + len(query)], alpha) for i in range(0, len(target) - len(query) + 1, step)]


# AUXILIAR: alínea 6. a) (informação mútua numa determinada janela)
def mutualInfo(query, target, alpha):
    prob_conjuntas = np.zeros([len(alpha), len(alpha)], dtype=float)

    # Probabilidade query
    q_alpha = np.array([np.count_nonzero(query == x) for x in alpha], float)
    q_alpha /= len(query)

    # Probabilidade target
    t_alpha = np.array([np.count_nonzero(target == x) for x in alpha], float)
    t_alpha /= len(target)

    # Probabilidade Conjunta P(query, target)
    for i in range(len(query)):
        prob_conjuntas[query[i]][target[i]] += 1
    prob_conjuntas /= len(query)

    # Probabilidade "Independente": P(query) * P(target)
    pqpt = q_alpha.reshape((len(q_alpha), 1)) * t_alpha.reshape((1, len(t_alpha)))

    # Divisao: P(query, target) / P(query) * P(target)
    div = np.divide(prob_conjuntas, pqpt, out=np.zeros_like(pqpt), where=pqpt != 0)

    # P(query, target) * log2(  P(query, target) / P(query) * P(target)  )
    output = np.sum(prob_conjuntas * np.log2(div, out=np.zeros_like(pqpt), where=div != 0))
    return output


# Alínea 6. b) (determine a variação da informação mútua entre GuitarSolo e em repeat e repeatNoise)
def guitarSoloRepeatNoise(dataGuitarSolo, dataRepeat, dataRepeatNoise, alphabet, passo):
    listaInfoMutua = calcMultiTargets(dataGuitarSolo, [dataRepeat, dataRepeatNoise], alphabet, passo)

    print("\n Informação mútua guitarSolo: Repeat Vs. RepeatNoise:")
    print("> Repeat: \n", np.around(listaInfoMutua[0], decimals=4))
    print("> RepeatNoise: \n", np.around(listaInfoMutua[1], decimals=4))

    plt.figure()
    plt.subplot(2, 1, 1)
    graficoInfoMutua(list(range(1, len(listaInfoMutua[0]) + 1)), listaInfoMutua[0], 'b', 'target01 - repeat')

    plt.subplot(2, 1, 2)
    graficoInfoMutua(list(range(1, len(listaInfoMutua[1]) + 1)), listaInfoMutua[1], 'r', 'target02 - repeatNoise')

    return listaInfoMutua


# AUXILIAR: alínea 6. b) (visualize graficamente a evolução da informação mútua)
def graficoInfoMutua(x, y, cor, title):
    plt.plot(x, y, cor)
    plt.xlabel('Janela')
    plt.ylabel('Informação Mútua')
    plt.title(title)
    # plt.ylim(0, 1)
    # plt.xlim(0, 1)


# AUXILIAR: alínea 6. b) e c) (rotina para calcular info. mutua em multiplos targets)
def calcMultiTargets(query, listaTargets, alphabet, passo):
    listaInfoMutua = [None] * len(listaTargets)
    for i in range(len(listaTargets)):
        listaInfoMutua[i] = shazam(query, listaTargets[i], alphabet, passo)

    return listaInfoMutua


# Alínea 6. c) (simulador de identificação de música em multiplos ficheiros)
def identif_musica(query, listaTargets, alphabet, passo):
    listaInfoMutua = calcMultiTargets(query, listaTargets, alphabet, passo)
    listaMaxInfoMutua = [None] * len(listaInfoMutua)
    listaNumSong = list(range(len(listaInfoMutua)))  # Lista A ORDENAR (numeracao/indice das songs)

    for i in range(len(listaInfoMutua)):
        listaMaxInfoMutua[i] = np.amax(listaInfoMutua[i])

    # Ordenacao em 2 listas, mas tendo como referencia apenas a primeira
    # o [1]: como faz return das 2 listas ordenadas, apenas quero a segunda (lista dos indices)
    listaNumSong = list(zip(*sorted(zip(listaMaxInfoMutua, listaNumSong), reverse=True)))[1]

    print("\n Informação mútua máxima para cada Song (ordem decrescente): ")
    for i in listaNumSong:
        print(f"> Song0{i + 1}.wav: ", listaMaxInfoMutua[i])

    return listaInfoMutua  # (nota: nao ordenado)


# MAIN
def main():
    plt.close('all')

    fnames = ["english.txt", "guitarSolo.wav", "homer.bmp", "homerBin.bmp", "kid.bmp", "Song01.wav", "Song02.wav",
              "Song03.wav", "Song04.wav", "Song05.wav", "Song06.wav", "Song07.wav", "target01 - repeat.wav",
              "target02 - repeatNoise.wav"]

    fnames = ["data/" + file for file in fnames]

    for i in range(0, 5):
        file_data = None

        if fnames[i][-4:] == ".wav":
            file_data, fs = get_data(fnames[i])
            if len(file_data.shape) > 1:
                file_data = file_data[:, 0]  # only uses first sound channel

        elif fnames[i][-4:] == ".bmp":
            file_data = get_data(fnames[i])
            file_data = file_data.ravel()  # flattens image array

        elif fnames[i][-4:] == ".txt":
            file_data = get_data(fnames[i])

        if file_data is not None:
            print("\n", (fnames[i][5:]).upper(), ":")

            # Alínea 3. (alínea 1. + alínea 2.)
            histograma(file_data, fnames[i])

            if fnames[i][-4:] == ".txt":
                alfabeto, count = alphabet_text(file_data)
            else:
                alfabeto, count = alphabet(file_data)

            ent = entropia(count)
            print("> Entropia: ", ent)

            # Alínea 4.
            huffman_media, huffman_variancia = huffman_media_variancia(file_data, count)
            print("> Huffman: número médio de bits por símbolo: ", huffman_media)
            print("> Huffman: variância dos comprimentos dos códigos: ", huffman_variancia)

            # Alínea 5.
            print(f'> Entropia agrupada: {grouping(file_data)}')


    # PRE - alínea 6. b) e c)
    data_guitar_solo, fs = get_data(fnames[1])
    alfabeto_guitar, count = alphabet(data_guitar_solo)
    passo = int(len(data_guitar_solo) / 4)

    # Alínea 6. b)
    guitarSoloRepeatNoise(data_guitar_solo, get_data(fnames[12])[0], get_data(fnames[13])[0], alfabeto_guitar, passo)

    # Alínea 6. c)
    identif_musica(data_guitar_solo, [get_data(fnames[i])[0] for i in range(5, 12)], alfabeto_guitar, passo)


if __name__ == "__main__":
    main()
