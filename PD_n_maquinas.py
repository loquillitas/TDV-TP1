

class Estado:
    def __init__(self, instancia, capacidades_maquinas):
        self.capacidades_de_las_maquinas = list(capacidades_maquinas)  # Lista de capacidades de las máquinas
        self.beneficio_actual = 0  # Beneficio acumulado
        self.mejor_beneficio = 0  # Mejor beneficio encontrado
        self.Instancia = instancia  # Lista de tuplas (beneficio, GPUs necesarias)
        self.asignaciones = [0] * len(instancia)  # Asignaciones actuales
        self.mejor_asignacion = [0] * len(instancia)  # Mejor asignación encontrada



def PD(i, estado, memo):
    # Caso base: no hay más instancias o no hay más capacidad en todas las máquinas
    if i < 0 or all(c <= 0 for c in estado.capacidades_de_las_maquinas):
        return 0

    # Convertimos las capacidades a una tupla para usarla como clave en memo
    c_tuple = tuple(estado.capacidades_de_las_maquinas)

    # Si ya hemos calculado este estado, lo retornamos
    if (i, c_tuple) in memo:
        return memo[(i, c_tuple)]

    # No agregar la instancia
    beneficio_no_agrego = PD(i - 1, estado, memo)

    # intnciamos variables 
    b_agrego = 0  
    mejor_maquina = 0
    # Recorremos las máquinas para ver si podemos agregar la instancia
    for j in range(len(estado.capacidades_de_las_maquinas)):

        if estado.Instancia[i][1] <= estado.capacidades_de_las_maquinas[j]:  # Si cabe en la máquina `j`
            # Guardamos temporalmente las capacidades actuales
            capacidades_previas = list(estado.capacidades_de_las_maquinas)

            # Reducimos la capacidad de la máquina `j`
            estado.capacidades_de_las_maquinas[j] -= estado.Instancia[i][1]            

            # Calculamos el beneficio agregando la instancia a la máquina `j`
            beneficio_con_instancia = estado.Instancia[i][0] + PD(i - 1, estado, memo)

            # modifico la mejor asignacion
            if b_agrego < beneficio_con_instancia:
                estado.mejor_asignacion[i] = j + 1
                mejor_maquina = j + 1
                b_agrego = beneficio_con_instancia

            # Restauramos las capacidades originales (backtracking)
            estado.capacidades_de_las_maquinas = capacidades_previas
        
    # Guardamos el mejor valor en memo como un diccionario
    memo[(i, c_tuple)] = max(beneficio_no_agrego, b_agrego)

    # Agregamos la mejor asignacion
    estado.mejor_asignacion[i] = mejor_maquina

    return memo[(i, c_tuple)]
