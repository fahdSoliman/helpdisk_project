## qa araelectra models , lfqa, BigScience model for summerization 3 example
from django.conf import settings
from cachetools import LRUCache
from transformers import ElectraForQuestionAnswering, AutoTokenizer, pipeline
from arabert import ArabertPreprocessor
from transformers import  AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer,util
import stanza

model_cache = LRUCache(maxsize=3)

class QnAGenerator:
    prep_object = ArabertPreprocessor(model_name="araelectra-base-discriminator")
    qa_modelname = settings.BASE_DIR + "\\LLM_models\\AraElectra-Arabic-SQuADv2-QA"

    def __init__(self, text="اسمي محمد وأنا أعمل في التجارة احب السباحة وركوب الخيل") -> None:
        self.text = text
        self.context = self.pre_process_context(self.text)
        self.qa_model = ElectraForQuestionAnswering.from_pretrained(self.qa_modelname)
        self.tokenizer = AutoTokenizer.from_pretrained(self.qa_modelname) 
        self.qa_pipe = pipeline('question-answering', model=self.qa_model, tokenizer=self.tokenizer) 
        pass

    def pre_process_context(self, text):
        context = self.prep_object.preprocess(text)
        return context
    
    def pre_process_question(self, question):
        q = self.prep_object.preprocess(question)
        return q

    def predict(self, question):
        QA_input = {
            'question': self.pre_process_question(question),
            'context': self.context
        }
        qa_res = self.qa_pipe(QA_input)
        return qa_res

    def update_text(self, updated_text):
        self.text = updated_text
        self.context = self.pre_process_context(self.text)
        return



'''
Author:
Vladimir Blagojevic: dovlex [at] gmail.com
'''
class LFQA:
    
    def __init__(self) -> None:
        self.model_dir = settings.BASE_DIR + "\\LLM_models\\bart_lfqa"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        pass

    def prepare_inputs(self, document, question):
        conditioned_doc = "<P> " + " <P> ".join([d for d in document])
        query_and_docs = "question: {} context: {}".format(question, conditioned_doc)
        return query_and_docs
    
    def generate_answer(self, query_and_docs):
        model_input = self.tokenizer(query_and_docs, truncation=True,padding=True, return_tensors="pt")
        generated_answers_encoded = self.model.generate(input_ids=model_input["input_ids"],
                                                attention_mask=model_input["attention_mask"],
                                                min_length=64,
                                                max_length=200,
                                                do_sample=False, 
                                                early_stopping=True,
                                                num_beams=8,
                                                temperature=1.0,
                                                top_k=None,
                                                top_p=None,
                                                eos_token_id=self.tokenizer.eos_token_id,
                                                no_repeat_ngram_size=3,
                                                num_return_sequences=1)
        generated_text = self.tokenizer.batch_decode(generated_answers_encoded, skip_special_tokens=True,clean_up_tokenization_spaces=True)

        return generated_text[0]

class SentenceTrans:

    def __init__(self) -> None:
        self.model_dir = settings.BASE_DIR + "\\LLM_models\\paraphrase-multilingual-mpnet-base-v2"
        self.model = SentenceTransformer(self.model_dir)
        pass

    def calc_embeddings(self, corpus):
        corpus_embeddings = self.model.encode(corpus)
        return corpus_embeddings
    
    def semantic_search(self, question_embeddings, corpus_embeddings):
        elected = util.semantic_search(query_embeddings=question_embeddings, 
                                       corpus_embeddings=corpus_embeddings, 
                                       top_k=5, 
                                       score_function='cos_sim')
        return elected




class StanfordModel:
    def __init__(self) -> None:
        self.model_dir = settings.BASE_DIR + "\\LLM_models\\ar_stanza"
        self.model = stanza.Pipeline(lang='ar', dir=self.model_dir, logging_level='error', download_method=None)
        pass

    def NLP(self, document):
        structured = self.model(document)
        return structured
    
    def sentece_split(self, structured):
        sentences = []
        for sent in structured.sentences:
            sentences.append(sent.text)
        return sentences
