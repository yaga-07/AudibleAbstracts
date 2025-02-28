from typing import List, Dict
import torch
import numpy as np
from string import punctuation
import re
from transformers.models.speecht5.number_normalizer import EnglishNumberNormalizer
from termcolor import colored


number_normalizer = EnglishNumberNormalizer()

def preprocess(text):
    text = number_normalizer(text).strip()
    text = text.replace("-", " ")
    if text[-1] not in punctuation:
        text = f"{text}."

    abbreviations_pattern = r'\b[A-Z][A-Z\.]+\b'

    def separate_abb(chunk):
        chunk = chunk.replace(".","")
        print(chunk)
        return " ".join(chunk)

    abbreviations = re.findall(abbreviations_pattern, text)
    for abv in abbreviations:
        if abv in text:
            text = text.replace(abv, separate_abb(abv))
    return text

class MultiTurnParlerTTS():
    def __init__(self,
                 speakers,
                 model,
                 tokenizer):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = model.to(self.device)
        self.tokenizer = tokenizer
        self.speakers = speakers
        self.speaker_ids = {f"speaker_{i+1}":
             {"name": speaker.name,
              "description": speaker.description,
              "description_input_ids": tokenizer(speaker.description, return_tensors="pt").to(self.device)}
             for i, speaker in enumerate(self.speakers)}

    def generate_audio(self, text: List[Dict[str, str]]):
      final_audio = []
      for turn in text:
        speaker_description_input_ids = self.speaker_ids[turn['role'].lower()]['description_input_ids']
        speaker_prompt_input_ids = self.tokenizer(preprocess(turn['content']), return_tensors="pt").to(self.device)
        generation = self.model.generate(
            input_ids=speaker_description_input_ids.input_ids, prompt_input_ids=speaker_prompt_input_ids.input_ids,
            attention_mask=speaker_description_input_ids.attention_mask, prompt_attention_mask=speaker_prompt_input_ids.attention_mask,
            do_sample=True, temperature=1.0
        )

        final_audio.append(generation.cpu().numpy().squeeze())

      return np.concatenate(final_audio)


    def __repr__(self) -> str:
        s = "Speakers Config: \n"
        for i in self.speaker_ids:
            s += f"{colored(i, 'yellow')} \n"
            s += f"Name: {colored(self.speaker_ids[i]['name'], 'green')} \n"
            s += f"Description: {colored(self.speaker_ids[i]['description'], 'cyan')} \n"
        return s