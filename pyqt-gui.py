from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.QtWidgets import QWidget

# class MapDisplay(QScrollArea):
#     def __init__(self, parent = None):
#         super().__init__(parent)
        
#         self.image_label = QLabel()
        
#         self.image = QImage("test.png")
        
#         self.image_label.setPixmap(QPixmap.fromImage(self.image))
        
#         self.setBackgroundRole(QPalette.Dark)
#         self.setWidget(self.image_label)

SCALE_FACTOR = 1.25


class PhotoViewer(QGraphicsView):
    coordinatesChanged = pyqtSignal(QPoint)

    def __init__(self, parent):
        super().__init__(parent)
        self._zoom = 0
        # self._pinned = False
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

    # def zoomPinned(self):
    #     return self._pinned

    # def setZoomPinned(self, enable):
    #     self._pinned = bool(enable)

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

class MainForm(QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__()

        self.main_box = QHBoxLayout(self)

        self.button_vertical_box = QVBoxLayout()

        self.scroll = QScrollArea(self)

        dic = {}
        
        for i in range(30):
            dic['foo '+str(i)] = [i]

        for key, _ in sorted(dic.items()):
            btn = QPushButton(key, self)
            self.button_vertical_box.addWidget(btn)

        holder = QWidget()
        holder.setLayout(self.button_vertical_box)
        
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        self.scroll.setWidget(holder)
        
        self.main_box.addWidget(self.scroll)
        
        self.setLayout(self.main_box)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Python")
        
        main_layout = QHBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.contract_selection_bar = MainForm(self)
        
        self.map_viewer = PhotoViewer(self)
        self.map_viewer.setPhoto(QPixmap("test.png"))
        
        # self.map_viewer.setSizePolicy(
        #     QSizePolicy.Expanding, QSizePolicy.Expanding
        # )
        
        main_layout.addWidget(self.contract_selection_bar, stretch=1)
        main_layout.addWidget(self.map_viewer, stretch=4)
        
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        
        self.show()

        # show all the widgets
        self.show()

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