import tkinter as tk
from tkinter import messagebox
import json
import os

class AgregarBaseDeDatos:
    def __init__(self, master):
        self.master = master
        self.master.title("Agregar Base de Datos")
        self.master.geometry("500x400")
        self.master.configure(bg="#e0f7fa")

        # Variables para almacenar las credenciales de conexión
        self.host_var = tk.StringVar()
        self.port_var = tk.StringVar()
        self.dbname_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Crear elementos de la interfaz
        self.label = tk.Label(master, text="Agregar Base de Datos", font=("Arial", 16), bg="#e0f7fa")
        self.label.pack(pady=10)

        input_frame = tk.Frame(master, bg="#e0f7fa")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Host:", font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5)
        self.host_entry = tk.Entry(input_frame, textvariable=self.host_var, font=("Arial", 12))
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Puerto:", font=("Arial", 12), bg="#e0f7fa").grid(row=1, column=0, padx=5, pady=5)
        self.port_entry = tk.Entry(input_frame, textvariable=self.port_var, font=("Arial", 12))
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Nombre de la BD:", font=("Arial", 12), bg="#e0f7fa").grid(row=2, column=0, padx=5, pady=5)
        self.dbname_entry = tk.Entry(input_frame, textvariable=self.dbname_var, font=("Arial", 12))
        self.dbname_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Usuario:", font=("Arial", 12), bg="#e0f7fa").grid(row=3, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(input_frame, textvariable=self.username_var, font=("Arial", 12))
        self.username_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Contraseña:", font=("Arial", 12), bg="#e0f7fa").grid(row=4, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*", font=("Arial", 12))
        self.password_entry.grid(row=4, column=1, padx=5, pady=5)

        self.agregar_button = tk.Button(master, text="Agregar", font=("Arial", 12), bg="#004d40", fg="white", command=self.agregar_base_datos)
        self.agregar_button.pack(pady=10)

        self.borrar_button = tk.Button(master, text="Borrar", font=("Arial", 12), bg="#004d40", fg="white", command=self.borrar_campos)
        self.borrar_button.pack(pady=10)

    def agregar_base_datos(self):
        host = self.host_var.get()
        port = self.port_var.get()
        dbname = self.dbname_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        if not all([host, port, dbname, username, password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        credenciales = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "username": username,
            "password": password
        }

        try:
            with open("Back/database_config.json", "w") as file:
                json.dump(credenciales, file)
            messagebox.showinfo("Éxito", "Base de datos agregada correctamente")
            self.master.destroy()  # Cerrar la ventana después de agregar la base de datos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la base de datos: {e}")

    def borrar_campos(self):
        self.host_var.set("")
        self.port_var.set("")
        self.dbname_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        
        # Borrar contenido del archivo JSON
        try:
            with open("Back/database_config.json", "w") as file:
                json.dump({}, file)
            messagebox.showinfo("Éxito", "Campos borrados correctamente y archivo JSON limpiado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo limpiar el archivo JSON: {e}")