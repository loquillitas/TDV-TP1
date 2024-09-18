class Estado:
    def __init__(self, instancia, capacidades_maquinas):
        self.capacidades_de_las_maquinas = list(capacidades_maquinas)  # Lista de capacidades de las máquinas
        self.beneficio_actual = 0  # Beneficio acumulado
        self.mejor_beneficio = 0  # Mejor beneficio encontrado
        self.Instancia = instancia  # Lista de tuplas (beneficio, GPUs necesarias)
        self.asignaciones = [0] * len(instancia)  # Asignaciones actuales
        self.mejor_asignacion = [0] * len(instancia)  # Mejor asignación encontrada



def PD(i, estado, memo):
    # memo: dicionario. Permite operaciones de inserción y búsqueda en tiempo O(1) y ocupa menos espacio que una lista multidimensional
    # los pesos de las maquinas se pasan junto a estado 

    # Caso base: no hay más instancias o no hay más capacidad en todas las máquinas
    if i < 0 or all(c <= 0 for c in estado.capacidades_de_las_maquinas):
        return 0

    # si los gpu necesarios son negativos, paso a la siguiente instancia
    if estado.Instancia[i][1] < 0:
        return PD(i - 1, estado, memo)
        
            
    # Convertimos las capacidades a una tupla para usarla como clave en memo
    c_tuple = tuple(estado.capacidades_de_las_maquinas)

    # Si ya lo calculamos, lo devolvemos
    if (i, c_tuple) in memo:
        return memo[(i, c_tuple)]

    # Calculo beneficio de no agregar la instancia con un llamado recursivo
    beneficio_no_agrego = PD(i - 1, estado, memo)

    # intanciamos variables, van a guardar el mejor beneficio y la mejor máquina para la i-esima instancia
    b_agrego = 0  
    mejor_maquina = -1
    # Recorremos las máquinas para ver en cuales podemos agregar la instancia
    for j in range(len(estado.capacidades_de_las_maquinas)):
        # para la i-esima instancia, vamos a recorrer todas las maquinas y nos quedamos con la que nos de mayor beneficio

        # Si la instancia cabe en la máquina `j`, verificamos la capacidad disponible
        if estado.Instancia[i][1] <= estado.capacidades_de_las_maquinas[j] and estado.capacidades_de_las_maquinas[j] > 0:

            # Guardamos temporalmente las capacidades actuales
            capacidades_previas = list(estado.capacidades_de_las_maquinas)

            # Reducimos la capacidad de la máquina `j` para el llamado recursivo
            estado.capacidades_de_las_maquinas[j] -= estado.Instancia[i][1]

            # guardamos temporalmente la mejor asignación
            mejor_asignacion_actual = estado.mejor_asignacion[i]

            # Actualizamos la mejor asignación de la i-esima instancia con la máquina `j`
            estado.mejor_asignacion[i] = j + 1

            # Calculamos el beneficio de agregar la instancia a la máquina `j`
            beneficio_con_instancia = estado.Instancia[i][0] + PD(i - 1, estado, memo)

            # Ahora que tenemos los beneficios, actualizamos el mejor beneficio
            # Verificamos si es el mejor beneficio encontrado 
            if beneficio_con_instancia >= b_agrego:
                mejor_maquina = j + 1
                b_agrego = beneficio_con_instancia

            # restauramos capacidades originales (backtracking)
            estado.capacidades_de_las_maquinas = capacidades_previas

            # guardamos la mejor asignación
            estado.mejor_asignacion[i] = mejor_asignacion_actual

        
    # Guardamos el mejor valor en memo
    memo[(i, c_tuple)] = max(beneficio_no_agrego, b_agrego)

    # Actualizamos la mejor asignación solo si agregamos la instancia
    if b_agrego > beneficio_no_agrego and b_agrego>mejor_asignacion_actual:
        estado.mejor_asignacion[i] = mejor_maquina
 

    return memo[(i, c_tuple)]

# Pruebas
# (beneficio, GPUs necesarias)
maquina3 = [500, 500, 500, 400, 400, 400, 400, 400]
instacia3 = [(1000,499), (100, 700), (10, 500), (100, 4), (100, 1), (100,1), (100,1), (100,1)]
Estado3 = Estado(instacia3, maquina3)
expected3 = 509
memo = {}
print(PD(len(Estado3.Instancia)-1, Estado3, memo), expected3)  # True
print(Estado3.mejor_asignacion)
