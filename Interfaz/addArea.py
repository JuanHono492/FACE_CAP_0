import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

areas_path = 'areas.json'

def cargar_areas():
    if os.path.exists(areas_path):
        with open(areas_path, 'r') as f:
            data = json.load(f)
            return data.get('areas', [])
    return []

def guardar_areas(areas):
    with open(areas_path, 'w') as f:
        json.dump({"areas": areas}, f, indent=4)

def agregar_area(area):
    if not area or any(char in area for char in r'\/:*?"<>|'):
        messagebox.showwarning("Advertencia", "El nombre del área no puede estar vacío o contener caracteres especiales.")
        return
    areas = cargar_areas()
    if area not in areas:
        areas.append(area)
        guardar_areas(areas)
        actualizar_lista_areas()

def eliminar_area(area):
    areas = cargar_areas()
    if area in areas:
        areas.remove(area)
        guardar_areas(areas)
        actualizar_lista_areas()

def actualizar_lista_areas():
    lista_areas.delete(0, tk.END)
    for area in cargar_areas():
        lista_areas.insert(tk.END, area)

def agregar_area_interfaz():
    area = entrada_area.get()
    agregar_area(area)
    entrada_area.delete(0, tk.END)

def eliminar_area_interfaz():
    seleccion = lista_areas.curselection()
    if seleccion:
        area = lista_areas.get(seleccion)
        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el área '{area}'?"):
            eliminar_area(area)

def cargar_areas_desde_archivo():
    archivo_path = filedialog.askopenfilename(title="Seleccionar archivo JSON", filetypes=[("Archivos JSON", "*.json")])
    if archivo_path:
        try:
            with open(archivo_path, 'r') as f:
                data = json.load(f)
                for area in data.get('areas', []):
                    agregar_area(area)
            messagebox.showinfo("Éxito", "Áreas cargadas correctamente.")
        except json.JSONDecodeError:
            messagebox.showwarning("Error", "El archivo seleccionado no es un JSON válido.")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

def gestionar_areas(root, username, regresar_a_principal, cargar_login_view):

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Gestión de Áreas")
    root.configure(bg="#e0f7fa")

    estilo_label = {"font": ("Arial", 12), "bg": "#e0f7fa"}
    estilo_entry = {"font": ("Arial", 12)}

    tk.Label(root, text="Nombre del Área:", **estilo_label).pack(pady=10)
    global entrada_area
    entrada_area = tk.Entry(root, **estilo_entry)
    entrada_area.pack(pady=5)

    tk.Button(root, text="Agregar Área", command=agregar_area_interfaz, bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=10)

    tk.Label(root, text="Áreas existentes:", **estilo_label).pack(pady=10)
    global lista_areas
    lista_areas = tk.Listbox(root, font=("Arial", 12))
    lista_areas.pack(pady=5, fill=tk.BOTH, expand=True)

    tk.Button(root, text="Eliminar Área", command=eliminar_area_interfaz, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Cargar Áreas desde Archivo JSON", command=cargar_areas_desde_archivo, bg="#2196f3", fg="white", font=("Arial", 12)).pack(pady=10)

    # Botón para regresar a la vista principal
    tk.Button(root, text="Regresar a Principal", command=lambda: regresar_a_principal(username, cargar_login_view), bg="#ff9800", fg="white", font=("Arial", 12)).pack(pady=10)

    actualizar_lista_areas()