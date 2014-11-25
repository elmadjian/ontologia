!#/usr/bin/python
# -*- coding: utf-8 -*-

'''================================================================
   ARQUIVO: script.py
   CONTEÚDO: conversor de dados .ris em .owl
   OBJETIVO: popular a ontologia com publicações e dados de
             indivíduos
   ================================================================'''

import os.path
import sys
import re

#programa principal
def main(argv):

    #lê arquivo de entrada .ris
    reader = Reader(argv)
    filename = reader.getFilename

    with open(filename, 'r') as data:


#interpreta padrão com expressões regulares
def runPattern(line):
    patterns


#=========================#
if __name__ == "__main__":
    main(sys.argv)


#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#classe READER:
#>>> classe responsável por fazer a leitura do arquivo de entrada
#==================================================================
#define a classe de leitura do arquivo problema.dat
class Reader:

#__init__(tuple) -> self
#>>> construtor
#=============================================================
def __init__(self, argv):
    #se houver mais de um nome como parâmetro do programa: ERRO
    if len(argv) > 2:
        print("ERRO: você chamou %s com mais de um parâmetro" % argv[0])
        exit()
    #se houver um parâmetro: salva o nome em self.filename
    elif len(argv) == 2:
        self.filename = argv[1]
    #se não houver parâmetro, pede que o usuário digite o nome do arquivo
    else:
        self.filename = input("Por favor, digite o nome do arquivo para leitura:")

    #se o arquivo não existir: ERRO
    if not os.path.isfile(self.filename):
        print("ERRO: arquivo %s inexistente" % self.fileName)
        exit()

#>>> devolve o nome do arquivo lido
#==============================================================
def getFilename(self):
    return self.filename
