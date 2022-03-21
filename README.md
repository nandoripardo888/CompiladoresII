
# trabalho de Compiladores II

## Arquivos de códigos-fonte presentes
1. **main.py** - executa todo o código fonte.
2. **analisadorSintatico.py** - contém o arquivo do analisador sintático.
3. **analisadorLexico.py** - contém o código analisador Léxico.
4. **exemplo1.txt** - contém um arquivo de programa a ser analisado.
5. **exemplo2.txt** - contém um arquivo de programa inválido a ser analisado.


### introdução
Este projeto é a implementação de um compilador, onde foi implementado um gerador de codigo intermediário e uma maquina hipotetica para a execução deste codigo. O gerador de código gera uma pilha de instruções PÓS-FIXA e a maquina hipotética com o auxilio de pilhas de dados e alguns registradores executa e gera a saída do código.

<p style="text-align:center"><img alt="" height="403" src="https://github.com/nandoripardo888/CompiladoresII/blob/master/modeloComp.PNG" width="582" /></p>

> O foco deste trabalho, está na geração de código e maquina hipotetica, no entanto algumas partes que são necessárias para a construção de um compilador (Análise léxica, sintática e semântica) também são apresentadas aqui.

##### O desenvolvimento está dividido nas seguintes partes

-   Analisador Léxico
-  Analisador Sintático
-  Analisado Semântico
-  Geração de Código
-  Maquina Hipotética


{imagem das fases de um compilador}

## DESENVOLVIMENTO

## Analisador Léxico
### Simbolos
como simbolos permitidos pela linguagem temos a seguinte tabela

------------
| Palavra Token  | Expressão regular correspondente  |
| ------------ | ------------ |
|  KeyWords |  if, then, else, write, read, integer, real, program, begin, end |
| Identificadores  | (Letra)\* |
|  Numero |  (Digito)\* |
| Letra  | a..z  |
| Dígito  | 0..9  |
| Operadores  |  =   >=   >   <    <=  <> |
|Símbolos | ; , : $ ( ) { } [ ]  |

### regras Léxicas
O automato a seguir valida a formações dos Tokens

<h3 style="text-align:center">autômato analisador</h3>

<p style="text-align:center"><img alt="" height="300" src="https://github.com/nandoripardo888/CompiladoresPy/blob/main/automato.png" width="400" /></p>


## Analisador Sintático
### Gram&aacute;tica Livre de Contexto da Linguagem - Forma BNF X Geração de codigo
abaixo segue a tabela da GLC mapeada com a respectiva intrução gerada.

| GLC  | Geração Código |
| ------------ | ------------ |
|`<programa> -> program ident <corpo> .  ` | ` G['INPP', '']` |
|`<corpo> -> <dc> begin <comandos> end  `| `G['PARA', 0]`  |
| `<dc> -> <dc_v> <mais_dc> │ <dc_p> │ λ` | `G['DSVI','BEGIN']`  |
| ` <mais_dc> -> ; <dc> │ λ ` |   |
| `<dc_v> ->  <tipo_var> : <variaveis>`  |   |
| `<tipo_var> -> real │ integer`  |   |
| `<variaveis> -> ident <mais_var>`	  |  `G['ALME', 1]` |
| `<mais_var> -> , <variaveis>`  |   |
|`<dc_p> -> procedure ident <parametros> <corpo_p>`  | `G['DESM', QUANTIDADEITENSPILHAD ]['RTPR', '' ]`  |
| `<parametros> -> (<lista_par>) │ λ`  |   |
|` <lista_par> -> <tipo_var> : <variaveis> <mais_par>`  |   |
|  `<mais_par> -> ; <lista_par> │ λ` |   |
| `<corpo_p> -> <dc_loc> begin <comandos> end`  |   |
|  `<dc_loc> -> <dc_v> <mais_dcloc> │ λ` |   |
| `<mais_dcloc> -> ; <dc_loc> │ λ`  |   |
| `<lista_arg> -> (<argumentos>) │ λ`  | `G['PUSHER',FIMPROCEDURE]`  |
| ` <argumentos> -> ident <mais_ident>` |   |
| `<mais_ident> -> , <argumentos> │ λ` |   |
|`<comandos> -> <comando> <mais_comandos>`  |   |
| `<mais_comandos> -> ; <comandos> │ λ` |   |
| `<comando> -> read (ident) │write (ident) │if <condicao> then <comandos> <pfalsa> $ │while <condicao> do <comandos> $ │ident <restoIdent>` | `G['LEIT', '']['ARMZ', ENDERECOAUXILIAR]│G['CRVL', 'ENDERECOAUXILIAR'] ['IMPR',  '']│G['DSVF', 'NEXT'] ['DSVS', 'NEXT']│G['DSVF', 'posicaoFinalWhile'] ['DSVS', 'posicaoinicioWhile']`  |
| `<restoIdent> -> := <expressao> │ <lista_arg>` |   |
|`<condicao> -> <expressao> <relacao> <expressao>`  |   |
|` <relacao> -> = │ <> │ >= │ <= │ > │ <` | `G['CPIG', '']│['CDES', '']│['CMAI', '']│['CPMI', '']│['CPMA', '']│['CMAI', '']`  |
| `<expressao> -> <termo> <outros_termos>` |   |
|  `<termo> -> <op_un> <fator> <mais_fatores>`|   |
| `<op_un> -> - │ λ` | `G['INVE','']`  |
| `<fator> -> ident │ numero_int │ numero_real │ (<expressao>)` |   |
|` <outros_termos> -> <op_ad> <termo> <outros_termos> │ λ` | `G['SOMA', ''] ['SUBT', '']`  |
| `<op_ad> -> + │ -` |   |
| `<mais_fatores> -> <op_mul> <fator> <mais_fatores> │ λ` |  `G['MULT', ''] ['DIVI', '']` |
| `<op_mul> -> * │ /` |   |
|` <pfalsa> -> else <comandos> │ λ` |   |

## Analisador Semântico

<p>para an&aacute;lise Sem&acirc;ntica foram adicionadas as seguintes regras</p>

- atribuir tipo ao identificador na tabela de simbolos -&gt;&nbsp;{Memoria.tipo=real or Memoria.tipo=integer} e&nbsp;{inserir(Memoria.tipo)}

- atribuir tipo ao identificador na tabela de simbolos -&gt;&nbsp;{Memoria.tipo=real or Memoria.tipo=integer} e&nbsp;{inserir(Memoria.tipo)}

- verificar se um&nbsp;identificador foi declarada para ser usada. -&gt;&nbsp;{emtabela{ident.termo}

- garantir unicidade de identificador -&gt;&nbsp;{setvarutilizada(ident.termo)} {emtabela(ident.termo)}

- verificar variaveis utilizadas -&gt;&nbsp;{setvarutilizada(ident.termo)

- verificar se a quantidade de parametros passadas na função está de acordo com a assinatura da função {Memoria.quantidadeParametros}

- verificar se escopo da função, para criar funções com mesmo identificador, em escopos diferentes {emtabela{ident.termo, ident.escopo}}

- verificar se comentário '{ }' e '/\* \*/'


## Gerador de Código

como vimos na tabela acima, os códigos são gerados na hora da analise sintática, e utiliza a operação pós fixa, abaixo segue a tabela com as instruções geradas

| INSTRUÇÃO  |    |
| ------------ | ------------ |
|  CRCT k | carrega constante k na pilha D  |
| CRVL n  | carrega valor de endereço n na pilha D |
| SOMA   |soma topo da pilha com seu antecessor   |
| SUBT   | subtrai o elemento do topo do antecessor  |
| MULT   |  multiplica elemento do topo pelo antecessor |
| DIVI  |divide elemento do antecessor pelo do topo   |
|  INVE  | inverte sinal do topo  |
| CPME   | comparação de menor  |
| CPMA   | comparação de maior  |
|  CPIG  | comparação de igualdade  |
| CDES   | comparação de desigualdade  |
| CPMI   | comparação <=  |
| CMAI   | comparação >=  |
| ARMZ n  | armazena o topo da pilha no endereço n de D  |
| DSVI p   | desvio incondicional para a instrução de endereço p  |
| DSVF p   |desvie para a instrução de endereço p caso a condição resultante seja falsa   |
|  PARAM | Aloca memória e copia valor da posição n para o topo de D  |
| PUSHER e  | Empilha o índice e da instrução seguinte à chamada do procedimento |
| CHPR p  | Desvia para instrução de índice p no array C, obtido na TS  |
|  DESM m | Desaloca m posições de memória, a partir do topo s de D  |
| RTPR  | Retorna do procedimento – endereço de retorno estará no topo de D – e desempilha o endereço  |



## Maquina Hipotética

para a maquina Hipotetica foi criado os seguintes componentes
#### PILHAS
		pilhaC -> area de codigo, onde ficava armazeda as instruções
		pilhaD -> area de dados em tempo de execução
		tabelaSimbolo -> tabela contendo todos os simbolos do algoritmo

#### Registradores
		i -> inteiro que alocava o topo da pilha de codigo (pilhaC)
		s -> inteiro que alocava o topo da pilha de dados (pilhaD)

a maquina hipotetica faz a leitura da pilha de código e execura cada uma das instruções. 
há um modo debug, onde é setado para Sim ou Não ao iniciar o programa, no modo debug, o usuário não se preocupa em digitar os valores de entrada, ele seta todas as entradas para o valor 10, para que o usuário (Professor) apenas sente, relaxe, e veja a saída.

## Informações Gerais: 
- O analisador sintático construído foi do tipo Descendente Preditivo Recursivo. Para cada símbolo não-terminal da gramática, uma nova função foi construída. As produções da gramática foram representadas por chamadas sucessivas dessas funções.

- o programa main.py ao iniciar ira procurar todos os arquivos com extensão  .txt e irá tentar compilar cada um deles, gerando uma saida individual para cada uma das entradas encontradas onde constará o algoritmo analisado, a tabela de simbolos, o codigo intermediário e a saidá final da maquina execução do algoritmo pela maquina hipotética, ou caso a aprensente algum erro esse erro, vai gerar um arquivo especificando o erro. (entrada.txt) -> (entrada_saida.txt).

- foi implementado um modo debug, onde é perguntado assim que inicia a apliacação, se quer executar em debug, caso selecione SIM(S) então, sempre que for ter uma entrada do teclado, ao invés de pedir ao usuário que entre com o valor será colocado como valor de entrada o valor 10, para tornar mais rapido o teste para o professor

- Quando um erro léxico ou Sintático ou Semântico é encontrado em um arquivo que está sendo compilado,  a compilação para este arquivo  é parado imediatamente, uma vez que o analisador sintático pode encontrar erros em cascata devido ao erro inicial. e para os erros Sintáticos e semânticos é colocado no arquivo de saída (entrada_saida.txt) o erro e a linha onde este se encontra.

- No emulador terminal serão printados cada uma dos algortmos avaliádos, se foi compilado com sucesso ou não, e o resultado da execução.

- por fim se o arquivo são salvos de saída são na mesma pasta da aplicação.

- segue como arquivos de exemplo os algoritmos passados ao decorrer da diciplina
