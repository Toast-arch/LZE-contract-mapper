import os
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image

from PyQt5.QtWidgets import QWidget

from .contract_selector import ContractSelector
from .photo_viewer import PhotoViewer
from .statics import LZCM_RESOURCE_PATH, LZCM_RS_L0_PATH, LZCM_TMP_MAP_PATH, RS_CONTRACT_LIST

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.contract_display_list = []

        self.setWindowTitle("Python")
        
        main_layout = QHBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.contract_selection_bar = ContractSelector(self, self.contract_toggled)
        
        # initialize map & tmp map
        base_map = Image.open(LZCM_RS_L0_PATH)        
        base_map.save(LZCM_TMP_MAP_PATH)
        
        self.map_viewer = PhotoViewer(self)
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))

        main_layout.addWidget(self.contract_selection_bar)
        main_layout.addWidget(self.map_viewer)
        
        self.setMinimumSize(1150, 600)
        self.resize(800, 600)
        
        self.show()

        # show all the widgets
        self.show()
    
    def contract_toggled(self, b):        
        if b.isChecked() and b not in self.contract_display_list:
            for contract in RS_CONTRACT_LIST:
                if b.text() == contract.name:
                    self.contract_display_list.append(contract)
                    break
        else:
            self.contract_display_list = [contract for contract in self.contract_display_list if contract.name != b.text()]
        
        self.refresh_map()
    
    def refresh_map(self):
        tmp_map = Image.open(LZCM_RS_L0_PATH)

        for contract in self.contract_display_list:
            contract_image = Image.open(os.path.join(LZCM_RESOURCE_PATH, "RS_contracts" , contract.image_name))

            tmp_map.paste(contract_image, contract.coordinates, contract_image)

        tmp_map.save(LZCM_TMP_MAP_PATH)
        
        self.map_viewer.setPhoto(QPixmap(LZCM_TMP_MAP_PATH))