import matplotlib.pyplot as plt
import numpy as np
from huffmancodec import *


def histograma(data, fname):
    data, count = alphabet_text(data)

    plt.figure()
    hist = plt.bar(data, count, edgecolor='black', linewidth=0.3)

    plt.title("Ocorrências dos símbolos de " + fname[8:])
    plt.xlabel("Símbolos")
    plt.ylabel("Ocorrências")

    return hist


# AUXILIAR: Alfabeto para texto
def alphabet_text(data):
    output = np.unique(data)
    #output = np.array([chr(i) for i in range(0, 128)])
    #output.sort()
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
    with open(fname) as f:
        text = f.read()
    return np.array([char for char in text], dtype='<U1')


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


# MAIN
def main():
    plt.close('all')

    '''
    # Customize matplotlib
    plt.rcParams.update(
        {
            'text.usetex': False,
            'font.family': 'stixgeneral',
            'mathtext.fontset': 'stix',
        }
    )
    '''

    fnames = ["bible.txt", "finance.csv", "jquery-3.6.0.js", "random.txt"]

    fnames = ["dataset/" + file for file in fnames]

    file_data = get_data(fnames[3])
    histograma(file_data, fnames[3])
    alfabeto, count = alphabet_text(file_data)

    ent = entropia(count)
    print("> Entropia: ", ent)
    '''
    for i in range(0, 1):
        file_data = get_data(fnames[i])

        if file_data is not None:
            histograma(file_data, fnames[i])

            print("\n", fnames[i][8:], ":")

            alfabeto, count = alphabet_text(file_data)

            ent = entropia(count)
            print("> Entropia: ", ent)

            # huffman_media, huffman_variancia = huffman_media_variancia(file_data, count)
            # print("> Huffman: número médio de bits por símbolo: ", huffman_media)
            # print("> Huffman: variância dos comprimentos dos códigos: ", huffman_variancia)

            # print(f'> Entropia agrupada: {grouping(file_data)}')
    '''


if __name__ == "__main__":
    main()
