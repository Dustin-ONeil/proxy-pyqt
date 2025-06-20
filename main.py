import sys
import os
import re
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QScrollArea, QVBoxLayout,
    QPushButton, QFileDialog, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
from image_card import ImageCard
from pdf_exporter import PDFExporter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Grid Viewer")
        self.resize(1200, int(0.8 * QApplication.primaryScreen().size().height()))
        self.image_cards = []
        self.dark_mode_enabled = False
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        # Scrollable image grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container = QWidget()
        self.grid_layout = QGridLayout()
        self.container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.container)

        # Bottom controls: Dark Mode + Export
        button_layout = QHBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        export_button = QPushButton("Export PDF")
        export_button.clicked.connect(self.export_pdf)

        button_layout.addWidget(self.dark_mode_checkbox)
        button_layout.addStretch()
        button_layout.addWidget(export_button)

        # Load images into grid
        self.load_images()

        # Final layout
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)

    def load_images(self):
        image_dir = "images"
        image_data = []

        for f in os.listdir(image_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                filepath = os.path.join(image_dir, f)
                name, _ = os.path.splitext(f)
                clean_name = re.sub(r"\s*\(.*?\)", "", name).strip()
                image_data.append((filepath, clean_name))

        cols = 3
        for idx, (path, title) in enumerate(image_data):
            row, col = divmod(idx, cols)
            card = ImageCard(path, title)
            card.set_dark_mode(self.dark_mode_enabled)
            self.grid_layout.addWidget(card, row, col)
            self.image_cards.append(card)

    def toggle_dark_mode(self, state):
        self.dark_mode_enabled = state == Qt.Checked

        # App-wide style
        if self.dark_mode_enabled:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #f0f0f0;
                }
                QScrollArea {
                    background-color: #121212;
                }
                QPushButton {
                    background-color: #333;
                    color: #fff;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QCheckBox {
                    color: #ccc;
                }
            """)
        else:
            self.setStyleSheet("")

        # Update all image cards
        for card in self.image_cards:
            card.set_dark_mode(self.dark_mode_enabled)

    def export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if not filename:
            return
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        selected_cards = [card for card in self.image_cards if card.is_checked()]
        if not selected_cards:
            return

        exporter = PDFExporter(filename)
        exporter.export(selected_cards)

        # ✅ Automatically open the exported PDF
        webbrowser.open_new(r'file://' + os.path.abspath(filename))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
