from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
import os

from .statics import LZCM_RESOURCE_PATH, RS_CONTRACT_LIST

class ContractCheckBox(QWidget):
    def __init__(self, parent = None, contract_name = None, image_path = None, toggled_checkbox_connect = None):
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
    def __init__(self, parent=None, toggled_checkbox_connect = None):
        super(ContractSelector, self).__init__()

        self.setFixedWidth(260)

        self.main_box = QHBoxLayout(self)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(0)

        self.button_vertical_box = QVBoxLayout()

        self.scroll = QScrollArea(self)
        
        for contract in RS_CONTRACT_LIST:
            btn = ContractCheckBox(self, contract[0], os.path.join(LZCM_RESOURCE_PATH, "RS_contracts", contract[1]), toggled_checkbox_connect)
            self.button_vertical_box.addWidget(btn)

        holder = QWidget()
        holder.setLayout(self.button_vertical_box)
        
        self.scroll.setWidget(holder)
        
        self.main_box.addWidget(self.scroll)
        
        self.setLayout(self.main_box)