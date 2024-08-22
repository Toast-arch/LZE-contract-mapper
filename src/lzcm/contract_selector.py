from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
import os

from .statics import LZEMap
from .statics import LZCM_RESOURCE_PATH

class ContractCheckBox(QWidget):
    def __init__(self, parent, contract_name: str, image_path: str, toggled_checkbox_connect):
        super().__init__(parent)
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)
        
        self.setMaximumHeight(70)
        
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
    def __init__(self, parent, selected_map: LZEMap, toggled_checkbox_connect):
        super(ContractSelector, self).__init__(parent)

        self.setFixedWidth(260)

        self.selected_map = selected_map
        self.toggled_checkbox_connect = toggled_checkbox_connect
        
        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)

        self.button_vertical_box = QVBoxLayout()

        self.scroll = QScrollArea(self)
        
        for contract in self.selected_map.contract_list:
            btn = ContractCheckBox(self, contract.name, os.path.join(LZCM_RESOURCE_PATH, self.selected_map.contract_images_path, contract.image_name), self.toggled_checkbox_connect)
            self.button_vertical_box.addWidget(btn)

        self.holder = QWidget()
        self.holder.setLayout(self.button_vertical_box)
        
        self.scroll.setWidget(self.holder)
        
        self.main_box.addWidget(self.scroll)
        
        self.setLayout(self.main_box)
    
    def reset(self):
        for i in reversed(range(self.button_vertical_box.count())): 
            self.button_vertical_box.itemAt(i).widget().deleteLater()
            self.button_vertical_box.itemAt(i).widget().setParent(None)
        
        for contract in self.selected_map.contract_list:
            btn = ContractCheckBox(self, contract.name, os.path.join(LZCM_RESOURCE_PATH, self.selected_map.contract_images_path, contract.image_name), self.toggled_checkbox_connect)
            self.button_vertical_box.addWidget(btn)