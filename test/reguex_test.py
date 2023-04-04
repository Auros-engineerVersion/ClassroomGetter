import re

strings = {\
'いろはうた' : '''
いろはにほへと　ちりぬるを
わかよたれそ　つねならむ
うえのおくやま　けふこえて
あさきゆめみし　えひもせず
''',\
    
'俳句' : 'なつくさや　つわものどもが　ゆめのあと',\
'alphabet' : 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'}

match = re.search('abcd', strings.get('alphabet'))
print(match.span())