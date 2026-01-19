## Text2Speech (Piper TTS wrapper)

Project ini adalah wrapper Python sederhana di atas `piper-tts` untuk mengubah teks (`.txt`) menjadi file audio `.wav` dengan model Bahasa Indonesia.

### Requirements

- Python 3.10+ (kamu pakai 3.13, aman)
- `piper-tts` dan dependency lain:

```bash
pip install -r requirements.txt
```

### Struktur folder yang dipakai

- `models/id_ID-news_tts-medium.onnx`
- `models/id_ID-news_tts-medium.onnx.json`
- `main.py`
- folder output: `wav/` (dibuat otomatis)

Pastikan kedua file model ada di folder `models/` sesuai path di `main.py`.

### Cara pakai

1. Siapkan file teks, misalnya:

```bash
echo "Halo ini contoh text to speech dari Piper." > test.txt
```

2. Jalankan:

```bash
python main.py test.txt
```

3. Output:

- File audio akan tersimpan sebagai:

```text
wav/test.wav
```

Nama file `.wav` **mengikuti nama file `.txt`** input.

### Mengatur kecepatan suara

Di `main.py` ada konstanta:

```python
SPEED = 1.2  # 1.0 = normal, >1.0 lambat, <1.0 cepat
```

Ubah nilainya:

- `SPEED = 1.0` → normal  
- `SPEED > 1.0` → bicara lebih lambat  
- `SPEED < 1.0` → bicara lebih cepat  

Lalu jalankan lagi perintah:

```bash
python main.py your_text_file.txt
```

### Catatan teknis singkat

- `PiperVoice` diload dari `piper-tts`, lalu `voice.config.length_scale` di-set ke `SPEED`.
- `voice.synthesize(teks)` mengembalikan stream `AudioChunk`, dan setiap chunk ditulis ke file WAV via `audio_chunk.audio_int16_bytes`.
- Sample rate dan format audio (`22050 Hz`, mono, 16-bit PCM) diambil dari config model (`voice.config.sample_rate`).


