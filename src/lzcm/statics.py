import os
import lzcm

LZCM_RESOURCE_PATH = os.path.join(lzcm.__file__[:-11], 'resources')

LZCM_TMP_MAP_PATH = os.path.join(LZCM_RESOURCE_PATH, "tmp.png")

SCALE_FACTOR = 1.25

class Contract:
    def __init__(self, name: str, level: int, image_name: str, coordinates: tuple[int]):
        self.name = name
        self.level = level
        self.image_name = image_name
        self.coordinates = coordinates

class LZEMap:
    def __init__(self, name: str, levels: int, image_name: str, contract_images_path, contract_list: list[Contract]):
        self.name = name
        self.levels = levels
        self.image_paths = [os.path.join(LZCM_RESOURCE_PATH, "maps", image_name)] if levels == 1 else [os.path.join(LZCM_RESOURCE_PATH, "maps", "{}_L{}.png".format(image_name[:-4], i)) for i in range(levels)]
        self.contract_images_path = contract_images_path
        self.contract_list = contract_list

RS_CONTRACT_LIST = [
    Contract('Art',                     1, 'RS_art.png',                        (100, 100)),
    Contract('Bass',                    0, 'RS_bass.png',                       (100, 100)),
    Contract('Bronze Bull',             1, 'RS_bull.png',                       (100, 100)),
    Contract('Blue Passport',           0, 'RS_blue_passport.png',              (100, 100)),
    Contract('Console',                 1, 'RS_console.png',                    (100, 100)),
    Contract('Data Drive',              1, 'RS_data_drive.png',                 (100, 100)),
    Contract('Drug Stash',              1, 'RS_drugs_t.png',                    (100, 100)),
    Contract('Drug Stash Bridge',       0, 'RS_drugs_bridge.png',               (100, 100)),
    Contract('Drug Stash Snowmobile',   0, 'RS_drugs_snow.png',                 (100, 100)),
    Contract('Filter',                  0, 'RS_filter.png',                     (100, 100)),
    Contract('Hard Drive',              1, 'RS_hard_drive.png',                 (100, 100)),
    Contract('Lucky Bullet',            1, 'RS_lucky_bullet.png',               (100, 100)),
    Contract('Personnel Data',          1, 'RS_personnel_data.png',             (100, 100)),
    Contract('Petri Dish',              1, 'RS_petri_dish.png',                 (100, 100)),
    Contract('Photo Friend',            0, 'RS_photo_friend.png',               (100, 100)),
    Contract('Red ID',                  1, 'RS_red_id.png',                     (100, 100)),
    Contract('Red Passport',            1, 'RS_red_passport.png',               (100, 100)),
    Contract('Research Document',       0, 'RS_research_documents.png',         (100, 100)),
    Contract('Stamp',                   0, 'RS_stamp.png',                      (100, 100)),
    Contract('Tablet',                  0, 'RS_tablet.png',                     (100, 100)),
    Contract('Vial',                    0, 'RS_vial.png',                       (100, 100)),
    Contract('Weapon Case',             1, 'RS_weapon_case.png',                (100, 100)),
    Contract('X-Ray',                   1, 'RS_xray.png',                       (100, 100)),
    Contract('Yellow ID',               1, 'RS_yellow_id.png',                  (100, 100))
]

CT_CONTRACT_LIST = [
    Contract('Alien Matter',            0, 'CT_alien_matter.png',               (100,100)),
    Contract('Analog Data',             0, 'CT_analog_data.png',                (100,100)),
    Contract('Atmospheric Analyzer',    0, 'CT_atmospheric_analyzer.png',       (100,100)),
    Contract('Award',                   0, 'CT_award.png',                      (100,100)),
    Contract('Backup Power',            0, 'CT_backup_power.png',               (100,100)),
    Contract('Bomb',                    0, 'CT_bomb.png',                       (100,100)),
    Contract('Cap',                     0, 'CT_cap.png',                        (100,100)),
    Contract('Classified Papers',       0, 'CT_classified_papers.png',          (100,100)),
    Contract('Crystal',                 0, 'CT_crystal.png',                    (100,100)),
    Contract('Footage',                 0, 'CT_footage.png',                    (100,100)),
    Contract('Glass Planet',            0, 'CT_glass_planet.png',               (100,100)),
    Contract('Gold Bar',                0, 'CT_gold_bar.png',                   (100,100)),
    Contract('Grenade Blueprint',       0, 'CT_grenade_blueprint.png',          (100,100)),
    Contract('Headset',                 0, 'CT_headset.png',                    (100,100)),
    Contract('Keys',                    0, 'CT_keys.png',                       (100,100)),
    Contract('Locker Keys',             0, 'CT_locker_key.png',                 (100,100)),
    Contract('Log Device',              0, 'CT_log_device.png',                 (100,100)),
    Contract('Pattern Key',             0, 'CT_pattern_key.png',                (100,100)),
    Contract('Piggy Bank',              0, 'CT_piggy_bank.png',                 (100,100)),
    Contract('Solar',                   0, 'CT_solar.png',                      (100,100)),
    Contract('Thermal Goggles',         0, 'CT_thermal_goggles.png',            (100,100)),
    Contract('Weapon Blueprint',        0, 'CT_weapon_blueprint.png',           (100,100))
]

MAP_LIST = [
    LZEMap("Research Station", 2, "RS.png", "RS_contracts", RS_CONTRACT_LIST),
    LZEMap("Caves of Turion", 1, "CT.png", "CT_contracts", CT_CONTRACT_LIST)
]