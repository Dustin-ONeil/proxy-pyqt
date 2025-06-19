from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class ImageCard(QFrame):  # <-- subclass QFrame instead of QWidget
    def __init__(self, image_path, title, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.title = title

        # Set frame style for a 3D border
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)  # thickness of the border

        # Set background color and texture with stylesheet
        self.setStyleSheet("""
            QFrame {
                background-color: #eef5ff;
                background-image:
                    repeating-linear-gradient(
                        45deg,
                        rgba(255, 255, 255, 0.1),
                        rgba(255, 255, 255, 0.1) 2px,
                        transparent 2px,
                        transparent 6px
                    );
            }
            QCheckBox, QLabel {
                background: transparent;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet("background: transparent;")

        title_label = QLabel(self.title)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("background: transparent;")

        top_layout.addWidget(self.checkbox)
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(title_label)
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        pixmap = QPixmap(self.image_path).scaled(300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background: transparent;")

        layout.addLayout(top_layout)
        layout.addWidget(image_label)
        self.setLayout(layout)

    def is_checked(self):
        return self.checkbox.isChecked()
