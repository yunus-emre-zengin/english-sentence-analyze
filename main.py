import spacy
import benepar
import json
from nltk import Tree
from fastapi import FastAPI
from pydantic import BaseModel

# --- Uygulama Başlangıcında Modelleri Yükle ---
# Bu kısım sadece bir kez çalışır ve modelleri hafızaya alır.
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
print("SpaCy model loaded.")

print("Adding benepar pipe...")
if "benepar" not in nlp.pipe_names:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})
print("Benepar pipe added.")
# ------------------------------------------------

# FastAPI uygulamasını başlat
app = FastAPI(
    title="Penn Treebank Parser API",
    description="Bir İngilizce cümlenin yapısal analizini JSON formatında döndürür.",
    version="1.0.0"
)

# İstek gövdesinin formatını belirleyen Pydantic modeli
class ParseRequest(BaseModel):
    sentence: str

# Ağacı JSON'a çeviren yardımcı fonksiyon
def tree_to_json(tree):
    return {
        "label": tree.label(),
        "children": [
            tree_to_json(child) if isinstance(child, Tree) 
            else {"label": "TOKEN", "value": child} 
            for child in tree
        ]
    }

@app.get("/", tags=["Health Check"])
def read_root():
    """API'nin çalışıp çalışmadığını kontrol etmek için basit bir endpoint."""
    return {"status": "API is running"}

@app.post("/parse", tags=["Parsing"])
def parse_sentence(request: ParseRequest):
    """
    Verilen cümleyi analiz eder ve yapı ağacını JSON olarak döndürür.
    """
    doc = nlp(request.sentence)
    sent = list(doc.sents)[0]
    parse_tree_string = sent._.parse_string
    
    tree = Tree.fromstring(parse_tree_string)
    json_output = tree_to_json(tree)
    
    return json_output


@app.post("/parse-string", tags=["Parsing"])
def parse_sentence_string(request: ParseRequest):
    """
    Verilen cümleyi analiz eder ve yapı ağacını ham string olarak döndürür.
    """
    doc = nlp(request.sentence)
    sent = list(doc.sents)[0]
    parse_tree_string = sent._.parse_string
    
    # Sonucu JSON yerine düz metin olarak döndür
    return PlainTextResponse(content=parse_tree_string)
