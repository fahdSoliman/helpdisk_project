# translate model m2m100 facebook model class with its procedures
from django.conf import settings
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class Translator:
    def __init__(self):
        self.model_dir = settings.BASE_DIR + "\\LLM_models\\m2m100_418M"
        self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_dir)
        self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_dir)
    
    def translate_to_en(self, text):
        self.tokenizer.src_lang = "ar"
        encoded_ar = self.tokenizer(text, return_tensors="pt")
        generated_tokens = self.model.generate(**encoded_ar, forced_bos_token_id=self.tokenizer.get_lang_id("en"))
        out = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

        return out[0]
    
    def translate_to_ar(self, text):
        self.tokenizer.src_lang = "en"
        encoded_en = self.tokenizer(text, return_tensors="pt", padding=True)
        generated_tokens = self.model.generate(**encoded_en, forced_bos_token_id=self.tokenizer.get_lang_id("ar"))
        out = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return out
    


'''@misc{fan2020englishcentric,
      title={Beyond English-Centric Multilingual Machine Translation}, 
      author={Angela Fan and Shruti Bhosale and Holger Schwenk and Zhiyi Ma and Ahmed El-Kishky and Siddharth Goyal and Mandeep Baines and Onur Celebi and Guillaume Wenzek and Vishrav Chaudhary and Naman Goyal and Tom Birch and Vitaliy Liptchinsky and Sergey Edunov and Edouard Grave and Michael Auli and Armand Joulin},
      year={2020},
      eprint={2010.11125},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}'''