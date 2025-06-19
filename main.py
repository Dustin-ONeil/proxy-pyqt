import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QScrollArea, QVBoxLayout,
    QPushButton, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt
from image_card import ImageCard
from pdf_exporter import PDFExporter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Grid Viewer")
        self.image_cards = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Scrollable container for grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(10)

        scroll_area.setWidget(container)

        # Load images into grid
        self.load_images()

        # Export button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        export_button = QPushButton("Export PDF")
        export_button.clicked.connect(self.export_pdf)
        button_layout.addWidget(export_button)

        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)

        # Resize window width to fit exactly 3 columns of cards + spacing + margins
        self.adjust_window_size()

    def load_images(self):
        image_dir = "images"
        image_data = []

        for f in sorted(os.listdir(image_dir)):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                filepath = os.path.join(image_dir, f)
                name, _ = os.path.splitext(f)
                clean_name = re.sub(r"\s*\(.*?\)", "", name).strip()
                image_data.append((filepath, clean_name))

        cols = 3
        for idx, (path, title) in enumerate(image_data):
            row, col = divmod(idx, cols)
            card = ImageCard(path, title)
            self.grid_layout.addWidget(card, row, col)
            self.image_cards.append(card)

    def adjust_window_size(self):
        card_width = 320  
        spacing = self.grid_layout.horizontalSpacing()
        margins = self.grid_layout.contentsMargins()

        cols = 3
        total_width = cols * card_width + (cols - 1) * spacing
        total_width += margins.left() + margins.right()
        total_width += 40  # window frame buffer

        screen = QApplication.primaryScreen().availableGeometry()
        max_width = screen.width() - 50
        max_height = int(screen.height() * 0.9)  # 80% of screen height

        final_width = min(total_width, max_width)
        final_height = max_height

        self.setFixedSize(final_width, final_height)


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
