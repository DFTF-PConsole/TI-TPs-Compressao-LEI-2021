#!/bin/bash

#	LEIA O README.md

#	Faz a compressão e a descompressão utilizando e juntando as componentes em anexo.

#	EXECUTAR: bash codec.sh -1|2 -i caminho/para/fonte [flags opcionais, ordem aleatoria...] 


#	Trabalho Pratico n. 2 - Meta 2
#	
#	PL2 / Prof. Rui Paiva
#	17 de novembro de 2021
#	
#	Autores (Grupo 9):
#	    > João Ricardo Botelho, n. 2019155348, uc2019155348@student.uc.pt
#	    > Guilherme Branco, n. 2020216924, mbranco@student.dei.uc.pt
#	    > Dario Felix, n. 2018275530, dario@student.dei.uc.pt



# Constantes

# Flags (valores default)
COMP=0
VERIFICAR=0
COMPILAR=0
VARIANTE=0
FONTE=""
DESTINO="output.codec"


declare -a PACKAGE_ARRAY=("make" "cargo" "rustc" "openjdk-17-jdk" "openjdk-17-jre" "gcc" "g++")

ARITH_PATH="ARITH/"
BWT_PATH="BWT/"
BWT_EXE_PATH="BWT/target/release/"
LZ77_PATH="LZ77/"
MTF_PATH="MTF/"

ARITH_COMPILE_FILE="Makefile"
ARITH_EXE_FILE="arithm-coding"
BWT_COMPILE_FILE="Cargo.toml"
BWT_EXE_FILE="bwt"
LZ77_COMPILE_FILE="Makefile"
LZ77_EXE_FILE="lz77"
MTF_COMPILE_FILE="MTF.java"
MTF_EXE_FILE="MTF.class"
MTF_REAL_EXE_FILE="MTF"



function abortar {
	echo ""
	echo "*** SCRIPT INTERROMPIDO ***"
	set -e
	exit 0
}


function abortarComAjuda {
	echo ""
	echo "Para obter ajuda, digite: bash codec.sh --ajuda"
	echo "Para obter informações ao longo da execução do script, acrescente a flag '-v'"
	abortar	
}


function echoIndent {
	printf " %-35s%s\n" "$1" "$2"
}


function echoIndentCondicional {
	if  (( $VERIFICAR == 1 ))
	then
		echoIndent "$1" "$2"
	fi
}


function echoCondicional {
	if  (( $VERIFICAR == 1 ))
	then
		echo "$1"
	fi
}


function zeroFloat {
	if [ $(echo "$1 > 1.0" | bc -l) -eq 1 ]
	then
		echo 0 &> /dev/null
	else
		echo "0"
	fi
}


function utilizacao {
	echo "Utilização: bash codec.sh [flags opcionais, ordem aleatoria...] -1|2 -i caminho/para/fonte -o caminho/para/destino"
	echo "     -h   --ajuda            ajuda"
	echo "     -c   --comprimir        comprimir [default]"
	echo "     -d   --descomprimir     descomprimir"
	echo "     -v   --verificar        informações ao longo da execução do script"
	echo "     -x   --compilar         com compilação (útil na primeira utilização)"
	echo "     -1   --bwt-mtf-arith    variante: BWT + MTF + ARITH"
	echo "     -2   --lz77-arith       variante: LZ77 + ARITH"
	echo "     -i=* --fonte=*          indicar caminho/para/fonte (input)"
	echo "     -i * --fonte *          [^equivalente]"
	echo "     -o=* --destino=*        indicar caminho/para/destino (output) [default=output.codec]"
	echo "     -o * --destino *        [^equivalente]"
	echo ""
	echo "Ex. 1: bash codec.sh -i bible.txt -2 -o bible.txt.codec -x"
	echo "Ex. 2: bash codec.sh --lz77-arith -d -i=bible.txt.codec"
}


function deleteFile {
	if [ -f "$1" ]
	then
		rm "$1"
	fi
}


function checkFileMsg {
	if [ -f "$1" ]
	then
		echoIndentCondicional "$1:" "$2"
	else
		echoIndent "$1:" "$3"
		abortar
	fi
}


function isPackageNotInstalled {
	dpkg --status "$1" &> /dev/null
	if [ $? -eq 0 ]
	then
		echoIndentCondicional "$1:" "instalado"
	else
		echoIndent "$1:" "não instalado"
		echo ""
		while true
		do
			echo "Deseja instalar a package '$1' (necessária para compilar)? [Y/N]"
			printf "> "
			read yn
			case $yn in
				[Yy]* )
					echo ""
					sudo apt-get update && sudo apt-get install -y "$1"
					echo ""
					echoIndentCondicional "$1:" "instalado"
					break
					;;
				[Nn]* )
					echo ""
					break
					;;
				* ) 
					echo "Por favor responda 'yes' ou 'no'."
					;;
			esac
		done
	fi
}


function checkPackage {
	dpkg --status "$1" &> /dev/null
	if ! [ $? -eq 0 ]
	then
		echoIndent "$1:" "não instalado"
		abortar
	fi
}


function checkCompileFiles {
	declare -a filesArray=("$ARITH_PATH$ARITH_COMPILE_FILE" "$BWT_PATH$BWT_COMPILE_FILE" "$LZ77_PATH$LZ77_COMPILE_FILE" "$MTF_PATH$MTF_COMPILE_FILE")
	
	for i in "${filesArray[@]}"
	do
		checkFileMsg "$i" "encontrado" "não encontrado"
	done
	
	echoCondicional ""
}


function compile {
	declare -a filesArray=("$ARITH_PATH$ARITH_EXE_FILE" "$BWT_EXE_PATH$BWT_EXE_FILE" "$LZ77_PATH$LZ77_EXE_FILE" "$MTF_PATH$MTF_EXE_FILE")
	
	if (( $COMPILAR == 1 ))
	then
		echoCondicional ""
		echoCondicional "### COMPILANDO... ###"
		echoCondicional ""
		
		for i in "${filesArray[@]}"
		do
			deleteFile "$i"
		done
		
		make -C $ARITH_PATH &> /dev/null
		cargo build --release --manifest-path=$BWT_PATH$BWT_COMPILE_FILE &> /dev/null
		make -C $LZ77_PATH &> /dev/null
		javac $MTF_PATH$MTF_COMPILE_FILE -sourcepath $MTF_PATH -d $MTF_PATH &> /dev/null
	fi
	
	for i in "${filesArray[@]}"
	do
		checkFileMsg "$i" "compilado" "não compilado"
	done
	
	echoCondicional ""
}


function checking {
	echoCondicional "### VERIFICANDO... ###"
	echoCondicional ""
	
	if (( $COMPILAR == 1 ))
	then
		for i in "${PACKAGE_ARRAY[@]}"
		do
			isPackageNotInstalled "$i"
			checkPackage "$i"
		done
		echoCondicional ""
		
		checkCompileFiles
	fi
	
	checkFileMsg "$FONTE" "encontrado" "não encontrado"
	
	if touch "$DESTINO"
	then
		deleteFile "$DESTINO"
	else
		echoIndent "$DESTINO:" "acesso negado"
		abortar
	fi
	
	echoCondicional ""
}


function erroComponente {
	echo "Não foi possivel concluir a operação porque ocorreu um erro desconhecido numa das componentes (possiveis causas: ficheiro incompativel com a variante em uso, ou corrompido, ou não está em UTF-8)"
	abortar
}


function checkOutFile {
	if ! [ -f "$1" ]
	then
		erroComponente
	fi
}


function compressing {
	echoCondicional ""
	echo "### COMPRIMINDO... ###"
	echo ""
	
	fileSizeNonComp=$(stat -c%s "$FONTE")
	temp=$(echo "scale=3; $fileSizeNonComp / 1024" | bc)
	echoIndent "Tamanho do Ficheiro:" "$(zeroFloat $temp)$temp KB"
	
	start=`date +%s.%3N`
	
	if (( $VARIANTE == 1 ))
	then
		./$BWT_EXE_PATH$BWT_EXE_FILE --input $FONTE &> /dev/null
		checkOutFile $FONTE.bwt
		java -cp $MTF_PATH $MTF_REAL_EXE_FILE - $FONTE.bwt temp0.codec &> /dev/null
		checkOutFile temp0.codec
	elif (( $VARIANTE == 2 ))
	then
		./$LZ77_PATH$LZ77_EXE_FILE -c -i $FONTE -o temp0.codec -l 255 -s 65535 &> /dev/null
		checkOutFile temp0.codec
	else
		abortar
	fi
	./$ARITH_PATH$ARITH_EXE_FILE e temp0.codec $DESTINO &> /dev/null 
	
	end=`date +%s.%3N`
	
	checkOutFile $DESTINO
	
	deleteFile $FONTE.bwt
	deleteFile temp0.codec
	
	fileSizeComp=$(stat -c%s "$DESTINO")
	if (( $fileSizeComp == 0 ))
	then
		erroComponente
	fi
	
	temp=$(echo "scale=3; $fileSizeComp / 1024" | bc)
	echoIndent "Tamanho do Ficheiro Comprimido:" "$(zeroFloat $temp)$temp KB"
		
	temp=$(echo "scale=3; $fileSizeNonComp / $fileSizeComp" | bc)
	echoIndent "Taxa de Compressão (Ratio):" " $(zeroFloat $temp)$temp"
	
	duration=$( echo "$end - $start" | bc -l )
	echoIndent "Tempo de Compressão:" " $(zeroFloat $duration)$duration seg"
}


function decompressing {
	echoCondicional ""
	echo "### DESCOMPRIMINDO... ###"
	echo ""
	
	start=`date +%s.%3N`
	
	./$ARITH_PATH$ARITH_EXE_FILE d $FONTE temp0.codec &> /dev/null
	checkOutFile temp0.codec
	if (( $VARIANTE == 1 ))
	then
		java -cp $MTF_PATH $MTF_REAL_EXE_FILE + temp0.codec temp1.codec.bwt &> /dev/null
		checkOutFile temp1.codec.bwt
		./$BWT_EXE_PATH$BWT_EXE_FILE -r --input temp1.codec.bwt &> /dev/null
		checkOutFile temp1.codec.bwt.rev
		mv temp1.codec.bwt.rev $DESTINO
	elif (( $VARIANTE == 2 ))
	then
		./$LZ77_PATH$LZ77_EXE_FILE -d -i temp0.codec -o $DESTINO -l 255 -s 65535 &> /dev/null
		checkOutFile $DESTINO
	else
		abortar
	fi
	
	end=`date +%s.%3N`
	
	deleteFile temp0.codec
	deleteFile temp1.codec.bwt
	
	fileSize=$(stat -c%s "$DESTINO")
	if (( $fileSize == 0 ))
	then
		erroComponente
	fi
	
	duration=$( echo "$end - $start" | bc -l )
	echoIndent "Tempo de Descompressão:" " $(zeroFloat $duration)$duration seg"
}


function main {
	declare -a flagArray=()
	declare -a valueArray=()
	
	countFlag=0
	
	for i in "$@"
	do
		case $i in
			-h|--ajuda)
				utilizacao
				set -e
				exit 0
				;;
			-c|--comprimir)
				COMP=0
				shift
				;;
			-d|--descomprimir)
				COMP=1
				shift
				;;
			-v|--verificar)
				VERIFICAR=1
				shift
				;;
			-x|--compilar)
				COMPILAR=1
				shift
				;;
			-1|--bwt-mtf-arith)
				VARIANTE=1
				shift
				;;
			-2|--lz77-arith)
				VARIANTE=2
				shift
				;;
			-i=*|--fonte=*)
				FONTE="${i#*=}"
				shift
				;;
			-i|--fonte)
				countFlag=$((countFlag+1))
				flagArray[${#flagArray[@]}]=FONTE
				shift
				;;
			-o=*|--destino=*)
				DESTINO="${i#*=}"
				shift
				;;
			-o|--destino)
				countFlag=$((countFlag+1))
				flagArray[${#flagArray[@]}]=DESTINO
				shift
				;;
			*)    # outros
				if  (( $countFlag >= 1 ))
				then
					valueArray[${#valueArray[@]}]=$i
					countFlag=$((countFlag-1))
					shift
				else
					echo "Argumentos inválidos! (Flag inválida: '$i')"
					abortarComAjuda
				fi
		esac
	done
	
	if  (( $VARIANTE == 0 ))
	then
		echo "Argumentos inválidos! (Variante não definida)"
		abortarComAjuda
	fi
	
	for i in "${flagArray[@]}"
	do
		if  (( ${#valueArray[@]} >= 1 ))
		then
			declare $i="${valueArray[0]}"
			valueArray=("${valueArray[@]:1}")
		else
			echo "Argumentos inválidos! (Flag '$i' sem valor)"
			abortarComAjuda
		fi
	done
	
	if [ "$FONTE" = "" ]
	then
		echo "Argumentos inválidos! (Introduza uma fonte)"
		abortarComAjuda
	fi
	
	if [ "$FONTE" = "$DESTINO" ]
	then
		echo "Argumentos inválidos! (A fonte (input) não pode ser igual ao destino (output))"
		abortarComAjuda
	fi
	
	checking
	
	compile
	
	if (( $COMP == 0 ))
	then
		compressing
	else
		decompressing
	fi
}



# RUN
main "$@"

