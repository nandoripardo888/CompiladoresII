
# trabalho de Compiladores II

#### introdução
O presente trabalho é a implementação de um compilador, focando principalmente nas fases de geração de código e execução do código gerado em uma maquina hipotética, nesse sentido, serão abreviadas algumas partes que são necessárias para a construção do presente trabalho tais quais analisador Sintático e Semântico, mas que não é o foco agora.

######  O desenvolvimento está dividido nas seguintes partes

1. Analisador Léxico
2. Analisador Sintático
3. Analisado Semântico
4. Geração de Código
5. Maquina Hipotética

## DESENVOLVIMENTO
| Palavra Token  | Expressão regular correspondente  |
| ------------ | ------------ |
|  KeyWords |  if, then, else, write, read, integer, real, program, begin, end |
| Identificadores  | (Letra)\* |
|  Numero |  (Digito)\* |
| Letra  | a..z  |
| Dígito  | 0..9  |
| Operadores  |  =, >=,  >, <, <=,
|  Símbolos |   |
