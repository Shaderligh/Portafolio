import ast
import operator
import re
import tkinter as tk

BG = "#14141f"
PANEL = "#1c1c2b"
NUM_BG = "#26263a"
NUM_HOVER = "#33334d"
FUNC_BG = "#3a3a57"
FUNC_HOVER = "#4a4a6e"
OP_BG = "#7c5cff"
OP_HOVER = "#947aff"
EQ_BG = "#ff6b9d"
EQ_HOVER = "#ff8ab3"
TEXTO = "#f1f1f8"
TEXTO_SUAVE = "#8b8ba7"

OPERADORES = "+−×÷"

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluar(nodo):
    if isinstance(nodo, ast.Expression):
        return evaluar(nodo.body)
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return nodo.value
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in OPS:
        return OPS[type(nodo.op)](evaluar(nodo.left), evaluar(nodo.right))
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in OPS:
        return OPS[type(nodo.op)](evaluar(nodo.operand))
    raise ValueError("Expresión no válida")


def formatear(valor):
    if isinstance(valor, float):
        if valor.is_integer() and abs(valor) < 1e15:
            return str(int(valor))
        texto = f"{valor:.10g}"
        return texto.replace("e+", "e")
    return str(valor)


class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.expr = ""
        self.historial = ""
        self.terminado = False
        self.error = False

        self.crear_pantalla()
        self.crear_botones()
        self.root.bind("<Key>", self.tecla)
        self.actualizar()

    def crear_pantalla(self):
        marco = tk.Frame(self.root, bg=PANEL)
        marco.pack(fill="x", padx=18, pady=(18, 10))

        self.lbl_historial = tk.Label(
            marco, text="", bg=PANEL, fg=TEXTO_SUAVE,
            font=("Segoe UI", 13), anchor="e",
        )
        self.lbl_historial.pack(fill="x", padx=16, pady=(14, 0))

        self.lbl_pantalla = tk.Label(
            marco, text="0", bg=PANEL, fg=TEXTO,
            font=("Segoe UI", 42, "bold"), anchor="e",
        )
        self.lbl_pantalla.pack(fill="x", padx=16, pady=(0, 14))

    def crear_botones(self):
        cuadricula = tk.Frame(self.root, bg=BG)
        cuadricula.pack(padx=14, pady=(0, 18))

        filas = [
            [("C", "func"), ("⌫", "func"), ("%", "func"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("±", "func"), ("0", "num"), (".", "num"), ("=", "eq")],
        ]

        estilos = {
            "num": (NUM_BG, NUM_HOVER),
            "func": (FUNC_BG, FUNC_HOVER),
            "op": (OP_BG, OP_HOVER),
            "eq": (EQ_BG, EQ_HOVER),
        }

        for r, fila in enumerate(filas):
            for c, (texto, tipo) in enumerate(fila):
                normal, hover = estilos[tipo]
                boton = tk.Button(
                    cuadricula, text=texto, width=4, height=2,
                    font=("Segoe UI", 18, "bold"),
                    bg=normal, fg=TEXTO,
                    activebackground=hover, activeforeground=TEXTO,
                    bd=0, relief="flat", cursor="hand2",
                    command=lambda t=texto: self.pulsar(t),
                )
                boton.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                boton.bind("<Enter>", lambda e, b=boton, h=hover: b.config(bg=h))
                boton.bind("<Leave>", lambda e, b=boton, n=normal: b.config(bg=n))

    def pulsar(self, valor):
        if valor.isdigit():
            self.agregar_digito(valor)
        elif valor == ".":
            self.agregar_punto()
        elif valor in OPERADORES:
            self.agregar_operador(valor)
        elif valor == "=":
            self.calcular()
        elif valor == "C":
            self.limpiar()
        elif valor == "⌫":
            self.borrar()
        elif valor == "±":
            self.cambiar_signo()
        elif valor == "%":
            self.porcentaje()
        self.actualizar()

    def preparar_entrada(self):
        if self.error:
            self.expr = ""
            self.historial = ""
            self.error = False
        if self.terminado:
            self.expr = ""
            self.historial = ""
            self.terminado = False

    def agregar_digito(self, d):
        self.preparar_entrada()
        if re.search(r"(^|[+−×÷])0$", self.expr):
            self.expr = self.expr[:-1]
        self.expr += d

    def agregar_punto(self):
        self.preparar_entrada()
        if not self.expr or self.expr[-1] in OPERADORES:
            self.expr += "0"
        if re.search(r"\d*\.\d*$", self.expr):
            return
        self.expr += "."

    def agregar_operador(self, op):
        if self.error:
            return
        self.terminado = False
        if not self.expr:
            if op == "−":
                self.expr = "−"
            return
        if self.expr == "−":
            return
        if self.expr[-1] in OPERADORES:
            if len(self.expr) > 1 and self.expr[-2] in OPERADORES:
                self.expr = self.expr[:-2] + op
            elif op == "−" and self.expr[-1] in "×÷":
                self.expr += op
            else:
                self.expr = self.expr[:-1] + op
            return
        if self.expr[-1] == ".":
            self.expr += "0"
        self.expr += op

    def limpiar(self):
        self.expr = ""
        self.historial = ""
        self.terminado = False
        self.error = False

    def borrar(self):
        if self.error or self.terminado:
            self.limpiar()
            return
        self.expr = self.expr[:-1]

    def cambiar_signo(self):
        if self.error:
            return
        self.terminado = False
        coincidencia = re.search(r"\d+\.?\d*$", self.expr)
        if not coincidencia:
            return
        inicio = coincidencia.start()
        antes_es_signo = inicio > 0 and self.expr[inicio - 1] == "−"
        antes_es_unario = antes_es_signo and (
            inicio - 1 == 0 or self.expr[inicio - 2] in OPERADORES
        )
        if antes_es_unario:
            self.expr = self.expr[: inicio - 1] + self.expr[inicio:]
        else:
            self.expr = self.expr[:inicio] + "−" + self.expr[inicio:]

    def porcentaje(self):
        if self.error:
            return
        coincidencia = re.search(r"\d+\.?\d*$", self.expr)
        if not coincidencia:
            return
        numero = float(coincidencia.group())
        self.expr = self.expr[: coincidencia.start()] + formatear(numero / 100)
        self.terminado = False

    def calcular(self):
        if not self.expr or self.error:
            return
        limpia = self.expr
        while limpia and limpia[-1] in OPERADORES + ".":
            limpia = limpia[:-1]
        if not limpia:
            return
        formula = limpia.replace("×", "*").replace("÷", "/").replace("−", "-")
        try:
            resultado = evaluar(ast.parse(formula, mode="eval"))
        except ZeroDivisionError:
            self.historial = limpia + " ="
            self.expr = "No se puede dividir entre 0"
            self.error = True
            return
        except Exception:
            self.historial = ""
            self.expr = "Error"
            self.error = True
            return
        self.historial = limpia + " ="
        self.expr = formatear(resultado).replace("-", "−")
        self.terminado = True

    def actualizar(self):
        texto = self.expr if self.expr else "0"
        largo = len(texto)
        if self.error:
            tam = 18
        elif largo > 16:
            tam = 22
        elif largo > 12:
            tam = 28
        elif largo > 9:
            tam = 34
        else:
            tam = 42
        self.lbl_pantalla.config(text=texto, font=("Segoe UI", tam, "bold"))
        self.lbl_historial.config(text=self.historial)

    def tecla(self, evento):
        t = evento.char
        mapa = {"*": "×", "/": "÷", "-": "−", ",": "."}
        if t in mapa:
            t = mapa[t]
        if t.isdigit() or t in OPERADORES or t in ".%":
            self.pulsar(t)
        elif evento.keysym in ("Return", "KP_Enter") or t == "=":
            self.pulsar("=")
        elif evento.keysym == "BackSpace":
            self.pulsar("⌫")
        elif evento.keysym == "Escape" or t.lower() == "c":
            self.pulsar("C")


def main():
    root = tk.Tk()
    Calculadora(root)
    root.mainloop()


if __name__ == "__main__":
    main()
