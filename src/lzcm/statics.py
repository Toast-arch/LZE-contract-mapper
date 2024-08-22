import os
import lzcm

LZCM_RESOURCE_PATH = os.path.join(lzcm.__file__[:-11], 'resources')

LZCM_RS_L0_PATH = os.path.join(LZCM_RESOURCE_PATH, "RS_L0.png")
LZCM_TMP_MAP_PATH = os.path.join(LZCM_RESOURCE_PATH, "tmp.png")

SCALE_FACTOR = 1.25

RS_CONTRACT_LIST = [
    ('Blue Passport', 'RS_blue_passport.png'),
    ('Console', 'RS_console.png'),
    ('Data Drive', 'RS_data_drive.png'),
    ('Drug Stash Snowmobile', 'RS_drugs_snow.png'),
    ('Filter', 'RS_filter.png'),
    ('Hard Drive', 'RS_hard_drive.png'),
    ('Lucky Bullet', 'RS_lucky_bullet.png'),
    ('Personnel Data', 'RS_personnel_data.png'),
    ('Petri Dish', 'RS_petri_dish.png'),
    ('Photo Friend', 'RS_photo_friend.png'),
    ('Red Passport', 'RS_red_passport.png'),
    ('Research Document', 'RS_research_documents.png'),
    ('Stamp', 'RS_stamp.png'),
    ('Weapon Case', 'RS_weapon_case.png'),
    ('Yellow ID', 'RS_yellow_id.png')
]