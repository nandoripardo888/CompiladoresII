from inspect import stack
from CStack import Stack

class MaqHip:
    def __init__(self,tabelaSimbolo,stackCodigoGerado):
        self.pilhaD = Stack()
        self.pilhaM = Stack()
        self.pilhaC = Stack()
        self.tabelaSimbolo = tabelaSimbolo
        self.stackCodigoGerado:Stack = stackCodigoGerado
        self.ResultadoExecucao = Stack()
        #registradores
        self.i = 0
        self.s = 0
        self.isDebug = False

    def executar(self):
        while self.i < self.stackCodigoGerado.size():
            instr = self.stackCodigoGerado.items[self.i][0]
            valor = self.stackCodigoGerado.items[self.i][1]
            
            if instr == 'INPP':
                self.i += 1
                self.pilhaD.Free()
            
            elif instr == 'CRCT':
                self.pilhaD.push(float(valor))
                self.i+=1
            
            elif instr == 'CRVL':
                self.s +=1
                self.pilhaD.push(float(self.pilhaD.items[valor]))
                self.i +=1
            
            elif instr == 'SOMA':
                self.pilhaD.push(float(self.pilhaD.pop(-2) + self.pilhaD.pop()))
                self.i+=1
            
            elif instr == 'SUBT':
                self.pilhaD.push(float(self.pilhaD.pop(-2) - self.pilhaD.pop()))
                self.i+=1
            
            elif instr == 'MULT':
                self.pilhaD.push(float(self.pilhaD.pop(-2) * self.pilhaD.pop()))
                self.i+=1
            
            elif instr == 'DIVI':
                self.pilhaD.push(float(self.pilhaD.pop(-2) / self.pilhaD.pop()))
                self.i+=1
            
            elif instr == 'INVE':
                itemIverter = float(self.pilhaD.pop())
                self.pilhaD.push(float( -1 * itemIverter))
                self.i+=1
            
            elif instr == 'CPME':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) < self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'CPMA':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) > self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'CPIG':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) == self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'CDES':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) != self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'CPMI':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) <= self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'CMAI':
                self.pilhaD.push(1 if self.pilhaD.pop(-2) >= self.pilhaD.pop() else 0)
                self.i+=1
            
            elif instr == 'ARMZ':
                self.pilhaD.items[int(valor)]=(self.pilhaD.pop())
                self.i+=1
            
            elif instr == 'DSVI':
                self.i = int(valor)
            
            elif instr == 'DSVF':
                if self.pilhaD.pop() == 0:
                    self.i = int(valor)
                else:
                    self.i += 1
            
            elif instr == 'LEIT':
                if self.isDebug:
                    entrada = 10
                else:
                     entrada = int(input("valor entrada: "))
                self.ResultadoExecucao
                self.pilhaD.push(entrada)
                self.ResultadoExecucao.push(entrada)
                self.i+=1
            
            elif instr == 'IMPR':
                saida = str(self.pilhaD.pop())
                print("imprimir " + saida)
                self.ResultadoExecucao.push("imprimir " + saida)
                self.i+=1

            elif instr == 'ALME':
                self.pilhaD.push(0)
                self.i+=1
            
            elif instr == 'PARA':
                print("Fim da execução")
                self.ResultadoExecucao.push("Fim da execução")
                self.i+=1
            
            elif instr == 'PARAM':
                self.pilhaD.push(self.pilhaD.items[valor])
                self.i+=1
            
            elif instr == 'PUSHER':
                self.pilhaD.push(valor)
                self.i+=1
            
            elif instr == 'CHPR':
                self.i = int(valor)

            elif instr == 'DESM':
                for j in range(valor):
                    self.pilhaD.pop()
                    self.i+=1
            
            elif instr == 'RTPR':
                self.i = self.pilhaD.pop()
            

            

            

                
            
            




