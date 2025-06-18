import whisper
import pandas as pd
from rapidfuzz import fuzz


# 音声ファイルを文字起こしする関数
# [IN] (str) audio_file: 音声ファイルのパス
# [IN] (str) lang: 言語コード（デフォルトは英語 "en"）
# [OUT] (str) user_sentence: ユーザーの発音の文字起こし
def transcript(audio_file, lang="en"):
    if audio_file is None:
        print("音声ファイルが指定されていません。")
        return ""
    model = whisper.load_model("medium")
    # Whisperで文字起こし
    voice = model.transcribe(audio_file, language=lang)
    user_sentence = voice["text"].strip()
    return user_sentence


# 正しい文とユーザーの発音を比較して類似度を返す関数
# [IN] (str) collect_sentence: 正しい文
# [IN] (str) user_sentence: ユーザーの発音の文字起こし
# [OUT] (dict) result: AIの文、ユーザーの発音、類似度スコアを含む辞書
def evaluate(collect_sentence, user_sentence):
    # 類似度計算
    similarity = fuzz.ratio(collect_sentence, user_sentence)
    result = {
        "AIの文": collect_sentence,
        "あなたの発音": user_sentence,
        "類似度スコア": similarity,
    }
    return result


if __name__ == "__main__":
    # テスト用の音声ファイルと文
    collect_sentence = "The old lighthouse stood resilient against the relentless crashing waves, a steadfast beacon guiding ships through treacherous waters."
    audio_filename = "audio/record.wav"

    # 音声評価を実行
    user_sentence = transcript(audio_filename)
    result = evaluate(collect_sentence, user_sentence)
    print(result)
