import xml.etree.ElementTree as ET
import pandas as pd
import requests

# ﾌｧｲﾙをﾀﾞｳﾝﾛｰﾄﾞ
url = 'https://i18n.ankiweb.net/translation-memory/ja.all-projects.tmx'
response = requests.get(url)
response.raise_for_status()  # ｴﾗｰﾁｪｯｸ

# ﾀﾞｳﾝﾛｰﾄﾞしたXMLﾃﾞｰﾀを解析
root = ET.fromstring(response.content)

# 翻訳と翻訳後のﾃｷｽﾄを抽出
translations = []
for tu in root.findall('.//tu'):
    en_text = None
    ja_text = None
    for tuv in tu.findall('tuv'):
        lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang')
        seg = tuv.find('seg').text
        if lang == 'en-US':
            en_text = seg
        elif lang == 'ja':
            ja_text = seg
    if en_text and ja_text:
        translations.append((en_text, ja_text))

# Pandas DataFrameに変換
df = pd.DataFrame(translations, columns=['English', 'Japanese'])

# 結果を表示
print(df)

# 結果をCSVﾌｧｲﾙに保存
df.to_csv(r'G:\among anki\Python\Anki-Manuals-all\Anki-Manuals-jp\terms\translations.csv', index=False)