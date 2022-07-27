# Comparação dos Sistemas Referidos no Estado da Arte (Benchmark)

Compara a **compressão** e **descompressão** dos sistemas documentados, utilizando os ficheiros em análise em [dataset/](dataset/).



## Documentação
### Compatibilidade de SO:
Este script em bash é compatível com Unix/Linux e Mac. Apenas foi testado no Ubuntu.
Todos os sistemas utilizados são packages/libraries do Unix e poderá ser pedido para instalar (ent, rzip, bzip2, gzip, lzma).



## Métricas
* Entropia (em bits por símbolo/byte)
* Tamanho do ficheiro comprimido (em KB)
* Taxa de compressão (ratio)
* Tempo de compressão (em segundos)
* Tempo de descompressão (em segundos)



## Sistemas
* rzip:	[Linux man page](https://linux.die.net/man/1/rzip)
* bzip2: [Linux man page](https://linux.die.net/man/1/bzip2)
* gzip:	[Linux man page](https://linux.die.net/man/1/gzip)
* lzma:	[Linux man page](https://linux.die.net/man/1/lzma)



## Utilização
```bash
bash benchmark.sh
```



## Âmbito
FCTUC - Licenciatura em Engenharia Informática	<br />
Teoria da Informação - PL2 / Prof. Rui Paiva <br />
Trabalho Prático n. 2 - Meta 2 | 23 de dezembro de 2021



## Autores
### Grupo 9:
* **João Ricardo Botelho**, n. 2019155348, uc2019155348@student.uc.pt, GitHub: [@Jrbotelho](https://github.com/Jrbotelho)
* **Guilherme Branco**, n. 2020216924, mbranco@student.dei.uc.pt, GitHub: [@AdventurousGui](https://github.com/AdventurousGui)
* **Dario Felix**, n. 2018275530, dario@student.dei.uc.pt, GitHub: [@DFTF-PConsole](https://github.com/DFTF-PConsole)

