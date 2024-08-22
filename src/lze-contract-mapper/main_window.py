from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image

from PyQt5.QtWidgets import QWidget

from .contract_selector import ContractSelector
from .photo_viewer import PhotoViewer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python")
        
        main_layout = QHBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.contract_selection_bar = ContractSelector(self, self.contract_toggled)
        
        self.map_viewer = PhotoViewer(self)
        self.map_viewer.setPhoto(QPixmap("./tmp_map.png"))
        
        main_layout.addWidget(self.contract_selection_bar)
        main_layout.addWidget(self.map_viewer)
        
        self.setMinimumSize(1150, 600)
        self.resize(800, 600)
        
        self.show()

        # show all the widgets
        self.show()

    def contract_toggled(self, b):
        print(f"{b.text()} {b.isChecked()}")
        self.refresh_map([])
    
    def reset_map(self):
        self.map_viewer.setPhoto(QPixmap("./src/lze-contract-mapper/resources/RS_L0.png"))
    
    def refresh_map(self, contract_list: list):
        base_map = Image.open("./src/lze-contract-mapper/resources/RS_L0.png")

        contract_image = Image.open("./src/lze-contract-mapper/resources/RS_contracts/RS_filter.png")

        base_map.paste(contract_image, (100, 100), contract_image)

        base_map.save("./tmp_map.png")
        
        self.map_viewer.setPhoto(QPixmap("./tmp_map.png"))