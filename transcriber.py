import argparse
import whisper_timestamped
import srt
from datetime import timedelta

class AudioTranscriber:
    """
    Class to transcribe audio into subtitles using Whisper with timestamps.
    Separate lines in grouping words until reaching a minimum character count
    """

    def __init__(self, model: str = "base", language: str = "en", min_chars: int = 10):
        """
        Initializes the class with the model, language, and minimum character count per block.
        """
        self.model_name = model
        self.language = language
        self.min_chars = min_chars
        self.model = whisper_timestamped.load_model(self.model_name)

    def transcribe_audio(self, audio_path: str) -> dict:
        """
        Transcribes the audio using the loaded model.
        :param audio_path: Path to the audio file.
        :return: Dictionary with the transcription result.
        """
        return whisper_timestamped.transcribe(self.model, audio_path, language=self.language)

    def process_transcription(self, result: dict) -> list:
        """
        Processes the transcription result to generate subtitle blocks.
        Delegates the processing to specialized functions depending on the segment content.
        :param result: Dictionary with the transcription result.
        :return: List of srt.Subtitle objects.
        """
        subtitles = []
        index = 1

        for segment in result.get("segments", []):
            if "words" in segment:
                # Procesa segmento con marcas de palabras
                segment_subtitles, index = self._process_segment_with_words(segment, index)
                subtitles.extend(segment_subtitles)
            else:
                # Procesa segmento sin marcas a nivel de palabra
                subtitle = self._process_segment_without_words(segment, index)
                subtitles.append(subtitle)
                index += 1

        return subtitles

    def _process_segment_with_words(self, segment: dict, start_index: int) -> (list, int):
        """
        Processes a segment that contains individual word timestamps.
        Accumulates words until reaching the minimum character count, then creates a subtitle block.
        :param segment: Segment dictionary containing 'words' key.
        :param start_index: Starting index for the subtitles.
        :return: Tuple with a list of srt.Subtitle objects and the next index value.
        """
        subtitles = []
        accumulated_text = ""
        start_time = None
        end_time = None
        index = start_index

        for word_info in segment["words"]:
            text = word_info.get("text", "").strip()
            if not text:
                continue

            if not accumulated_text:
                start_time = word_info["start"]

            # Append word with a space if accumulated_text is not empty
            accumulated_text = f"{accumulated_text} {text}" if accumulated_text else text
            end_time = word_info["end"]

            # Check if the accumulated text meets the minimum character requirement
            if len(accumulated_text) >= self.min_chars:
                subtitles.append(
                    srt.Subtitle(
                        index=index,
                        start=timedelta(seconds=start_time),
                        end=timedelta(seconds=end_time),
                        content=accumulated_text,
                    )
                )
                index += 1
                # Reset accumulation for the next subtitle block
                accumulated_text = ""
                start_time = None
                end_time = None

        # If any text remains after the loop, create a final subtitle block
        if accumulated_text:
            start_td = timedelta(seconds=start_time) if start_time is not None else timedelta(0)
            end_td = timedelta(seconds=end_time) if end_time is not None else timedelta(0)
            subtitles.append(srt.Subtitle(index=index, start=start_td, end=end_td, content=accumulated_text))
            index += 1

        return subtitles, index

    def _process_segment_without_words(self, segment: dict, index: int) -> srt.Subtitle:
        """
        Processes a segment that does not contain individual word timestamps.
        Creates a subtitle block using the segment's overall start and end times.
        :param segment: Segment dictionary without 'words' key.
        :param index: Subtitle index.
        :return: srt.Subtitle object.
        """
        start = timedelta(seconds=segment["start"])
        end = timedelta(seconds=segment["end"])
        content = segment.get("text", "").strip()
        return srt.Subtitle(index=index, start=start, end=end, content=content)

    def save(self, subtitles: list, output_path: str):
        """
        Generates and saves the SRT file from the subtitle list.
        :param subtitles: List of srt.Subtitle objects.
        :param output_path: Path and filename for the output file.
        """
        srt_content = srt.compose(subtitles)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(srt_content)
        print(f"Subtitles saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio to Subtitle Transcriber")
    parser.add_argument("audio", help="Path to the input audio file")
    parser.add_argument("output", help="Path to save the output subtitle file")
    parser.add_argument("--model", default="base", help="Whisper model to use (default: base)")
    parser.add_argument("--language", default="en", help="Language for transcription (default: en)")
    parser.add_argument("--min_chars", type=int, default=10, help="Minimum characters per subtitle block (default: 10)")

    args = parser.parse_args()
    transcriber = AudioTranscriber(model=args.model, language=args.language, min_chars=args.min_chars)
    transcription_result = transcriber.transcribe_audio(args.audio)
    subtitles = transcriber.process_transcription(transcription_result)
    transcriber.save(subtitles, args.output)