import os
import cv2
import imutils
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import json
import subprocess
import sys
import numpy as np
import shutil


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

file_path = resource_path("haarcascade_frontalface_default.xml")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo Haar Cascade no se encuentra en la ruta: {file_path}")

areas_path = 'areas.json'
label_to_name_path = os.path.join('Back', 'label_to_name.json')

def cargar_areas():
    if os.path.exists(areas_path):
        try:
            with open(areas_path, 'r') as f:
                data = json.load(f)
                return data.get('areas', [])
        except json.JSONDecodeError as e:
            print(f"Error al cargar JSON desde {areas_path}: {e}")
    else:
        print(f"El archivo {areas_path} no existe.")
    return []

def cargar_label_to_name():
    if os.path.exists(label_to_name_path):
        try:
            with open(label_to_name_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error al cargar JSON desde {label_to_name_path}: {e}")
    else:
        print(f"El archivo {label_to_name_path} no existe.")
    return {}

def centrar_imagen(frame, width, height):
    h, w = frame.shape[:2]
    top = max((height - h) // 2, 0)
    bottom = max(height - h - top, 0)
    left = max((width - w) // 2, 0)
    right = max(width - (w + left), 0)
    color = [0, 0, 0]
    frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return frame

def eliminar_usuario(root):
    selected_item = tabla.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
        return

    idx = selected_item[0]
    usuario = tabla.item(idx)['values']

    personPath = os.path.join('Data', usuario[1])
    if os.path.exists(personPath):
        import shutil
        shutil.rmtree(personPath)
        mostrar_notificacion(f'Carpeta eliminada: {personPath}', root, color="red")

    tabla.delete(idx)
    mostrar_notificacion(f'Usuario {usuario[1]} eliminado.', root, color="red")

def capturar_desde_camara(root, nombre, areas):
    dataPath = 'Data'
    personPath = os.path.join(dataPath, nombre)

    if not os.path.exists(personPath):
        os.makedirs(personPath)
        mostrar_notificacion(f'Carpeta creada: {personPath}', root, color="green")

    cap = cv2.VideoCapture(0)
    mostrar_notificacion('Capturando datos desde la cámara...', root, color="green")

    count = 0
    face_cascade = cv2.CascadeClassifier(resource_path('haarcascade_frontalface_default.xml'))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            resized_face = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
            for i in range(2):
                cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), resized_face)
                count += 1
            cv2.putText(frame, f'Capturado: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        label_captura.imgtk = imgtk
        label_captura.configure(image=imgtk)

        if cv2.waitKey(1) == 27 or count >= 200:
            break
    root.update()   
    cap.release()
    cv2.destroyAllWindows()
    usuarios_capturados.append({"nombre": nombre, "rostros": count, "areas": areas})
    actualizar_tabla()
    mostrar_notificacion(f'Captura completada. Se guardaron {count} imágenes en {personPath}', root, color="green")
    limpiar_formulario()

def capturar_desde_archivo(root, nombre, areas):
    dataPath = 'Data'
    personPath = os.path.join(dataPath, nombre)

    if not os.path.exists(personPath):
        os.makedirs(personPath)
        mostrar_notificacion(f'Carpeta creada: {personPath}', root, color="green")

    video_path = filedialog.askopenfilename(title="Seleccionar archivo de video", filetypes=[("Archivos de video", "*.mp4 *.avi")])
    if not video_path:
        mostrar_notificacion("No se seleccionó ningún archivo de video.", root)
        return

    cap = cv2.VideoCapture(video_path)
    mostrar_notificacion('Capturando datos desde el archivo de video...', root, color="green")

    count = 0
    face_cascade = cv2.CascadeClassifier(resource_path('haarcascade_frontalface_default.xml'))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=200)
        frame = centrar_imagen(frame, 200, 200)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            resized_face = cv2.resize(gray[y:y+h, x:x + w], (50, 50))
            for i in range(2):
                cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), resized_face)
                count += 1
            cv2.putText(frame, f'Capturado: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        imgtk = ImageTk.PhotoImage(image=img)
        label_captura.imgtk = imgtk
        label_captura.configure(image=imgtk)

        if cv2.waitKey(1) == 27 or count >= 200:
            break
    root.update()
    cap.release()
    cv2.destroyAllWindows()
    usuarios_capturados.append({"nombre": nombre, "rostros": count, "areas": areas})
    actualizar_tabla()
    mostrar_notificacion(f'Captura completada. Se guardaron {count} imágenes en {personPath}', root, color="green")
    limpiar_formulario()

def capturar_datos(root):
    nombre = nombre_entry.get()
    if nombre:
        areas = [area for area, var in area_vars.items() if var.get()]
        if opcion_var.get() == 0:
            threading.Thread(target=capturar_desde_camara, args=(root, nombre, areas)).start()
        else:
            threading.Thread(target=capturar_desde_archivo, args=(root, nombre, areas)).start()
    else:
        mostrar_notificacion("El nombre no puede estar vacío.", root)

def mostrar_notificacion(mensaje, root, color="green"):
    notificacion_label.config(text=mensaje, foreground=color)
    root.after(5000, limpiar_notificacion, root)

def limpiar_notificacion(root):
    notificacion_label.config(text="")

def limpiar_formulario():
    nombre_entry.delete(0, tk.END)
    label_captura.configure(image='')
    for var in area_vars.values():
        var.set(False)

def actualizar_tabla():
    for i in tabla.get_children():
        tabla.delete(i)
    for idx, usuario in enumerate(usuarios_capturados, start=1):
        tabla.insert("", "end", values=(idx, usuario["nombre"], usuario["rostros"], ", ".join(usuario["areas"])))

def entrenar_modelo(dataPath='Data', label_to_name_path=os.path.join('label_to_name.json'), model_path=os.path.join('modelo_entrenado.xml')):
    peopleList = os.listdir(dataPath)
    labels = []
    facesData = []
    last_label = 0

    # Cargar label_to_name si existe
    if os.path.exists(label_to_name_path):
        with open(label_to_name_path, 'r') as f:
            label_to_name = json.load(f)
    else:
        label_to_name = {}

    if label_to_name:
        last_label = int(max(label_to_name.keys(), key=int))

    desired_size = (100, 100)

    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        last_label += 1

        # Obtener las áreas asociadas al usuario
        areas = [usuario['areas'] for usuario in usuarios_capturados if usuario['nombre'] == nameDir]
        areas = areas[0] if areas else []

        label_to_name[str(last_label)] = {'nombre': nameDir, 'areas': areas}

        for fileName in os.listdir(personPath):
            labels.append(last_label)
            imagePath = os.path.join(personPath, fileName)
            image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                resized_image = cv2.resize(image, desired_size)
                facesData.append(resized_image)

    labels = np.array(labels)
    facesData = np.array(facesData)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(model_path):
        face_recognizer.read(model_path)

    face_recognizer.update(facesData, labels)
    face_recognizer.save(model_path)

    with open(label_to_name_path, 'w') as f:
        json.dump(label_to_name, f, indent=4)

    shutil.rmtree(dataPath)


def subir_datos_al_modelo(root):
    try:
        entrenar_modelo()
        limpiar_tabla()
        mostrar_notificacion('Datos subidos correctamente', root, color="green")
    except Exception as e:
        mostrar_notificacion(f'Error al subir los datos: {e}', root, color="red")

def limpiar_tabla():
    for i in tabla.get_children():
        tabla.delete(i)

def regresar_a_principal(root, username, cargar_login_view):
    for widget in root.winfo_children():
        widget.destroy()
    from Interfaz.Principal import principal_view
    principal_view(root, username, cargar_login_view)

def iniciar_interfaz(root, username, regresar_a_principal, cargar_login_view):
    global nombre_entry, opcion_var, area_vars, tabla, notificacion_label, label_captura, usuarios_capturados
    for widget in root.winfo_children():
        widget.destroy()

    frame_formulario = ttk.Frame(root)
    frame_formulario.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    ttk.Label(frame_formulario, text="Nombre:").pack(anchor=tk.W)
    nombre_entry = ttk.Entry(frame_formulario)
    nombre_entry.pack(fill=tk.X)

    opcion_var = tk.IntVar(value=0)
    ttk.Radiobutton(frame_formulario, text="Capturar desde cámara", variable=opcion_var, value=0).pack(anchor=tk.W)
    ttk.Radiobutton(frame_formulario, text="Capturar desde archivo", variable=opcion_var, value=1).pack(anchor=tk.W)

    areas = cargar_areas()
    area_vars = {}
    for area in areas:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_formulario, text=area, variable=var)
        chk.pack(anchor=tk.W)
        area_vars[area] = var

    ttk.Button(frame_formulario, text="Capturar datos", command=lambda: capturar_datos(root)).pack(pady=10)

    notificacion_label = ttk.Label(frame_formulario, text="")
    notificacion_label.pack(pady=10)

    frame_derecho = ttk.Frame(root)
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    frame_tabla = ttk.Frame(frame_derecho)
    frame_tabla.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Rostros", "Áreas"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Rostros", text="Rostros")
    tabla.heading("Áreas", text="Áreas")
    tabla.pack(fill=tk.BOTH, expand=True)

    ttk.Button(frame_tabla, text="Eliminar usuario", command=lambda: eliminar_usuario(root)).pack(pady=10)

    ttk.Button(frame_tabla, text="Entrenar modelo", command=lambda: subir_datos_al_modelo(root)).pack(pady=10)

    ttk.Button(frame_tabla, text="Regresar a Principal", command=lambda: regresar_a_principal(root, username, cargar_login_view)).pack(pady=10)

    frame_captura = ttk.Frame(frame_derecho)
    frame_captura.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    label_captura = ttk.Label(frame_captura)
    label_captura.pack(fill=tk.BOTH, expand=True)

    label_to_name = cargar_label_to_name()

    usuarios_capturados = []