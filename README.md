# Audio Subtitle Generator

Easily convert audio files into subtitles with OpenAI's Whisper.  

- Transcribes audio files into subtitles with timestamps
- Multiple languages
- Adjustable subtitle length for readability. (Timestamped words)

## Installation

### Requirements

- Python 3.8+
- `whisper_timestamped`
- `srt`

### Install dependencies

```sh
pip install whisper_timestamped srt
```

## Usage

```sh
python transcriber.py <audio_file> <output_file> --model <whisper_model> --language <lang_code> --min_chars <min_characters>
```

### Example

```sh
python transcriber.py input.mp3 output.srt --model large --language en --min_chars 12
```

## Available Whisper Models

Whisper offers several models with varying sizes and capabilities. Here is a brief description of each model along with their recommended use cases and characteristics:

- `tiny`
  - **Size:** ~39 MB
  - **Recommended for:** Very fast transcription with lower accuracy.
  - **Characteristics:** Suitable for real-time applications with limited resources.

- `base`
  - **Size:** ~74 MB
  - **Recommended for:** Fast transcription with moderate accuracy.
  - **Characteristics:** Good balance between speed and accuracy for general use.

- `small`
  - **Size:** ~244 MB
  - **Recommended for:** Higher accuracy transcription with moderate speed.
  - **Characteristics:** Suitable for applications where accuracy is more important than speed.

- `medium`
  - **Size:** ~769 MB
  - **Recommended for:** High accuracy transcription with slower speed.
  - **Characteristics:** Ideal for detailed transcription tasks where accuracy is critical.

- `large`
  - **Size:** ~1550 MB
  - **Recommended for:** Highest accuracy transcription with the slowest speed.
  - **Characteristics:** Best for applications requiring the most accurate transcription, regardless of speed.

## License

GPL-3.0 License