#region イベント
WM_DELETE_WINDOW = 'WM_DELETE_WINDOW'
BUTTON_PRESS = '<ButtonPress>'
MOUSE_WHEEL_UP = '<ButtonPress-4>'
MOUSE_WHEEL_DOWN = '<ButtonPress-5>'
NOTEBOOK_TAB_CHANGED = '<<NotebookTabChanged>>'
CONFIGURE = '<Configure>'
TEXT = "text"
STATE = 'state'
TK_DEFAULT_FONT = 'TkDefaultFont'
BACKGROUND = 'background'
#endregion

#region 単語
MAIN = 'メイン'
RESET = '元に戻す'
NO_DATA = '未設定'
SETTING_WINDOW = '設定画面'
SAVE = '保存'
RUN = '実行'
COMPLETE = '完了'
BROWS = '参照'
WARNING = '警告'
LOADING = '更新中'
FINISHING = '終了中'
NORMAL_DATA = '設定'
ADVANCED_DATA = '高度な設定'
#endregion

#region UI
ROOT_TITLE = 'ClassroomHack'
TITLE = 'title'
GUEST_MODE = 'ゲストモード'
DESCRIPTION = 'description'

USER_EMAIL = 'ユーザーのメールアドレス'
USER_PASSWORD = 'ユーザーのパスワード'
SAVE_FOLDER_PATH = '保存先のフォルダ'
LOADING_WAIT_TIME = 'ページの読み込みを待つ時間'
WEB_DRIVER_OPTIONS = 'Web Driverのオプション'
SEARCH_DEPTH = '探索の深度'
#endregion

#region 文章
STOP_OR_CONTINUE = '入力の途中で閉じようとしています。'
SETTING_RESET_MESSAGE = '設定を適用するには再起動が必要です。'
PROFILE_WARNING = '入力した値が正しくありません。再入力してください。'
WEB_DRIVER_QUIT = 'Web Driverを終了しています。'

INCLUDE_THIS_IN_PATH = '保存の際、自身をパスに含める'

USER_EMAIL_DESC = '''
    googleアカウントのメールアドレスを入力してください。
    このアカウントはclassroomへのログイン、ファイルのダウンロードの際に必要となります。'''

USER_PASSWORD_DESC = '''
    googleアカウントのパスワードを入力してください。
    このアカウントはclassroomへのログイン、ファイルのダウンロードの際に必要となります。'''

SAVE_FOLDER_PATH_DESC = '''
    入手したファイルを保存する場所です。'''
    
LOADING_WAIT_TIME_DESC = '''
    ページの読み込みを待つ時間です。
    これがあまりにも短い場合、正常に動作しない可能性があります。
    ご自身のインターネット環境に合わせて設定してください。'''

WEB_DRIVER_OPTIONS_DESC = '''
    Web Driverが起動する際のオプションです。
    ここで指定するオプションによっては、ファイルのダウンロードが行われない可能性があります。
    詳細はhttps://peter.sh/experiments/chromium-command-line-switches/を参照してください。
    ※--headlessは古いオプションです。代わりに--headless=newを使用してください。'''

SEARCH_DEPTH_DESC = '''
    探索を行う際の深度です。深度により、以下のように探索する範囲が変わります。
    深度0の場合: なんちゃら学（ここで終了）
    深度1の場合: なんちゃら学 -> 第1回（ここで終了）
    深度2の場合: なんちゃら学 -> 第1回 -> Hoge.pdf（ここで終了）'''
#endregion

#json dictionary keys
VALUE = 'value'
TYPE = '_type'
ENCODE = 'encode'
DECODE = 'decode'