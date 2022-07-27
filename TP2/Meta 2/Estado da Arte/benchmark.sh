#!/bin/bash

#	LEIA O README.md

#	Comparação dos Sistemas Referidos no Estado da Arte (Benchmark) + Entropia

#	EXECUTAR: bash benchmark.sh


#	Trabalho Pratico n. 2 - Meta 2
#	
#	PL2 / Prof. Rui Paiva
#	17 de novembro de 2021
#	
#	Autores (Grupo 9):
#	    > João Ricardo Botelho, n. 2019155348, uc2019155348@student.uc.pt
#	    > Guilherme Branco, n. 2020216924, mbranco@student.dei.uc.pt
#	    > Dario Felix, n. 2018275530, dario@student.dei.uc.pt



declare -a allPackageArray=("rzip" "bzip2" "gzip" "lzma")
declare -a allFilesArray=("bible.txt" "finance.csv" "jquery-3.6.0.js" "random.txt")
declare -a filesArray=()
declare -a packageArray=()

flagEnt=0

pathDataset="dataset/"
pathComp="comp/"
pathDecomp="decomp/"

numSpaces=30
numTest=5

globalDuration=0.0



function abortar {
	echo ""
	echo "*** SCRIPT ABORTADO ***"
	set -e
	exit 0
}


function echoIndent {
	printf " %-${numSpaces}s%s\n" "$1" "$2"
}


function zeroFloat {
	if [ $(echo "$1 > 1.0" | bc -l) -eq 1 ]; then
		echo 0 &> /dev/null
	else
		echo "0"
	fi
}


function isPackageNotInstalled {
	dpkg --status $1 &> /dev/null
	if [ $? -eq 0 ]; then
		echoIndent "$1:" "installed"
	else
		echoIndent "$1:" "not installed"
		echo ""
		while true; do
			echo "Do you want to install this package?"
			printf "> "
			read yn
			case $yn in
				[Yy]* ) echo ""; sudo apt-get update && sudo apt-get install -y $1; echo ""; echoIndent "$1:" "installed"; break;;
				[Nn]* ) echo ""; break;;
				* ) echo "Please answer yes or no.";;
			esac
		done
	fi
}


function checkPackage {
	dpkg --status $1 &> /dev/null
	if [ $? -eq 0 ]; then
		packageArray[${#packageArray[@]}]=$1
	else
		echoIndent "$1:" "ignored"
	fi
}


function deleteFile {
	if [ -f $1 ]; then
		rm $1
	fi
}


function checkFiles {
	for val in "${allFilesArray[@]}"; do
		fileName=$pathDataset$val
		if [ -f $fileName ]; then
			echoIndent "$fileName:" "exist"
			filesArray[${#filesArray[@]}]=$val
		else
			echoIndent "$fileName:" "does not exist"
		fi
	done
}


function checkDirectory {
	if ! [ -f $pathComp ]; then
		mkdir $pathComp &> /dev/null
	fi
	if ! [ -f $pathDecomp ]; then
		mkdir $pathDecomp &> /dev/null
	fi
}


function info {
	for val in "${filesArray[@]}"; do
		echo "> $val"
		
		fileName=$pathDataset$val
		
		if [ $flagEnt -eq 1 ]; then
			temp=$(ent $fileName | head -n 1 | cut -b 11-15)
			echoIndent "ENTROPY:" "$(zeroFloat $temp)$temp bits per byte"
		else
			echoIndent "ENTROPY:" "ignored"
		fi
		
		fileSizeNonComp=$(stat -c%s "$fileName")
		temp=$(echo "scale=3; $fileSizeNonComp / 1024" | bc)
		echoIndent "SIZE:" "$(zeroFloat $temp)$temp KB"
		
		echo ""
	done
	echo ""
}


function averageTimeComp {
	fileName=$2
	fileNameComp=$3
	sumDuration=0.0
	
	for val in $(seq 1 $numTest); do
	
		deleteFile $fileNameComp
		
		start=`date +%s.%3N`
		if [ "$1" = "rzip" ]; then
		   rzip -9 -P -k -o $fileNameComp $fileName &> /dev/null
		elif [ "$1" = "bzip2" ]; then
		   bzip2 -z -k -9 $fileName -c > $fileNameComp
		elif [ "$1" = "gzip" ]; then
		   gzip -c -k -9 $fileName > $fileNameComp
		else	# lzma
		   lzma -z -k -9 $fileName -c > $fileNameComp
		fi
		end=`date +%s.%3N`
		duration=$( echo "$end - $start" | bc -l )
		sumDuration=$( echo "$sumDuration + $duration" | bc -l )
	done
	
	globalDuration=$(echo "scale=3; $sumDuration / $numTest" | bc)
}


function averageTimeDecomp {
	fileNameComp=$2
	fileNameDecomp=$3
	sumDuration=0.0
	
	for val in $(seq 1 $numTest); do
	
		deleteFile $fileNameDecomp
		
		start=`date +%s.%3N`
		if [ "$1" = "rzip" ]; then
		   rzip -d -P -k -o $fileNameDecomp $fileNameComp &> /dev/null
		elif [ "$1" = "bzip2" ]; then
		   bzip2 -d -k -9 $fileNameComp -c > $fileNameDecomp
		elif [ "$1" = "gzip" ]; then
		   gzip -c -k -9 -d $fileNameComp > $fileNameDecomp
		else	# lzma
		   lzma -d -k -9 $fileNameComp -c > $fileNameDecomp
		fi
		end=`date +%s.%3N`
		duration=$( echo "$end - $start" | bc -l )
		sumDuration=$( echo "$sumDuration + $duration" | bc -l )
	done
	
	globalDuration=$(echo "scale=3; $sumDuration / $numTest" | bc)
}


function comp {
	for val in "${filesArray[@]}"; do
		echo "> $val"
		
		if [ "$1" = "rzip" ]; then
		   extension=.rz
		elif [ "$1" = "bzip2" ]; then
		   extension=.bz2
		elif [ "$1" = "gzip" ]; then
		   extension=.gz
		else	# lzma
		   extension=.lzma
		fi
		
		fileName=$pathDataset$val
		fileNameComp=$pathComp$val$extension
		fileNameDecomp=$pathDecomp$val$extension.txt
		
		averageTimeComp "$1" "$fileName" "$fileNameComp"
		duration=$globalDuration
		
		fileSizeComp=$(stat -c%s "$fileNameComp")
		temp=$(echo "scale=3; $fileSizeComp / 1024" | bc)
		echoIndent "COMP. SIZE:" "$(zeroFloat $temp)$temp KB"
		
		fileSizeNonComp=$(stat -c%s "$fileName")
		temp=$(echo "scale=3; $fileSizeNonComp / $fileSizeComp" | bc)
		echoIndent "RATIO:" "$(zeroFloat $temp)$temp"
		
		echoIndent "COMP. TIME (AVG):" "$(zeroFloat $duration)$duration sec"
		
		averageTimeDecomp "$1" "$fileNameComp" "$fileNameDecomp"
		duration=$globalDuration
		echoIndent "DECOMP. TIME (AVG):" "$(zeroFloat $duration)$duration sec"
		
		echo ""
	done
	echo ""
}


function checking {
	echo "### CHECKING... ###"
	echo ""
	isPackageNotInstalled ent
	dpkg --status ent &> /dev/null
	if ! [ $? -eq 0 ]; then
		echoIndent "ent:" "ignored"
	else
		flagEnt=1
	fi
	for val in "${allPackageArray[@]}"; do
		isPackageNotInstalled $val
		checkPackage $val
	done
	echo ""
	checkDirectory
	checkFiles
}


function compressing {
	echo "### COMPRESSING AND DECOMPRESSING... ###"
	echo ""
	
	echo ">>> INFO <<<"
	echo ""
	info
	echo ""
	
	for val in "${packageArray[@]}"; do
		if [ "$val" = "rzip" ]; then
		   echo ">>> rzip (Linux Library: rzip / .rz)"
		elif [ "$val" = "bzip2" ]; then
		   echo ">>> bzip2 (Linux Library: bzip2 / .bz2)"
		elif [ "$val" = "gzip" ]; then
		   echo ">>> Deflate (Linux Library: gzip / .gz)"
		elif [ "$val" = "lzma" ]; then
		   echo ">>> LZMA (Linux Library: lzma / .lzma)"
		else
		   echoIndent "$val:" "unknown"
		   abortar
		fi
		echo ""
		comp $val
		echo ""
	done
}


function main {
	checking
	
	echo ""
	echo ""
	echo ""
	
	compressing
}



# RUN
main | tee STDOUT.txt



