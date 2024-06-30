import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from usuarios import verificar_credenciales, registrar_usuario
from Interfaz.Principal import cargar_login_view, principal_view
from Interfaz.addArea import gestionar_areas  # Import relativo si están en el mismo módulo

def login():
    username = username_entry.get()
    password = password_entry.get()

    if verificar_credenciales(username, password):
        loading_label.grid(row=5, column=0, columnspan=2, pady=10)
        root.after(2000, lambda: open_principal_view(username))
    else:
        messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos")

def open_principal_view(username):
    loading_label.grid_forget()
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("800x650")
    principal_view(root, username, cargar_login_view)

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

def show_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Registro de Usuario")
    register_window.geometry("400x300")
    register_window.configure(bg="#00AA66")

    def register():
        username = new_username_entry.get()
        password = new_password_entry.get()
        if registrar_usuario(username, password):
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
            register_window.destroy()
        else:
            messagebox.showerror("Error de registro", "El nombre de usuario ya existe")

    tk.Label(register_window, text="Nombre de usuario:", font=("Arial", 12), bg="#ffffff").pack(pady=10)
    new_username_entry = tk.Entry(register_window, font=("Arial", 12))
    new_username_entry.pack(pady=10)

    tk.Label(register_window, text="Contraseña:", font=("Arial", 12), bg="#ffffff").pack(pady=10)
    new_password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
    new_password_entry.pack(pady=10)

    tk.Button(register_window, text="Registrar", command=register, font=("Arial", 12), bg="#004d40", fg="#ffffff").pack(pady=10)

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.geometry("800x700")
root.configure(bg="#00AA66")

# Crear un frame principal para centrar el contenido con fondo blanco y borde
main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
main_frame.pack(expand=True, padx=20, pady=20)

# Cargar la imagen con Pillow
logo_image = Image.open("Interfaz/logo.png")
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(main_frame, image=logo, bg="#ffffff")
logo_label.grid(row=0, column=0, columnspan=2, pady=20)

# Crear un frame para el formulario
form_frame = tk.Frame(main_frame, bg="#ffffff")
form_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Crear etiquetas y campos de entrada para el inicio de sesión
tk.Label(form_frame, text="Nombre de usuario:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(form_frame, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Contraseña:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=5)

toggle_button = tk.Button(form_frame, text="Mostrar contraseña", command=toggle_password_visibility, font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
toggle_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

login_button = tk.Button(form_frame, text="Iniciar sesión", command=login, font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

register_button = tk.Button(form_frame, text="Registrar", command=show_register_window, font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Etiqueta para la animación de carga
loading_label = tk.Label(form_frame, text="Cargando...", font=("Arial", 12), bg="#ffffff")

# Iniciar el bucle de la ventana
root.mainloop()
