from abc import abstractmethod
from os import SEEK_CUR, supports_effective_ids
from typing import ChainMap, Hashable

tabelaSimbolo={
    "+":"op_ad",
    "-":"op_ad",
    "*":"op_mul",
    "/":"op_mul",
    ":=":"ATRIBUIÇÃO",
    "=":"relacao",
    "<>":"relacao",
    ">":"relacao",
    ">=":"relacao",
    "<":"relacao",
    "<=":"relacao",
    "if":"if",
    "then":"then",
    "else":"else",
    "write":"write",
    "read":"read",
    "id":"ident",
    "int":"numero_int",
    "float":"numero_real",
    "integer":"tipo_var",
    "real":"tipo_var",
    "program":"program",
    "(":"(",
    ")":")",
    "{":"{",
    "}":"}",
    "begin":"begin",
    "end":"end",
    ",":",",
    ":":":",
    "$":"$",
    ";":";"
}

def getSimbolo(word_):
    valor = tabelaSimbolo.get(word_,None)
    if valor is None:
        raise Exception('Operador inválido, linha: ' + str(ScannerLexema.LINHA))
    return valor

class HashTable_:
    DefOpeAritmeticos = ["+","-","*","/"]
    defOperadores = ["=","<>",">",">=","<","<=",":="]
    defSimbolos = ["{","}","(",")",",","$",";",":"]
    defKeywords = ["while","for","if","then","else","write","read","integer","real","program","begin","end"]
    def getKeywordsValidos(word_):
        if word_ in HashTable_.defKeywords:
            return getSimbolo(word_)
        else:
            return getSimbolo("id")
    def getOperadoresValidos(word_):
        if word_ in HashTable_.defOperadores:
            return getSimbolo(word_)
        elif word_ in HashTable_.DefOpeAritmeticos:
            return getSimbolo(word_)
        elif word_ in HashTable_.defSimbolos:
            return getSimbolo(word_)
        else:
             raise Exception('Operador inválido, linha: ' + str(ScannerLexema.LINHA))

        
class Token:
    INIT = 0
    IDENTIFICADOR = 1
    INTEIRO = 2
    FLOAT = 3
    ESPACO = 4
    OPERADORESARITMETICOS = 5 #{"+":5,"-":6,"*":7,"/":8}
    OPERADORES = 6 #{"=":9,"!=":10,">":11,">=":12,"<":13,"<=":14}
    KEYWORDS = 7 #{"while":15,"for":16,"if":17}

    def getOperdor(self,char_):
        return self.OPERADORESARITMETICOS.get(char_)
    
    def getOperdor(self,char_):
        return self.OPERADORES.get(char_)
    
    def getKeywords(self,char_):
        return self.KEYWORDS.get(char_)

    def __init__(self, tipo,termo):
        self.tipo = tipo
        self.termo = termo
    def __str__(self):
        return "Token{"+ str(self.tipo) +"," + str(self.termo) + "}"
    def pretty(token):
        pass

class ScannerLexema:
    LINHA = 1
    def __str__(self):
        return ''.join(self.conteudo)

    def __init__(self, path):
        self.conteudo=[]
        self.estado = 0
        self.pos= 0
        try:
            file = open(path,'r')
            self.conteudo = [line for line in file.read()]
        except:
            print('erro ao ler arquivo')
    
    def isletra(self,char_):
        return (char_ >= 'a' and char_ <= 'z') or (char_ >= 'A' and char_ <='Z' )
    
    def isSimbolo(self,char_):
        return char_ in ["+","-","*","/","<",">","=","{","}","(",")",",","$",";",":"]
    
    def isoperador(self,char_):
        return char_ in ["+","-","*","/","<",">","=","{","}","(",")"]

    def isdigito(self,char_):
        return (char_ >= '0' and char_ <= '9')
    
    def isEspaco(self,char_):
        if (char_ == '\n'):
            self.LINHA +=1
        return (char_ == ' ' or char_ == '\n' or char_ == '\t')

    def isEof(self):
        return self.pos >= len(self.conteudo)

    def nextChar(self):
        if (self.isEof()):
            return "$$"
        else:
            self.pos +=1
            return self.conteudo[self.pos-1]
    
    #def back(self,char_=None):
    #    if (char_ != '$$'):
    #        self.pos -=1
    def back(self,char_=None):
            self.pos -=1

    def NextToken(self):
        if self.isEof():
            return None
        self.estado = 0
        termo = ''
        while 1:
            if self.isEof():
                self.pos = len(self.conteudo)+1
            char_ = self.nextChar()
            # estado 0, verifica se é letra, digito ou espaço em branco
            if self.estado == 0:
                if (self.isletra(char_)):
                    termo +=char_
                    self.estado = 1
                elif (self.isdigito(char_)):
                    termo += char_
                    self.estado = 3
                elif (self.isSimbolo(char_)):
                    termo += char_
                    self.estado = 7
                elif (self.isEspaco(char_)):
                    self.estado = 0
                elif (char_ == "$$"):
                    break
                else:
                    raise Exception('Token não reconhecido:' + str(self.LINHA))
                continue
            # estado 1, enquanto for letra, continuar lendo
            if self.estado == 1:
                if (self.isletra(char_) or self.isdigito(char_)):
                    termo +=char_
                    self.estado = 1
                    continue
                else:
                    self.estado = 2
            # estado 2, retorna IDENTIFICADOR
            if self.estado == 2:
                self.back(char_)
                return Token(HashTable_.getKeywordsValidos(termo),termo)
            # estado 3, enquanto for digito continuar lendo
            if self.estado == 3:
                if (self.isdigito(char_)):
                    termo +=char_
                    self.estado = 3
                    continue
                elif (char_ == '.'):
                    self.estado = 4
                    continue
                elif (not(self.isletra(char_))):
                    self.estado = 6
                else:
                    raise Exception('Número não reconhecido Linha: ' + str(self.LINHA))
            if self.estado == 4:
                if (self.isdigito(char_)):
                    termo +=char_
                    self.estado = 4
                    continue
                elif (not(self.isletra(char_))):
                    self.estado = 5
                else:
                    raise Exception('Número não reconhecido Linha: ' + str(self.LINHA))
            # estado 5, retorna REAL
            if self.estado == 5:
                self.back(char_)
                return Token(getSimbolo("float"),termo)
            # estado 6, retorna INTEIRO
            if self.estado == 6:
                self.back(char_)
                return Token(getSimbolo("int"),termo)
            if (self.estado == 7):
                #if (termo in ['<','>',":"] and char_ in ["<",">","="]):
                #    self.estado = 9
                #    termo += char_
                #else:
                    self.back(char_)
                    self.estado = 8
            if (self.estado == 8):
                if termo  in tabelaSimbolo.keys():
                    return Token(HashTable_.getOperadoresValidos(termo),termo)
                else:
                    raise Exception('Simbolo não reconhecido:' + str(self.LINHA))
 

"""scans = ScannerLexema(r'D:\nando docs\nando_documentos\faculdade\compiladores\Compilador_EXEC\entradas.txt')

#print(scans.conteudo)
token = Token(Token.INIT,"")

while not(token is None):
    token = scans.NextToken()
    if isinstance(token,Token):
        print(token)"""


