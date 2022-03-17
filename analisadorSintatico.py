from inspect import stack
from ntpath import join
from os import scandir
from xmlrpc.client import boolean
from analisadorLexico import *
from CStack import Stack


class tabelaHsh():
  #$tabelaSimbolo = []
  #[termo,tipo,valor]
    def __init__(self):
        self.tabelaSimbolo = []
        self.enderecoRelativo = 0

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
    
    # 5 valores -> termo|token|valor|usado|tipo|EnderecoRelativo <-#
    def inserir(self,token,termo,tipo,linha):
        if not(self.emTabela(termo)):
            self.tabelaSimbolo.append([termo,token,"","",tipo,self.enderecoRelativo])
            self.enderecoRelativo+=1
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
    
    def getEnderecoRelativo(self,termo,linha):
        self.simboloEncontrado(termo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return elemento[5]

    def setVarUtilizada(self,termo,linha):
        self.simboloEncontrado(termo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                elemento[3] = 'used'
                
    


    
def escreverDocumento(path,lista,listaVar):
    with open(path, 'w') as f:
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("\t\t\t\tVARIAVEIS\n")
        f.write("%s\n" % " | ".join(map(str,["termo","token","valor","usado","tipo","EnderecoRelativo"])))
        f.write("#"*40 + "\n")
        for item in listaVar:
            #f.write("%s\n" % item)
            f.write("%s\n" % '|'.join(map(str,item)))
        f.close
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("#"*40 + "\n" + "#"*40 + "\n")
        f.write("\t\t\t\FUNCTIONS\n")
        f.write("%s\n" % " | ".join(map(str,["termo","token","valor","usado","tipo","EnderecoRelativo"])))
        for item in lista:
            f.write("%s\n" % item)
        f.close

class AnalisadorSintatico:
    simbolo =""
    LINHA = 1
    arquivo = ""
    memoria={"termo":"","token":"","valor":"","usado":"",'tipo':""}
    
    # FUNÇÕES DE GERAÇÃO DE CODIGO
    def gerarCodigoDeOperacaoVariavel(self, termo):
        #se ControleOperacaoVariavel
        # 1 - está declarando variavel
        # 2 - está imprimindo variavel(WRITE)
        # default - está escrevendo variavel(READ)
        if self.ControleOperacaoVariavel == 1 :
            self.stackCodigoGerado.push(['ALME', 1]) #cod declarar variável
        elif self.ControleOperacaoVariavel == 2 :
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(termo,self.scan.LINHA)])
        else:
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(termo,self.scan.LINHA)]) #escreve no endereço relativo


         

    # -----------------------------

    def __init__(self,path):
        self.scan = ScannerLexema(path)
        self.path = path
        self.tabelaHASH = tabelaHsh()
        self.tokens_saida = []
        self.stackCodigoGerado = Stack()
        #VARIAVEIS DE CONTROLE
        self.ControleOperacaoVariavel = 1 # controla <variveis> ao usar a função gerarCodigoDeOperacaoVariavel

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
            self.stackCodigoGerado.push(['INPP', '']) #cod inicia programa
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
                self.stackCodigoGerado.push(['PARA', 0]) #cod parar o programa
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

    def parIdent(self, tipoOperacao):
        #se tipoOperacao
        # 1 - está imprimindo variavel(WRITE)
        # 2 - está escrevendo variavel(READ)
        self.tokens_saida.append("<parIdent>")
        print("<parIdent>")
        if self.simbolo.termo == "(":
            self.obtemSimbolo()
            if self.simbolo.tipo == "ident":
                self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
                #cod faz imprime ou READ ou WRITE
                if tipoOperacao == 1 :
                    self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.scan.LINHA)])
                elif tipoOperacao == 2:
                    self.stackCodigoGerado.push(['ARMZ', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.scan.LINHA)]) #escreve no endereço relativo
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
            posicaoInicioIf = self.stackCodigoGerado.size() #Salva na recursão o index do if na pilha, para futuramente trocar o valor next, para onde ele deve saltar caso seja false
            self.stackCodigoGerado.push(['DSVF', 'NEXT']) #cod entra no comando da condição
            self.obtemSimbolo()
            self.comandos()
            posicaoFimIf = self.stackCodigoGerado.size() #Salva na recursão o index do if na pilha, para futuramente trocar o valor next, para onde ele deve saltar após entrar no if e finalizar os comandos
            self.stackCodigoGerado.push(['DSVS', 'NEXT'])
            self.pFalsa(posicaoInicioIf)
            if self.simbolo.termo == "$":
                self.stackCodigoGerado.items[posicaoFimIf][1] = self.stackCodigoGerado.size()
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado "$" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "then" LINHA:' + str(self.scan.LINHA))

    def pFalsa(self,posicaoInicioIf):
        self.tokens_saida.append("<pFalsa>")
        print("<pFalsa>")
        if self.simbolo.termo == "else":
            self.stackCodigoGerado.items[posicaoInicioIf][1] = self.stackCodigoGerado.size()
            self.obtemSimbolo()
            self.comandos()
        else:
            pass

    def condicao(self):
        self.tokens_saida.append("<condicao>")
        print("<condicao>")
        self.expressao()
        relacao = self.relacao()
        self.expressao()
        self.stackCodigoGerado.push(relacao)

    def relacao(self):
        self.tokens_saida.append("<relacao>")
        print("<relacao>")
        if self.simbolo.termo == "=":
            self.obtemSimbolo()
            return  ['CPIG', '']
        elif self.simbolo.termo == "<":
            self.obtemSimbolo()
            if self.simbolo.termo == ">":
                self.obtemSimbolo()
                return  ['CDES', '']
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
                return  ['CPMI', '']
            else:
                return ['CPME', '']
        elif self.simbolo.termo == ">":
            self.obtemSimbolo()
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
                return  ['CMAI', '']
            else:
                return  ['CPMI', '']
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
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.scan.LINHA)])
            self.obtemSimbolo()
        elif self.simbolo.tipo == "numero_int":
            self.stackCodigoGerado.push(['CRCT', self.simbolo.termo])
            self.obtemSimbolo()
        elif self.simbolo.tipo == "numero_real":
            self.stackCodigoGerado.push(['CRCT', self.simbolo.termo])
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
            self.stackCodigoGerado.push(['LEIT', '']) #cod fazendo leitura
            self.obtemSimbolo()
            self.parIdent(2)
        elif self.simbolo.termo == "write":
            self.obtemSimbolo()
            self.parIdent(1)
        elif self.simbolo.tipo == "ident":
            self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
            self.memoria['tipo']=self.tabelaHASH.getTipo(self.simbolo.termo,self.scan.LINHA)
            simboloMemoria = self.simbolo
            self.obtemSimbolo()
            self.atribuirVal()
            self.stackCodigoGerado.push(['ARMZ', self.tabelaHASH.getEnderecoRelativo(simboloMemoria.termo,self.scan.LINHA)]) #escreve no endereço relativo
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
            self.stackCodigoGerado.push(['ALME', 1]) #cod definir variável
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