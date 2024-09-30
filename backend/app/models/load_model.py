from transformers import AutoTokenizer, AutoModel

def load_model(model_name: str) -> tuple[AutoTokenizer, AutoModel]:
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    return tokenizer, model