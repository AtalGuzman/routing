
# Modelamiento matemático I

## Variable de decisión
Sea $X_{i,j}$, se asigna al vehículo i la demanda j. Donde $X_{i,j}$ está en {0,1}

## Parámetros
### Matriz de costos $C$ en $M_{n,m}$
Dónde $C_{i,j} \in$  Naturales, costo de que el vehículo i supla la demanda j

### Vector de capacidad $Cap$ en $M_{1,n}$
Dónde $Cap_{i} \in$ los Naturales, capacidad del vehículo i.

### Vector de incompatibilidad $I$ en $M_{m,m}$
Dónde $I_{i,j} \in$  {0,1}, representa la incompatibilidad de la demanda i con la demanda j

## Restricciones
### Capacidad del vehículo
$\sum_{j = 1}^{m} X_{i,j} C_{i,j} \leq Cap_{i}, \forall i$
### Asignación de demanda
$\sum_{i=1}^{n} X_{i,j} \leq 1, \forall j$
### Incompatibilidad de demandas
$\sum_{i=m} I_{i,j} = 0, \forall i$

## Función Objetivo
$min$  $\sum_{i=0}^{n-1} \sum_{j=0}^{m-1} X_{i,j} \times C{i,j}$

# Modelamiento Matemático II

## Variable de decisión
* Sea $X$, vector de largo $m$ con $m$ igual al número de demandas.
* $X_{i} \in {0,...,n}$, enteros, con n igual al número de vehículos. Representa que el vehículo $X_i$ suple la demanda $i$

## Parámetros
Respecto al modelamiento anterior, solo varía la representación de la incompatibilidad de demandas

### Incompatibilidad de demandas
* Sea $I$ vector de largo $m$, con $m$ igual al número de demandas. 
* Entonces $I_{i}$, incompatibilidad entre la demanda $i$ y la demanda $I_i$

Dado lo anterior, se deben modificar las restricciones y la evaluación de la función objetivo

## Restricciones
### Capacidad del vehículo
* $\sum_{i} C_{X_i,i} \leq Cap_j$   $/ \{X_i = j\}$  $ \forall j$
### Asignación de demanda
* Observar que por el modo en que se representa solución esta restricción queda salvada inmediatamente.
### Incompatibilidad de demandas
* Si $I_{i} = j \rightarrow X_i \neq X_j, \forall i,j. $ 
* Se obvia el caso en que i, sea igual a j. Se asume que el incompatibilidad no tendrá ese error, es decir, que la demanda i sea incompatible son si misma.

# Funcion Objetivo

$min$ $\sum_{i=0}^{m} C_{x_i, i}$, con $m$ = n° de demandas

Dado que la estructura para representar la solución y las restricciones se simplifica, se opta por usar este modelamiento
