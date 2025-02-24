import os
import potrace
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QSlider
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from rembg import remove, new_session
from PIL import Image, ImageFilter
import numpy as np

class BackgroundRemoverWorker(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, input_path, output_path, session, opacity, format):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.session = session
        self.opacity = opacity
        self.format = format  # 'PNG' ou 'SVG'

    @pyqtSlot()
    def run(self):
        try:
            input_image = Image.open(self.input_path)
        except IOError as e:
            self.error_signal.emit(f"Impossible d'ouvrir l'image : {e}")
            return

        try:
            output_image = remove(input_image, session=self.session)
            output_image = self.postprocess_image(output_image)
            
            if self.format == 'SVG':
                # Convertir en binaire pour potrace (noir et blanc basé sur l'alpha)
                alpha = output_image.split()[3]  # Canal alpha
                binary_image = alpha.point(lambda x: 0 if x < 128 else 255, '1')  # Seuil à 128
                
                # Convertir en tableau numpy pour potrace
                bitmap = np.array(binary_image)
                
                # Créer un objet potrace et tracer les contours
                trace = potrace.Bitmap(bitmap)
                path = trace.trace()
                
                # Générer le contenu SVG
                svg_content = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
                svg_content += f'<svg width="{output_image.width}" height="{output_image.height}" xmlns="http://www.w3.org/2000/svg">\n'
                for curve in path:
                    svg_content += '  <path d="'
                    parts = []
                    for i, segment in enumerate(curve):
                        if i == 0:
                            # Premier point de la courbe
                            start_x, start_y = segment.end_point if segment.is_corner else segment.c1
                            parts.append(f"M {start_x} {start_y}")
                        if segment.is_corner:
                            # Segment de coin : ligne droite
                            c_x, c_y = segment.c
                            end_x, end_y = segment.end_point
                            parts.append(f"L {c_x} {c_y}")
                            parts.append(f"L {end_x} {end_y}")
                        else:
                            # Segment de Bézier : courbe cubique
                            c1_x, c1_y = segment.c1
                            c2_x, c2_y = segment.c2
                            end_x, end_y = segment.end_point
                            parts.append(f"C {c1_x} {c1_y} {c2_x} {c2_y} {end_x} {end_y}")
                    svg_content += " ".join(parts) + ' Z" fill="black" />\n'  # 'Z' ferme le chemin
                svg_content += '</svg>'
                
                # Écrire le fichier SVG
                with open(self.output_path, 'w') as svg_file:
                    svg_file.write(svg_content)
            else:
                output_image.save(self.output_path, "PNG")
            self.result_signal.emit(self.output_path)
        except Exception as e:
            self.error_signal.emit(f"Erreur lors de la suppression du fond : {e}")

    def postprocess_image(self, image):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        background = Image.new('RGBA', image.size, (255, 255, 255, self.opacity))
        final_image = Image.alpha_composite(background, image)
        return final_image.filter(ImageFilter.SMOOTH_MORE)

class ImageBackgroundRemover(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = new_session('u2netp')
        self.opacity = 0
        self.format = 'PNG'  # Format par défaut
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Remove background 1.7")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.input_path = ""
        self.output_path = ""

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Layout pour les boutons et options
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

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
        self.remove_button.clicked.connect(self.start_background_removal)
        button_layout.addWidget(self.remove_button)

        self.model_combo = QComboBox(self)
        self.model_combo.addItems(['u2netp', 'u2net', 'u2net_human_seg', 'silueta'])
        self.model_combo.setFont(QFont("Helvetica", 10))
        self.model_combo.currentTextChanged.connect(self.update_model)
        button_layout.addWidget(self.model_combo)

        # Options avancées
        options_layout = QVBoxLayout()
        self.layout.addLayout(options_layout)

        # Slider pour opacité
        options_layout.addWidget(QLabel("Opacité du fond :"))
        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(255)
        self.opacity_slider.setValue(0)
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(25)
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        options_layout.addWidget(self.opacity_slider)

        # Choix du format
        options_layout.addWidget(QLabel("Format de sortie :"))
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(['PNG', 'SVG'])
        self.format_combo.setFont(QFont("Helvetica", 10))
        self.format_combo.currentTextChanged.connect(self.update_format)
        options_layout.addWidget(self.format_combo)

        # Layout pour les images
        image_layout = QHBoxLayout()
        self.layout.addLayout(image_layout)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(380, 450)
        image_layout.addWidget(self.image_label)

        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedSize(380, 450)
        image_layout.addWidget(self.preview_label)

        self.worker_thread = BackgroundRemoverWorker("", "", self.session, self.opacity, self.format)
        self.worker_thread.result_signal.connect(self.on_remove_background_success)
        self.worker_thread.error_signal.connect(self.on_remove_background_error)

    def update_model(self, model_name):
        self.session = new_session(model_name)

    def update_opacity(self, value):
        self.opacity = value

    def update_format(self, format_name):
        self.format = format_name

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.jpg *.jpeg *.png)", options=options)
        if file_path:
            try:
                with Image.open(file_path) as img:
                    img.verify()
                self.input_path = file_path
                output_dir = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier de sortie")
                if output_dir:
                    base = os.path.splitext(os.path.basename(file_path))[0]
                    ext = '.svg' if self.format == 'SVG' else '.png'
                    self.output_path = os.path.join(output_dir, base + "-no-bg" + ext)
                    self.show_image(file_path)
            except (IOError, SyntaxError) as e:
                QMessageBox.critical(self, "Erreur", f"Le fichier sélectionné n'est pas une image valide : {e}")

    def start_background_removal(self):
        if not self.input_path:
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner un fichier image valide.")
            return

        self.worker_thread = BackgroundRemoverWorker(self.input_path, self.output_path, self.session, self.opacity, self.format)
        self.worker_thread.result_signal.connect(self.on_remove_background_success)
        self.worker_thread.error_signal.connect(self.on_remove_background_error)
        self.worker_thread.start()

    def on_remove_background_success(self, output_path):
        QMessageBox.information(self, "Résultat", "Le fichier de sortie a été enregistré avec succès.")
        self.show_image(self.input_path)
        # Pour SVG, on génère un PNG temporaire pour l'affichage
        display_path = output_path
        if self.format == 'SVG':
            temp_png = output_path.replace('.svg', '_temp.png')
            with Image.open(self.input_path) as img:
                processed_img = remove(img, session=self.session)
                processed_img = self.postprocess_image(processed_img)
                processed_img.save(temp_png, "PNG")
            display_path = temp_png
        image = QImage(display_path)
        if not image.isNull():
            pixmap = QPixmap.fromImage(image)
            max_width = self.preview_label.width()
            max_height = self.preview_label.height()
            self.preview_label.setPixmap(pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if self.format == 'SVG' and os.path.exists(temp_png):
            os.remove(temp_png)

    def on_remove_background_error(self, error_message):
        QMessageBox.critical(self, "Erreur", error_message)

    def postprocess_image(self, image):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        background = Image.new('RGBA', image.size, (255, 255, 255, self.opacity))
        final_image = Image.alpha_composite(background, image)
        return final_image.filter(ImageFilter.SMOOTH_MORE)

    def show_image(self, image_path):
        image = QImage(image_path)
        if not image.isNull():
            pixmap = QPixmap.fromImage(image)
            max_width = self.image_label.width()
            max_height = self.image_label.height()
            self.image_label.setPixmap(pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication([])
    window = ImageBackgroundRemover()
    window.show()
    app.exec_()
