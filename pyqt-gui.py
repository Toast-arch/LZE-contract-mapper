from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image
import sys

from PyQt5.QtWidgets import QWidget

SCALE_FACTOR = 1.25

RS_CONTRACT_DICT = {
    ('Blue Passport', 'RS_blue_passport.png'),
    ('Console', 'RS_console.png'),
    ('Data Drive', 'RS_data_drive.png'),
    ('Drug Stash Snowmobile', 'RS_drugs_snow.png'),
    ('Filter', 'RS_filter.png'),
    ('Hard Drive', 'RS_hard_drive.png'),
    ('Lucky Bullet', 'RS_lucky_bullet.png'),
    ('Personel Data', 'RS_personel_data.png'),
    ('Petri Dish', 'RS_petri_dish.png'),
    ('Photo Friend', 'RS_photo_friend.png'),
    ('Red Passport', 'RS_red_passport.png'),
    ('Research Document', 'RS_research_documents.png'),
    ('Stamp', 'RS_stamp.png'),
    ('Weapon Case', 'RS_weapon_case.png'),
    ('Yellow ID', 'RS_yellow_id.png'),
}

class ContractCheckBox(QWidget):
    def __init__(self, parent = None, contract_name = None, image_path = None, toggled_checkbox_connect = None):
        super().__init__(parent)

        self.main_box = QHBoxLayout(self)

        self.check_box = QCheckBox(contract_name, self)
        self.check_box.toggled.connect(lambda:toggled_checkbox_connect(self.check_box))
        
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap(image_path))
        self.image_label.setFixedSize(50, 50)
        self.image_label.setScaledContents(True)

        self.main_box.addWidget(self.check_box)
        self.main_box.addWidget(self.image_label)

        self.setLayout(self.main_box)


class ContractSelector(QWidget):
    def __init__(self, parent=None, toggled_checkbox_connect = None):
        super(ContractSelector, self).__init__()

        self.setFixedWidth(250)

        self.main_box = QHBoxLayout(self)

        self.button_vertical_box = QVBoxLayout()

        self.scroll = QScrollArea(self)

        # dic = {}
        
        # for i in range(30):
        #     dic['foo '+str(i)] = [i]
        
        for contract in RS_CONTRACT_DICT:
            btn = ContractCheckBox(self, contract[0], "./src/lze-contract-mapper/ressources/RS_contracts/" + contract[1], toggled_checkbox_connect)
            # btn.toggled.connect(lambda:toggled_checkbox_connect(btn))
            self.button_vertical_box.addWidget(btn)

        # for key, _ in sorted(dic.items()):
        #     btn = ContractCheckBox(self, key, "./src/lze-contract-mapper/ressources/RS_contracts/RS_filter.png")
        #     self.button_vertical_box.addWidget(btn)

        holder = QWidget()
        holder.setLayout(self.button_vertical_box)
        
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        self.scroll.setWidget(holder)
        
        self.main_box.addWidget(self.scroll)
        
        self.setLayout(self.main_box)

class PhotoViewer(QGraphicsView):
    coordinatesChanged = pyqtSignal(QPoint)

    def __init__(self, parent):
        super().__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._photo.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def resetView(self, scale=1):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if (scale := max(1, scale)) == 1:
                self._zoom = 0
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height()) * scale
                self.scale(factor, factor)
                self.centerOn(self._photo)
                self.updateCoordinates()

    def setPhoto(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        if not self.hasPhoto():
            self._zoom = 0
        self.resetView(SCALE_FACTOR ** self._zoom)

    def zoomLevel(self):
        return self._zoom

    def zoom(self, step):
        zoom = max(0, self._zoom + (step := int(step)))
        if zoom != self._zoom:
            self._zoom = zoom
            if self._zoom > 0:
                if step > 0:
                    factor = SCALE_FACTOR ** step
                else:
                    factor = 1 / SCALE_FACTOR ** abs(step)
                self.scale(factor, factor)
            else:
                self.resetView()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.zoom(delta and delta // abs(delta))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resetView()

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def updateCoordinates(self, pos=None):
        if self._photo.isUnderMouse():
            if pos is None:
                pos = self.mapFromGlobal(QCursor.pos())
            point = self.mapToScene(pos).toPoint()
        else:
            point = QPoint()
        self.coordinatesChanged.emit(point)

    def mouseMoveEvent(self, event):
        self.updateCoordinates(event.pos())
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.coordinatesChanged.emit(QPoint())
        super().leaveEvent(event)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python")
        
        main_layout = QHBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.contract_selection_bar = ContractSelector(self, self.contract_toggled)
        
        self.map_viewer = PhotoViewer(self)
        self.map_viewer.setPhoto(QPixmap("./tmp_map.png"))
        
        main_layout.addWidget(self.contract_selection_bar, stretch=1)
        main_layout.addWidget(self.map_viewer, stretch=4)
        
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        
        self.show()

        # show all the widgets
        self.show()

    def contract_toggled(self, b):
        print(f"{b.text()} {b.isChecked()}")
        self.refresh_map([])
    
    def refresh_map(self, contract_list: list):
        base_map = Image.open("./src/lze-contract-mapper/ressources/RS_L0.png")

        contract_image = Image.open("./src/lze-contract-mapper/ressources/RS_contracts/RS_filter.png")

        base_map.paste(contract_image, (100, 100), contract_image)

        base_map.save("./tmp_map.png")
        
        self.map_viewer.setPhoto(QPixmap("./tmp_map.png"))
    
# create pyqt5 app
App = QApplication(sys.argv)
App.setStyle('Fusion')

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())


# app = QApplication([])

# app.setStyle('Fusion')

# window = QWidget()
# layout = QHBoxLayout()

# layout.addWidget(QPushButton('Left'))
# layout.addWidget(QPushButton('Right'))

# window.setLayout(layout)
# window.show()

# label = QLabel('Hello World')
# label.show()

app.exec()