# CODEC

Faz a **compressão** e a **descompressão** utilizando e conectando as componentes em anexo.
Também **verifica** e **compila** as componentes.
Ficheiros em análise em [dataset/](dataset/).

<br />

## Documentação
### Compatibilidade de SO:
Este script em bash é compatível com Unix/Linux e Mac. Apenas foi testado no Ubuntu.
Poder-lhe-á ser pedido para instalar packages/libraries do Unix para compilar e executar o código (make, cargo, rustc, openjdk-17-jdk, openjdk-17-jre, gcc, g++).

<br />

### Descrição do CODEC:
**Variante 1**: Burrows–Wheeler Transform (BWT) + Move-To-Front (MTF) + Arithmetic Coding <br />
**Variante 2**: LZ77 + Arithmetic Coding

<br />

## Métricas Apresentadas
- Tamanho do ficheiro comprimido (em KB)
- Taxa de compressão (ratio)
- Tempo de compressão (em segundos)
- Tempo de descompressão (em segundos)

<br />

## Componentes do CODEC
1. Arithmetic Coding *(C++)*, em [ARITH/](ARITH/), fonte: [github.com/dmitrykravchenko2018](https://github.com/dmitrykravchenko2018/arithmetic_coding)
2. Burrows–Wheeler Transform *(Rust)*, em [BWT/](BWT/), fonte: [github.com/izflare](https://github.com/izflare/BWT)
3. LZ77 *(C)*, em [LZ77/](LZ77/), fonte: [github.com/cstdvd](https://github.com/cstdvd/lz77)
4. Move-To-Front  *(Java)*, em [MTF/](MTF/), fonte: [github.com/fujiawu](https://github.com/fujiawu/burrows-wheeler-compression)

<br />

## Utilização
```shell
bash codec.sh [flags opcionais, ordem aleatoria...] -1|2 -i caminho/para/fonte -o caminho/para/destino
```
<pre>
-h   --ajuda           ajuda
-c   --comprimir       comprimir [default]
-d   --descomprimir    descomprimir
-v   --verificar       informações ao longo da execução do script
-x   --compilar        com compilação (útil na primeira utilização)
-1   --bwt-mtf-arith   variante: BWT + MTF + ARITH
-2   --lz77-arith      variante: LZ77 + ARITH
-i=* --fonte=*         indicar caminho/para/fonte (input)
-i * --fonte *         ^equivalente
-o=* --destino=*       indicar caminho/para/destino (output) [default=output.codec]
-o * --destino *       ^equivalente

Notas: '*' denota caminho/para/ficheiro;
       é apenas mandatório indicar a variante ('-1' ou '-2') e a fonte ('-i' ou equivalente).
</pre>

<br />

### Pré-requisitos e Primeira Utilização:
#### Compilação: ####
Para poder executar o script é necessário primeiro compilar cada uma das componentes.
Pode fazê-lo de duas formas seguintes:

1. de **modo manual**, compilando componente a componente, e respeitando sempre a estrutura-padrão dos ficheiros, ou seja, fazer cumprir os manifestos/makefiles.
Para mais detalhes sobre como os ficheiros são usados no script, ver as constantes ("..._PATH", "..._EXE_FILE", "..._COMPILE_FILE", etc.) declaradas no inicio do [codec.sh](codec.sh). <br />
Esta forma poder-lhe-á ser útil caso não queira instalar as packages utilizadas pelo script (ver constante "PACKAGE_ARRAY"), e utilizar umas outras equivalentes. 
Note-se que também pode alterar a constante "PACKAGE_ARRAY", desde que a sua utilização seja equivalente, e assim utilizar a 2º opção.

2. ou **automaticamente**, utilizando o próprio script (recomendado). Para isso deve incluir a flag "-x" na execução do comando:
```console
user@PC:/path/to/script$ bash codec.sh -x ...
```
Basta fazê-lo uma vez, na primeira utilização. <br />
O script irá verificar se as packages se encontram instaladas (make, cargo, rustc, openjdk-17-jdk, openjdk-17-jre, gcc, g++). 
No caso de não estarem, ser-lhe-á questionado se as pretende instalar (responda "yes"): caso negue, a execução do script terminará.

#### Execução: ####
Existem várias formas de executar o script, como por exemplo:
- **utilizando 'bash'**: <br />
```console
user@PC:/path/to/script$ bash codec.sh ...
```

<br />

- **executando diretamente**: <br />
```console
user@PC:/path/to/script$ ./codec.sh ...
```

Note-se que poderá ser necessário atribuir permissões antes de executar:
```console
user@PC:/path/to/script$ chmod u+x codec.sh
```

<br />

### Exemplo de Compressão:
```console
user@PC:/path/to/script$ bash codec.sh -i bible.txt -2 -o bible.txt.codec -x
```

<br />

### Exemplo de Descompressão:
```console
user@PC:/path/to/script$ bash codec.sh --lz77-arith -d -i=bible.txt.codec
```

<br />

## Âmbito
FCTUC - Licenciatura em Engenharia Informática	<br />
Teoria da Informação - PL2 / Prof. Doutor Rui Paiva <br />
Trabalho Prático n. 2 | 23 de dezembro de 2021

<br />

## Autores
### Grupo 9:
* **João Ricardo Botelho**, n. 2019155348, uc2019155348@student.uc.pt, GitHub: [@Jrbotelho](https://github.com/Jrbotelho)
* **Guilherme Branco**, n. 2020216924, mbranco@student.dei.uc.pt, GitHub: [@AdventurousGui](https://github.com/AdventurousGui)
* **Dario Felix**, n. 2018275530, dario@student.dei.uc.pt, GitHub: [@DFTF-PConsole](https://github.com/DFTF-PConsole)

