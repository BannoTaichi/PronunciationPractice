import whisper
import pandas as pd
from rapidfuzz import fuzz


def transcript(filename, lang="en"):
    model = whisper.load_model("medium")
    # Whisperで文字起こし
    voice = model.transcribe(filename, language=lang)
    user_sentence = voice["text"].strip()
    return user_sentence


# 外国語選択と録音時間の入力から録音して類似度を返す(1個の文について評価)
def evaluate(collect_sentence, user_sentence):
    # 類似度計算
    similarity = fuzz.ratio(collect_sentence, user_sentence)
    result = [
        {
            "AIの文": collect_sentence,
            "あなたの発音": user_sentence,
            "類似度スコア": similarity,
        }
    ]

    # DataFrameに変換
    df = pd.DataFrame(result, columns=["AIの文", "あなたの発音", "類似度スコア"])
    df.index = range(1, len(df) + 1)
    return df


if __name__ == "__main__":
    # テスト用の音声ファイルと文
    collect_sentence = "Hello, how are you?"
    audio_filename = "../audio/record.wav"

    # 音声評価を実行
    user_sentence = transcript(audio_filename)
    df_result = evaluate(collect_sentence, user_sentence)
    print(df_result)
