from ast import arguments
from inspect import stack
from ntpath import join
from os import scandir
from xmlrpc.client import boolean

from zmq import PUSH
from analisadorLexico import *
from CStack import Stack


class tabelaHsh():
  #$tabelaSimbolo = []
  #[termo,tipo,valor]
    def __init__(self):
        self.tabelaSimbolo = []
        self.enderecoRelativo = 0
        #controla as procedures na tabela de simbolos
        self.escopo = 0
        self.tamanhoPilhaD = 0

    # uso para verificar se existe no escopo
    def emTabelaEscopo(self,termo,escopo):
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                return True
        return False

    #uso para verficiar em qualquer escopo
    def emTabela(self,termo,escopo):    
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                return True
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return True
        return False

    def simboloEncontrado(self,termo,escopo,linha):
        if not(self.emTabela(termo,escopo)):
            raise ValueError('Erro semantico, o identificador "'+ termo +'" não foi declado LINHA:' + str(linha))
        else:
            pass
    
    # 5 valores -> termo|token|valor|usado|tipo|EnderecoRelativo|escopo|enderecoPilhaD|enderecoPilhaC|numeroParametros <-#
    # o parametro enderecoPilhaC é somente para ser passado no caso de função
    def inserir(self,token,termo,tipo,enderecoPilhaC,linha):
        if not(self.emTabelaEscopo(termo,self.escopo)):
            self.tabelaSimbolo.append([termo,token,"-","-",tipo,self.enderecoRelativo,self.escopo,self.tamanhoPilhaD,enderecoPilhaC,0])
            self.enderecoRelativo+=1
            self.tamanhoPilhaD+=1
        else:
            raise Exception('Erro semantico, já foi declarado uma variável com este mesmo nome "'+ termo +'" --> LINHA:' + str(linha))

    def addValor(self,termo,escopo,valor):
        self.simboloEncontrado(termo,escopo,0)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                elemento[2] = valor
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                elemento[2] = valor

    def getTipo(self,termo,escopo,linha):
        self.simboloEncontrado(termo,escopo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                return elemento[4]
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return elemento[4]
    
    def getEnderecoRelativo(self,termo,escopo,linha):
        self.simboloEncontrado(termo,escopo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                return elemento[5]
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                return elemento[5]

    def setVarUtilizada(self,termo,escopo,linha):
        self.simboloEncontrado(termo,escopo,linha)
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo and elemento[6] == escopo:
                elemento[3] = 'used'
        for elemento in self.tabelaSimbolo:
            if elemento[0] == termo:
                elemento[3] = 'used'
    
    def getEnderecoPilha(self,termo,escopo,linha):
         self.simboloEncontrado(termo,escopo,linha)
         for elemento in self.tabelaSimbolo:
             if elemento[0] == termo and elemento[6] == escopo:
                if elemento[4] == 'procedure':
                    return elemento[8]

    def getNumeroParametro(self,termo,escopo,linha):
         self.simboloEncontrado(termo,escopo,linha)
         for elemento in self.tabelaSimbolo:
             if elemento[0] == termo and elemento[6] == escopo:
                if elemento[4] == 'procedure':
                    return elemento[9]

                
    
def escreverDocumentoErro(path,erroGerado):
    with open(path, 'w') as f:
        f.write("#"*40 + "\n")
        f.write("  ALGORITMO\n")
        f.write(erroGerado)
        f.close()

    
def escreverDocumento(path,pilhaCodigo,tabelaSimbolo,resultadoExecucao,arquivoAlgoritmo):

    with open(path, 'w') as f:
        f.write("#"*40 + "\n")
        f.write("  ALGORITMO\n")
        f.write("\n")
        fileAlgoritmo = open(arquivoAlgoritmo,'r')
        f.write(fileAlgoritmo.read())
        fileAlgoritmo.close()
        f.write("\n")
        #*****************************************************************************
        f.write("#"*40 + "\n")
        f.write("  VARIAVEIS\n")
        f.write("\n")
        nomes = ["termo","token","valor","usado","tipo","EndRel","escopo","endPilhaD","endPilhaC","numParam"]
        col_width = max(len(row) for row in nomes)+1
        f.write("|".join(word.ljust(col_width) for word in nomes))
        f.write("\n")
        for item in tabelaSimbolo:
            #f.write("%s\n" % item)
            #f.write("%s\n" % '\t\t\t'.join(map(str,item)))
            f.write("|".join(word.ljust(col_width) for word in map(str,item)))
            f.write("\n")
        #f.close
        f.write("\n")
        #*****************************************************************************
        f.write("#"*40 + "\n")
        f.write("  CODIGO GERADO\n")
        f.write("\n")
        col_width = len(str(len(pilhaCodigo)))+1
        i = 0
        for item in pilhaCodigo:
            lista = [i," ".join(map(str,item))]
            f.write("|".join(word.ljust(col_width) for word in map(str,lista)))
            f.write("\n")
            i+=1
        #f.close
        f.write("\n")
        #*****************************************************************************
        f.write("#"*40 + "\n")
        f.write("  SAIDA\n")
        f.write("\n")
        col_width = len(str(len(resultadoExecucao)))+1
        i = 0
        for item in resultadoExecucao:
            lista = [i,item]
            f.write("|".join(word.ljust(col_width) for word in map(str,lista)))
            f.write("\n")
            i+=1
        f.close()

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
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(termo,self.tabelaHASH.escopo,self.scan.LINHA)])
        else:
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(termo,self.tabelaHASH.escopo,self.scan.LINHA)]) #escreve no endereço relativo


         

    # -----------------------------

    def __init__(self,path):
        self.scan = ScannerLexema(path)
        self.path = path
        self.tabelaHASH = tabelaHsh()
        self.tokens_saida = []
        self.stackCodigoGerado = Stack()
        #VARIAVEIS DE CONTROLE
        self.ControleOperacaoVariavel = 1 # controla <variveis> ao usar a função gerarCodigoDeOperacaoVariavel
        #CONTROLA PROCEDURES
        self.isParametro = False #controla se estou dentro da assinatura de parametros de uma procedure ou não, e caso esteja então  não criar na pilha de codgo ['ALME','1']


    def obtemSimbolo(self):
        self.token = self.scan.NextToken()
        self.simbolo = None
        if self.token != None:
             self.simbolo = self.token
    
    def analise(self):
        self.obtemSimbolo()
        self.programa()
        if self.simbolo.tipo == 'isEof':
            self.tokens_saida.append("TUDO CERTO")
            print("Analise Sintatica OK")
            #escreverDocumento(self.path + "_saida.txt",self.tokens_saida,self.tabelaHASH.tabelaSimbolo)
        else:
            raise Exception('Erro sintatico, esperado fim de cadeia LINHA:' + str(self.scan.LINHA))

    def programa(self):
        self.tokens_saida.append("<programa>")
        #print("<programa>")
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
        #print("<corpo>")
        self.dc()
        if self.simbolo.termo == "begin":
            self.obtemSimbolo()
            self.comandos()
            if self.simbolo.termo == "end":
                self.obtemSimbolo()
                if self.simbolo.termo == ".":
                    self.stackCodigoGerado.push(['PARA', 0]) #cod parar o programa
                    self.obtemSimbolo()
                else:
                    raise Exception('Erro sintatico, esperado "." LINHA:' + str(self.scan.LINHA))
            else:
                raise Exception('Erro sintatico, esperado "end" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "begin" LINHA:' + str(self.scan.LINHA))
    
    def dc(self):
        self.tokens_saida.append("<dc>")
        #print("<dc>")
        if self.simbolo.tipo == "procedure":
            self.obtemSimbolo()
            self.dcP()
        elif self.simbolo.tipo == "tipo_var":
            self.memoria["tipo"] = self.simbolo.termo
            self.obtemSimbolo()
            self.dcV()
            self.maisDc()
        else :
            pass
    
    def dcP(self):
        self.tokens_saida.append("<dcP>")
        #print("<dcP>")
        if self.simbolo.tipo == "ident":
                if self.tabelaHASH.escopo == 0: # caso futuramente permita criar mais de uma procedure então verificar se está no primeiro escopo, gerar somente uma vez esse salto, e não ao inicio de cada função
                    posicaoSaltoBeginPrincipal = self.stackCodigoGerado.size() #guardo a posção da função na pilha que salta para o begin principal
                    self.stackCodigoGerado.push(['DSVI','BEGIN'])
                indexProcedureTabelaSimbolo = len(self.tabelaHASH.tabelaSimbolo)
                self.tabelaHASH.inserir(self.simbolo.tipo,self.simbolo.termo,'procedure',self.stackCodigoGerado.size(),self.scan.LINHA)#regra semantica para identificar unicidade do identificador e inserir na tabela
                self.tabelaHASH.escopo=1 # como vai ser permitido somente 1 procedure, posso deixar estatico 1, do contrario, poderia ir crescendo esse escopo
                tamanhoPilhaDAtual = self.tabelaHASH.tamanhoPilhaD
                self.obtemSimbolo()
                self.parametros()
                self.tabelaHASH.tabelaSimbolo[indexProcedureTabelaSimbolo][9] = self.memoria["NumeroParametros"]
                self.memoria["NumeroParametros"] = 0
                self.corpoP()
                m = self.tabelaHASH.tamanhoPilhaD - tamanhoPilhaDAtual
                self.stackCodigoGerado.push(['DESM', m ])
                self.stackCodigoGerado.push(['RTPR', '' ])
                self.tabelaHASH.tamanhoPilhaD = tamanhoPilhaDAtual # caso queira permitir mais procedures uma dia mais procedures um dia, 
                self.tabelaHASH.escopo = 0
                self.stackCodigoGerado.items[posicaoSaltoBeginPrincipal][1] = self.stackCodigoGerado.size()


    
    def parametros(self):
        self.tokens_saida.append("<parametros>")
        #print("<parametros>")
        self.memoria["NumeroParametros"] = 0 #quantifica a quantidade de parametros, para armazenar na tabela de simbolos
        if self.simbolo.tipo == "(":
            self.isParametro = True
            self.obtemSimbolo()
            self.listaPar()
            if self.simbolo.tipo == ")":
                self.isParametro = False
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado ")" LINHA:' + str(self.scan.LINHA))
        else:
             pass

    def listaPar(self):
        self.tokens_saida.append("<parametros>")
        #print("<parametros>")
        if self.simbolo.tipo == "tipo_var":
            self.obtemSimbolo()
            if self.simbolo.termo == ":":
                self.obtemSimbolo()
                self.variaveis()
                self.maisPar()
            else:
                raise Exception('Erro sintatico, esperado ":" LINHA:' + str(self.scan.LINHA))
        else:
             raise Exception('Erro sintatico, esperado "tipo_var" LINHA:' + str(self.scan.LINHA))

    def maisPar(self):
        self.tokens_saida.append("<maisPar>")
        #print("<maisPar>")
        if self.simbolo.tipo == ";":
            self.obtemSimbolo()
            self.listaPar()
        else:
            pass
    
    def corpoP(self):
        self.tokens_saida.append("<corpoP>")
        #print("<corpoP>")
        self.dcLoc()
        if self.simbolo.tipo == "begin":
            self.obtemSimbolo()
            self.comandos()
            if self.simbolo.tipo == "end":
                self.obtemSimbolo()
            else:
                raise Exception('Erro sintatico, esperado "end" LINHA:' + str(self.scan.LINHA))
        else:
            raise Exception('Erro sintatico, esperado "begin" LINHA:' + str(self.scan.LINHA))

        


    
    def dcLoc(self):
        self.tokens_saida.append("<dcLoc>")
        #print("<dcLoc>")
        if self.simbolo.tipo == "tipo_var":
            self.memoria["tipo"] = self.simbolo.termo
            self.obtemSimbolo()
            self.dcV()
            self.maisDcLoc()
        else:
            pass
    
    def maisDcLoc(self):
        self.tokens_saida.append("<maisDcLoc>")
        #print("<maisDcLoc>")
        if self.simbolo.tipo ==";":
            self.obtemSimbolo()
            self.dcLoc()
        else:
            pass

    
    def listaArg(self):
        self.tokens_saida.append("<listaArg>")
        #print("<listaArg>")
        self.argumentos()
        if self.simbolo.termo == ")":
            self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperado ")" LINHA:' + str(self.scan.LINHA))
            

    def argumentos(self):
        self.tokens_saida.append("<argumentos>")
        #print("<argumentos>")
        if self.simbolo.tipo == "ident":
            self.memoria["NumeroParametros"] -= 1 # vai subtraindo o numero de parametros, para verificar se todos foram passados
            self.stackCodigoGerado.push(['PARAM',self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)])
            self.obtemSimbolo()
            self.maisIdent()
        else:
            raise Exception('Erro sintatico, esperado "ident" LINHA:' + str(self.scan.LINHA))

    def maisIdent(self):
        self.tokens_saida.append("<maisIdent>")
        #print("maisIdent")
        if self.simbolo.termo == ",":
            self.obtemSimbolo()
            self.argumentos()
        else:
            pass
    



    def maisDc(self):
        self.tokens_saida.append("<maisDc>")
        #print("<maisDc>")
        if self.simbolo.tipo == ";":
            self.obtemSimbolo()
            self.dc()
        else:
            pass


    def dcV(self):
        self.tokens_saida.append("<dcV>")
        #print("<dcV>")
        if self.simbolo.termo == ":":
                self.obtemSimbolo()
                self.variaveis() #troquei caso de erro, eu troquei o obtem simbolo que estava aqui abaixo, e coloquei no variaveis
        else:
                raise Exception('Erro sintatico, esperado ":" LINHA:' + str(self.scan.LINHA))

    def comandos(self):
        self.tokens_saida.append("<comandos>")
        #print("<comandos>")
        self.comando()
        self.maisComandos()
    
    def maisComandos(self):
        self.tokens_saida.append("<maisComandos>")
        #print("<maisComandos>")
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
        #print("<parIdent>")
        if self.simbolo.termo == "(":
            self.obtemSimbolo()
            if self.simbolo.tipo == "ident":
                self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
                #cod faz imprime ou READ ou WRITE
                if tipoOperacao == 1 :
                    self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)])
                elif tipoOperacao == 2:
                    self.stackCodigoGerado.push(['ARMZ', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)]) #escreve no endereço relativo
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
        #print("<atribuirVal>")
        if self.simbolo.termo == "=":
                self.obtemSimbolo()
                self.expressao()
        else:
            raise Exception('Erro sintatico, esperado "=" LINHA:' + str(self.scan.LINHA))

    def condicional(self):
        self.tokens_saida.append("<condicional>")
        #print("<condicional>")
        self.condicao()
        if self.simbolo.termo == "then":
            posicaoInicioIf = self.stackCodigoGerado.size() #Salva na recursão o index do if na pilha, para futuramente trocar o valor next, para onde ele deve saltar caso seja false
            self.stackCodigoGerado.push(['DSVF', 'NEXT']) #cod entra no comando da condição
            self.obtemSimbolo()
            self.comandos()
            posicaoFimIf = self.stackCodigoGerado.size() #Salva na recursão o index do if na pilha, para futuramente trocar o valor next, para onde ele deve saltar após entrar no if e finalizar os comandos
            self.stackCodigoGerado.push(['DSVI', 'NEXT'])
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
        #print("<pFalsa>")
        if self.simbolo.termo == "else":
            self.stackCodigoGerado.items[posicaoInicioIf][1] = self.stackCodigoGerado.size()
            self.obtemSimbolo()
            self.comandos()
        else:
            pass

    def condicao(self):
        self.tokens_saida.append("<condicao>")
        #print("<condicao>")
        self.expressao()
        relacao = self.relacao()
        self.expressao()
        self.stackCodigoGerado.push(relacao)

    def relacao(self):
        self.tokens_saida.append("<relacao>")
        #print("<relacao>")
        if self.simbolo.termo == "=":
            self.obtemSimbolo()
            return  ['CPIG', ''] #cod igual
        elif self.simbolo.termo == "<":
            self.obtemSimbolo()
            if self.simbolo.termo == ">":
                self.obtemSimbolo()
                return  ['CDES', ''] #cod desigual
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
                return  ['CPMI', ''] #cod menor igual
            else:
                return ['CPME', ''] #cod menor
        elif self.simbolo.termo == ">":
            self.obtemSimbolo()
            if self.simbolo.termo == "=":
                self.obtemSimbolo()
                return  ['CMAI', ''] #cod maior igual
            else:
                return  ['CPMA', ''] #cod maior
        else:
            raise Exception('Erro sintatico, esperado "operador" LINHA:' + str(self.scan.LINHA))


    def expressao(self):
        self.tokens_saida.append("<expressao>")
        #print("<expressao>")
        self.termo()
        self.outrosTermos()

    def termo(self):
        self.tokens_saida.append("<termo>")
        #print("<termo>")
        opUn = self.opUn()
        self.fator()
        self.maisFatores()
        if opUn != None:
            self.stackCodigoGerado.push(opUn)


    def opUn(self):
        self.tokens_saida.append("<opUn>")
        #print("<opUn>")
        if self.simbolo.termo == "-":
            self.obtemSimbolo()
            return ['INVE', '']
        else:
            pass
    
    def outrosTermos(self):
        self.tokens_saida.append("<outrosTermos>")
        #print("<outrosTermos>")
        if self.simbolo.termo == "+":
            self.opAd()
            self.termo()
            self.outrosTermos()
            self.stackCodigoGerado.push(['SOMA', ''])
        elif  self.simbolo.termo == "-":
            self.opAd()
            self.termo()
            self.outrosTermos()
            self.stackCodigoGerado.push(['SUBT', ''])

    def opAd(self):
        self.tokens_saida.append("<opAd>")
        #print("<opAd>")
        if self.simbolo.termo == "+":
            self.obtemSimbolo()
        elif self.simbolo.termo == "-":
            self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperador "+" ou operador "-" LINHA:' + str(self.scan.LINHA))

    def opMul(self):
        self.tokens_saida.append("<opMul>")
        #print("<opMul>")
        if self.simbolo.termo == "*":
            self.obtemSimbolo()
        elif self.simbolo.termo == "/":
            self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperador "+" ou operador "-" LINHA:' + str(self.scan.LINHA))

    def maisFatores(self):
        self.tokens_saida.append("<maisFatores>")
        #print("<maisFatores>")
        if self.simbolo.termo == "*":
            self.opMul()
            self.fator()
            self.maisFatores()
            self.stackCodigoGerado.push(['MULT', ''])
        if self.simbolo.termo == "/":
            self.opMul()
            self.fator()
            self.maisFatores()
            self.stackCodigoGerado.push(['DIVI', ''])
        else:
            pass
    
    def fator(self):
        self.tokens_saida.append("<fator>")
        #print("<fator>")
        if self.simbolo.tipo == "ident":
            self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
            self.stackCodigoGerado.push(['CRVL', self.tabelaHASH.getEnderecoRelativo(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)])
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
        #print("<comando>")
        if self.simbolo.termo == "read":
            self.stackCodigoGerado.push(['LEIT', '']) #cod fazendo leitura
            self.obtemSimbolo()
            self.parIdent(2)
        elif self.simbolo.termo == "write":
            self.obtemSimbolo()
            self.parIdent(1)
            self.stackCodigoGerado.push(['IMPR', ''])
        elif self.simbolo.tipo == "ident":
            self.tabelaHASH.setVarUtilizada(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)#regra semantica seta que a variável foi utilizada
            self.memoria['tipo']=self.tabelaHASH.getTipo(self.simbolo.termo,self.tabelaHASH.escopo,self.scan.LINHA)
            simboloMemoria = self.simbolo
            self.obtemSimbolo()
            if self.simbolo.termo == ":":
                self.obtemSimbolo()
                self.atribuirVal()
                self.stackCodigoGerado.push(['ARMZ', self.tabelaHASH.getEnderecoRelativo(simboloMemoria.termo,self.tabelaHASH.escopo,self.scan.LINHA)]) #escreve no endereço relativo
            else:
                posicaoPusher = self.stackCodigoGerado.size()
                self.stackCodigoGerado.push(['PUSHER','PUSHER'])
                if self.simbolo.termo == "(":
                    quantidadeParametrosEsperado = self.tabelaHASH.getNumeroParametro(simboloMemoria.termo,self.tabelaHASH.escopo,self.scan.LINHA)
                    self.memoria["NumeroParametros"] = quantidadeParametrosEsperado
                    self.obtemSimbolo()
                    self.listaArg()
                    if self.memoria["NumeroParametros"] != 0:
                        quantidadeParametrosPassados = quantidadeParametrosEsperado - self.memoria["NumeroParametros"] 
                        raise Exception('Erro semantico, na procedure ' + str(simboloMemoria.termo) + ' eram esperados: ' + str(quantidadeParametrosEsperado) + ' PARAM, porém foram passados: ' + str(quantidadeParametrosPassados) + ' PARAM  LINHA:' + str(self.scan.LINHA - 1)) 
                self.stackCodigoGerado.push(['CHPR',self.tabelaHASH.getEnderecoPilha(simboloMemoria.termo,self.tabelaHASH.escopo,self.scan.LINHA)])
                self.stackCodigoGerado.items[posicaoPusher][1] = self.stackCodigoGerado.size() 
            #else:
                #raise Exception('Erro sintatico, esperado uma expressão ou uma funcão LINHA:' + str(self.scan.LINHA))  
        elif self.simbolo.tipo == "if":
            self.obtemSimbolo()
            self.condicional()
        elif self.simbolo.tipo == "while":
            self.obtemSimbolo()
            self.loopWhile()
        else:
            raise Exception('Erro sintatico, esperado "comando" LINHA:' + str(self.scan.LINHA))   


    def variaveis(self):
        self.tokens_saida.append("<variaveis>")
        #print("<variaveis>")
        if self.simbolo.tipo == "ident":
            self.tabelaHASH.inserir(self.simbolo.tipo,self.simbolo.termo,self.memoria["tipo"],"",self.scan.LINHA)#regra semantica para identificar unicidade do identificador
            if not(self.isParametro):
                self.stackCodigoGerado.push(['ALME', 1]) #cod definir variável
            else:
                self.memoria["NumeroParametros"] +=1
            self.obtemSimbolo()
            self.maisVar()
            #self.obtemSimbolo()
        else:
            raise Exception('Erro sintatico, esperado "ident" LINHA:' + str(self.scan.LINHA))
    
    def maisVar(self):
        self.tokens_saida.append("<maisVar>")
        #print("<maisVar>")
        if self.simbolo.tipo == ",":
             self.obtemSimbolo()
             self.variaveis()
        else:
            pass
    
    def loopWhile(self):
        self.tokens_saida.append("<loopWhile>")
        #print("<loopWhile>")
        posicaoInicioWhile = self.stackCodigoGerado.size() #posição inicial do while, para ser armazenada no desvia sempre, para sempre voltar do inicio
        self.condicao()
        posicaoWhileTrocarNext =  self.stackCodigoGerado.size() #Salva na recursão o index do while na pilha, para futuramente trocar o valor next, para onde ele deve saltar caso seja a condição retorne false
        self.stackCodigoGerado.push(['DSVF', 'NEXT']) #cod faz desvio caso seja falso D[s] = 0
        if self.simbolo.tipo == "do":
            self.obtemSimbolo()
            self.comandos()
            self.stackCodigoGerado.push(['DSVI', posicaoInicioWhile])
            if self.simbolo.tipo == "$":
                self.stackCodigoGerado.items[posicaoWhileTrocarNext][1] = self.stackCodigoGerado.size()
                self.obtemSimbolo()

    
            
            

"""sintatico = AnalisadorSintatico(r'entradas.txt')
sintatico.analise()
print(sintatico.tabelaHASH.tabelaSimbolo)"""