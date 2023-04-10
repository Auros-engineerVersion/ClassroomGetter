import settings as cfg
from src.controls import Controls

c = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
c.driver.get('https://classroom.google.com/u/0/c/MzExOTI0MzQyMzIz')
c.driver.find_element('xpath', "//div[@jsmodel='PTCFbe']").click()

print('AAA')