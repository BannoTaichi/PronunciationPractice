from flask import Flask, render_template, request
from .generate import create_sentences
from .transcript import transcript, evaluate
from .record import Recorder
from ast import literal_eval
from pyaudio import paInt16

FORMAT = paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "app/audio/record.wav"
USE_MODEL = False  # geminiAPIを使用するかどうか

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/record", methods=["POST"])
def record():
    # index.htmlからのデータ取得
    use_my_text = request.form.get("use_my_text")
    if use_my_text == "Yes":
        use_my_text = True
    else:
        use_my_text = False
    raw_text = request.form.get("raw_text", None)
    language = request.form.get("language")

    # idxが0ならindex.html、-1ならrecord.htmlからのアクセス
    idx = int(request.form.get("idx", -1))

    if idx == 0:  # 初回アクセス時の処理
        foreigns, japaneses = create_sentences(
            raw_text, language, use_my_text=use_my_text, use_model=USE_MODEL
        )
        data = {
            "recording": True,
            "language": language,
            "idx": idx,
            "foreigns": foreigns,
            "japaneses": japaneses,
            "pronunciations": [],
            "scores": [],
        }
        return render_template("record.html", data=data)

    else:  # 音声ファイルがアップロードされた場合の処理
        data = request.form.get("data")
        data = literal_eval(data)

        print(
            f"""
Index:        {data['idx']}
Foreign:      {data['foreigns'][data['idx']]}
Japanese:     {data['japaneses'][data['idx']]}
Pronunciation:{data['pronunciations'][data['idx']]}
Score:        {data['scores'][data['idx']]}\n"""
        )

        if data["idx"] < len(data["foreigns"]) - 1:  # 次のインデックスに進む
            data["recording"] = True
            data["idx"] += 1
            return render_template("record.html", data=data)

        else:  # 最後のインデックスに到達した場合、結果を表示
            return render_template("result.html", data=data)


@app.route("/sound", methods=["POST"])
def sound():
    data = request.form.get("data")
    data = literal_eval(data)

    foreigns = data["foreigns"]

    recorder = Recorder(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        chunk=CHUNK,
        lang=data["language"],
        filename=OUTPUT_FILENAME,
    )
    recorder.run_GUI()
    print("録音GUI終了")

    pronunciation = transcript(OUTPUT_FILENAME, lang=recorder.lang)
    score = int(
        evaluate(collect_sentence=foreigns[data["idx"]], pronunciation=pronunciation)[
            "類似度"
        ]
    )

    data["recording"] = False
    data["pronunciations"].append(pronunciation)
    data["scores"].append(score)
    return render_template("record.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
