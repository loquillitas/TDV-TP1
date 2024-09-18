class Estado:
    def __init__(self, instancia, capacidades_maquinas):
        self.capacidades_de_las_maquinas = list(capacidades_maquinas)  # Lista de capacidades de las máquinas
        self.beneficio_actual = 0  # Beneficio acumulado
        self.mejor_beneficio = 0  # Mejor beneficio encontrado
        self.Instancia = instancia  # Lista de tuplas (beneficio, GPUs necesarias)
        self.asignaciones = [0] * len(instancia)  # Asignaciones actuales
        self.mejor_asignacion = [0] * len(instancia)  # Mejor asignación encontrada



def PD(i, c1, c2, estado, memo):

    # Caso base: no hay más instancias o no hay mas capacidad
    if i < 0 or (c1 <= 0 and c2 <= 0):
        return 0

    # si los gpu necesarios son negativos, paso a la siguiente instancia
    if estado.Instancia[i][1] < 0:
        return PD(i - 1, c1, c2, estado, memo)
        
    # si alguna maquina tiene capacidad negativa, la seteamos a 0
    if c1 < 0:
        c1 = 0
    if c2 < 0:
        c2 = 0
        
    # Si ya calculamos el valor, lo retornamos
    if memo[i][c1][c2] != -1:    #     elif i != 0 and c1 > 0 and c2 > 0 and memo[i][c1][c2] != -1:
        return memo[i][c1][c2]
    
    # Si la instancia no cabe en ninguna máquina, no la agregamos
    if estado.Instancia[i][1] > c1 and estado.Instancia[i][1] > c2:
        memo[i][c1][c2] = PD(i - 1, c1, c2, estado, memo)

    # Si la instancia cabe en ambas máquinas, vemos si (1) No agregarla, (2) Agregarla a la máquina 1 o (3) Agregarla a la máquina 2
    if estado.Instancia[i][1] <= c1 and estado.Instancia[i][1] <= c2:
        memo[i][c1][c2] = max(
            memo[i - 1][c1][c2],  #(1)
            estado.Instancia[i][0] + PD(i - 1, c1 - estado.Instancia[i][1], c2, estado, memo), #(2)
            estado.Instancia[i][0] + PD(i - 1, c1, c2 - estado.Instancia[i][1], estado, memo)  #(3)
        )

    # Si la instancia cabe en la máquina 1, vemos si (1) No agregarla o (2) Agrergarla 
    elif (estado.Instancia[i][1] <= c1 and estado.Instancia[i][1] > c2):
        memo[i][c1][c2] = max(
            PD(i - 1, c1, c2, estado, memo),  #(1)
            estado.Instancia[i][0] + PD(i - 1, c1 - estado.Instancia[i][1], c2, estado, memo)  #(2)
        )
    
    # Si la instancia cabe en la máquina 2, vemos si (1) No agregarla o (3) Agrergarla
    elif (estado.Instancia[i][1] <= c2 and estado.Instancia[i][1] > c1):
        memo[i][c1][c2] = max(
            PD(i - 1, c1, c2, estado, memo),  #(1)
            estado.Instancia[i][0] + PD(i - 1, c1, c2 - estado.Instancia[i][1], estado, memo)  #(3)
        )
    

    return memo[i][c1][c2]



# MOXILA DINAMICA #
def moxila(i, W, w, p, pd):  # i: cantidad de objetos, W: peso máximo, w: pesos, p: beneficios, pd: memoria
    # Caso base: no hay más objetos o no hay más capacidad
    if i == 0 or W == 0:
        return 0
    
    # Si ya calculamos el valor, lo retornamos
    if pd[i][W] != -1:
        return pd[i][W]
    
    # Si el objeto no cabe en la mochila, no lo agregamos
    if w[i - 1] > W:
        pd[i][W] = moxila(i - 1, W, w, p, pd)
    else:
        # Si cabe, vemos si es mejor no agregarlo            o agregarlo
        pd[i][W] = max(moxila(i - 1, W, w, p, pd)    ,    p[i - 1] + moxila(i - 1, W - w[i - 1], w, p, pd))
    
    return pd[i][W]


# Maquinas
maquina1 = [1000, 1000]
maquina2 = [5000, 5000]

# Instancias (beneficio, GPUs necesarias)
instancia1 = [(10000,500), (100,300), (100,400), (100,600), (10000,600)]
instancia2 = [(123132,123123),(500,10), (15,30), (25,50), (3,5000)]

# Estados (instancia, maquina)
Estado1 = Estado(instancia1, maquina1)
Estado2 = Estado(instancia2, maquina2)

# valores esperados
expected1 = 20200
expected2 = 543

# Prueba 1 --> Estado1
c1 = Estado1.capacidades_de_las_maquinas[0]
c2 = Estado1.capacidades_de_las_maquinas[1]
memo = [[[-1 for _ in range(c2 + 1)] for _ in range(c1 + 1)] for _ in range(len(Estado1.Instancia) + 1)]
#####################
print(PD(len(Estado1.Instancia)-1, c1, c2, Estado1, memo), expected1)  # True

# Prueba 2 --> Estado2
c1 = Estado2.capacidades_de_las_maquinas[0]
c2 = Estado2.capacidades_de_las_maquinas[1]
memo = [[[-1 for _ in range(c2 + 1)] for _ in range(c1 + 1)] for _ in range(len(Estado2.Instancia) + 1)]
#####################
print(PD(len(Estado2.Instancia)-1, c1, c2, Estado2, memo), expected2)  # True
