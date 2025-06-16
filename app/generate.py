import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


# Google Geminiを使用して文を生成するクラス
class Model:
    def __init__(self):
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.lan = "en"  # デフォルトの言語は英語

    # AIによる文生成
    # [IN] (str) language: 言語（デフォルトは英語）
    # [IN] (str) level: レベル（デフォルトは中級）
    # [OUT] (str) response: 生成された文
    def generate_text(self, language="英語", level="中級"):
        if language == "韓国語":
            self.lan = "ko"
        prompt = f"""
            {language}の文を{level}向けに5個生成してください。
            最初の説明も数字も一切不要です。
            {language}の文章と和訳を空白を空けて出力してください。
        """
        response = self.model.generate_content(prompt).text

        return response

    # テキストを行ごとに分割し、偶数行を外国語、奇数行を日本語としてペアにする
    # [IN] (str) text: 生成されたテキスト
    # [OUT] (list, list): 外国語の文と日本語の文のリスト
    def separate_sentences(self, text):
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        pairs = [
            {self.lan: lines[i], "ja": lines[i + 1]} for i in range(0, len(lines), 2)
        ]

        foreigns = [pair["en"] for pair in pairs]
        japaneses = [pair["ja"] for pair in pairs]

        return foreigns, japaneses


if __name__ == "__main__":
    # 言語とレベルの設定
    language = "英語"
    level = "初級"

    # 言語とレベルに応じて文を生成
    model = Model()
    while True:
        try:
            response = model.generate_text(language, level)
            foreigns, japaneses = model.separate_sentences(response)
            break
        except:
            continue

    for foreign, japanese in zip(foreigns, japaneses):
        print(f"\n原文: {foreign}")
        print(f"和訳: {japanese}")
