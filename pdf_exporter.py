from PyQt5.QtGui import QPainter, QImage, QPen, QColor
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtPrintSupport import QPrinter


class PDFExporter:
    def __init__(self, filename, page_size=None):
        self.filename = filename
        self.page_size = page_size  # Optional, e.g. QPageSize.A4

    def mm_to_pixels(self, printer, mm):
        dpi = printer.resolution()
        inches = mm / 25.4
        return int(dpi * inches)

    def export(self, image_cards):
        if not image_cards:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setResolution(300)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(self.filename)
        printer.setPageSize(QPrinter.Letter)  # or QPrinter.Letter
        printer.setFullPage(True)
        printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)

        page_rect = printer.pageRect()

        # Sizes in millimeters
        img_w_mm = 63
        img_h_mm = 88
        crop_mm = 3.175
        cutline_len_mm = 16    # Length of red trim lines at page edges
        corner_len_mm = 7     # Length of cyan corner marks on images

        # Convert sizes to pixels
        img_w_px = self.mm_to_pixels(printer, img_w_mm)
        img_h_px = self.mm_to_pixels(printer, img_h_mm)
        crop_px = self.mm_to_pixels(printer, crop_mm)
        cutline_px = self.mm_to_pixels(printer, cutline_len_mm)
        corner_px = self.mm_to_pixels(printer, corner_len_mm)

        # Grid setup
        cols, rows = 3, 3
        grid_w = img_w_px * cols
        grid_h = img_h_px * rows

        offset_x = (page_rect.width() - grid_w) // 2
        offset_y = (page_rect.height() - grid_h) // 2

        painter = QPainter()
        painter.begin(printer)

        def draw_cut_lines():
            pen = QPen(QColor(0, 0, 0))  # Bright red
            pen.setWidth(4)
            painter.setPen(pen)

            # Vertical red lines at all column edges (0 to cols)
            for col in range(cols + 1):
                x = offset_x + col * img_w_px
                painter.drawLine(x, 0, x, cutline_px)  # Top edge
                painter.drawLine(x, page_rect.height() - cutline_px, x, page_rect.height())  # Bottom edge

            # Horizontal red lines at all row edges (0 to rows)
            for row in range(rows + 1):
                y = offset_y + row * img_h_px
                painter.drawLine(0, y, cutline_px, y)  # Left edge
                painter.drawLine(page_rect.width() - cutline_px, y, page_rect.width(), y)  # Right edge

        def draw_corner_marks(x, y):
            pen = QPen(QColor(255, 0, 255))  # Magenta
            pen.setWidth(4)                  # Thicker
            painter.setPen(pen)

            corner_len_mm = 1
            corner_px = self.mm_to_pixels(printer, corner_len_mm)

            # Top-left corner
            painter.drawLine(x, y, x + corner_px, y)
            painter.drawLine(x, y, x, y + corner_px)

            # Top-right corner
            painter.drawLine(x + img_w_px, y, x + img_w_px - corner_px, y)
            painter.drawLine(x + img_w_px, y, x + img_w_px, y + corner_px)

            # Bottom-left corner
            painter.drawLine(x, y + img_h_px, x + corner_px, y + img_h_px)
            painter.drawLine(x, y + img_h_px, x, y + img_h_px - corner_px)

            # Bottom-right corner
            painter.drawLine(x + img_w_px, y + img_h_px, x + img_w_px - corner_px, y + img_h_px)
            painter.drawLine(x + img_w_px, y + img_h_px, x + img_w_px, y + img_h_px - corner_px)

        for idx, card in enumerate(image_cards):
            grid_idx = idx % (cols * rows)
            row = grid_idx // cols
            col = grid_idx % cols

            if grid_idx == 0 and idx > 0:
                printer.newPage()

            if grid_idx == 0:
                draw_cut_lines()

            x = offset_x + col * img_w_px
            y = offset_y + row * img_h_px

            image = QImage(card.image_path)
            if image.isNull():
                continue

            if card.is_cropped():
                # Crop image by 3.175mm on all sides
                crop_rect = QRect(
                    crop_px,
                    crop_px,
                    max(1, image.width() - 2 * crop_px),
                    max(1, image.height() - 2 * crop_px),
                )
                image_to_draw = image.copy(crop_rect)
            else:
                image_to_draw = image

            # Scale to exact card size
            scaled_image = image_to_draw.scaled(
                img_w_px,
                img_h_px,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )

            painter.drawImage(x, y, scaled_image)

            # Draw cyan corner marks on top of image
            draw_corner_marks(x, y)

        painter.end()
