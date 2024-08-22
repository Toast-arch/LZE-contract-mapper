from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
from PyQt5.QtGui import QColor, QBrush, QPixmap, QCursor
from PyQt5.QtCore import pyqtSignal, QPoint, QRectF, Qt
from PIL import Image

from .statics import LZEMap, SCALE_FACTOR, MAP_LIST, LZCM_TMP_MAP_PATH

class MapWidget(QWidget):
    def __init__(self, parent, selected_map: LZEMap, selected_level: int, map_btn_pressed, level_btn_pressed):
        super().__init__(parent)
        
        self.map_btn_pressed = map_btn_pressed
        self.level_btn_pressed = level_btn_pressed
        
        self.map_selector = MapSelector(self, map_btn_pressed)
        
        self.map_viewer = PhotoViewer(self)
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))

        self.level_selector = LevelSelector(self, selected_map.levels, self.level_btn_pressed)
        
        map_layout = QVBoxLayout(self)
        map_layout.setContentsMargins(0, 0, 0, 0)
        map_layout.setSpacing(0)
        
        map_layout.addWidget(self.map_selector)
        map_layout.addWidget(self.map_viewer)
        map_layout.addWidget(self.level_selector)
        
        self.setLayout(map_layout)
    
    def update_selected_map(self, selected_map: LZEMap):
        self.level_selector.update_level_amount(selected_map.levels)
        self.refresh_map_viewer()
    
    def refresh_map_viewer(self):
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))
    
class MapButton(QWidget):
    def __init__(self, parent, map_name, clicked_btn_connect):
        super().__init__(parent)
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        self.setMaximumHeight(70)
        
        self.check_box = QPushButton(map_name, self)
        self.check_box.clicked.connect(lambda:clicked_btn_connect(self.check_box))

        self.main_box.addWidget(self.check_box)
        
        self.setLayout(self.main_box)

class MapSelector(QWidget):
    def __init__(self, parent, map_btn_pressed):
        super(MapSelector, self).__init__(parent)

        self.setFixedHeight(30)
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        for map in MAP_LIST:
            btn = MapButton(self, map.name, map_btn_pressed)
            self.main_box.addWidget(btn)
        
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

class LevelButton(QWidget):
    def __init__(self, parent, i, clicked_btn_connect):
        super().__init__(parent)
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        self.setMaximumHeight(70)
        
        self.check_box = QPushButton(str(i), self)
        self.check_box.clicked.connect(lambda:clicked_btn_connect(self.check_box))
        
        self.main_box.addWidget(self.check_box)
        
        self.setLayout(self.main_box)

class LevelSelector(QWidget):
    def __init__(self, parent, levels: int, level_btn_pressed):
        super(LevelSelector, self).__init__(parent)

        self.level_btn_pressed = level_btn_pressed
        
        self.setFixedHeight(30)
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        for i in range(levels):
            btn = LevelButton(self, i, self.level_btn_pressed)
            self.main_box.addWidget(btn)
        
        self.setLayout(self.main_box)
    
    def update_level_amount(self, levels):
        for i in reversed(range(self.main_box.count())): 
            self.main_box.itemAt(i).widget().deleteLater()
            self.main_box.itemAt(i).widget().setParent(None)
        
        for i in range(levels):
            btn = LevelButton(self, i, self.level_btn_pressed)
            self.main_box.addWidget(btn)