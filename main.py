import os
import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import face_recognition

# Dossier où sont stockées les images de célébrités
IMAGE_DIR = 'image/'

# Fonction pour comparer l'image importée avec celles dans la base
def find_match(image_path):
    # Charger l'image importée
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(unknown_encoding) == 0:
        return "Aucun visage détecté dans l'image.", None

    unknown_encoding = unknown_encoding[0]

    # Parcourir les images de célébrités dans le dossier
    for folder in os.listdir(IMAGE_DIR):  # Supposons que chaque personne a son propre dossier dans `image/`
        person_folder_path = os.path.join(IMAGE_DIR, folder)
        if os.path.isdir(person_folder_path):  # Vérifie que c'est un dossier
            for file_name in os.listdir(person_folder_path):
                if file_name.endswith(('png', 'jpg', 'jpeg')):
                    celeb_image_path = os.path.join(person_folder_path, file_name)
                    celeb_image = face_recognition.load_image_file(celeb_image_path)
                    celeb_encoding = face_recognition.face_encodings(celeb_image)

                    if len(celeb_encoding) == 0:
                        continue

                    # Comparaison des visages
                    result = face_recognition.compare_faces([celeb_encoding[0]], unknown_encoding)
                    if result[0]:
                        return f"Célébrité trouvée : {folder}", celeb_image_path

    return "Aucune correspondance trouvée.", None


# Fonction pour ouvrir le fichier
def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        match_result, celeb_image_path = find_match(file_path)
        
        # Affichage de l'image sélectionnée
        img = Image.open(file_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        
        panel.configure(image=img)
        panel.image = img
        
        # Affichage de l'image de la célébrité si une correspondance est trouvée
        if celeb_image_path:
            celeb_img = Image.open(celeb_image_path)
            celeb_img = celeb_img.resize((300, 300), Image.Resampling.LANCZOS)
            celeb_img = ImageTk.PhotoImage(celeb_img)
            celeb_panel.configure(image=celeb_img)
            celeb_panel.image = celeb_img
        else:
            celeb_panel.config(image='')  # Ne pas afficher d'image si aucune correspondance

        result_label.config(text=match_result)

# Configuration de l'interface graphique avec tkinter
root = tk.Tk()
root.title("Reconnaissance Faciale de Célébrités")
root.geometry("700x450")  # Redimensionner pour inclure deux images

# Ajouter un bouton pour charger l'image
load_btn = tk.Button(root, text="Charger une image", command=load_image)
load_btn.pack(pady=20)

# Label pour afficher l'image importée
panel = Label(root)
panel.pack(side="left", padx=10)

# Label pour afficher l'image de la célébrité correspondante
celeb_panel = Label(root)
celeb_panel.pack(side="right", padx=10)

# Label pour afficher les résultats
result_label = Label(root, text="Résultat : ", font=("Helvetica", 14))
result_label.pack(pady=10)

root.mainloop()
