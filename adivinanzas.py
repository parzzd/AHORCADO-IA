import numpy as np
import tkinter as tk
from tkinter import *

# Define the words or phrases for guessing
palabras_a_adivinar = ["PERRO", "GATO", "RATA"]


class JuegoAdivinanza:
    def __init__(self, canvas):
        self.palabra = np.random.choice(palabras_a_adivinar)
        self.intentos = 5
        self.letras_adivinadas = []
        self.palabra_en_juego = ["_" for _ in range(len(self.palabra))]
        self.canvas = canvas  

    def dibujar_ahorcado(self):
        if self.intentos==4:
        #lineas
            self.canvas.create_line(350, 60, 350, 400, width=10, fill='green')#|
            self.canvas.create_line(345, 60, 500, 60, width=10, fill='green')#----
            self.canvas.create_line(445, 60, 445, 120, width=10, fill='green')#|
        elif self.intentos==3:
        #jeta
            self.canvas.create_oval(400, 100, 500, 200, width=2, fill='black')
        elif self.intentos==2:
        #cuerpo
            self.canvas.create_line(445, 195, 445, 300, width=10, fill='black')#|
        elif self.intentos==1:
        #piernas
            self.canvas.create_line(445, 300, 395, 335, width=10, fill='black')#|
            self.canvas.create_line(445, 300, 495, 335, width=10, fill='black')#|
        #brazos
        
            self.canvas.create_line(445, 220, 395, 255, width=10, fill='black')#|
            self.canvas.create_line(445, 220, 495, 255, width=10, fill='black')#|
        elif self.intentos==0:            
        #cara
            #ojo izq
            self.canvas.create_line(445, 125, 425, 135, width=4, fill='white')#X
            self.canvas.create_line(425, 125, 445, 135, width=4, fill='white')#X
            #ojo der
            self.canvas.create_line(475, 125, 455, 135, width=4, fill='white')#X
            self.canvas.create_line(455, 125, 475, 135, width=4, fill='white')#X    
            #boca
            self.canvas.create_line(430, 170, 470, 170, width=5, fill='white')#-
            
    def adivinar_letra(self, letra):
        if letra == self.palabra:
            self.palabra_en_juego = list(self.palabra)
            return "¡Ganaste!"

        if letra in self.palabra:
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.palabra_en_juego[i] = letra
            if "_" not in self.palabra_en_juego:
                return "¡Ganaste!"
        else:
            self.intentos -= 1
            self.dibujar_ahorcado()
            if self.intentos == 0:
                return "¡Perdiste! La palabra era: " + self.palabra

        return "".join(self.palabra_en_juego)


class InterfazJuego:
    def __init__(self, ventana):
        self.ventana = ventana
        self.canvas = Canvas(width=300, height=210, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.juego = JuegoAdivinanza(self.canvas)

        self.ventana.title("JUEGO DE ADIVINANZA")

        self.label_palabra_juego = tk.Label(ventana, text=" ".join(self.juego.palabra_en_juego))
        self.label_palabra_juego.pack(fill=tk.X)

        self.label_vidas = tk.Label(ventana, text=f"vidas: {self.juego.intentos}")
        self.label_vidas.pack(fill=tk.X)

        self.ingresar_letra = tk.Entry(ventana)
        self.ingresar_letra.pack()

        self.boton_adivinar = tk.Button(ventana, text="Adivinar", command=self.adivinar)
        self.boton_adivinar.pack()

    def adivinar(self):
        letra = self.ingresar_letra.get().upper()
        resultado = self.juego.adivinar_letra(letra)
        if letra in self.juego.letras_adivinadas:
            return

        self.juego.letras_adivinadas.append(letra)
        self.label_palabra_juego.config(text=resultado)
        self.label_vidas.config(text=f"vidas: {self.juego.intentos}")


ventana = tk.Tk()
app = InterfazJuego(ventana)
ancho = ventana.winfo_height()
alto = ventana.winfo_width()
ventana.geometry(f"900x500+{ancho + 80}+{alto}")

ventana.mainloop()
