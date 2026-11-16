import random
import time

# ==========================================
# 1. MODELO DE DATOS DEL PRODUCTO
# ==========================================
class Producto:
    def __init__(self, id_val, nombre, precio, categoria, stock, calificacion_promedio):
        self.id = id_val
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.calificacionPromedio = calificacion_promedio

    def __repr__(self):
        return f"ID: {self.id} | {self.nombre:<25} | Precio: ${self.precio:>7.2f} | Cat: {self.categoria:<12} | Stock: {self.stock:>3} | Rating: {self.calificacionPromedio}"


# ==========================================
# 2. GENERACION DE DATOS DE PRUEBA (50 PRODUCTOS)
# ==========================================
def generar_productos(n=50):
    categorias = ["Electrónica", "Ropa", "Libros", "Hogar", "Deportes"]
    adjetivos = ["Smart", "Pro", "Ultra", "Max", "Premium", "Económico", "Compacto", "Ergonómico"]
    sustantivos = ["Camisa", "Audífonos", "Laptop", "Libro", "Lámpara", "Zapatillas", "Mochila", "Reloj", "Cafetera", "Silla"]
    
    productos = []
    ids_usados = set()
    
    while len(productos) < n:
        id_val = random.randint(1000, 9999)
        if id_val not in ids_usados:
            ids_usados.add(id_val)
            nombre = f"{random.choice(adjetivos)} {random.choice(sustantivos)} {random.randint(1, 100)}"
            precio = round(random.uniform(10.0, 1500.0), 2)
            categoria = random.choice(categorias)
            stock = random.randint(0, 100)
            calificacion = round(random.uniform(1.0, 5.0), 1)
            
            productos.append(Producto(id_val, nombre, precio, categoria, stock, calificacion))
            
    return productos


# ==========================================
# 3. ALGORITMOS DE ORDENAMIENTO
# ==========================================

# Algoritmo 1: Quick Sort
def quick_sort(arr, key_func, reverse=False):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    if reverse:
        menores = [x for x in arr if key_func(x) > key_func(pivote)]
        iguales = [x for x in arr if key_func(x) == key_func(pivote)]
        mayores = [x for x in arr if key_func(x) < key_func(pivote)]
    else:
        menores = [x for x in arr if key_func(x) < key_func(pivote)]
        iguales = [x for x in arr if key_func(x) == key_func(pivote)]
        mayores = [x for x in arr if key_func(x) > key_func(pivote)]
    return quick_sort(menores, key_func, reverse) + iguales + quick_sort(mayores, key_func, reverse)


# Algoritmo 2: Merge Sort
def merge_sort(arr, key_func, reverse=False):
    if len(arr) <= 1:
        return arr
    
    medio = len(arr) // 2
    izquierda = merge_sort(arr[:medio], key_func, reverse)
    derecha = merge_sort(arr[medio:], key_func, reverse)
    
    return merge(izquierda, derecha, key_func, reverse)

def merge(left, right, key_func, reverse):
    resultado = []
    i = j = 0
    while i < len(left) and j < len(right):
        val_i = key_func(left[i])
        val_j = key_func(right[j])
        
        if reverse:
            condicion = val_i >= val_j
        else:
            condicion = val_i <= val_j
            
        if condicion:
            resultado.append(left[i])
            i += 1
        else:
            resultado.append(right[j])
            j += 1
    resultado.extend(left[i:])
    resultado.extend(right[j:])
    return resultado


# Algoritmo 3: Insertion Sort
def insertion_sort(arr, key_func, reverse=False):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        if reverse:
            while j >= 0 and key_func(a[j]) < key_func(key):
                a[j + 1] = a[j]
                j -= 1
        else:
            while j >= 0 and key_func(a[j]) > key_func(key):
                a[j + 1] = a[j]
                j -= 1
        a[j + 1] = key
    return a


# ==========================================
# 4. ALGORITMOS DE BUSQUEDA
# ==========================================

# Búsqueda Binaria (por ID)
def busqueda_binaria_id(arr_ordenado, id_buscado):
    inicio = 0
    fin = len(arr_ordenado) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if arr_ordenado[medio].id == id_buscado:
            return medio
        elif arr_ordenado[medio].id < id_buscado:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

# Búsqueda Lineal (por subcadena en el nombre)
def busqueda_lineal_nombre(arr, subcadena):
    resultados = []
    sub = subcadena.lower()
    for prod in arr:
        if sub in prod.nombre.lower():
            resultados.append(prod)
    return resultados


# ==========================================
# 5. FUNCIÓN PRINCIPAL Y MEDICIONES
# ==========================================
def main():
    print("=== 1. GENERACION DE DATOS ===")
    productos = generar_productos(50)
    print(f"Se han generado {len(productos)} productos exitosamente.\n")

    # Criterios de ordenamiento (lambdas)
    key_precio = lambda p: p.precio                    # Ascendente
    key_rating = lambda p: p.calificacionPromedio      # Descendente

    algoritmos = [
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
        ("Insertion Sort", insertion_sort)
    ]

    print("=== 2. MEDICION DE TIEMPOS DE ORDENAMIENTO ===")
    print(f"{'Algoritmo':<15} | {'Precio (Asc) [ms]':<18} | {'Rating (Desc) [ms]'}")
    print("-" * 57)

    for nombre_alg, func in algoritmos:
        # Medir Criterio 1: Precio (Ascendente)
        t0 = time.perf_counter()
        _ = func(productos, key_precio, reverse=False)
        t1 = time.perf_counter()
        t_precio = (t1 - t0) * 1000

        # Medir Criterio 2: Calificación (Descendente)
        t0 = time.perf_counter()
        _ = func(productos, key_rating, reverse=True)
        t1 = time.perf_counter()
        t_rating = (t1 - t0) * 1000

        print(f"{nombre_alg:<15} | {t_precio:<18.4f} | {t_rating:<18.4f}")

    print("\n=== 3. PRUEBAS DE BUSQUEDA BINARIA POR ID ===")
    productos_por_id = sorted(productos, key=lambda p: p.id)
    
    ids_existentes = [p.id for p in random.sample(productos, 10)]
    ids_inexistentes = [99999 + i for i in range(10)]

    t0 = time.perf_counter()
    for _ in range(1000): 
        for id_val in ids_existentes:
            busqueda_binaria_id(productos_por_id, id_val)
        for id_val in ids_inexistentes:
            busqueda_binaria_id(productos_por_id, id_val)
    t1 = time.perf_counter()
    print(f"Tiempo total (10 exist. + 10 no exist. x 1000 iteraciones): {(t1 - t0)*1000:.4f} ms")

    print("\n=== 4. PRUEBAS DE BUSQUEDA LINEAL POR NOMBRE (SUBCADENA) ===")
    subs_existentes = ["Smart", "Pro", "Max", "Camisa", "Libro", "Reloj", "Cafetera", "Silla", "Mochila", "Ultra"]
    subs_inexistentes = ["Xyz123", "Abc999", "Notfound", "FooBar", "Test111", "Zonked", "BlahBlah", "GhostItem", "Void", "Missing"]

    t0 = time.perf_counter()
    for _ in range(1000):
        for sub in subs_existentes:
            busqueda_lineal_nombre(productos, sub)
        for sub in subs_inexistentes:
            busqueda_lineal_nombre(productos, sub)
    t1 = time.perf_counter()
    print(f"Tiempo total Busqueda Lineal por Subcadena (x 1000 iteraciones): {(t1 - t0)*1000:.4f} ms")

if __name__ == "__main__":
    main()