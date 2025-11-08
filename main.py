import os
import json
import shutil
from datetime import datetime
import openai

class DocumentUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def read_chat_json(self, chat_path):
        """チャットJSONファイルを読み込む"""
        with open(chat_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def read_md_file(self, md_path):
        """マークダウンファイルを読み込む"""
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_updated_content(self, original_content, chat_content):
        """OpenAI APIを使用して更新されたコンテンツを生成"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "system", "content": "既存のマークダウンドキュメントをチャット履歴に基づいて更新してください。"},
                    {"role": "user", "content": f"元のドキュメント:\n{original_content}\n\nチャット履歴:\n{chat_content}\n\n上記の情報を元に、ドキュメントを更新してください。あくまで入力しているのは要約であるため，変更する部分に関しては元の文書を元に適切な位置に追記もしくは修正をしてください．また，チャットの内容が元の文書の内容とあまり関連度が高くない場合は追記しないでください．"}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

    def save_updated_document(self, content, output_path):
        """更新されたドキュメントを保存"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def process_project(self, project_path):
        """プロジェクトごとの処理"""
        chat_path = os.path.join(project_path, 'chat.json')
        if not os.path.exists(chat_path):
            print(f"Chat file not found in {project_path}")
            return

        # チャットデータの読み込み
        chat_data = self.read_chat_json(chat_path)

        # プロジェクト内の全MDファイルを処理
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith('.md'):
                    md_path = os.path.join(root, file)
                    
                    # 新しい保存先のパスを生成
                    current_date = datetime.now().strftime('%Y%m%d')
                    new_folder = os.path.join(project_path, current_date)
                    new_md_path = os.path.join(new_folder, file)

                    # 既存のドキュメントを読み込む
                    original_content = self.read_md_file(md_path)

                    # 更新されたコンテンツを生成
                    updated_content = self.generate_updated_content(original_content, json.dumps(chat_data, ensure_ascii=False))
                    
                    if updated_content:
                        # 新しいドキュメントを保存
                        self.save_updated_document(updated_content, new_md_path)
                        print(f"Updated document saved: {new_md_path}")

def main():
    # OpenAI APIキーを設定
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    # DocumentUpdaterのインスタンスを作成
    updater = DocumentUpdater(api_key)

    # system_docsフォルダのパス
    base_path = "system_docs"
    
    # 各プロジェクトフォルダを処理
    for item in os.listdir(base_path):
        project_path = os.path.join(base_path, item)
        if os.path.isdir(project_path):
            print(f"Processing project: {item}")
            updater.process_project(project_path)

if __name__ == "__main__":
    main()