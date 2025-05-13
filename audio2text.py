import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from opencc import OpenCC
from dp import get_result
import config

class Audio2Text:
    def __init__(self, model_path=config.model_path):
        self.cc = OpenCC('t2s')

        self.processor = WhisperProcessor.from_pretrained(model_path)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_path)
        self.model.config.forced_decoder_ids = None

    def transcribe(self, audio_path):
        audio, sr = librosa.load("test2.m4a", sr=16000)
        input_features = self.processor(audio, sampling_rate=16000, return_tensors="pt").input_features

 
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        simplified = self.cc.convert(transcription)

        fix_res = self._fix_text(simplified)

        return fix_res

    def _fix_text(self, text):
        # return text
        prompt = config.prompt1
        fix_res = get_result(prompt, text)

        return fix_res