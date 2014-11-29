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

    #extrai o nome do objeto Professor
    autor = filename[:-4]

    #faz o parsing do arquivo .ris
    lista = list()
    index = [0];
    with open(filename, 'r') as data:
        for line in data:
            runPattern(line, lista, index)

    #converte os dados para OWL
    entradas = ""
    for hashmap in lista:
        #print(hashmap.items(),"\n")
        interpreter = Interpreter(hashmap, autor)
        entradas += interpreter.createIndividual()

    #salva os dados em OWL num arquivo de saída
    writer = Writer()
    writer.writeFile(entradas)


#interpreta padrão com expressões regulares
#=================================================================
def runPattern(line, lista, index):
    #padrões de busca regex
    patterns = [

    #padrões para o arquivo .ris de publicações
    "(TY)\s*-\s*(.+)",      #tipo
    "(PY)\s*-\s*([\d]{4})", #ano de publicação
    "(AU)\s*-\s*(.+)",      #autor
    "(T1)\s*-\s*(.+)",      #título do artigo em conferência
    "(TI)\s*-\s*(.+)",      #título do artigo em revista / conferência
    "(JO)\s*-\s*(.+)",      #revista

    #padrões para o arquivo .ris de currículo
    "(NOME)\s*-\s*(.+)",    #nome completo
    "(CITA)\s*-\s*(.+)",    #nome para citação (muitas ocorrências!)
    "(FO)\d+d\s*-\s*(.+)"   #local onde estudou
    ]
    i = index[0]-1

    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            if match.group(1) == 'TY':
                hashmap = {'TY': match.group(2)}
                lista.insert(index[0], hashmap)
                index[0] += 1
            elif match.group(1) == 'CITA':
                cita = match.group(2).split(';')
                lista[i]['CITA'] = cita
            elif match.group(1) == 'AU':
                authors = match.group(2).split(';')
                lista[i]['AU'] = authors
            elif match.group(1) == 'JO':
                lista[i]['JO'] = re.sub(",.*", "", match.group(2))
            else:
                lista[i][match.group(1)] = match.group(2)




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
class Writer:

    #>>> construtor
    #__init__([filename]) -> self
    #===============================================================
    def __init__(self, filename = "saida.owl"):
        self.filename = filename

    #>>> cria um arquivo 'saida.owl'
    #writeFile(string) -> None
    #===============================================================
    def writeFile(self, text):
        data = open(self.filename, 'w')
        data.write(text)
        data.close()



#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#classe Interpreter:
#>>>
#===================================================================
class Interpreter:

    #>>> construtor
    #recebe um dicionário com dados gerados pelo scriptlattes
    #__init__(dict, [string]) -> None
    #===============================================================
    def __init__(self, hashmap, autor = None):
        self.hashmap  = hashmap
        self.ontoName = "&renata;FOAF-modified#"
        self.autor    = autor

    #>>> coloca 'underline' em strings com espaços
    #putUnderline(string) -> string
    #================================================================
    def putUnderline(self, text):
        modified_text = re.sub("\s+", "_", text)
        return modified_text

    #>>> cria um indivíduo
    #createIndividual() -> string
    #================================================================
    def createIndividual(self):
        if self.hashmap['TY'] == 'MEMBRO':
            return self._createProfessor()
        elif self.hashmap['TY'] == 'JOUR':
            return self._createJournal()
        elif self.hashmap['TY'] == 'CONF':
            return self._createConferece()
        else:
            return ""


    #>>> cria um indivíduo do tipo Professor
    #_createProfessor() -> string
    #=================================================================
    def _createProfessor(self):
        nome = self.putUnderline(self.hashmap['NOME'])
        self.autor = nome
        individuo = "<owl:NamedIndividual rdf:about=\"{0}{1}\">\n".format(self.ontoName, nome)
        individuo += "\t<rdf:type rdf:resource=\"{0}Professor\"/>\n".format(self.ontoName)
        for citacao in self.hashmap['CITA']:
            individuo += "\t<nomeCitacao>"+citacao+"</nomeCitacao>\n"
        individuo += "\t<renata:firstName>"+re.sub("\s.*$", "", self.hashmap['NOME'])+"</renata:firstName>\n"
        individuo += "\t<renata:familyName>"+re.sub("^.*? ", "", self.hashmap['NOME'])+"</renata:familyName>\n"
        individuo += "\t<renata:name>"+self.hashmap['NOME']+"</renata:name>\n"
        individuo += "\t<afiliado rdf:resource="+self.ontoName+"Departamento_de_Ciência_Da_Computação/>\n"
        individuo += "</owl:NamedIndividual>\n"
        return individuo

    #>>> cria um indivíduo do tipo ArtigoEmRevista
    #_createPublication() -> string
    #=================================================================
    def _createJournal(self):
        #criando o artigo em revista
        artigo  = self.putUnderline(self.hashmap['TI'])
        revista = self.putUnderline(self.hashmap['JO'])
        individuo = "<owl:NamedIndividual rdf:about=\""+self.ontoName + artigo+"\">\n"
        individuo += "\t<rdf:type rdf:resource=\""+self.ontoName+"ArtigoEmRevista\"/>\n"
        for autor in self.hashmap['AU']:
            individuo += "\t<autor>"+autor.strip()+"</autor>\n"
        individuo += "\t<titulo>"+self.hashmap['TI']+"</titulo>\n"
        individuo += "\t<anoPublicacao>"+self.hashmap['PY']+"</anoPublicacao>\n"
        individuo += "\t<temAutor rdf:resource=\""+self.ontoName + self.autor+"\"/>\n"
        individuo += "\t<publicadoEm rdf:resource=\""+self.ontoName + revista+"\"/>\n"
        individuo += "</owl:NamedIndividual>\n\n"

        #criando a revista
        individuo += "<owl:NamedIndividual rdf:about=\""+self.ontoName + revista+"\">\n"
        individuo += "\t<rdf:type rdf:resource=\""+self.ontoName+"Revista\"/>\n"
        individuo += "\t<titulo>"+self.hashmap['JO']+"</titulo>\n"
        individuo += "</owl:NamedIndividual>\n"
        return individuo

    #>>> cria um indivíduo do tipo ArtigoEmConferencia
    #_createConferece() -> string
    #=================================================================
    def _createConferece(self):
        #criando o artigo em conferência
        artigo = self.putUnderline(self.hashmap['T1'])
        conf   = self.putUnderline(self.hashmap['TI'])
        individuo = "<owl:NamedIndividual rdf:about=\""+self.ontoName + artigo+"\">\n"
        individuo += "\t<rdf:type rdf:resource=\""+self.ontoName+"ArtigoEmConferencia\"/>\n"
        for autor in self.hashmap['AU']:
            individuo += "\t<autor>"+autor.strip()+"</autor>\n"
        individuo += "\t<titulo>"+self.hashmap['T1']+"</titulo>\n"
        individuo += "\t<anoPublicacao>"+self.hashmap['PY']+"</anoPublicacao>\n"
        individuo += "\t<temAutor rdf:resource=\""+self.ontoName + self.autor+"\"/>\n"
        individuo += "\t<publicadoEm rdf:resource=\""+self.ontoName + conf+"\"/>\n"
        individuo += "</owl:NamedIndividual>\n\n"

        #criando a conferência
        individuo += "<owl:NamedIndividual rdf:about=\""+self.ontoName + conf+"\">\n"
        individuo += "\t<rdf:type rdf:resource=\""+self.ontoName+"Conferencia\"/>\n"
        individuo += "\t<titulo>"+self.hashmap['TI']+"</titulo>\n"
        individuo += "</owl:NamedIndividual>\n"
        return individuo


#=========================#
if __name__ == "__main__":
    main(sys.argv)
