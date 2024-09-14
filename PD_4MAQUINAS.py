class Estado:
    def __init__(self, instancia, capacidades_maquinas):
        self.capacidades_de_las_maquinas = list(capacidades_maquinas)  # Lista de capacidades de las máquinas
        self.beneficio_actual = 0  # Beneficio acumulado
        self.mejor_beneficio = 0  # Mejor beneficio encontrado
        self.Instancia = instancia  # Lista de tuplas (beneficio, GPUs necesarias)
        self.asignaciones = [0] * len(instancia)  # Asignaciones actuales
        self.mejor_asignacion = [0] * len(instancia)  # Mejor asignación encontrada



def PD(i, c1, c2, c3, c4, estado, memo):

    # Caso base: no hay más instancias o no hay más capacidad en todas las máquinas
    if i < 0 or (c1 <= 0 and c2 <= 0 and c3 <= 0 and c4 <= 0):
        return 0

    # Si ya calculamos el valor, lo retornamos
    if memo[i][c1][c2][c3][c4] != -1:
        return memo[i][c1][c2][c3][c4]

    beneficio_no_agrego = PD(i - 1, c1, c2, c3, c4, estado, memo)  # No agregar la instancia
    b_agrego1 = -1 # Inicializamos con un valor muy bajo
    b_agrego2 = -1
    b_agrego3 = -1
    b_agrego4 = -1

    if estado.Instancia[i][1] <= c1:
        b_agrego1 = estado.Instancia[i][0] + PD(i - 1, c1 - estado.Instancia[i][1], c2, c3, c4, estado, memo)

    if estado.Instancia[i][1] <= c2:
        b_agrego2 = estado.Instancia[i][0] + PD(i - 1, c1, c2 - estado.Instancia[i][1], c3, c4, estado, memo)

    if estado.Instancia[i][1] <= c3:
        b_agrego3 = estado.Instancia[i][0] + PD(i - 1, c1, c2, c3 - estado.Instancia[i][1], c4, estado, memo)

    if estado.Instancia[i][1] <= c4:
        b_agrego4 = estado.Instancia[i][0] + PD(i - 1, c1, c2, c3, c4 - estado.Instancia[i][1], estado, memo)

    # Guardamos el valor máximo en memo
    memo[i][c1][c2][c3][c4] = max(beneficio_no_agrego, b_agrego1, b_agrego2, b_agrego3, b_agrego4)

    # Actualizamos la mejor asignación
    if memo[i][c1][c2][c3][c4] == beneficio_no_agrego:
        estado.mejor_asignacion[i] = 0
    elif memo[i][c1][c2][c3][c4] == b_agrego1:
        estado.mejor_asignacion[i] = 1
    elif memo[i][c1][c2][c3][c4] == b_agrego2:
        estado.mejor_asignacion[i] = 2
    elif memo[i][c1][c2][c3][c4] == b_agrego3:
        estado.mejor_asignacion[i] = 3
    elif memo[i][c1][c2][c3][c4] == b_agrego4:
        estado.mejor_asignacion[i] = 4

    return memo[i][c1][c2][c3][c4]



## TEST ##
maquina3 = [5, 5, 5, 5]
instacia3 = [(109, 1), (100, 1), (100, 1), (100, 1), (100, 1)]
Estado3 = Estado(instacia3, maquina3)
expected3 = 509
c1 = Estado3.capacidades_de_las_maquinas[0]
c2 = Estado3.capacidades_de_las_maquinas[1]
c3 = Estado3.capacidades_de_las_maquinas[2]
c4 = Estado3.capacidades_de_las_maquinas[3]
memo = [[[[[-1 for _ in range(c4 + 1)] for _ in range(c3 + 1)] for _ in range(c2 + 1)] for _ in range(c1 + 1)] for _ in range(len(Estado3.Instancia) + 1)]
print(PD(len(Estado3.Instancia)-1, c1, c2, c3, c4, Estado3, memo), expected3)  # True
print(Estado3.mejor_asignacion)
