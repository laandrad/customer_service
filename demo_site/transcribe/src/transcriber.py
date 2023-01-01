import soundfile as sf
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration


class Transcriber:
    def __init__(self):
        self.model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-medium-librispeech-asr")
        self.processor = Speech2TextProcessor.from_pretrained("facebook/s2t-medium-librispeech-asr")

    def transcribe(self, audio_file):
        data, _ = sf.read(audio_file)
        input_features = self.processor(
            data[:, 0],
            sampling_rate=16_000,
            return_tensors="pt"
        ).input_features
        generated_ids = self.model.generate(input_ids=input_features)
        transcription = self.processor.batch_decode(generated_ids)
        return transcription
