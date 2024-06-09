import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt
from rembg import remove, new_session
from PIL import Image, ImageFilter

class ImageBackgroundRemover(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.session = new_session('u2netp')  # Modèle par défaut, Autres: u2net, u2netp, deeplabv3, u2net_human_seg, isnet-general-use, etc.

    def init_ui(self):
        self.setWindowTitle("Remove background 1.0")
        self.setFixedSize(800, 600)  # Taille fixe de la fenêtre
        self.setStyleSheet("background-color: #f0f0f0;")  # Couleur de fond

        self.input_path = ""
        self.output_path = ""

        # Layout principal
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Layout horizontal pour les boutons
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        # Bouton pour sélectionner l'image
        self.select_button = QPushButton("Sélectionner un fichier image", self)
        self.select_button.setFont(QFont("Helvetica", 10))
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #87ceeb;
                color: #ffffff;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00bfff;
            }
        """)
        self.select_button.clicked.connect(self.select_file)
        button_layout.addWidget(self.select_button)

        # Bouton pour supprimer le fond
        self.remove_button = QPushButton("Supprimer le fond", self)
        self.remove_button.setFont(QFont("Helvetica", 12))
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4500;
                color: #ffffff;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6347;
            }
        """)
        self.remove_button.clicked.connect(self.remove_background)
        button_layout.addWidget(self.remove_button)

        # Label pour afficher l'image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(760, 500)  # Taille fixe pour la prévisualisation
        self.layout.addWidget(self.image_label)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.jpg *.jpeg *.png)", options=options)
        if file_path:
            try:
                # Validation du fichier sélectionné
                with Image.open(file_path) as img:
                    img.verify()  # Vérifie si le fichier est une image valide
                self.input_path = file_path
                output_dir = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier de sortie")
                if output_dir:
                    base = os.path.splitext(os.path.basename(file_path))[0]
                    self.output_path = os.path.join(output_dir, base + "-no-bg.png")
                    self.show_image(file_path)  # Prévisualiser automatiquement l'image sélectionnée
            except (IOError, SyntaxError) as e:
                QMessageBox.critical(self, "Erreur", f"Le fichier sélectionné n'est pas une image valide : {e}")

    def remove_background(self):
        if not self.input_path:
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner un fichier image valide.")
            return

        try:
            input_image = Image.open(self.input_path)
        except IOError as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir l'image : {e}")
            return

        try:
            output_image = remove(input_image, session=self.session)
            output_image = self.postprocess_image(output_image)
            output_image.save(self.output_path, "PNG")
            QMessageBox.information(self, "Résultat", "Le fichier de sortie a été enregistré avec succès.")
            self.show_image(self.output_path)  # Affiche l'image de sortie
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression du fond : {e}")

    def postprocess_image(self, image):
        # Appliquer un lissage pour améliorer les bords
        return image.filter(ImageFilter.SMOOTH_MORE)

    def show_image(self, image_path):
        image = QImage(image_path)
        if image.isNull():
            QMessageBox.critical(self, "Erreur", "Impossible de charger l'image.")
            return

        pixmap = QPixmap.fromImage(image)
        # Calculer la taille maximale pour l'affichage de l'image
        max_width = self.image_label.width()
        max_height = self.image_label.height()
        self.image_label.setPixmap(pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication([])
    window = ImageBackgroundRemover()
    window.show()
    app.exec()

