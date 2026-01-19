import os
import sys
import wave
from piper import PiperVoice

model_path = "models/id_ID-news_tts-medium.onnx"  # atau ganti ke id_ID-gadis-medium.onnx jika itu yang dipakai di CLI
config_path = "models/id_ID-news_tts-medium.onnx.json"  # pastikan ada

# Parameter kecepatan suara (speed)
# 1.0 = normal, > 1.0 = lebih lambat, < 1.0 = lebih cepat
# Contoh: 0.8 = cepat, 1.2 = lambat
SPEED = 1.2  # Ubah nilai ini untuk mengatur kecepatan

# Ambil nama file teks dari argumen CLI
if len(sys.argv) < 2:
    raise SystemExit("Usage: python main.py <input_text_file.txt>")

text_path = sys.argv[1]

with open(text_path, "r", encoding="utf-8") as f:
    teks = f.read().strip()

# Nama output WAV mengikuti nama file teks
base_name = os.path.splitext(os.path.basename(text_path))[0]
out_dir = "wav"
os.makedirs(out_dir, exist_ok=True)
output_file = os.path.join(out_dir, f"{base_name}.wav")

# Load model (sama seperti sebelumnya)
voice = PiperVoice.load(model_path, config_path=config_path, use_cuda=True)

# Ubah length_scale di config untuk mengatur kecepatan
voice.config.length_scale = SPEED

SAMPLE_RATE = voice.config.sample_rate  # Ini 22050 seperti print Anda
CHANNELS = 1  # mono, standar piper
SAMPLE_WIDTH = 2  # 16-bit PCM

print(f"Sample rate dari model: {SAMPLE_RATE} Hz")
print(f"Kecepatan suara: {SPEED}x ({'normal' if SPEED == 1.0 else 'lambat' if SPEED > 1.0 else 'cepat'})")

# Synthesize mengembalikan audio data
audio_data = voice.synthesize(teks)

with wave.open(output_file, "wb") as wav_file:
    # Set header WAV
    wav_file.setnchannels(CHANNELS)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.setsampwidth(SAMPLE_WIDTH)
    
    # Tulis audio data ke file (AudioChunk punya audio_int16_bytes)
    for audio_chunk in audio_data:
        wav_file.writeframes(audio_chunk.audio_int16_bytes)

file_size = os.path.getsize(output_file)
print(f"Selesai! Ukuran file: {file_size} bytes")

if file_size > 44:  # minimal header WAV ~44 bytes
    print("File seharusnya playable. Coba buka dengan player audio.")
else:
    print("Masih kecil/0 → coba teks lebih panjang atau cek phonemization.")
