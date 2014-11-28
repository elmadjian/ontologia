#!/usr/bin/env python
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
#=================================================================
def main(argv):
    #lê arquivo de entrada .ris
    reader = Reader(argv)
    filename = reader.getFilename()

    with open(filename, 'r') as data:
        for line in data:
            runPattern(line)


#interpreta padrão com expressões regulares
#=================================================================
def runPattern(line):
    #padrões de busca regex
    patterns = [

    #padrões para o arquivo .ris de publicações
    "(PY)\s*-\s*([\d]{4})", #ano de publicação
    "(AU)\s*-\s*(.+)",      #autor
    "(TI)\s*-\s*(.+)",      #título
    "(JO)\s*-\s*(.+)",      #revista

    #padrões para o arquivo .ris de currículo Lattes
    "(NOME)\s*-\s*(.+)",    #nome completo
    "(CITA)\s*-\s*(.+)",    #nome para citação (muitas ocorrências!)
    "(FO)\d+d\s*-\s*(.+)"   #local onde estudou
    ]

    #dicionário para busca
    hashmap = {
    'PY':   "anoPublicacao",
    'AU':   "autor",
    'TI':   "titulo",
    'JO':   "revista",
    'NOME': "nome",
    'CITA': "citacao",
    'FO':   "localDeEstudo"
    }

    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            print (hashmap[match.group(1)],"-->",match.group(2))





#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#classe READER:
#>>> classe responsável por fazer a leitura do arquivo de entrada
#==================================================================
#define a classe de leitura do arquivo problema.dat
class Reader:

#>>> construtor
#__init__(tuple) -> self
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
    #getFilename() -> self.filename
    #==============================================================
    def getFilename(self):
        return self.filename


#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#classe MAKER:
#>>> classe responsável por construir uma saída OWL
#==================================================================
class Maker:
    

#=========================#
if __name__ == "__main__":
    main(sys.argv)
