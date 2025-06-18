import pyaudio
import wave
import pandas as pd
from rapidfuzz import fuzz
import threading
import tkinter as tk

try:
    from transcript import evaluate, transcript
except:
    from .transcript import evaluate, transcript


# 録音アプリケーションのクラス
class Recorder:
    def __init__(self, format, channels, rate, chunk, lang, filename):
        self.format = format  # 音声フォーマット
        self.channels = channels  # チャンネル数
        self.rate = rate  # サンプリングレート
        self.chunk = chunk  # チャンクサイズ
        self.set_lang(lang)  # 言語設定
        self.filename = filename  # 保存する音声ファイル名

        # PyAudioの初期化
        self.audio = pyaudio.PyAudio()
        input_device_index = self.select_device()  # デバイスの選択
        self.stream = self.audio.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk,
            input_device_index=input_device_index,
        )

    # 言語設定メソッド
    def set_lang(self, lang):
        if lang == "韓国語":
            self.lang = "ko"
        else:
            self.lang = "en"

    # 入力デバイスを選択
    def select_device(self):
        p = pyaudio.PyAudio()  # pyaudio の初期化
        input_device_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(
                f"Device {i}: {info['name'].encode('shift-jis').decode('utf-8', errors='ignore')}"
            )
            if "マイク" or "Microphone" in info["name"]:  # 適切なデバイス名を指定
                input_device_index = i
                break

        if input_device_index is None:
            print(
                "適切な入力デバイスが見つかりませんでした。デフォルトのデバイスを使用します。"
            )
            input_device_index = p.get_default_input_device_info()["index"]
        return input_device_index

    # 録音を開始するメソッド
    def start_recording(self):
        global recording
        stream = self.stream
        chunk = self.chunk

        print("録音開始")
        frames = []
        recording = True
        while recording:
            data = stream.read(chunk)
            frames.append(data)
        self.frames = frames

    # 録音を停止して音声ファイルを保存
    def stop_recording(self):
        global recording
        audio = self.audio
        stream = self.stream

        if not recording:  # すでに録音が停止している場合は何もしない
            return

        print("録音停止")
        recording = False
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.save_audio()  # 音声ファイルを保存

    # 音声ファイルを保存するメソッド
    def save_audio(self):
        output_filename = self.filename
        frames = self.frames
        with wave.open(output_filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(frames))
        print("音声ファイルを保存しました:", output_filename)

    # 録音ボタンが押されたときの処理
    def on_record_button_click(self):
        global recording
        recording = True
        threading.Thread(target=self.start_recording).start()

    # GUI を表示
    def run_GUI(self):
        root = tk.Tk()
        root.title("録音アプリ")
        record_button = tk.Button(
            root, text="録音開始", command=self.on_record_button_click
        )
        record_button.pack(pady=10)
        stop_button = tk.Button(root, text="録音停止", command=self.stop_recording)
        stop_button.pack(pady=10)
        root.mainloop()


if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    OUTPUT_FILENAME = "../audio/record.wav"

    recorder = Recorder(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        chunk=CHUNK,
        lang="英語",
        filename=OUTPUT_FILENAME,
    )

    recorder.run_GUI()

    sentence = "Hello, how are you?"
    user_sentence = transcript(OUTPUT_FILENAME, lang=recorder.lang)
    result = evaluate(sentence, user_sentence)
    print(result)
