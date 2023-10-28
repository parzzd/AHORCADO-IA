import numpy as np
import tkinter as tk
from tkinter import *
import random
import string

# Define las palabras o frases para adivinar
palabras_a_adivinar = ["FELICIDAD", "TRISTEZA", "SORPRESA", "ALEGRIA", "IGUALDAD", "JUSTICIA", "EDUCACION", "CIENCIA", "TECNOLOGIA", "INTERNET", "COMPUTADORA", "TELEVISION", "DEPORTISTA", "CIENTIFICO", "ABOGADO", "ESTUDIANTE", "JARDIN", "CIUDAD", "INVIERNO", "PRIMAVERA", "CONTINENTE", "OCEANO", "SELVA", "TUNDRA", "ARTICO", "MONTAÑA", "VIAJANTE", "NUBE", "LLUVIOSO", "TORMENTA", "AVENTURA", "HOSPITAL", "RESPLANDOR", "LAMPARA", "SUSPENDER", "CARRETERA", "EDIFICIO", "CAMARERO", "CAMARERA", "CARNAVAL", "DESLIZAR", "ELEGANTE", "FRAGANCIA", "GLADIADOR", "HIPOPOTAMO", "INSECTO", "MARAVILLOSO", "NOCTURNO", "ORQUIDEA", "PASAJERO", "QUESADILLA", "RADIANTE", "SIMPATIA", "TRENZADO", "UNIVERSO", "VENTANA", "YACIMIENTO", "ZAFIRO", "BISONTE", "CASCADA", "DESORDEN", "EJERCICIO", "FRAMBUESA", "GRANJERO", "HUEVO", "IMAGINACION", "JIRAFA", "KILOMETRO", "LOCOMOTORA", "MAMUT", "NARIZ", "OPORTUNO", "PARAGUAS", "QUESADILLA", "REMOLACHA", "SALVAJE", "TELEFONO", "UNICORNIO", "VACACIONES", "XILOFONO", "YOGUR", "ZARZAMORA", "ARQUITECTO", "BUFANDA", "CALIGRAFIA", "DENTISTA", "ELEFANTE", "FLAMENCO", "GACELA", "HELICOPTERO", "INSECTARIO", "JOYERIA", "CONOCIMIENTO", "LENGUAJE", "MACETERO", "NARIZOTA", "OCTOGONO", "PARADIGMA", "QUERIDO", "RESTAURANTE", "SUBMARINO", "TORMENTOSO", "ULTRAVIOLETA", "VENERABLE", "ZAPATERO"]

class JuegoAdivinanza:
    def __init__(self, canvas):
        self.palabra = random.choice(palabras_a_adivinar).upper()
        self.intentos = {"usuario": 5, "ia": 5}
        self.letras_adivinadas = {"usuario": [], "ia": []}
        self.palabra_en_juego = ["_" for _ in range(len(self.palabra))]
        self.canvas = canvas
        self.user_turn = True  # Inicialmente, es el turno del usuario

    def cambiar_turno(self):
        self.user_turn = not self.user_turn

    def dibujar_ahorcado(self):
        if self.intentos["usuario"] == 4:
            # línea
            self.canvas.create_line(350, 60, 350, 400, width=10, fill='green')  # |
            self.canvas.create_line(345, 60, 500, 60, width=10, fill='green')  # ----
            self.canvas.create_line(445, 60, 445, 120, width=10, fill='green')  # |
        elif self.intentos["usuario"] == 3:
            # cabeza
            self.canvas.create_oval(400, 100, 500, 200, width=2, fill='black')
        elif self.intentos["usuario"] == 2:
            # cuerpo
            self.canvas.create_line(445, 195, 445, 300, width=10, fill='black')  # |
        elif self.intentos["usuario"] == 1:
            # piernas
            self.canvas.create_line(445, 300, 395, 335, width=10, fill='black')  # |
            self.canvas.create_line(445, 300, 495, 335, width=10, fill='black')  # |
            # brazos
            self.canvas.create_line(445, 220, 395, 255, width=10, fill='black')  # |
            self.canvas.create_line(445, 220, 495, 255, width=10, fill='black')  # |
        elif self.intentos["usuario"] == 0:
            # cara
            # ojo izquierdo
            self.canvas.create_line(445, 125, 425, 135, width=4, fill='white')  # X
            self.canvas.create_line(425, 125, 445, 135, width=4, fill='white')  # X

            # ojo derecho
            self.canvas.create_line(475, 125, 455, 135, width=4, fill='white')  # X
            self.canvas.create_line(455, 125, 475, 135, width=4, fill='white')  # X
            # boca
            self.canvas.create_line(430, 170, 470, 170, width=5, fill='white')  # -

    def adivinar_letra(self, letra, jugador="usuario"):
        if letra == self.palabra:
            self.palabra_en_juego = list(self.palabra)
            return f"¡{jugador.capitalize()} ganó!"

        if letra and letra in self.palabra:
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.palabra_en_juego[i] = letra
            if "_" not in self.palabra_en_juego:
                return f"¡{jugador.capitalize()} ganó!"
        else:
            self.intentos[jugador] -= 1
            self.dibujar_ahorcado()
            if self.intentos[jugador] == 0:
                return f"¡{jugador.capitalize()} perdió! La palabra era: {self.palabra}"

        return "".join(self.palabra_en_juego)

    def resolucion_ia(self):
        if not self.user_turn:
            # Define la palabra objetivo
            palabra_objetivo = self.palabra

            # Parámetros del algoritmo genético
            tamano_poblacion = 100
            tasa_mutacion = 0.1
            num_generaciones = 1000

            # Función para generar una solución aleatoria
            def generar_solucion(longitud):
                return ''.join(random.choice(string.ascii_uppercase) for _ in range(longitud))

            # Función para evaluar la aptitud de una solución
            def evaluar_aptitud(solucion):
                return sum(1 for i, j in zip(solucion, palabra_objetivo) if i == j)

            # Función para seleccionar padres basados en la aptitud
            def seleccionar_padres(poblacion):
                padres = random.choices(poblacion, k=2, weights=[evaluar_aptitud(solucion) for solucion in poblacion])
                return padres

            # Función para cruzar dos soluciones
            def cruzar(padre1, padre2):
                punto_cruce = random.randint(1, len(padre1) - 1)
                hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
                hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
                return hijo1, hijo2

            # Función para mutar una solución
            def mutar(solucion):
                if random.random() < tasa_mutacion:
                    indice_mutacion = random.randint(0, len(solucion) - 1)
                    nueva_letra = random.choice(string.ascii_uppercase)
                    solucion = solucion[:indice_mutacion] + nueva_letra + solucion[indice_mutacion + 1:]
                return solucion

            # Crear una población inicial aleatoria
            poblacion = [generar_solucion(len(palabra_objetivo)) for _ in range(tamano_poblacion)]

            # Ciclo principal del algoritmo genético
            for generacion in range(num_generaciones):
                nueva_poblacion = []

                for _ in range(tamano_poblacion // 2):
                    # Seleccionar padres y cruzar
                    padre1, padre2 = seleccionar_padres(poblacion)
                    hijo1, hijo2 = cruzar(padre1, padre2)

                    # Aplicar mutación
                    hijo1 = mutar(hijo1)
                    hijo2 = mutar(hijo2)

                    nueva_poblacion.extend([hijo1, hijo2])

                poblacion = nueva_poblacion

                mejor_solucion = max(poblacion, key=evaluar_aptitud)

                print(f"Generación {generacion + 1}: {mejor_solucion} (Aptitud: {evaluar_aptitud(mejor_solucion)})")

            print("Adivinanza completada. Solución encontrada:", mejor_solucion)
            resultado = self.adivinar_letra(mejor_solucion, "ia")
            self.letras_adivinadas["ia"].append(mejor_solucion)
            self.intentos["ia"] -= 1
            return resultado

class InterfazJuego:
    def __init__(self, ventana):
        self.ventana = ventana
        self.canvas = Canvas(width=300, height=210, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.juego = JuegoAdivinanza(self.canvas)

        self.ventana.title("JUEGO DE ADIVINANZA")
        self.label_palabra_juego = tk.Label(ventana, text=" ".join(self.juego.palabra_en_juego))
        self.label_palabra_juego.pack(fill=tk.X)
        self.label_vidas = tk.Label(ventana, text=f"Vidas Usuario: {self.juego.intentos['usuario']} - Vidas IA: {self.juego.intentos['ia']}")
        self.label_vidas.pack(fill=tk.X)
        self.ingresar_letra = tk.Entry(ventana)
        self.ingresar_letra.pack()
        self.boton_adivinar = tk.Button(ventana, text="Adivinar", command=self.adivinar)
        self.boton_adivinar.pack()
        self.boton_cambiar_turno = tk.Button(ventana, text="Cambiar Turno", command=self.cambiar_turno)
        self.boton_cambiar_turno.pack()

    def adivinar(self):
        letra = self.ingresar_letra.get().upper()
        resultado = self.juego.adivinar_letra(letra)
        if letra in self.juego.letras_adivinadas["usuario"]:
            return
        self.juego.letras_adivinadas["usuario"].append(letra)
        self.label_palabra_juego.config(text=resultado)
        self.label_vidas.config(
            text=f"Vidas Usuario: {self.juego.intentos['usuario']} - Vidas IA: {self.juego.intentos['ia']}")
        self.ingresar_letra.delete(0, 'end') 

    def cambiar_turno(self):
        if not self.juego.user_turn and self.juego.intentos["ia"] > 0:
            resultado_ia = self.juego.resolucion_ia()
            self.label_palabra_juego.config(text=resultado_ia)
            self.label_vidas.config(
                text=f"Vidas Usuario: {self.juego.intentos['usuario']} - Vidas IA: {self.juego.intentos['ia']}")
            self.ingresar_letra.config(state="normal")
        self.juego.cambiar_turno()

ventana = tk.Tk()
app = InterfazJuego(ventana)
ancho = ventana.winfo_height()
alto = ventana.winfo_width()
ventana.geometry(f"900x500+{ancho + 80}+{alto}")
ventana.mainloop()
