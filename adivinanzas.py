import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import tkinter as tk

# Carga la red de Kohonen pre-entrenada
# kohonen_network = cargar_red_entrenada()

# Definir las palabras o frases para adivinar
palabras_a_adivinar = ["OTORRINOLARINGOLOGO", "NEUROCIRUJANO", "MATEMATICO", "PROFESOR", "PROGRAMADOR", "FOTOGRAFO"]


class JuegoAdivinanza:
    def __init__(self):
        self.palabra = np.random.choice(palabras_a_adivinar)
        self.intentos = 3
        self.letras_adivinadas = []
        self.palabra_en_juego =  ["_" for i in  range(len(self.palabra))]

    
        
    def adivinar_letra(self, letra):
        #se encuentra palabra
        if letra in self.palabra:
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.palabra_en_juego[i] = letra
            if "_" not in self.palabra_en_juego:
                return "¡Ganaste!"
        #no se encuentra
        else:
            self.intentos -= 1
            dibujar_ahorcado()
            if self.intentos == 0:
                return "¡Perdiste! La palabra era: " + self.palabra
        return "".join(self.palabra_en_juego)
    
   


    def obtener_pista_kohonen(self):
        # Aquí debes consultar la red de Kohonen y obtener la letra más probable
        # basada en la pista actual
        pass
def dibujar_ahorcado():
    pass



class InterfazJuego:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("JUEGO DE ADIVINANZA")
        self.juego = JuegoAdivinanza()

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
        if letra in self.juego.letras_adivinadas:
            return
        self.juego.letras_adivinadas.append(letra)
        resultado = self.juego.adivinar_letra(letra)
        self.label_palabra_juego.config(text=resultado)
        self.label_vidas.config(text=f"vidas: {self.juego.intentos}")

ventana = tk.Tk()
app = InterfazJuego(ventana)
ventana.geometry("500x500")
ventana.mainloop()
