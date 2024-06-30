import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import cv2
from pygrabber.dshow_graph import FilterGraph

def asignar_camaras_view(root, username, regresar_a_principal, cargar_login_view):
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear el frame principal
    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(expand=True, padx=20, pady=20, fill=tk.BOTH)

    ttk.Label(main_frame, text="Asignar Cámaras a Áreas", font=("Arial", 18)).pack(pady=10)

    areas = cargar_areas()
    cameras = detectar_camaras()

    # Combobox para seleccionar área
    ttk.Label(main_frame, text="Seleccionar Área", font=("Arial", 14)).pack(pady=5)
    area_var = tk.StringVar()
    area_combobox = ttk.Combobox(main_frame, textvariable=area_var, values=areas, state="readonly")
    area_combobox.pack(pady=5, padx=20, fill=tk.BOTH)

    # Listbox para seleccionar cámaras
    ttk.Label(main_frame, text="Seleccionar Cámara", font=("Arial", 14)).pack(pady=5)
    camera_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, font=("Arial", 12))
    for camera in cameras:
        camera_listbox.insert(tk.END, camera)
    camera_listbox.pack(pady=5, padx=20, fill=tk.BOTH)

    def asignar_camaras():
        area = area_var.get()
        selected_cameras = [camera_listbox.get(i) for i in camera_listbox.curselection()]
        if not area:
            messagebox.showwarning("Advertencia", "Seleccione un área.")
            return
        if not selected_cameras:
            messagebox.showwarning("Advertencia", "Seleccione al menos una cámara.")
            return
        guardar_asignacion(area, selected_cameras)
        messagebox.showinfo("Información", f"Cámaras asignadas a {area} correctamente.")

    # Botón para asignar cámaras
    ttk.Button(main_frame, text="Asignar Cámaras", command=asignar_camaras).pack(pady=10, padx=20, fill=tk.BOTH)

    # Botón para regresar a la vista principal
    ttk.Button(main_frame, text="Regresar a Principal", command=lambda: regresar_a_principal(root, username, cargar_login_view)).pack(pady=10, padx=20, fill=tk.BOTH)

def cargar_areas():
    areas_path = 'areas.json'
    if os.path.exists(areas_path):
        with open(areas_path, 'r') as f:
            data = json.load(f)
            return data.get('areas', [])
    return []

def detectar_camaras():
    graph = FilterGraph()
    devices = graph.get_input_devices()
    return devices

def guardar_asignacion(area, cameras):
    asignaciones_path = 'asignaciones.json'
    asignaciones = {}
    if os.path.exists(asignaciones_path):
        with open(asignaciones_path, 'r') as f:
            asignaciones = json.load(f)
    
    if area not in asignaciones:
        asignaciones[area] = []
    
    for camera in cameras:
        if camera not in asignaciones[area]:
            asignaciones[area].append(camera)

    with open(asignaciones_path, 'w') as f:
        json.dump(asignaciones, f, indent=4)
