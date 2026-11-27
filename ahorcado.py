import random
import tkinter as tk
from tkinter import messagebox

MAX_ERRORES = 6
LETRAS = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

BG = "#1e1e2e"
PANEL = "#2a2a3d"
TEXTO = "#e6e6f0"
ACENTO = "#7aa2f7"
VERDE = "#9ece6a"
ROJO = "#f7768e"
AMARILLO = "#e0af68"
BTN = "#3b3b55"
BTN_OFF = "#22222f"

PALABRAS = {
    "Animales": [
        "ELEFANTE", "JIRAFA", "COCODRILO", "MARIPOSA", "DELFIN", "TORTUGA",
        "MURCIELAGO", "CABALLO", "PINGUINO", "CANGURO", "LIBELULA", "ARDILLA",
    ],
    "Frutas": [
        "MANZANA", "PLATANO", "NARANJA", "SANDIA", "MANGO", "FRESA",
        "DURAZNO", "PAPAYA", "GUAYABA", "LIMON", "CEREZA", "MELON",
    ],
    "Países": [
        "MEXICO", "ARGENTINA", "COLOMBIA", "ESPANA", "JAPON", "BRASIL",
        "CANADA", "ALEMANIA", "PORTUGAL", "ECUADOR", "URUGUAY", "ITALIA",
    ],
    "Tecnología": [
        "COMPUTADORA", "TECLADO", "PROGRAMA", "INTERNET", "PANTALLA",
        "ALGORITMO", "VARIABLE", "SERVIDOR", "NAVEGADOR", "PYTHON",
        "BASEDEDATOS", "CELULAR",
    ],
    "Objetos": [
        "REFRIGERADOR", "VENTANA", "ESCRITORIO", "MOCHILA", "LAMPARA",
        "CUCHARA", "ALMOHADA", "ZAPATO", "PARAGUAS", "RELOJ", "TIJERAS",
    ],
}


class Ahorcado:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎮 Juego del Ahorcado")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.victorias = 0
        self.derrotas = 0
        self.categoria = tk.StringVar(value="Animales")

        self.palabra = ""
        self.adivinadas = set()
        self.errores = 0
        self.juego_activo = False
        self.botones = {}

        self._crear_interfaz()
        self.nueva_partida()

        # Teclado físico
        self.root.bind("<Key>", self._tecla_fisica)

    def _crear_interfaz(self):
        tk.Label(
            self.root, text="AHORCADO", font=("Segoe UI", 28, "bold"),
            bg=BG, fg=ACENTO,
        ).pack(pady=(15, 5))

        barra = tk.Frame(self.root, bg=BG)
        barra.pack(fill="x", padx=20)

        tk.Label(barra, text="Categoría:", bg=BG, fg=TEXTO,
                 font=("Segoe UI", 11)).pack(side="left")
        menu = tk.OptionMenu(barra, self.categoria, *PALABRAS.keys(),
                             command=lambda _: self.nueva_partida())
        menu.config(bg=BTN, fg=TEXTO, activebackground=ACENTO,
                    activeforeground="white", highlightthickness=0,
                    font=("Segoe UI", 11), bd=0)
        menu["menu"].config(bg=BTN, fg=TEXTO, font=("Segoe UI", 11))
        menu.pack(side="left", padx=8)

        self.lbl_marcador = tk.Label(
            barra, text="", bg=BG, fg=TEXTO, font=("Segoe UI", 11, "bold"))
        self.lbl_marcador.pack(side="right")

        centro = tk.Frame(self.root, bg=BG)
        centro.pack(pady=10, padx=20)

        self.canvas = tk.Canvas(centro, width=260, height=300, bg=PANEL,
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=(0, 15))

        info = tk.Frame(centro, bg=PANEL, width=300, height=300)
        info.grid(row=0, column=1)
        info.pack_propagate(False)

        self.lbl_intentos = tk.Label(
            info, text="", bg=PANEL, fg=TEXTO, font=("Segoe UI", 13, "bold"))
        self.lbl_intentos.pack(pady=(20, 5))

        self.lbl_falladas = tk.Label(
            info, text="", bg=PANEL, fg=ROJO, font=("Consolas", 13),
            wraplength=270, justify="center")
        self.lbl_falladas.pack(pady=5)

        self.lbl_mensaje = tk.Label(
            info, text="", bg=PANEL, fg=AMARILLO, font=("Segoe UI", 12, "bold"),
            wraplength=270, justify="center")
        self.lbl_mensaje.pack(pady=10)

        self.btn_pista = tk.Button(
            info, text="💡 Pista (-1 intento)", command=self.pedir_pista,
            bg=AMARILLO, fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
            bd=0, padx=10, pady=6, cursor="hand2")
        self.btn_pista.pack(pady=(10, 5))

        tk.Button(
            info, text="🔄 Nueva palabra", command=self.nueva_partida,
            bg=ACENTO, fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
            bd=0, padx=10, pady=6, cursor="hand2").pack(pady=5)

        self.lbl_palabra = tk.Label(
            self.root, text="", font=("Consolas", 30, "bold"),
            bg=BG, fg=TEXTO)
        self.lbl_palabra.pack(pady=10)

        teclado = tk.Frame(self.root, bg=BG)
        teclado.pack(pady=(0, 20), padx=20)

        columnas = 9
        for i, letra in enumerate(LETRAS):
            b = tk.Button(
                teclado, text=letra, width=3, height=1,
                font=("Segoe UI", 13, "bold"), bg=BTN, fg=TEXTO,
                activebackground=ACENTO, activeforeground="white",
                bd=0, cursor="hand2",
                command=lambda l=letra: self.adivinar(l))
            b.grid(row=i // columnas, column=i % columnas, padx=3, pady=3)
            self.botones[letra] = b

    def nueva_partida(self):
        self.palabra = random.choice(PALABRAS[self.categoria.get()])
        self.adivinadas = set()
        self.errores = 0
        self.juego_activo = True
        self.lbl_mensaje.config(text="¡Adivina la palabra!", fg=AMARILLO)
        self.btn_pista.config(state="normal")
        for b in self.botones.values():
            b.config(state="normal", bg=BTN, fg=TEXTO)
        self._actualizar()

    def adivinar(self, letra: str):
        if not self.juego_activo or letra in self.adivinadas:
            return

        self.adivinadas.add(letra)
        boton = self.botones[letra]

        if letra in self.palabra:
            boton.config(state="disabled", bg=VERDE, fg="#1e1e2e",
                         disabledforeground="#1e1e2e")
        else:
            self.errores += 1
            boton.config(state="disabled", bg=ROJO, fg="#1e1e2e",
                         disabledforeground="#1e1e2e")

        self._actualizar()
        self._revisar_fin()

    def pedir_pista(self):
        if not self.juego_activo:
            return
        if self.errores >= MAX_ERRORES - 1:
            self.lbl_mensaje.config(
                text="No puedes pedir pista con 1 intento.", fg=ROJO)
            return

        ocultas = [l for l in set(self.palabra) if l not in self.adivinadas]
        if not ocultas:
            return

        letra = random.choice(ocultas)
        self.errores += 1  
        self.adivinadas.add(letra)
        self.botones[letra].config(state="disabled", bg=AMARILLO,
                                   fg="#1e1e2e", disabledforeground="#1e1e2e")
        self.lbl_mensaje.config(text=f"Pista: la letra «{letra}»", fg=AMARILLO)
        self._actualizar()
        self._revisar_fin()

    def _revisar_fin(self):
        if all(l in self.adivinadas for l in self.palabra):
            self.juego_activo = False
            self.victorias += 1
            self.lbl_mensaje.config(text="🎉 ¡GANASTE!", fg=VERDE)
            self._actualizar()
            self._terminar("¡Felicidades!", f"¡Ganaste! La palabra era {self.palabra}.")
        elif self.errores >= MAX_ERRORES:
            self.juego_activo = False
            self.derrotas += 1
            self.lbl_mensaje.config(
                text=f"💀 Perdiste. Era: {self.palabra}", fg=ROJO)
            self._actualizar()
            self._terminar("Fin del juego", f"Perdiste. La palabra era {self.palabra}.")

    def _terminar(self, titulo, texto):
        for b in self.botones.values():
            b.config(state="disabled")
        self.btn_pista.config(state="disabled")
        if messagebox.askyesno(titulo, f"{texto}\n\n¿Jugar otra vez?"):
            self.nueva_partida()

    def _tecla_fisica(self, evento):
        letra = evento.char.upper()
        if letra in self.botones:
            self.adivinar(letra)

    def _actualizar(self):

        texto = " ".join(l if l in self.adivinadas else "_" for l in self.palabra)
        self.lbl_palabra.config(text=texto)

        restantes = MAX_ERRORES - self.errores
        self.lbl_intentos.config(text=f"Intentos restantes: {restantes}")
        falladas = sorted(l for l in self.adivinadas if l not in self.palabra)
        self.lbl_falladas.config(
            text="Falladas: " + (" ".join(falladas) if falladas else "—"))
        self.lbl_marcador.config(
            text=f"🏆 {self.victorias}   ☠ {self.derrotas}")

        self._dibujar_ahorcado()

    def _dibujar_ahorcado(self):
        c = self.canvas
        c.delete("all")
        color = TEXTO


        c.create_line(30, 270, 170, 270, width=5, fill=color)   # base
        c.create_line(60, 270, 60, 30, width=5, fill=color)     # poste
        c.create_line(60, 30, 170, 30, width=5, fill=color)     # viga
        c.create_line(60, 70, 90, 30, width=4, fill=color)      # soporte
        c.create_line(170, 30, 170, 65, width=3, fill=AMARILLO) # cuerda

        e = self.errores
        if e >= 1:  # cabeza
            c.create_oval(145, 65, 195, 115, width=3, outline=ROJO)
        if e >= 2:  # cuerpo
            c.create_line(170, 115, 170, 190, width=3, fill=ROJO)
        if e >= 3:  # brazo izquierdo
            c.create_line(170, 130, 140, 165, width=3, fill=ROJO)
        if e >= 4:  # brazo derecho
            c.create_line(170, 130, 200, 165, width=3, fill=ROJO)
        if e >= 5:  # pierna izquierda
            c.create_line(170, 190, 145, 235, width=3, fill=ROJO)
        if e >= 6:
            c.create_line(170, 190, 195, 235, width=3, fill=ROJO)
            c.create_text(160, 85, text="x", fill=ROJO, font=("Consolas", 12, "bold"))
            c.create_text(180, 85, text="x", fill=ROJO, font=("Consolas", 12, "bold"))


def main():
    root = tk.Tk()
    Ahorcado(root)
    root.mainloop()


if __name__ == "__main__":
    main()
