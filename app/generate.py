import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

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


def create_sentences(use_my_text, raw_text, language, use_model=False):
    if use_my_text == "Yes" and raw_text:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"\s*[.?!]\s*", raw_text)
            if sentence.strip()
        ]
        foreigns = sentences
        japaneses = []
    else:
        model = Model()
        if use_model:
            sentences = model.generate_text(language)
        else:
            sentences = """
            The old lighthouse stood resilient against the relentless crashing waves, a steadfast beacon guiding ships through treacherous waters.

            古びた灯台は、容赦なく打ち寄せる波に耐え、危険な海域を航行する船を導く、揺るぎない灯台として立っていた。

            Despite facing numerous setbacks, she remained determined to pursue her dream of becoming a renowned astrophysicist, fueled by her unwavering passion for the cosmos.

            幾多の挫折に直面しても、彼女は宇宙に対する揺るぎない情熱に突き動かされ、著名な天体物理学者になるという夢を追い続ける決意を固くしていた。

            The intricate tapestry of cultures in the city created a vibrant and dynamic atmosphere, where traditions from around the world intertwined harmoniously.

            その都市の複雑に織りなされた文化のタペストリーは、活気に満ちたダイナミックな雰囲気を作り出し、世界中の伝統が調和して絡み合っていた。

            He grappled with the ethical dilemma of whether to prioritize short-term profits or long-term sustainability, knowing that the decision would have far-reaching consequences.

            彼は、短期的な利益を優先すべきか、長期的な持続可能性を優先すべきかという倫理的なジレンマに苦しみ、その決定が広範囲に及ぶ結果をもたらすことを知っていた。

            The abandoned train station, a relic of a bygone era, echoed with the ghosts of forgotten journeys and whispered tales of farewells and reunions.

            見捨てられた駅は、過ぎ去った時代の遺物であり、忘れられた旅の亡霊がこだまし、別れと再会の物語を囁いていた。
            """

        foreigns, japaneses = model.separate_sentences(sentences)
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
