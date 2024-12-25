import csv
import json

# 入力ファイルと出力ファイルのパスを指定
input_file = ''
output_file = 'faq.json'

# ステップ1: 入力TSVファイルからNo、タイトル、本文を抽出
with open(input_file, 'r', encoding='utf-8') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    headers = next(reader)  # ヘッダー行を読み込む
    print(headers)  # ヘッダー行を表示して確認

# 入力ファイルの実際のヘッダーに基づいてフィールド名を更新
fieldnames = ['No', 'タイトル', 'ナレッジID', '本文', '作成日時', '作成者', '最終更新日時', '最終更新者', 'タグ', 'キーワード', 'サイト名', 'サイトID', '接続状況（0：未接続 / 1：接続中）', 'カテゴリー', 'カテゴリID']

# JSON文字列からtextフィールドの日本語テキストを抽出して結合する関数
def extract_text_from_json(json_str):
    try:
        data = json.loads(json_str)
        text_parts = []

        # 再帰的にJSONノードを探索してtextフィールドを抽出
        def extract_text(node):
            if isinstance(node, dict):
                if 'text' in node:
                    text_parts.append(node['text'])
                for key in node:
                    extract_text(node[key])
            elif isinstance(node, list):
                for item in node:
                    extract_text(item)

        extract_text(data)
        return ''.join(text_parts)
    except json.JSONDecodeError:
        return json_str

faq_list = []

# 入力TSVファイルを読み込み、必要なデータを抽出してリストに追加
with open(input_file, 'r', encoding='utf-8') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter='\t', fieldnames=fieldnames)
    next(reader)  # ヘッダー行をスキップ
    for row in reader:
        no = row['No']
        title = row['タイトル']
        body = extract_text_from_json(row['本文'])
        faq_list.append({"No": no, "タイトル": title, "本文": body})

# 抽出したデータをJSON形式で出力ファイルに保存
with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(faq_list, jsonfile, ensure_ascii=False, indent=4)

print(f"Converted data has been saved to {output_file}")