import tkinter as tk

def principal_view(root, username, cargar_login_view):
    from Interfaz.addArea import gestionar_areas
    from Interfaz.Agregarbd import AgregarBaseDeDatos
    from Interfaz.Data import iniciar_interfaz
    from Interfaz.AsignarCamaras import asignar_camaras_view
    from Back.Reconocimiento_gray import FaceRecognitionApp
    

    def cargar_usuarios():
        iniciar_interfaz(root, username, regresar_a_principal, cargar_login_view)

    def agregar_database():
        AgregarBaseDeDatos(tk.Toplevel(root))

    def agregar_area():
        gestionar_areas(root, username, regresar_a_principal, cargar_login_view)

    def asignacion_camaras():
        asignar_camaras_view(root, username, regresar_a_principal, cargar_login_view)

    def ejecutar_reconocimiento():
        for widget in root.winfo_children():
            widget.destroy()
        FaceRecognitionApp(root, regresar_a_principal)

    def mostrar_notificacion(mensaje, color="green"):
        notificacion_label.config(text=mensaje, fg=color)
        root.after(2000, limpiar_notificacion)

    def regresar_a_principal(*args):
        for widget in root.winfo_children():
            widget.destroy()
        principal_view(root, username, cargar_login_view)

    def limpiar_notificacion():
        notificacion_label.config(text="")

    def cerrar_sesion():
        for widget in root.winfo_children():
            widget.destroy()
        cargar_login_view(root)

    root.geometry("800x720")
    root.configure(bg="#e0f7fa")

    main_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
    main_frame.pack(expand=True, padx=20, pady=20, fill=tk.BOTH)

    bienvenida_label = tk.Label(main_frame, text=f"Bienvenido, {username}", font=("Arial", 18), bg="white", fg="black")
    bienvenida_label.pack(pady=10)

    notificacion_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
    notificacion_label.pack(pady=10)

    button_style = {
        "font": ("Arial", 14), "bg": "#004d40", "fg": "white",
        "activebackground": "#00332d", "activeforeground": "white",
        "bd": 2, "relief": tk.RAISED, "borderwidth": 3
    }

    tk.Button(main_frame, text="Agregar áreas", command=agregar_area, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Asignar cámaras", command=asignacion_camaras, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Cargar Usuarios", command=cargar_usuarios, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Conectar base de datos", command=agregar_database, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Ejecutar Reconocimiento Facial", command=ejecutar_reconocimiento, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Cerrar sesión", command=cerrar_sesion, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)

def cargar_login_view(root):
    for widget in root.winfo_children():
        widget.destroy()
    from FACE_CAP import login_view
    login_view(root)

