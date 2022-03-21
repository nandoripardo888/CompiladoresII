from MaqHip import MaqHip
from CStack import Stack
print("Deus me Ama")

codigoGerado = Stack()
codigoGerado.push(['INPP',''])
codigoGerado.push(['CRCT','0'])
codigoGerado.push(['CRCT','10'])
codigoGerado.push(['CPME',''])
codigoGerado.push(['',''])
maquina = MaqHip([],codigoGerado)
maquina.executar()
