import settings
from src.controls import Controls

def main():
    print("run")
    controls = Controls(settings.PROFILE_PATH, settings.PROFILE_NAME)
    controls.move('https://classroom.google.com/u/0/h')
    
try:
    main()
except BaseException as e:
    print('\033[31m')
    print(e)
    print('\033[0m')
finally:
    settings.back_origin_enviroment()