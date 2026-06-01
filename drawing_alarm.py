import os
import requests
import google.generativeai as genai

# 直接貼り付けず、GitHubの環境変数（Secrets）から読み込むようにします
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

def generate_motif_idea():
    """Gemini APIを使ってランダムなモチーフとアドバイスを生成する"""
    # APIキーのセットアップ
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 動作が速く安価なモデルを指定
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AIへの指示（プロンプト）
    prompt = """
    あなたは美大の講師です。毎日のデッサンの練習用に、身近なモチーフ案をランダムに1つ提案してください。
    出力は以下のフォーマットのみにしてください。
    
    今日のモチーフ：[モチーフ名]
    アドバイス：[形をとる時のコツや、陰影のつけ方などの簡単なアドバイスを100文字程度で]
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"モチーフの取得に失敗しました: {e}"

def send_discord_notify(message):
    """Discordへメッセージを送信する"""
    payload = {
        "username": "デッサン提案Bot",
        "content": message
    }
    requests.post(WEBHOOK_URL, json=payload)

def main():
    # 1. AIにランダムなモチーフ案を生成させる
    ai_message = generate_motif_idea()
    
    # 2. 生成されたテキストをDiscordに送信する
    send_discord_notify(ai_message)

if __name__ == "__main__":
    main()