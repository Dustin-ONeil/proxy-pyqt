from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QRect
import re

class ImageCard(QFrame):
    def __init__(self, image_path, title, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.title = title

        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)

        self.dark_mode = False
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)

        # Checkboxes
        checkbox_layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)

        self.cropped_checkbox = QCheckBox("Cropped")
        if re.search(r"(?i)^.*[a-zA-Z]{3}-\d+-.*\.jpg$", self.image_path, re.IGNORECASE):
            self.cropped_checkbox.setChecked(False)
        else: 
            self.cropped_checkbox.setChecked(True)
        self.cropped_checkbox.stateChanged.connect(self.update_image)

        checkbox_layout.addWidget(self.checkbox)
        checkbox_layout.addWidget(self.cropped_checkbox)

        # Title label
        self.title_label = QLabel(self.title)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)

        top_layout.addLayout(checkbox_layout)
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(self.title_label)
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

        self.update_image()
        self.update_stylesheet()

    def update_image(self):
        original_image = QImage(self.image_path)


        if self.is_cropped():
            dpi = 300
            crop_mm = 6.35
            crop_px = int((crop_mm / 25.4) * dpi)
            # img_w_mm = 63
            # img_h_mm = 88

            crop_rect = QRect(
                crop_px,
                crop_px,
                max(1, original_image.width() - 2 * crop_px),
                max(1, original_image.height() - 2 * crop_px)
            )
            image = original_image.copy(crop_rect)
        else:
            image = original_image

        pixmap = QPixmap.fromImage(image).scaled(
            300, 400,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

    def is_checked(self):
        return self.checkbox.isChecked()

    def is_cropped(self):
        return self.cropped_checkbox.isChecked()
    
    # def is_from_MPC_fill(self):
    #     if re.match(r'^.*xxx-111-.*\.jpg$', self.image_path):
    #         return False
    #     else: 
    #         return True

    def set_dark_mode(self, enabled: bool):
        self.dark_mode = enabled
        self.update_stylesheet()

    def update_stylesheet(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QFrame {
                    background-color: #1e1e1e;
                    border: 2px solid #444;
                }
                QLabel {
                    color: #f0f0f0;
                    background: transparent;
                }
                QCheckBox {
                    color: #f0f0f0;
                    background: transparent;
                }
            """)
        else:
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
                QLabel, QCheckBox {
                    background: transparent;
                    color: black;
                }
            """)
