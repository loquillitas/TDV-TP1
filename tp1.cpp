#include <iostream>
#include <list>
#include <vector>
#include <fstream>
using namespace std;


////////////////////////////// PSEUDO CÓDIGO FUERZA BRUTA /////////////////////////////

// i =indice de la instacian actual (int)
//capacidades_de_las_maquinas: lista con las capacidades en cada máquina lis[int] siendo len(capacidades_de_las_maquinas) = #de maquinas
//Instancia: (beneficio, gpus_usados) lista de tuplas con el beneficio y las gpus necesarias de la instancia actual (list[tuple(int, int)])
//beneficio_actual: beneficio acumulado hasta el momento (int)
//mejor_beneficio: mejor beneficio encontrado hasta el momento (int)

//FB (i, capacidades_de_las_maquinas, beneficio_actual):
//    si i == len(Instancia): #caso base donde ta recorrí todas las instancias
//        si beneficio_actual > mejor_beneficio:
//            mejor_beneficio = beneficio_actual
//              return mejor_beneficio
//    sino:
// OPCION1: No asignamos la instancia i a ninguna máquina
//        mejor_beneficio = FB(i+1, capacidades_de_las_maquinas, beneficio_actual)

// OPCION 2: Asignamos la instancia i a alguna máquina si hay capacidad suficiente, es decir, si los gpus_disponibles <= gpus_usados 
//siendo los (gpus_disponibles = capacidades_de_las_maquinas[j])

// si gpus_disponibles <= gpus_usados:
//   FB(i+1, capacidades_de_las_maquinas - gpus_usados, beneficio_actual + beneficio_i)




struct Estado {
    list<int> capacidades_de_las_maquinas; // Lista con las capacidades en cada máquina
    int beneficio_actual; // Beneficio acumulado hasta el momento
    int mejor_beneficio; // Mejor beneficio encontrado hasta el momento
    const list<pair<int, int>>& Instancia; // Lista de tuplas con el beneficio y las GPUs necesarias de la instancia actual
    vector<int> asignaciones;
    vector<int> mejor_asignacion;

};

////////////////////////// FUERZA BRUTA ///////////////////////////


void FB(int i, Estado& estado) { 
  
    if (i == estado.Instancia.size()) { // Caso base: recorrimos todas las instancias
        if (estado.beneficio_actual > estado.mejor_beneficio) {
            estado.mejor_beneficio = estado.beneficio_actual;
            estado.mejor_asignacion = estado.asignaciones;
        }
        return;
    }

    // Opción 1: No asignamos la instancia i a ninguna máquina
    estado.asignaciones[i] = 0;
    FB(i + 1, estado);

    // Opción 2: Asignamos la instancia i a alguna máquina si hay capacidad suficiente
    auto it_instancia = next(estado.Instancia.begin(), i); //it_instancia toma la instancia sub i (next me permite conectar con la i)
    for (auto it_maquina = estado.capacidades_de_las_maquinas.begin(); it_maquina != estado.capacidades_de_las_maquinas.end(); ++it_maquina) {

        if (*it_maquina >= it_instancia->second) { // Si hay capacidad suficiente) { 
            *it_maquina -= it_instancia->second; // Resto la capacidad
            estado.beneficio_actual += it_instancia->first; // Sumo el beneficio
            estado.asignaciones[i] = 1;

            // cout << "Asignando instancia " << i << " con beneficio " << it_instancia->first << " y GPUs " << it_instancia->second << endl;
            // cout << "Capacidad restante de la máquina: " << *it_maquina << endl;
            // cout << "Beneficio actual: " << estado.beneficio_actual << endl;

            FB(i + 1, estado); 

            *it_maquina += it_instancia->second; // Restaurar capacidad
            estado.beneficio_actual -= it_instancia->first; // Restaurar beneficio
            estado.asignaciones[i] = 0;
            // cout << "Desasignando instancia " << i << " con beneficio " << it_instancia->first << " y GPUs " << it_instancia->second << endl;
            // cout << "Capacidad restaurada de la máquina: " << *it_maquina << endl;
            // cout << "Beneficio restaurado: " << estado.beneficio_actual << endl;
        }
            //cout << "Beneficio actual con FB: " << estado.beneficio_actual << endl;
    }
}



///////////////////////////// BACKTRACKING /////////////////////////////
void BT(int i, Estado& estado) {
    if (i == estado.Instancia.size()) { // Caso base: recorrimos todas las instancias
        if (estado.beneficio_actual > estado.mejor_beneficio) {
            estado.mejor_beneficio = estado.beneficio_actual;
            estado.mejor_asignacion = estado.asignaciones;
        }
        return;
    }

    // Crear un iterador y avanzar hasta la posición i
    auto it = estado.Instancia.begin();
    advance(it, i);

    // Si GPU necesarios de la instancia i son negativos, paso a la siguiente instancia
    if (it->second < 0) {
        BT(i + 1, estado);
        return;
    }

    // si las capacidades de las máquinas son negativas, las seteo a 0
    for (int& capacidad : estado.capacidades_de_las_maquinas) {
        if (capacidad < 0) {
            capacidad = 0;
        }
    }

    // Poda por beneficio máximo alcanzable (poda de factibilidad)
    int beneficio_maximo_posible = estado.beneficio_actual;
    for (auto it = next(estado.Instancia.begin(), i); it != estado.Instancia.end(); ++it) {
        beneficio_maximo_posible += it->first;
    }
    if (beneficio_maximo_posible <= estado.mejor_beneficio) {
        return; // Poda
    }

    // Poda por capacidad insuficiente (poda de optimalidad)
    int capacidad_total_restante = 0;
    for (int capacidad : estado.capacidades_de_las_maquinas) {
        capacidad_total_restante += capacidad;
    }
    for (auto it = next(estado.Instancia.begin(), i); it != estado.Instancia.end(); ++it) {
        if (capacidad_total_restante < it->second) {
            return; // Poda
        }
    }

    // Opción 1: No asignamos la instancia i a ninguna máquina
    estado.asignaciones[i] = 0;
    BT(i + 1, estado);

    // Opción 2: Asignamos la instancia i a alguna máquina si hay capacidad suficiente
    auto it_instancia = next(estado.Instancia.begin(), i);
    for (auto it_maquina = estado.capacidades_de_las_maquinas.begin(); it_maquina != estado.capacidades_de_las_maquinas.end(); ++it_maquina) {
        if (*it_maquina >= it_instancia->second) { // Si hay capacidad suficiente en la máquina actual
            *it_maquina -= it_instancia->second; // Resto la capacidad de la máquina actual
            estado.beneficio_actual += it_instancia->first; // Sumo el beneficio
            estado.asignaciones[i] = 1;

            BT(i + 1, estado);

            *it_maquina += it_instancia->second; // Restaurar capacidad de la máquina actual
            estado.beneficio_actual -= it_instancia->first; // Restaurar beneficio
            estado.asignaciones[i] = 0;
        }
    }
}


/////////////////////////// PROGRAMACIÓN DINÁMICA ///////////////////////////

// int main() {
//     // Dos alternativas de máquinas
//     list<int> maquinas1 = {1000, 1000}; // Dos máquinas con 1000 GPU cada una
//     //list<int> maquinas2 = {500, 500, 500, 500}; // Cuatro máquinas con 500 GPU cada una
//     // ejemplo borde: dos maquinas de 1000 GPU, intancias: 500 500, 500 500, 600 500, 400 500, 100 100
//     // respuesta esperada: m1= 1100 beneficio (500 500, 400 500, 100 100), m2 = 1000 beneficio (600 500, 400 500)
//     // Instancias (beneficio, gpus_usados)
//     list<pair<int, int>> Instancia = {
//       //  {500, 500}, {500, 500}, {600, 500}, {400, 500}, {100, 100}
//          {100, 100}, {400, 500}, {600, 500}, {500, 500}, {500, 500}
//     };

// // si el beneficio es 
    
//     // Evaluar el beneficio máximo para cada alternativa
//     Estado estadoFB = {maquinas1, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};
//     Estado estadoBT = {maquinas1, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};

//     FB(0, estadoFB);
//     BT(0, estadoBT);

//     cout << "Mejor beneficio con FB y dos máquinas de 1000 GPU: " << estadoFB.mejor_beneficio << endl;
//     cout << "Asignaciones FB: ";

//     cout << "Mejor beneficio con BT y dos máquinas de 1000 GPU: " << estadoBT.mejor_beneficio << endl;
//     cout << "Asignaciones BT: ";

//     for (int asignacion : estadoFB.mejor_asignacion) {
//         cout << asignacion << " ";
//     }
//     cout << endl;

//     return 0;
// }


//////////////////// PRUEBAS //////////////////////

int main() {
    // Dos alternativas de máquinas
    list<int> maquinas1 = {2000, 2000}; // Dos máquinas con 1000 GPU cada una
    list<int> maquinas2 = {500, 500, 500, 500, 500, 500, 500, 500}; // Cuatro máquinas con 500 GPU cada una


    // Instancias (beneficio, gpus_usados)
    list<pair<int, int>> Instancia = {
        {100, 200}, {400, 700}, {600, 500}, {500, 500}, {500, 500}
    };

    // Evaluar el beneficio máximo para la alternativa usando FB
    Estado estadoFB1 = {maquinas1, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};
    FB(0, estadoFB1);

    Estado estadoFB2 = {maquinas2, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};
    FB(0, estadoFB2);


    cout << "Mejor beneficio con FB1 y dos máquinas de 1000 GPU: " << estadoFB1.mejor_beneficio << endl;
    cout << "Asignaciones FB1: ";

    for (int asignacion : estadoFB1.mejor_asignacion) {
        cout << asignacion << " ";
    }
    cout << endl;

/////////////////   FB   ////////////////////////

    cout << "Mejor beneficio con FB2 y dos máquinas de 1000 GPU: " << estadoFB2.mejor_beneficio << endl;
    cout << "Asignaciones FB2: ";
    
    for (int asignacion : estadoFB2.mejor_asignacion) {
        cout << asignacion << " ";
    }
    cout << endl;


//////////////////////   BT    //////////////////////////

    // Evaluar el beneficio máximo para la alternativa usando BT
    Estado estadoBT1 = {maquinas1, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};
    BT(0, estadoBT1);

    Estado estadoBT2 = {maquinas2, 0, 0, Instancia, vector<int>(Instancia.size(), 0), vector<int>(Instancia.size(), 0)};
    BT(0, estadoBT2);

    cout << "Mejor beneficio con BT1 y dos máquinas de 1000 GPU: " << estadoBT1.mejor_beneficio << endl;
    cout << "Asignaciones BT1: ";
    for (int asignacion : estadoBT1.mejor_asignacion) {
        cout << asignacion << " ";
    }
    cout << endl;

    //////////////////////

    
    cout << "Mejor beneficio con BT2 y dos máquinas de 1000 GPU: " << estadoBT2.mejor_beneficio << endl;
    cout << "Asignaciones BT2: ";
    for (int asignacion : estadoBT2.mejor_asignacion) {
        cout << asignacion << " ";
    }
    cout << endl;

    return 0;
}
