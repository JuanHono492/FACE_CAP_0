import cv2
import os
import numpy as np
import shutil
import json

# Directorio donde se encuentran los datos de entrenamiento
dataPath = 'Data'
peopleList = os.listdir(dataPath)
print('Lista de personas:', peopleList)

labels = []
facesData = []
last_label = 0  # Última etiqueta asignada

# Cargar el diccionario de nombres desde el archivo JSON si existe
label_to_name_path = os.path.join('Back', 'label_to_name.json')
if os.path.exists(label_to_name_path):
    with open(label_to_name_path, 'r') as f:
        label_to_name = json.load(f)
else:
    label_to_name = {}

# Obtener la última etiqueta asignada si el diccionario no está vacío
if label_to_name:
    last_label = int(max(label_to_name.keys()))

# Definir el tamaño deseado para las imágenes de entrenamiento
desired_size = (100, 100)

for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo las imágenes de', nameDir)

    # Incrementar el valor de la etiqueta para cada nueva persona
    last_label += 1

    # Agregar el nombre de la persona al diccionario si no existe
    if str(last_label) not in label_to_name:
        label_to_name[str(last_label)] = nameDir

    for fileName in os.listdir(personPath):
        print('Rostro:', nameDir + '/' + fileName)
        labels.append(last_label)  # Usar la etiqueta actual
        # Leer la imagen y redimensionarla al tamaño deseado
        imagePath = os.path.join(personPath, fileName)
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        if image is not None:
            resized_image = cv2.resize(image, desired_size)
            facesData.append(resized_image)
        else:
            print(f"No se pudo leer la imagen: {imagePath}")

# Convertir las listas de etiquetas y datos de rostros en matrices numpy
labels = np.array(labels)
facesData = np.array(facesData)

# Crear el objeto de reconocimiento facial o cargar el modelo existente
model_path = os.path.join('modelo_entrenado.xml')
if os.path.exists(model_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
    print("Modelo existente cargado desde:", model_path)
else:
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("Creando un nuevo modelo...")

# Entrenar el modelo con el nuevo conjunto de datos
print("Añadiendo nuevo entrenamiento al modelo...")
face_recognizer.update(facesData, labels)
face_recognizer.save(model_path)
print("Modelo actualizado y guardado en:", model_path)

# Guardar el diccionario de nombres en el archivo JSON
with open(label_to_name_path, 'w') as f:
    json.dump(label_to_name, f)

# Borrar las imágenes de entrenamiento después de que el modelo ha sido creado
print("Borrando imágenes de entrenamiento...")
shutil.rmtree(dataPath)
print("Imágenes de entrenamiento borradas.")
