from flask import Flask, render_template, request
from generate import Model
from record import Recorder
from transcript import transcript, evaluate
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/record", methods=["GET", "POST"])
def record():
    if request.method == "POST":
        # 言語、ユーザーが自分のテキストを使用するかどうか、録音時間を取得
        language = request.form.get("language")
        use_my_text = request.form.get("use_my_text")
        rec_time = int(request.form.get("rec_time"))

        # ユーザーが自分のテキストを使用する場合、テキストを取得
        # それ以外の場合はAIによる文生成
        if use_my_text == "Yes":
            raw_text = request.form.get("raw_text")
            sentences = [
                sentence.strip()
                for sentence in re.split(r"\s*[.?!]\s*", raw_text)
                if sentence.strip()
            ]
        else:
            model = Model()
            # sentences = model.generate_text(language=language)
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

        # 変数の内容をデバッグ用に出力
        print(
            f"Language: {language}\nUse My Text: {use_my_text}\nRec Time: {rec_time}\n\nForeigns: \n{foreigns}\nJapaneses: \n{japaneses}"
        )

        # 録音の順番をカウント
        num = len(sentences)
        try:
            idx = int(request.form.get("idx"))
        except:
            idx = 0

        return render_template(
            "record.html",
            foreigns=foreigns,
            japaneses=japaneses,
            num=num,
            idx=idx,
        )


if __name__ == "__main__":
    app.run(debug=True)
