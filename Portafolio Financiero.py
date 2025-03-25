import random
from tkinter import *
from tkinter import ttk


prob_cruce = 0.8
prob_mutacion = 0.03

inversion_max = 0
inversion_min = 0

ventana = Tk()
salario = IntVar()
perfil_n = StringVar()
nombre = StringVar()
correo = StringVar()
d_perfil = StringVar()
m_cromosoma = StringVar()
n_iteracion = IntVar()
n_poblacion = IntVar()
n_generaciones = IntVar()

salario.set(100)
perfil_n.set(0)
n_poblacion.set(10)
n_generaciones.set(1)

main_frame = Frame(ventana)
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
Result_frame = ttk.LabelFrame(main_frame, padding="20 10 20 10", style='My.TFrame')

def algoritmo_genetico():
    perfil = float(perfil_n.get())
    #Consrvador
    if perfil<=2.9 and perfil>=0.0:
        inversion_max = 10
        inversion_min = 5
        d_perfil.set("Conservador")
    #Conservador-Moderado
    if perfil<=4.49 and perfil>=3.0:
        inversion_max = 15
        inversion_min = 10
        d_perfil.set("Conservador - Agresivo")
    #Moderado
    if perfil<=6.49 and perfil>=4.5:
        inversion_max = 20
        inversion_min = 10
        d_perfil.set("Moderado")
    #Moderado-Agresivo
    if perfil<=8.49 and perfil>=6.5:
        inversion_max = 25
        inversion_min = 15
        d_perfil.set("Moderado-Agresivo")
    #Agresivo
    if perfil<=10.0 and perfil>=8.5:
        inversion_max = 30
        inversion_min = 20
        d_perfil.set("Agresivo")

    portafolio = [
                {"item" : "vivienda", "min" : 25, "max" : 40},
                {"item" : "emergencia", "min" : 0, "max" : 10},
                {"item" : "inversion", "min" : inversion_min, "max" : inversion_max},
                {"item" : "reduccion de gastos", "min" : 0, "max" : 5},
                {"item" : "educacion", "min" : 0, "max" : 20},
                {"item" : "alimentacion", "min" : 15, "max" : 25},
                {"item" : "ocio", "min" : 0, "max" : 10}
            ]

    poblacion = []
    for _ in range(n_poblacion.get()):
        cromosoma = []
        for i in portafolio:
            min_val = i.get("min")
            max_val = i.get("max")
            cromosoma.append(random.randint(min_val, max_val))
        poblacion.append(cromosoma)

    print("-------Poblacion Inicial-------")
    for i in range(n_poblacion.get()):
        print(poblacion[i])
    print("\n")

    def calcular_aptitud(cromosoma):
        porcentaje_total = 0
        salario_total = 0
        for i, objeto in enumerate(portafolio):
            porcentaje_total += cromosoma[i]
            if cromosoma[i]<=objeto["max"] and cromosoma[i]>=objeto["min"]:
                salario_total += (salario.get() * cromosoma[i] / 100)

        if porcentaje_total > 100:
            return 0
        else:
            return salario_total
    #Calcula el fitness del cromosoma si cumple con ganacias altas siguiendo la restricción del peso max
    #Si rompe la restriccion sera 0 ya q no nos sirve


    def seleccion(poblacion):
        aptitud =  [calcular_aptitud(c) for c in poblacion]
        #if sum(aptitud) == 0:
        #     aptitud = [1e-6] * len(poblacion)
        #return random.choices(poblacion, weights=aptitud, k=2)
        return random.choices(poblacion, weights=[calcular_aptitud(c) for c in poblacion], k=2)
    #Seleciona dos padres k=2 de la poblacion, esto con la fucnion weghts tomando las ganacias mas altas

    def cruce(padre1, padre2):
        if random.random() < prob_cruce:
            punto_cruce = random.randint(1, len(padre1) - 1)
            #genera un numero aleatorio entre 1 y el tamaño del cromosoma -1, esto como punto de corte para la siguiente generación
            hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
            hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
            return hijo1, hijo2
        else:
            return padre1, padre2
    #Genera el cruce de los cromosomas padre, corta una porcion de ambos y las une en uno nuev (cuerpo de padre 1, cabeza de padre 2)

    def mutacion(cromosoma):
        for i in range(len(cromosoma)):
            if random.random() < prob_mutacion:
                cromosoma[i] = 100 - random.randint(0,40)
        return cromosoma
    #Genera una mutación en todo el cromosoma, si es 0 lo vuelve 1 y si es 1 lo vuelve 0

    mejor_cromosoma = None
    mejor_aptitud = 0
    generacion_mejor_cromosoma = 0
    iteracion_mejor_cromosoma = 0
    j=1

    for generacion in range(n_generaciones.get()):
        nueva_poblacion = []
        for _ in range(n_poblacion.get() // 2):
            padre1, padre2 = seleccion(poblacion)
            hijo1, hijo2 = cruce(padre1, padre2)
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)
            nueva_poblacion.extend([hijo1, hijo2])
        poblacion = nueva_poblacion

    #--------------------------------------------------------------------------------    
        print("Padre 1: ", padre1)
        print("Padre 2: ", padre2)
        print("Hijo 1: ", hijo1)
        print("Hijo 2: ", hijo2)
        print("-------Población Generación ",generacion+1, "--------")
        for i in range(n_poblacion.get()):
            print(poblacion[i])
        print("\n")
    #--------------------------------------------------------------------------------

        for cromosoma in poblacion:
            aptitud = calcular_aptitud(cromosoma)
            j += 1
            if aptitud > mejor_aptitud:
                mejor_aptitud = aptitud
                mejor_cromosoma = cromosoma
                m_cromosoma.set(mejor_cromosoma)
                generacion_mejor_cromosoma = generacion+1
                iteracion_mejor_cromosoma = j
                n_iteracion.set(iteracion_mejor_cromosoma)

    GenerarInforme(mejor_cromosoma, portafolio)
    
    print("\nMejor solucion:", mejor_cromosoma)
    print("Ganancia maxima:", mejor_aptitud)
    print("Generacion del mejor cromosoma:", generacion_mejor_cromosoma)
    print("Número de tteraciones:", iteracion_mejor_cromosoma)

def LimpiarInformarcion():
    salario.set(100)
    n_poblacion.set(10)
    n_generaciones.set(1)
    perfil_n.set(0)
    nombre.set(None)
    correo.set(None)
    d_perfil.set(None)
    m_cromosoma.set(None)
    n_iteracion.set(0)
    for widget in Result_frame.winfo_children():
        widget.destroy()
    ventana.geometry("390x500")


def GenerarInforme(cromosoma, portafolio):
    ventana.geometry("390x760")
    Result_frame.grid(column=0, row=13, columnspan=6, rowspan=10, sticky=(N, W, E, S))
    ttk.Label(Result_frame, text="Sr/ Sra " + nombre.get() + ", a continuación se presenta tu Portafolio:", background='#c6c6c6').grid(column=0, row=0, columnspan=5, sticky=W, pady=(0, 0))
    
    ttk.Label(Result_frame, text="Perfil:", background='#c6c6c6').grid(column=0, row=1, sticky=W, pady=(10, 10))
    ttk.Label(Result_frame, textvariable=d_perfil, background='#c6c6c6').grid(column=1, row=1, columnspan=3, sticky=W, pady=(10, 10))
    
    ttk.Label(Result_frame, text="El mejor cromosoma: ", background='#c6c6c6').grid(column=0, row=2, sticky=W, pady=(0, 10))
    ttk.Label(Result_frame, textvariable=m_cromosoma, background='#c6c6c6').grid(column=1, row=2, columnspan=3, sticky=W, pady=(0, 10))
    
    ttk.Label(Result_frame, text="Número de iteraciones: ", background='#c6c6c6').grid(column=0, row=3, sticky=W, pady=(0, 10))
    ttk.Label(Result_frame, textvariable=n_iteracion, background='#c6c6c6').grid(column=1, row=3, sticky=W, pady=(0, 10))
    porcentaje_total = 0
    j = 0
    for i, objeto in enumerate(portafolio):
        porcentaje_total += cromosoma[i]
        ttk.Label(Result_frame, text=objeto["item"], background='#c6c6c6').grid(column=0, row=(4+i), sticky=W, pady=(0, 10))
        ttk.Label(Result_frame, text=(salario.get() * cromosoma[i] / 100), background='#c6c6c6').grid(column=1, row=(4+i), sticky=W, pady=(0, 10)) 
        j = i
    
    ttk.Label(Result_frame, text="Porcentaje Consumido: ", background='#c6c6c6').grid(column=0, row=(5+j), columnspan=4, sticky=W, pady=(0, 10))
    ttk.Label(Result_frame, text=porcentaje_total, background='#c6c6c6').grid(column=1, row=(5+j), sticky=W, pady=(0, 10))


def Interface_Grafica():
    #Canva Resultado
    s = ttk.Style()
    s.configure('My.TFrame', background='#c6c6c6', color='black')

    #Canvas_Frame
    ttk.Label(main_frame, text="!Hola!").grid(column=0, row=0, columnspan=2, sticky=(W,E), pady=(10, 10))
    ttk.Label(main_frame, text="Para empezar necesitamos que ingrese la siguiente información").grid(row=1, column=0, columnspan=7, sticky=(E,W), pady=(10, 0))
    #Información Personal
    ttk.Label(main_frame, text="Nombre: "). grid(column=0, row=2, sticky=(E), pady=(10, 0))
    nombre_Entry = ttk.Entry(main_frame, width=30, textvariable=nombre)
    nombre_Entry.grid(column=1, row=2, pady=(10, 0))
    nombre_Entry.focus()
    ttk.Label(main_frame, text="Correo: "). grid(column=0, row=3, sticky=(E), pady=(10, 0))
    mail_Entry = ttk.Entry(main_frame, width=30, textvariable=correo)
    mail_Entry.grid(column=1, row=3, pady=(10, 0))
    ttk.Label(main_frame, text="Salario Base: "). grid(column=0, row=4, sticky=(E), pady=(10, 0))
    salario_Entry = ttk.Entry(main_frame, width=30, textvariable=salario)
    salario_Entry.grid(column=1, row=4, pady=(10, 0))
    ttk.Label(main_frame, text="Perfil Financiero: "). grid(column=0, row=5, sticky=(E), pady=(10, 0))
    ttk.Label(main_frame, text="normalizado"). grid(column=0, row=6, sticky=(E), pady=(0, 0))
    perfil_Entry = ttk.Entry(main_frame, width=30, textvariable=perfil_n)
    perfil_Entry.grid(column=1, row=5, rowspan=2, sticky=(N,S), pady=(10, 0))
    ttk.Label(main_frame, text="______________________________________________________________________________"). grid(column=0, row=7, columnspan=10, sticky=(E), pady=(10, 0))
    ttk.Label(main_frame, text="Población: "). grid(column=0, row=8, sticky=(E), pady=(10, 0))
    poblacion_Entry = ttk.Entry(main_frame, width=30, textvariable=n_poblacion)
    poblacion_Entry.grid(column=1, row=8, pady=(10, 0))
    ttk.Label(main_frame, text="Generaciones: "). grid(column=0, row=9, sticky=(E), pady=(10, 0))
    generaciones_Entry = ttk.Entry(main_frame, width=30, textvariable=n_generaciones)
    generaciones_Entry.grid(column=1, row=9, pady=(10, 0))
    ttk.Label(main_frame, text="______________________________________________________________________________"). grid(column=0, row=10, columnspan=10, sticky=(E), pady=(10, 0))

    ttk.Button(main_frame, text="Generar Portafolio", width=10, padding="0 5 0 5", command=algoritmo_genetico).grid(column=0, row=11, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))
    ttk.Button(main_frame, text="Limpiar", width=15, padding="0 5 0 5", command=LimpiarInformarcion).grid(column=3, row=11, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))
    ttk.Label(main_frame, text="______________________________________________________________________________"). grid(column=0, row=12, columnspan=10, sticky=(E), pady=(0, 0))
    

    ventana.mainloop()

def main():
    ventana.geometry("390x500")
    ventana.title("Portafolio Financiero")
    Interface_Grafica()

if __name__ == "__main__":
    main()

