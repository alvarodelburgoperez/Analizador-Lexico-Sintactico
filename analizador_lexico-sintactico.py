import re
from lark import Lark, Transformer,Tree
import random

# FUNCIÓN PARA PONERLE COLOR A LOS STRINGS

def imprimir_color(texto, color):
    colores = {
        "rojo": "\033[91m",  # CÓDIGO COLOR ROJO
        "verde": "\033[92m",  # CÓDIGO COLOR VERDE
        "amarillo": "\033[93m",  # CÓDIGO COLOR AMARILLO
        "azul": "\033[94m",  # CÓDIGO COLOR AZUL

    }

    fin_color = "\033[0m"  # RESTAURAR AL COLOR PREDETERMINADO

    if color in colores:
        color_esc = colores[color]
        print(color_esc + texto + fin_color)
    else:
        print("Color no válido")



# GENERAR FRASE ALEATORIA 

def generar_frase():
    sujeto = random.choice(["Fernando Alonso", "El asturiano", "El samurái"])
    
    verbos_complementos = [("logra", ["un histórico podio", "un podio mágico", "una clasificación espectacular", "la deseada 33", "una victoria dominante"]),
                           ("consigue", ["un histórico podio", "un podio mágico", "una clasificación espectacular", "la deseada 33", "una victoria dominante"]),
                           ("humilla", ["a Hamilton", "a Vertappen", "a Carlos Sainz", "a Guanyu Zhou"]), 
                           ("pasa por encima", ["a Hamilton", "a Vertappen", "a Carlos Sainz", "a Guanyu Zhou"])]
    
    verbo, complementos = random.choice(verbos_complementos)
    complemento = random.choice(complementos)
    
    gp = random.choice(["en el Gran Premio de España", "en el Gran Premio de Brasil", "en el Gran Premio de Francia", "en el Gran Premio de Austria"])

    return f"{sujeto} {verbo} {complemento} {gp}"

frase = generar_frase()


print(" ")
print(" ")
# Imprimir la frase en rojo
imprimir_color(frase, "amarillo")
print(" ")
print(" ")


#---------- ANALIZADOR LÉXICO ----------

# DEFINICIÓN DE LOS TOKENS USANDO EXPRESIONES REGULARES

token_patterns = [
    (r'\b(Fernando Alonso|El asturiano|El samurái)\b', 'SUJETO'),
    (r'\b(logra|consigue|humilla|pasa por encima)\b', 'VERBO'),
    (r'\b(un histórico podio|un podio mágico|una clasificación espectacular|la deseada 33|una victoria dominante|a Hamilton|a Vertappen|a Carlos Sainz|a Guanyu Zhou)\b', 'COMPLEMENTO'),
    (r'\b(en el Gran Premio de España|en el Gran Premio de Brasil|en el Gran Premio de Francia|en el Gran Premio de Austria)\b', 'GP'),
    (r'\s+', 'ESPACIOS'),  # ESPACIOS EN BLANCO
]


# FUNCIÓN PARA HACER LOS TOKENS DE LA FRASE

def tokenize(code):
    tokens = []
    while code:
        code = code.lstrip()  # ELIMINAMOS LOS ESPACIOS EN BLANCO AL PRINCIPIO
        matched = False
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                value = match.group(0)
                tokens.append((value, token_type))
                code = code[match.end():]  # AVANZA EN EL CÓDIGO
                matched = True
                break
        if not matched:
            print("Error: Caracter no reconocido en '{}'".format(code[0]))
            break
    return tokens


# IMPRIMIMOS LOS TOKENS

mensaje = frase
tokens = tokenize(mensaje)
for token in tokens:
    print(token)

print(" ")
print(" ")


#---------- ANALIZADOR SINTÁCTICO ----------


# GRAMÁTICA DEL ANALIZADOR

gramatica = '''
    start: sentencia

    sentencia: sujeto verbo gp

    sujeto: "Fernando Alonso" | "El asturiano" | "El samurái"
    
    verbo: "logra"  complemento1 | "consigue"  complemento1 | "humilla"  complemento2 | "pasa por encima"  complemento2

    complemento1: "un histórico podio" | "un podio mágico" | "una clasificación espactacular" | "la deseada 33" | "una victoria dominante"

    complemento2: "a Hamilton" | "a Vertappen" | "a Carlos Sainz" | "a Guanyu Zhou"

    gp: "en el Gran Premio de España" | "en el Gran Premio de Brasil" | "en el Gran Premio de Francia" | "en el Gran Premio de Austria"

    %import common.WS_INLINE
    %ignore WS_INLINE
'''


# PARSER

parser = Lark(gramatica, parser='lalr')


# CLASE PARA TRANSFORMAR EL ÁRBOL

class TreeTransformer(Transformer):
    
    def __init__(self, tokens):
        self.tokens = tokens

    def sentencia(self,tokens):
        return ([token[0] for token in self.tokens])

    def sujeto(self, tokens):
        return ("Sujeto:", self.tokens[0][0])

    def verbo(self, tokens):
        return ("Verbo:",self.tokens[1][0])
    
    def complemento(self,tokens):
        return ("Complemento:",self.tokens[2][0])

    def gp(self, tokens):
        return ("GP:",self.tokens[3][0])
    

# TRANSFORMA LOS TOKENS EN UNA LISTA CON LOS VALORES DE LOS TOKENS
transformer = TreeTransformer(tokens)



nuevo = transformer.sentencia(tokens)

print(nuevo)
print(" ")
print(" ")


# DEFINIMOS LAS ETIQUETAS DE LOS NODOS

etiquetas = ['NOMBRE', 'VERBO', 'COMPLEMENTO', 'GP']


# GENERAMOS EL ÁRBOL CON LOS VALORES DE LOS TOKENS

def generar_arbol_con_valores(tokens, etiquetas):
    arbol = Tree('sentencia', [])
    for token, tag in zip(tokens, etiquetas):
        arbol.children.append(Tree(tag, [Tree(token, [])]))
    return arbol

arbol_con_valores = generar_arbol_con_valores(nuevo, etiquetas)


# IMPRIMIMOS EL ÁRBOL

arbol_str = arbol_con_valores.pretty()
imprimir_color(arbol_str, "verde")