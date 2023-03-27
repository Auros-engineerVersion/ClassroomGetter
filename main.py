import settings as cfg
from src.controls import Controls

try:
    controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    controls.move(cfg.TARGET_URL)
    
except BaseException as e:
    print('\033[31m' + e.args + '\033[0m')
    
finally:
    cfg.back_origin_enviroment()
    del controls