import cv2
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import sys

def resource_path(relative_path):
    """ Obtener la ruta absoluta a un recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FaceRecognitionApp:
    def __init__(self, root, volver_a_principal):
        self.root = root
        self.root.title("Reconocimiento Facial")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa")

        # Initialize canvas for video display
        self.canvas = tk.Canvas(self.root, width=640, height=480, bg="#000000")
        self.canvas.pack(pady=20)

        # Create a combobox for area selection
        self.area_selector = ttk.Combobox(self.root, font=("Arial", 12))
        self.area_selector.pack(pady=10)

        # Add a button to go back to the main window
        tk.Button(root, text="Regresar a Principal", command=volver_a_principal, bg="#ff9800", fg="white", font=("Arial", 12)).pack(pady=10)

        if not self.load_face_recognizer() or not self.load_areas():
            messagebox.showerror("Error", "No se ha encontrado archivo necesario. La aplicación se cerrará.")
            self.root.destroy()
            return

        # Start face recognition
        self.recognize_face()

    def load_areas(self):
        try:
            areas_json_file = resource_path('areas.json')
            if not os.path.exists(areas_json_file):
                print(f"Error: El archivo 'areas.json' no se encuentra en la ruta: {areas_json_file}")
                return False
            with open(areas_json_file, 'r') as areas_file:
                areas_data = json.load(areas_file)
            areas_list = areas_data.get('areas', [])
            self.area_selector['values'] = areas_list
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar 'areas.json': {e}")
            return False

    def load_face_recognizer(self):
        try:
            label_to_name_path = resource_path('label_to_name.json')
            if not os.path.exists(label_to_name_path):
                print(f"Error: El archivo 'label_to_name.json' no se encuentra en la ruta: {label_to_name_path}")
                return False
            with open(label_to_name_path, 'r') as f:
                self.label_to_name = json.load(f)

            # Create the face recognizer
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

            # Load the trained model if it exists
            model_path = resource_path('modelo_entrenado.xml')
            if os.path.exists(model_path):
                self.face_recognizer.read(model_path)
            else:
                print(f"El archivo del modelo entrenado no se encuentra en la ruta: {model_path}. Se necesita entrenar el modelo.")
                return False

            # Check if haarcascade file exists
            haarcascade_path = resource_path('haarcascade_frontalface_default.xml')
            if not os.path.exists(haarcascade_path):
                print(f"Error: El archivo Haar Cascade no se encuentra en la ruta: {haarcascade_path}")
                return False

            # Initialize video capture
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: No se pudo acceder a la cámara.")
                return False

            return True
        except (FileNotFoundError, cv2.error) as e:
            print(f"Error al cargar el modelo o los archivos necesarios: {e}")
            return False

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_area_status(self, person_areas, selected_area):
        if selected_area and selected_area in person_areas:
            return selected_area
        else:
            return None

    def recognize_face(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(resource_path('haarcascade_frontalface_default.xml'))
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            label, confidence = self.face_recognizer.predict(face_roi)

            if confidence > 99:
                person_name = 'Desconocido'
                person_areas = []
                color = '#FF0000'  # Red for unknown
            else:
                person_data = self.label_to_name.get(str(label))
                if person_data:
                    person_name = person_data.get('nombre', f'Persona {label}')
                    person_areas = person_data.get('areas', [])
                else:
                    person_name = f'Persona {label}'
                    person_areas = []

            selected_area = self.area_selector.get()
            area_status = self.get_area_status(person_areas, selected_area)

            if person_name == 'Desconocido':
                color = '#FF0000'  # Red for unknown
            elif area_status == selected_area:
                color = '#00FF00'  # Green if area matches
            else:
                color = '#FFA500'  # Orange if area does not match

            color_rgb = self.hex_to_rgb(color)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color_rgb, 2)
            text_y = y - 10

            cv2.putText(frame, person_name, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_rgb, 2)
            if area_status:
                cv2.putText(frame, area_status, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_rgb, 2)

            confidence_text = f'Confianza: {confidence:.2f}'
            cv2.putText(frame, confidence_text, (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_rgb, 2)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 480))
        img = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())

        self.canvas.img = img
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.root.after(10, self.recognize_face)

    def __del__(self):
        self.cap.release()

def main():
    def volver_a_principal():
        root.destroy()
        # Aquí deberías iniciar la ventana principal
        root = tk.Tk()
        app = FaceRecognitionApp(root, volver_a_principal)
        root.mainloop()



if __name__ == "__main__":
    main()
