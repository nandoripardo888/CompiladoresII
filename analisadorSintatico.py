from ntpath import join
from os import scandir
from analisadorLexico import *


class tabelaHsh():
  #$tabelaSimbolo = []
  #[termo,tipo,valor]
    def __init__(self):
        self.tabelaSimbolo = []

    def emTabela(self,termo):    
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return True
        return False

    def simboloEncontrado(self,termo,linha):
        if not(self.emTabela(termo)):
            raise ValueError('Erro semantico, o identificador "'+ termo +'" não foi declado LINHA:' + str(linha))
        else:
            pass
    
    # 5 valores -> termo|token|valor|usado|tipo <-#
    def inserir(self,token,termo,tipo,linha):
        if not(self.emTabela(termo)):
            self.tabelaSimbolo.append([termo,token,"","",tipo])
        else:
            raise Exception('Erro semantico, já foi declarado uma variável com este mesmo nome "'+ termo +'" --> LINHA:' + str(linha))

    def addValor(self,termo,valor):
        self.simboloEncontrado(termo,0)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                elemento[2] = valor

    def getTipo(self,termo,linha):
        self.simboloEncontrado(termo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return elemento[4]

    def setVarUtilizada(self,termo,linha):
        self.simboloEncontrado(termo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                elemento[3] = 'used'
                


    
def escreverDocumento(path,lista,listaVar):
    with open(path, 'w') as f:
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("\t\t\t\tVARIAVEIS\n")
        f.write("#"*40 + "\n")
        f.write("%s\n" % " | ".join(["termo","token","valor","usado","tipo"]))
        for item in listaVar:
            #f.write("%s\n" % item)
            f.write("%s\n" % '|'.join(item))
        f.close
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("\t\t\t\FUNCTIONS\n")
        f.write("%s\n" % " | ".join(["termo","token","valor","usado","tipo"]))
        for item in lista:
            f.write("%s\n" % item)
        f.close

class AnalisadorSintatico:
    simbolo =""
    LINHA = 1
    arquivo = ""
    memoria={"termo":"","token":"","valor":"","usado":"",'tipo':""}
    

    def __init__(self,path):
        self.scan = ScannerLexema(path)
        self.path = path
        self.tabelaHASH = tabelaHsh()
        self.tokens_saida = []

    def obtemSimbolo(self):
        self.token = self.scan.NextToken()
        self.simbolo = None
        if self.token != None:
             self.simbolo = self.token
    
    def analise(self):
        self.obtemSimbolo()
        self.programa()
        if self.simbolo is None:
            self.tokens_saida.append("TUDO CERTO")
            print("tudo Certo")
            #escreverDocumento(self.path + "_saida.txt",self.tokens_saida,self.tabelaHASH.tabelaSimbolo)
        else:
            raise Exception('Erro sintatico, esperado fim de cadeia LINHA:' + str(self.scan.LINHA))

    def programa(self):
        self.tokens_saida.append("<programa>")
        print("<programa>")
        if self.simbolo.termo == "program":
            self.obtemSimbolo()
            if self.simbolo.tipo == "ident":
                self.obtemSimbolo()
                self.corpo()
            else:
                raise Exception('Erro sintatico, esperado ident LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado program LINHA:' + str(self.scan.LINHA))
    
    def corpo(self):
        self.tokens_saida.append("<corpo>")
        print("<corpo>")
        self.dc()
        if self.simbolo.termo == "begin":
            self.obtemSimbolo()
            self.comandos()
            if self.simbolo.termo == "end":
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado "end" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "begin" LINHA:' + str(self.scan.LINHA))
    
    def dc(self):
        self.tokens_saida.append("<dc>")
        print("<dc>")
        if self.simbolo.tipo == "tipo_var":
            self.dcV()
            self.maisDc()
        else :
            pass
    
    def maisDc(self):
        self.tokens_saida.append("<maisDc>")
        print("<maisDc>")
        if self.simbolo.tipo == ";":
            self.obtemSimbolo()
            self.dc()
        else:
            pass


    def dcV(self):
        self.tokens_saida.append("<dcV>")
        print("<dcV>")
        if self.simbolo.tipo == "tipo_var":
            self.memoria["tipo"] = self.simbolo.termo
            self.obtemSimbolo()
            if self.simbolo.termo == ":":
                self.obtemSimbolo()
                self.variaveis()
                self.obtemSimbolo
            else:
                raise Exception('Erro sintatico, esperado ":" LINHA:' + str(self.scan.LINHA))
        else :
            pass

    def comandos(self):
        self.tokens_saida.append("<comandos>")
        print("<comandos>")
        self.comando()
        self.maisComandos()
    
    def maisComandos(self):
        self.tokens_saida.append("<maisComandos>")
        print("<maisComandos>")
        if self.simbolo.termo == ";":
            self.obtemSimbolo()
            self.comandos()
        else:
            pass

    def parIdent(self):
        self.tokens_saida.append("<parIdent>")
        print("<parIdent>")
        if self.simbolo.termo == "(":
            self.obtemSimbolo()
            if self.simbolo.tipo == "ident":
                self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
                self.obtemSimbolo()
                if self.simbolo.termo == ")":
                    self.obtemSimbolo()
                else:
                    raise Exception('Erro sintatico, esperado ")" LINHA:' + str(self.scan.LINHA))
            else:
                raise Exception('Erro sintatico, esperado "ident" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "(" LINHA:' + str(self.scan.LINHA))

    def atribuirVal(self):
        self.tokens_saida.append("<atribuirVal>")
        print("<atribuirVal>")
        if self.simbolo.termo == ":":
            self.obtemSimbolo()
            if self.simbolo.termo == "=":
                    self.obtemSimbolo()
                    self.expressao()
            else:
                raise Exception('Erro sintatico, esperado "=" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado ":" LINHA:' + str(self.scan.LINHA))

    def condicional(self):
        self.tokens_saida.append("<condicional>")
        print("<condicional>")
        self.condicao()
        if self.simbolo.termo == "then":
            self.obtemSimbolo()
            self.comandos()
            self.pFalsa()
            if self.simbolo.termo == "$":
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado "$" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "then" LINHA:' + str(self.scan.LINHA))

    def pFalsa(self):
        self.tokens_saida.append("<pFalsa>")
        print("<pFalsa>")
        if self.simbolo.termo == "else":
            self.obtemSimbolo()
            self.comandos()
        else:
            pass

    def condicao(self):
        self.tokens_saida.append("<condicao>")
        print("<condicao>")
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        self.tokens_saida.append("<relacao>")
        print("<relacao>")
        if self.simbolo.termo == "=":
            self.obtemSimbolo()
        elif self.simbolo.termo == "<":
            self.obtemSimbolo()
            if self.simbolo.termo == ">":
                self.obtemSimbolo()
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
            else:
                pass
        elif self.simbolo.termo == ">":
            self.obtemSimbolo()
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
            else:
                pass
        else:
            raise Exception('Erro sintatico, esperado "operador" LINHA:' + str(self.scan.LINHA))


    def expressao(self):
        self.tokens_saida.append("<expressao>")
        print("<expressao>")
        self.termo()
        self.outrosTermos()

    def termo(self):
        self.tokens_saida.append("<termo>")
        print("<termo>")
        self.opUn()
        self.fator()
        self.maisFatores()

    def opUn(self):
        self.tokens_saida.append("<opUn>")
        print("<opUn>")
        if self.simbolo.termo == "-":
            self.obtemSimbolo()
        else:
            pass
    
    def outrosTermos(self):
        self.tokens_saida.append("<outrosTermos>")
        print("<outrosTermos>")
        if self.simbolo.termo == "+" or self.simbolo.termo == "-":
            self.opAd()
            self.fator()
            self.maisFatores()
        else:
            pass

    def opAd(self):
        self.tokens_saida.append("<opAd>")
        print("<opAd>")
        if self.simbolo.termo == "+":
            self.obtemSimbolo()
        elif self.simbolo.termo == "-":
            self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperador "+" ou operador "-" LINHA:' + str(self.scan.LINHA))

    def opMul(self):
        self.tokens_saida.append("<opMul>")
        print("<opMul>")
        if self.simbolo.termo == "*":
            self.obtemSimbolo()
        elif self.simbolo.termo == "/":
            self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperador "+" ou operador "-" LINHA:' + str(self.scan.LINHA))

    def maisFatores(self):
        self.tokens_saida.append("<maisFatores>")
        print("<maisFatores>")
        if self.simbolo.termo == "*":
            self.opMul()
            self.fator()
            self.maisFatores()
        else:
            pass
    
    def fator(self):
        self.tokens_saida.append("<fator>")
        print("<fator>")
        if self.simbolo.tipo == "ident":
            self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
            self.obtemSimbolo()
        elif self.simbolo.tipo == "numero_int":
            self.obtemSimbolo()
        elif self.simbolo.tipo == "numero_real":
            self.obtemSimbolo()
        elif self.simbolo.termo == "(":
            self.obtemSimbolo()
            self.expressao()
            if self.simbolo.termo == ")":
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado ")" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "expressao" LINHA:' + str(self.scan.LINHA))
                
        

    def comando(self):
        self.tokens_saida.append("<comando>")
        print("<comando>")
        if self.simbolo.termo == "read":
            self.obtemSimbolo()
            self.parIdent()
        elif self.simbolo.termo == "write":
            self.obtemSimbolo()
            self.parIdent()
        elif self.simbolo.tipo == "ident":
            self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
            self.memoria['tipo']=self.tabelaHASH.getTipo(self.simbolo.termo,self.scan.LINHA)
            self.obtemSimbolo()
            self.atribuirVal()
        elif self.simbolo.tipo == "if":
            self.obtemSimbolo()
            self.condicional()
        else:
            raise Exception('Erro sintatico, esperado "comando" LINHA:' + str(self.scan.LINHA))   

    
    def variaveis(self):
        self.tokens_saida.append("<variaveis>")
        print("<variaveis>")
        if self.simbolo.tipo == "ident":
            self.tabelaHASH.inserir(self.simbolo.tipo,self.simbolo.termo,self.memoria["tipo"],self.scan.LINHA)#regra semantica para identificar unicidade do identificador
            self.obtemSimbolo()
            self.maisVar()
        else:
            raise Exception('Erro sintatico, esperado "ident" LINHA:' + str(self.scan.LINHA))
    
    def maisVar(self):
        self.tokens_saida.append("<maisVar>")
        print("<maisVar>")
        if self.simbolo.tipo == ",":
             self.obtemSimbolo()
             self.variaveis()
        else:
            pass
    

"""sintatico = AnalisadorSintatico(r'entradas.txt')
sintatico.analise()
print(sintatico.tabelaHASH.tabelaSimbolo)"""