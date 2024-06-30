import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import wmi

class CameraAssignmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asignar Cámaras a Áreas")

        # Diccionario de asignación de cámaras a áreas
        self.camara_area = {}

        # Cargar las áreas desde el archivo JSON
        areas_path = os.path.join('areas.json')
        with open(areas_path, 'r') as f:
            self.areas = json.load(f)['areas']

        # Cargar las asignaciones desde el archivo JSON
        self.load_assignments()

        # Crear widgets de la interfaz
        self.create_widgets()
        self.update_assignment_table()

    def create_widgets(self):
        self.camera_label = tk.Label(self.root, text="Seleccionar Cámara:")
        self.camera_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.camera_combobox = ttk.Combobox(self.root, values=self.get_available_cameras())
        self.camera_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.area_label = tk.Label(self.root, text="Seleccionar Área:")
        self.area_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.area_combobox = ttk.Combobox(self.root, values=self.areas)
        self.area_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.assign_button = tk.Button(self.root, text="Asignar Área a Cámara", command=self.assign_camera_to_area)
        self.assign_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.assignment_table = ttk.Treeview(self.root, columns=("Cámara", "Área"), show='headings')
        self.assignment_table.heading("Cámara", text="Cámara")
        self.assignment_table.heading("Área", text="Área")
        self.assignment_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.remove_button = tk.Button(self.root, text="Eliminar Asignación", command=self.remove_assignment)
        self.remove_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.back_button = tk.Button(self.root, text="Atrás", command=self.root.destroy)
        self.back_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def get_available_cameras(self):
        arr = []
        index = 0
        wmi_service = wmi.WMI()
        cameras = wmi_service.Win32_PnPEntity()
        for camera in cameras:
            if camera.Name and "camera" in camera.Name.lower():
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    arr.append(f'Camera {index}: {camera.Name}')
                    cap.release()
                index += 1
        return arr

    def assign_camera_to_area(self):
        camera = self.camera_combobox.get()
        area = self.area_combobox.get()
        if not camera or not area:
            messagebox.showwarning("Advertencia", "Debe seleccionar una cámara y un área.")
            return
        self.camara_area[camera] = area
        self.update_assignment_table()
        self.save_assignments()
        print(f"Área {area} asignada a {camera}")  # Depuración
        messagebox.showinfo("Asignación", f"Área {area} asignada a {camera}")

    def update_assignment_table(self):
        for item in self.assignment_table.get_children():
            self.assignment_table.delete(item)
        for camera, area in self.camara_area.items():
            self.assignment_table.insert("", "end", values=(camera, area))

    def remove_assignment(self):
        selected_item = self.assignment_table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar una asignación para eliminar.")
            return
        camera, area = self.assignment_table.item(selected_item)["values"]
        del self.camara_area[camera]
        self.update_assignment_table()
        self.save_assignments()
        messagebox.showinfo("Eliminar", f"Asignación de {camera} a {area} eliminada")

    def load_assignments(self):
        try:
            with open('camera_assignments.json', 'r') as f:
                self.camara_area = json.load(f)
        except FileNotFoundError:
            self.camara_area = {}

    def save_assignments(self):
        try:
            with open('camera_assignments.json', 'w') as f:
                json.dump(self.camara_area, f)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar asignaciones: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraAssignmentApp(root)
    root.mainloop()

