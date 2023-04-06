import settings as cfg
from src.browser.controls import Controls
from src import path_converter

try:
    controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    controls.move(url=cfg.TARGET_URL)
    #文字列の範囲を10からにすると、/archivedというpathも含まれてしまう
    #11にすれば大丈夫
    hrefs = controls.hrefs(controls.wait, '^.+/0/.{11,20}$')
    
    #授業タブへのリンクへと整形
    #それぞれのlinkに移動する
    for link in list(map(path_converter.to_tab_path, hrefs)):
        controls.move(link)
        #asideのtabリンクを全て取得し、移動する
        for href in controls.hrefs(controls.wait, '.*tc.{10,20}$'):
            controls.move(href, wait_time=2)
            controls.title()
            #pdf, 動画, docなどのパスを取得
            files = controls.hrefs(controls.wait, '.*file/d/.*')
            for file in files:
                print(file)
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    print(e)
    
finally:
    print('\033[0m')