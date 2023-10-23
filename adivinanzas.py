import numpy as np
import tkinter as tk
from tkinter import *
import random
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
    def resolucion_ia(self):
        # Define la longitud de la palabra secreta
        word_length = len(self.palabra)

        # Inicializa la población de soluciones candidatas
        population = []
        for _ in range(100):
            population.append("".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(word_length)))

        # Define la función de aptitud
        def fitness(solution):
            matches = 0
            for i, letter in enumerate(solution):
                if letter == palabras_a_adivinar[0][i]:
                    matches += 1
            return matches

        # Define una función simple de mutación
        def mutate(solution):
            index = random.randint(0, word_length - 1)
            new_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
            return solution[:index] + new_letter + solution[index + 1:]

        # Aplica el algoritmo genético
        for _ in range(1000):
            # Selecciona las soluciones más aptas
            parents = sorted(population, key=fitness, reverse=True)[:2]

            # Cruza las soluciones
            child1 = parents[0][:word_length // 2] + parents[1][word_length // 2:]
            child2 = parents[1][:word_length // 2] + parents[0][word_length // 2:]

            # Muta las soluciones
            child1 = mutate(child1)
            child2 = mutate(child2)

            # Reemplaza las soluciones menos aptas
            population[population.index(min(population, key=fitness))] = child1
            population[population.index(min(population, key=fitness))] = child2

        # Encuentra la solución
        solution = population[population.index(max(population, key=fitness))]
        print(solution)

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
    #resolver con boton IA


    def adivinar(self):
        letra = self.ingresar_letra.get().upper()
        resultado = self.juego.adivinar_letra(letra)
        if letra in self.juego.letras_adivinadas:
            return
    #ingresar forma de cambio IA
        self.juego.letras_adivinadas.append(letra)
        self.label_palabra_juego.config(text=resultado)
        self.label_vidas.config(text=f"vidas: {self.juego.intentos}")


ventana = tk.Tk()
app = InterfazJuego(ventana)
ancho = ventana.winfo_height()
alto = ventana.winfo_width()
ventana.geometry(f"900x500+{ancho + 80}+{alto}")

ventana.mainloop()
