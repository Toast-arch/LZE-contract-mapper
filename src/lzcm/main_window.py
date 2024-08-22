import os
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image

from PyQt5.QtWidgets import QWidget

from .contract_selector import ContractSelector
from .photo_viewer import PhotoViewer
from .statics import LZCM_RESOURCE_PATH, LZCM_RS_L0_PATH, LZCM_TMP_MAP_PATH

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python")
        
        main_layout = QHBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.contract_selection_bar = ContractSelector(self, self.contract_toggled)
        
        self.map_viewer = PhotoViewer(self)
        
        self.init_map()

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
    
    def init_map(self):
        base_map = Image.open(LZCM_RS_L0_PATH)
        
        base_map.save(LZCM_TMP_MAP_PATH)
        
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))
    
    def refresh_map(self, contract_list: list):
        base_map = Image.open(LZCM_RS_L0_PATH)

        contract_image = Image.open(os.path.join(LZCM_RESOURCE_PATH, "RS_contracts" , "RS_filter.png"))

        base_map.paste(contract_image, (100, 100), contract_image)

        base_map.save(LZCM_TMP_MAP_PATH)
        
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))