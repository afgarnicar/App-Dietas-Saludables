from tkinter import *
from tkinter import messagebox

# Ventana de inicio de sesión
class App1(Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion de nutrición")
        self.geometry("300x250")
        self.resizable(False, False)
        self.bind('<Escape>', lambda e: self.quit())
        self.configure(bg="white")
        self.font = "Arial"

        self.tituloPrincipal = Label(self, text="Bienvenido", bg="white", fg="black", font=(self.font, 20))
        self.tituloPrincipal.pack(pady=20)

        self.botonRegistro = Button(
            text="Registrate",
            font=(self.font, 12),
            command=self.vaina,
        )
        self.botonRegistro.pack(pady=10)

        self.botonInicio = Button(
            text="Iniciar Sesión",
            font=(self.font, 12),
            command=self.vaina2,
        )
        self.botonInicio.pack(pady=10)

    def abrir_app2(self, name, contrasena):
        self.destroy()
        app2 = App2(name, contrasena)
        app2.mainloop()  

    def createTopLevel(self, whatIsfor=""):
        self.nwWindow = Toplevel(self)
        self.nwWindow.title("Authentication")
        self.nwWindow.geometry("500x500+800+100")
        if whatIsfor == "Register":
            self.registerWin()
        elif whatIsfor == "Login":
            self.loginWin()

    def closeTopLevel(self):
        self.nwWindow.destroy()
        self.nwWindow.update()

    def vaina(self):
        self.createTopLevel("Register")
    
    def vaina2(self):
        self.createTopLevel("Login")

    def registerWin(self):
        self.titulo = Label(self.nwWindow, text="Registro", font=(self.font, 20))
        self.titulo.pack(pady=20)

        numero = Label(self.nwWindow, text="Numero de identificacion", font=(self.font, 12))
        numero.pack(pady=10)

        self.numeroEntry = Entry(self.nwWindow, font=(self.font, 12))
        self.numeroEntry.pack()

        name = Label(self.nwWindow, text="Nombre", font=(self.font, 12))
        name.pack(pady=10)

        self.nameEntry = Entry(self.nwWindow, font=(self.font, 12))
        self.nameEntry.pack()

        contrasena = Label(self.nwWindow, text="Contraseña", font=(self.font, 12))
        contrasena.pack(pady=10)

        self.contrasenaEntry = Entry(self.nwWindow, font=(self.font, 12), show="*")
        self.contrasenaEntry.pack()


        self.genero_var = StringVar()
        self.genero_var.set("Otro")

        genero = Label(self.nwWindow, text="Genero", font=(self.font, 12))
        genero.pack(pady=10)

        opciones_genero = ["Masculino", "Femenino", "Otro"]
        for genero in opciones_genero:
            Radiobutton(self.nwWindow, text=genero, variable=self.genero_var, value=genero).pack()

        self.botonRegistro = Button(
            self.nwWindow,
            text="Registrarse",
            font=(self.font, 12),
            command=self.register
        )
        self.botonRegistro.pack(pady=10)

    def register(self):
        name = self.nameEntry.get()
        contrasena = self.contrasenaEntry.get()
        genero = self.genero_var.get()
        numero = self.numeroEntry.get()
        open("usuarios.txt", "a").write(f"{numero},{name},{contrasena},{genero}\n")
        messagebox.showinfo("Registro", "Usuario registrado con exito")
        self.closeTopLevel()

    def loginWin(self):
        self.titulo = Label(self.nwWindow, text="Inicio de Sesión", font=(self.font, 20))
        self.titulo.pack(pady=20)

        name = Label(self.nwWindow, text="Nombre", font=(self.font, 12))
        name.pack(pady=10)

        self.nameEntry = Entry(self.nwWindow, font=(self.font, 12))
        self.nameEntry.pack()

        contrasena = Label(self.nwWindow, text="Contraseña", font=(self.font, 12))
        contrasena.pack(pady=10)

        self.contrasenaEntry = Entry(self.nwWindow, font=(self.font, 12), show="*")
        self.contrasenaEntry.pack()

        self.botonInicio = Button(
            self.nwWindow,
            text="Iniciar Sesión",
            font=(self.font, 12),
            command=self.login
        )
        self.botonInicio.pack(pady=10)

    def login(self):
        name = self.nameEntry.get()
        contrasena = self.contrasenaEntry.get()
        try:
            usuarios = open("usuarios.txt", "r").read().split("\n")
            for usuario in usuarios:
                if usuario == "":
                    continue
                usuario = usuario.split(",")
                if usuario[1] == name and usuario[2] == contrasena:
                    messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
                    self.closeTopLevel()
                    self.abrir_app2(name,contrasena)
                    return
            messagebox.showerror("Inicio de Sesión", "Nombre de usuario o contraseña incorrectos")
        except FileNotFoundError:
            messagebox.showerror("Inicio de Sesión", "No hay usuarios registrados")
            self.closeTopLevel()


class App2(Tk):
    def __init__(self, name, contrasena):
        super().__init__()
        self.title("Página principal")
        self.geometry("800x750+350+0")
        # self.resizable(False, False)
        self.bind('<Escape>', lambda e: self.quit())
        self.configure(bg="white")
        self.usu = name
        self.con = contrasena
        self.imc = None
        self.myFlag = True

        self.tituloPrincipal = Label(self, text=f"Bienvenido {self.usu.capitalize()}", bg="white", fg="black", font=("Arial", 20))
        self.tituloPrincipal.pack(pady=15)

        try:
            usuarios = open("dietas.txt", "r").read().split("\n")
            for usuario in usuarios:
                if usuario == "":
                    continue
                usuario = usuario.split(",")
                if usuario[0] == self.usu and usuario[1] == self.con:
                    self.myFlag = False
                    self.dieta = Label(self, text=f"Dieta asignada: \n{usuario[2]}", bg="white", fg="black", font=("Arial", 12))
                    self.dieta.pack()
                    self.descripcionDieta = Label(self, text="", font=("Arial", 10))
                    self.descripcionDieta.pack()
                    self.masDieta(usuario)
                    break
            if self.myFlag: 
                self.dieta = Label(self, text="No hay dieta asignada", bg="white", fg="black", font=("Arial", 12))
                self.dieta.pack()
                self.descripcionDieta = Label(self, text="", font=("Arial", 10))
                self.descripcionDieta.pack()
        except FileNotFoundError:
            messagebox.showerror("Error:", "No hay archivos de usuarios registrados")
            self.closeTopLevel()

        self.tituloCal = Label(self, text=f"Calculadora IMC", bg="white", fg="black", font=("Arial", 16))
        self.tituloCal.pack(pady=20)

        self.estatura = Label(self, text="Estatura (cm)", font=("Arial", 12))
        self.estatura.pack(pady=10)
        
        self.estaturaEntry = Entry(self, font=("Arial", 12))
        self.estaturaEntry.pack()
        
        self.peso = Label(self, text="Peso (kg)", font=("Arial", 12))
        self.peso.pack(pady=10)
        
        self.pesoEntry = Entry(self, font=("Arial", 12))
        self.pesoEntry.pack()
        
        self.botonCal = Button(
            self,
            text="Calcular",
            font=("Arial", 12),
            command=self.calcular
        )
        self.botonCal.pack(pady=10)

        self.resultado = Label(self, text=f"Tu IMC es: {self.imc}", font=("Arial", 12))
        self.resultado.pack(pady=10)

    def clasificarIMC(self):
        if self.imc < 18.5:
            self.code = 0
            self.dieta.config(text="Dieta asignada: \nTu índice de masa corporal es bajo. Debes considerar aumentar tu consumo calórico.")
        elif 18.5 <= self.imc and self.imc < 24.9:
            self.code = 1
            self.dieta.config(text="Dieta asignada: \nTienes un peso normal. ¡Sigue manteniendo un estilo de vida saludable!")
        elif 25 <= self.imc and self.imc < 29.9:
            self.code = 2
            self.dieta.config(text="Dieta asignada: \nTienes sobrepeso. Debes considerar reducir tu consumo calórico y aumentar la actividad física.")
        else:
            self.code = 3
            self.dieta.config(text="Dieta asignada: \nTienes obesidad. Es importante que consultes a un profesional para mejorar tu salud.")
        
        self.masDieta(otro=self.code)

        if self.myFlag:
            with open("dietas.txt", "a") as f:
                f.write(f"{self.usu},{self.con},{self.dieta['text'].split("\n")[1]},{self.code}\n")
        else:
            usuarios = open("dietas.txt", "r").read().split("\n")
            for i in range(len(usuarios)):
                if usuarios[i] == "":
                    continue
                usuario = usuarios[i].split(",")
                if usuario[0] == self.usu and usuario[1] == self.con:
                    usuarios[i] = f"{usuario[0]},{usuario[1]},{str(self.dieta['text'].split("\n")[1])},{self.code}"
                    break
            with open("dietas.txt", 'w') as archivo:
                for usuario in usuarios:
                    archivo.write(usuario + "\n")


    def calcular(self):
        peso = int(self.pesoEntry.get())
        estatura = float(self.estaturaEntry.get())
        self.imc = peso / (estatura/100)**2
        self.imc = round(self.imc, 2)
        self.resultado.config(text=f"Tu IMC es: {self.imc}")
        self.clasificarIMC()
        self.myFlag = False

    def masDieta(self, usuario=None, otro=None):
        if usuario:
            if usuario[3] == "0":
                self.descripcionDieta.config(text=f"Desayuno:\n2 huevos revueltos con queso, 2 rebanadas de pan intregal con mantequilla de maní,1 taza de leche\nMedia manaña: \n 1 porción de fruta, 1 puñado de frutos secos\nAlmuerzo: \n 200 gramos de carne magra, pollo o pescado, 1 taza de arroz integral, 1 taza de verduras\nMerienda: \n 1 batido de frutas con leche\nCena: \n 250 gramos de carne, pollo o pescado, 1 taza de pasta integal, 1 taza de verduras\nConsejos: \n 1. Si tienes problemas para comer mucho, prueba a comer bocados pequeños con frecuencia \n 2. No te saltes ninguna comida\n 3. Beba mucha agua")
            elif usuario[3] == "1":
                self.descripcionDieta.config(text=f"Desayuno: \n2 huevos revueltos con verduras, 1 taza de avena con leche descremada y fruta\nMedia mañana: \n 1 porción de fruta, 1 puñado de frutos secos\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n yogur natural con fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Consume una variedad de alimentos de todos los grupos alimenticios \n 2. Elige alimentos integrales y sin procesar \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Beba mucha agua")
            elif usuario[3] == "2":
                self.descripcionDieta.config(text=f"Desayuno: \n 2 huevos revueltos con verduras, 1 taza de avena com leche descremada y fruta\nMedia mañana: \n 1 taza de yogur natural con fruta\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n 1 pieza de fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Crea un déficit calórico de 500-1000 calorías diarias. Esto significa que debes quemar más calorías de las que consumes. Puedes hacerlo reduciendo tu ingesta calórica o aumentando tu actividad física \n 2. No te saltes ninguna comida \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Elige alimentos integrales y sin procesar \n 5. Beba mucha agua")
            else:
                self.descripcionDieta.config(text=f"Desayuno: \n 2 huevos revueltos con verduras, 1 taza de avena com leche descremada y fruta\nMedia mañana: \n 1 taza de yogur natural con fruta\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n 1 pieza de fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Crea un déficit calórico de 500-1000 calorías diarias. Esto significa que debes quemar más calorías de las que consumes. Puedes hacerlo reduciendo tu ingesta calórica o aumentando tu actividad física \n 2. No te saltes ninguna comida \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Elige alimentos integrales y sin procesar \n 5. Beba mucha agua")
        else:
            if otro == 0:
                self.descripcionDieta.config(text=f"Desayuno:\n2 huevos revueltos con queso, 2 rebanadas de pan intregal con mantequilla de maní,1 taza de leche\nMedia manaña: \n 1 porción de fruta, 1 puñado de frutos secos\nAlmuerzo: \n 200 gramos de carne magra, pollo o pescado, 1 taza de arroz integral, 1 taza de verduras\nMerienda: \n 1 batido de frutas con leche\nCena: \n 250 gramos de carne, pollo o pescado, 1 taza de pasta integal, 1 taza de verduras\nConsejos: \n 1. Si tienes problemas para comer mucho, prueba a comer bocados pequeños con frecuencia \n 2. No te saltes ninguna comida\n 3. Beba mucha agua")
            elif otro == 1:
                self.descripcionDieta.config(text=f"Desayuno: \n2 huevos revueltos con verduras, 1 taza de avena con leche descremada y fruta\nMedia mañana: \n 1 porción de fruta, 1 puñado de frutos secos\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n yogur natural con fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Consume una variedad de alimentos de todos los grupos alimenticios \n 2. Elige alimentos integrales y sin procesar \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Beba mucha agua")
            elif otro == 2:
                self.descripcionDieta.config(text=f"Desayuno: \n 2 huevos revueltos con verduras, 1 taza de avena com leche descremada y fruta\nMedia mañana: \n 1 taza de yogur natural con fruta\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n 1 pieza de fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Crea un déficit calórico de 500-1000 calorías diarias. Esto significa que debes quemar más calorías de las que consumes. Puedes hacerlo reduciendo tu ingesta calórica o aumentando tu actividad física \n 2. No te saltes ninguna comida \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Elige alimentos integrales y sin procesar \n 5. Beba mucha agua")
            else:
                self.descripcionDieta.config(text=f"Desayuno: \n 2 huevos revueltos con verduras, 1 taza de avena com leche descremada y fruta\nMedia mañana: \n 1 taza de yogur natural con fruta\nAlmuerzo: \n 200 gramos de pescado a la plancha con verduras al vapor, 1 taza de arroz integral\nMerienda: \n 1 pieza de fruta\nCena: \n 250 gramos de pollo a la parrilla con ensalada\nConsejos: \n 1. Crea un déficit calórico de 500-1000 calorías diarias. Esto significa que debes quemar más calorías de las que consumes. Puedes hacerlo reduciendo tu ingesta calórica o aumentando tu actividad física \n 2. No te saltes ninguna comida \n 3. Limita el consumo de alimentos procesados, azúcares añadidos y grasas saturadas y trans \n 4. Elige alimentos integrales y sin procesar \n 5. Beba mucha agua")

if __name__ == "__main__":
    
    iniciado = False
    login = App1()
    login.mainloop()