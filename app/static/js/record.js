let mediaRecorder;
let recordedChunks = [];
let audioContext;
let gainNode;
let sourceNode;
let destinationStream;

// 音声録音を開始する関数
function startRecording() {
  navigator.mediaDevices.getUserMedia({
    // 音声の取得設定
    audio: {  
      echoCancellation: false, // エコーキャンセリングを無効にする
      noiseSuppression: false, // ノイズ抑制を無効にする
      autoGainControl: true // 自動ゲインコントロールを有効にする
    }
  })
    .then(function(stream) {
      // AudioContext を使って音声処理
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
      gainNode = audioContext.createGain();
      gainNode.gain.value = 10.0; // ★音量倍率（1.0 = 元の大きさ, 2.0 = 2倍）

      // ストリームを取得して録音の準備
      sourceNode = audioContext.createMediaStreamSource(stream);
      const destination = audioContext.createMediaStreamDestination();

      // 音声処理の流れを設定
      sourceNode.connect(gainNode);
      gainNode.connect(destination);

      // 録音用のストリームを取得
      destinationStream = destination.stream;

      // 処理後のストリームを録音する
      mediaRecorder = new MediaRecorder(destinationStream, {
        mimeType: "audio/webm; codecs=opus",
        audioBitsPerSecond: 128000 // ★ビットレート（例: 128kbps）
      });

      // 録音データを保存するためのイベントリスナー
      mediaRecorder.ondataavailable = function(e) {
        recordedChunks.push(e.data);
      };

      // 録音停止時の処理
      mediaRecorder.onstop = function() {
        let blob = new Blob(recordedChunks, { type: 'audio/ogg; codecs=opus' });
        recordedChunks = [];
        let audioURL = URL.createObjectURL(blob);
        document.getElementById('audioElement').src = audioURL;
      };

      // 録音を開始
      mediaRecorder.start();
      console.log("録音開始");

      // ボタンのテキストを更新
      document.getElementById('recordButton').textContent = '録音停止';
    })
    .catch(function(err) {
      console.error('録音を開始できませんでした:', err);
    });
}

// 音声の再生を制御する関数
document.getElementById('recordButton').addEventListener('click', function() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    console.log("録音停止");

    document.getElementById('recordButton').textContent = '録音開始';
  } else {
    startRecording();
  }
});
