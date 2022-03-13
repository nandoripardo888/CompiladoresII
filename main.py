from analisadorSintatico import *
import os


print("serão analisados todos os algoritmos que estão na pasta com estensão txt")
lista=[]
for diretorio, subpastas, arquivos in os.walk("./"):
    for arquivo in arquivos:
        if arquivo.endswith(".txt") and not(arquivo.endswith("_saida.txt")):
            lista.append(os.path.join(diretorio, arquivo))

print('arquivos encontrados:')
print("\n".join(lista))
lista2 = []
for arq in lista:
    sintatico = AnalisadorSintatico(arq)
    print("*"*50)
    print(arq)
    try:
        sintatico.analise()
        lista2.append("SUCESSO!")
    except Exception as inst:
        print(inst)
        sintatico.tokens_saida.append(inst)
        lista2.append("FALHA! - " + str(inst))
    escreverDocumento(sintatico.path + "_saida.txt",sintatico.tokens_saida,sintatico.tabelaHASH.tabelaSimbolo)

for i in range(len(lista)):
    print(lista[i].replace("./","") + " -> " + lista2[i])
