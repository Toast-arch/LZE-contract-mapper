import os
import lzcm

LZCM_RESOURCE_PATH = os.path.join(lzcm.__file__[:-11], 'resources')

LZCM_RS_L0_PATH = os.path.join(LZCM_RESOURCE_PATH, "RS_L0.png")
LZCM_TMP_MAP_PATH = os.path.join(LZCM_RESOURCE_PATH, "tmp.png")

SCALE_FACTOR = 1.25

class Contract:
    def __init__(self, name: str, level: int, image_name: str, coordinates: tuple[int]):
        self.name = name
        self.level = level
        self.image_name = image_name
        self.coordinates = coordinates

RS_CONTRACT_LIST = [
    Contract('Art',                     1, 'RS_art.png',                (100, 100)),
    Contract('Bass',                    0, 'RS_bass.png',               (100, 100)),
    Contract('Bronze Bull',             1, 'RS_bull.png',               (100, 100)),
    Contract('Blue Passport',           0, 'RS_blue_passport.png',      (100, 100)),
    Contract('Console',                 1, 'RS_console.png',            (100, 100)),
    Contract('Data Drive',              1, 'RS_data_drive.png',         (100, 100)),
    Contract('Drug Stash',              1, 'RS_drugs_t.png',            (100, 100)),
    Contract('Drug Stash Bridge',       0, 'RS_drugs_bridge.png',       (100, 100)),
    Contract('Drug Stash Snowmobile',   0, 'RS_drugs_snow.png',         (100, 100)),
    Contract('Filter',                  0, 'RS_filter.png',             (100, 100)),
    Contract('Hard Drive',              1, 'RS_hard_drive.png',         (100, 100)),
    Contract('Lucky Bullet',            1, 'RS_lucky_bullet.png',       (100, 100)),
    Contract('Personnel Data',          1, 'RS_personnel_data.png',     (100, 100)),
    Contract('Petri Dish',              1, 'RS_petri_dish.png',         (100, 100)),
    Contract('Photo Friend',            0, 'RS_photo_friend.png',       (100, 100)),
    Contract('Red ID',                  1, 'RS_red_id.png',             (100, 100)),
    Contract('Red Passport',            1, 'RS_red_passport.png',       (100, 100)),
    Contract('Research Document',       0, 'RS_research_documents.png', (100, 100)),
    Contract('Stamp',                   0, 'RS_stamp.png',              (100, 100)),
    Contract('Tablet',                  0, 'RS_tablet.png',             (100, 100)),
    Contract('Vial',                    0, 'RS_vial.png',               (100, 100)),
    Contract('Weapon Case',             1, 'RS_weapon_case.png',        (100, 100)),
    Contract('X-Ray',                   1, 'RS_xray.png',               (100, 100)),
    Contract('Yellow ID',               1, 'RS_yellow_id.png',          (100, 100))
]