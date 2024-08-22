import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PIL import Image

from .contract_selector import ContractSelector
from .map_widget import MapWidget

from .statics import LZCM_RESOURCE_PATH, LZCM_TMP_MAP_PATH, MAP_LIST

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.contract_display_list = []
        self.setWindowTitle("Python")
        
        # init main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # init contract selector
        self.selected_map = MAP_LIST[0]
        self.selected_level = 0
        self.contract_selection_bar = ContractSelector(self, self.selected_map, self.contract_toggled)
        
        # init tmp map
        self.draw_clean_tmp_map()
        
        # initialize map & tmp map
        self.map_widget = MapWidget(self, self.selected_map, self.selected_level, self.map_btn_pressed, self.level_btn_pressed)
        
        # add everything to main_layout
        main_layout.addWidget(self.contract_selection_bar)
        main_layout.addWidget(self.map_widget)
        
        self.setMinimumSize(1200, 700)
        self.resize(1200, 700)
        
        self.show()
        
    def map_btn_pressed(self, b):
        print(f"New map: {b.text()}")
        
        for map in MAP_LIST:
            if map.name == b.text() and self.selected_map.name != map.name:
                # select new map
                self.selected_map = map
                self.selected_level = 0
                
                # reset contracts
                self.reset_contract_selector()
                
                self.draw_clean_tmp_map()
                
                self.map_widget.update_selected_map(self.selected_map)
    
    def level_btn_pressed(self, b):
        if self.selected_level != int(b.text()):
            print(f"Level updated to {b.text()}")
            self.selected_level = int(b.text())

            self.draw_clean_tmp_map()
            self.draw_contracts()
            
            self.map_widget.refresh_map_viewer()
    
    def contract_toggled(self, b):
        print(f"Contract toggled: {b.text()} -> {b.isChecked()}")
             
        if b.isChecked() and b not in self.contract_display_list:
            for contract in self.selected_map.contract_list:
                if b.text() == contract.name:
                    self.contract_display_list.append(contract)
                    break
        else:
            self.contract_display_list = [contract for contract in self.contract_display_list if contract.name != b.text()]
        
        self.draw_contracts()
        self.map_widget.refresh_map_viewer()
    
    def reset_contract_selector(self):
        self.contract_display_list = []
        
        self.contract_selection_bar.selected_map = self.selected_map
        self.contract_selection_bar.reset()
    
    def draw_clean_tmp_map(self):
        base_map = Image.open(self.selected_map.image_paths[self.selected_level])        
        base_map.save(LZCM_TMP_MAP_PATH)
    
    def draw_contracts(self):
        tmp_map = Image.open(self.selected_map.image_paths[self.selected_level])

        for contract in self.contract_display_list:
            contract_image = Image.open(os.path.join(LZCM_RESOURCE_PATH, self.selected_map.contract_images_path, contract.image_name))

            tmp_map.paste(contract_image, contract.coordinates, contract_image)

        tmp_map.save(LZCM_TMP_MAP_PATH)
