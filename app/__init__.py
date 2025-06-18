from flask import Flask, render_template, request
from .generate import create_sentences
from .transcript import transcript, evaluate
from .record import Recorder
import ast
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "app/audio/record.wav"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/record", methods=["POST"])
def record():
    # フォームからのデータ取得
    language = request.form.get("language")
    use_my_text = request.form.get("use_my_text")
    raw_text = request.form.get("raw_text", None)

    idx = int(request.form.get("idx", 0))
    foreigns = request.form.get("foreigns")
    japaneses = request.form.get("japaneses")
    scores = request.form.get("scores", "[]")
    pronunciations = request.form.get("pronunciations", "[]")

    # 初回アクセス時の処理
    if idx == 0:
        # geminiAPIを使用する場合は、use_model=Trueに設定
        foreigns, japaneses = create_sentences(
            use_my_text, raw_text, language, use_model=False
        )
        print(f"Foreigns: {foreigns}\nJapaneses: {japaneses}")
        return render_template(
            "record.html",
            recording=True,
            foreigns=foreigns,
            japaneses=japaneses,
            idx=idx,
            scores=scores,
            pronunciations=pronunciations,
        )
    # 音声ファイルがアップロードされた場合の処理
    else:
        foreigns = ast.literal_eval(foreigns)
        japaneses = ast.literal_eval(japaneses)
        scores = ast.literal_eval(scores)
        pronunciations = ast.literal_eval(pronunciations)
        print(pronunciations)

        print(f"\n\tIndex: {idx-1}")
        print(f"Foreign: {foreigns[idx-1]}")
        print(f"Japanese: {japaneses[idx-1]}")
        print(f"Pronunciation: {pronunciations[idx-1]}")
        print(f"\tScore: {scores[idx-1]}\n")

        # 次のインデックスに進む
        if idx < len(foreigns):
            return render_template(
                "record.html",
                recording=True,
                foreigns=foreigns,
                japaneses=japaneses,
                idx=idx,
                scores=scores,
                pronunciations=pronunciations,
                language=language,
            )
        # 最後のインデックスに到達した場合、結果を表示
        else:
            return render_template(
                "result.html",
                foreigns=foreigns,
                japaneses=japaneses,
                pronunciations=pronunciations,
                scores=scores,
            )


@app.route("/sound", methods=["POST"])
def sound():
    idx = int(request.form.get("idx", 0))
    foreigns = request.form.get("foreigns")
    japaneses = request.form.get("japaneses")
    scores = request.form.get("scores", "[]")
    pronunciations = request.form.get("pronunciations", "[]")
    language = request.form.get("language")

    foreigns = ast.literal_eval(foreigns)
    japaneses = ast.literal_eval(japaneses)
    pronunciations = ast.literal_eval(pronunciations)
    scores = ast.literal_eval(scores)

    recorder = Recorder(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        chunk=CHUNK,
        lang=language,
        filename=OUTPUT_FILENAME,
    )

    recorder.run_GUI()
    print("録音GUI終了")

    user_sentence = transcript(OUTPUT_FILENAME, lang=recorder.lang)
    score = evaluate(collect_sentence=foreigns[idx], user_sentence=user_sentence)[
        "類似度スコア"
    ]

    pronunciations.append(user_sentence)
    scores.append(score)

    return render_template(
        "record.html",
        recording=False,
        foreigns=foreigns,
        japaneses=japaneses,
        idx=idx,
        scores=scores,
        pronunciations=pronunciations,
        language=language,
    )


if __name__ == "__main__":
    app.run(debug=True)
