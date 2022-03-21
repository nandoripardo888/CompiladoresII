from MaqHip import MaqHip
from analisadorSintatico import *
import os



# print("serão analisados todos os algoritmos que estão na pasta com estensão txt")
lista=[]
# for diretorio, subpastas, arquivos in os.walk("./"):
#     for arquivo in arquivos:
#         if arquivo.endswith(".txt") and not(arquivo.endswith("_saida.txt")):
#             lista.append(os.path.join(diretorio, arquivo))
#teste rápido
lista = ['exemplo3.txt']
print('arquivos encontrados:')
print("\n".join(lista))
print("----------------")
lista2 = []
for arq in lista:
    print(arq)
    sintatico = AnalisadorSintatico(arq)
    try:
        sintatico.analise()
        MaqHipotetica = MaqHip(sintatico.tabelaHASH.tabelaSimbolo,sintatico.stackCodigoGerado)
        MaqHipotetica.executar()
        escreverDocumento(sintatico.path + "_saida.txt",sintatico.stackCodigoGerado.items,sintatico.tabelaHASH.tabelaSimbolo, MaqHipotetica.ResultadoExecucao.items,arq)
        lista2.append("compilado com SUCESSO!")
        print("arquivo gerado:" + sintatico.path + "_saida.txt")
    except Exception as inst:
        print(inst)
        sintatico.tokens_saida.append(inst)
        escreverDocumentoErro(sintatico.path + "_saida.txt",str(inst))
    print("----------------")


#print("\n".join(map(str,sintatico.stackCodigoGerado.items)))
