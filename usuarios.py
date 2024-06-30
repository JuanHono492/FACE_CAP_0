import json
import os

USERS_FILE = 'usuarios.json'

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

def guardar_usuarios(usuarios):
    with open(USERS_FILE, 'w') as file:
        json.dump(usuarios, file, indent=4)

def registrar_usuario(username, password):
    usuarios = cargar_usuarios()
    if username in usuarios:
        return False  # Usuario ya existe
    usuarios[username] = password
    guardar_usuarios(usuarios)
    return True

def verificar_credenciales(username, password):
    usuarios = cargar_usuarios()
    return usuarios.get(username) == password
