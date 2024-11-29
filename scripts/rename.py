import os

# Ruta al directorio con los archivos
directorio = "../pictures_128"

# Iterar sobre los archivos en el directorio
for nombre_archivo in os.listdir(directorio):
    # Verificar si el archivo termina con ".0.png"
    if nombre_archivo.endswith(".0.png"):
        # Crear el nuevo nombre eliminando ".0"
        nuevo_nombre = nombre_archivo.replace(".0.png", ".png")

        # Renombrar el archivo
        ruta_original = os.path.join(directorio, nombre_archivo)
        ruta_nueva = os.path.join(directorio, nuevo_nombre)
        os.rename(ruta_original, ruta_nueva)

        print(f"Renombrado: {nombre_archivo} -> {nuevo_nombre}")

print("Proceso completado.")