import spacy
import warnings

warnings.filterwarnings("ignore", message=r"\[W007\]", category=UserWarning)
warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)


nlp = spacy.load('en_core_web_sm')

def compare_strings(model, string1, string2):
    doc1 = model(string1)
    doc2 = model(string2)
    return doc1.similarity(doc2)

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    print(compare_strings(nlp, "Hello World", "Hello World"))