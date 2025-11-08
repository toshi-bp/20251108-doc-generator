# README for Doc Updater Python

## 概要
このプロジェクトは、チャット内容に基づいて古いドキュメントを新しいものに更新するためのPythonスクリプトです。OpenAI APIを使用して、ドキュメントの内容を生成し、更新されたドキュメントを指定されたフォルダに保存します。

## ディレクトリ構造
```
doc-updater-python
├── src                  # ソースコード
│   ├── main.py         # エントリーポイント
│   ├── updater.py      # ドキュメント更新ロジック
│   ├── openai_client.py # OpenAI APIとの通信
│   ├── parser.py       # データ解析
│   ├── file_manager.py  # ファイルの読み書き
│   └── config.py       # 設定情報
├── system_docs         # 元のドキュメント
│   ├── Aプロジェクト
│   └── Bプロジェクト
├── updated_docs        # 更新されたドキュメント
├── tests               # テスト
│   ├── test_updater.py
│   └── test_parser.py
├── requirements.txt     # 必要なパッケージ
├── .gitignore          # Git無視ファイル
└── README.md           # このドキュメント
```

## 使用方法
1. 必要なパッケージをインストールします。
   ```
   pip install -r requirements.txt
   ```

2. `src/config.py`にOpenAI APIキーやファイルパスを設定します。

3. スクリプトを実行します。
   ```
   python src/main.py
   ```

## 依存関係
- Python 3.x
- requests
- openai

## 貢献
このプロジェクトへの貢献は大歓迎です。プルリクエストを作成するか、イシューを報告してください。

## ライセンス
このプロジェクトはMITライセンスの下で提供されています。詳細はLICENSEファイルを参照してください。