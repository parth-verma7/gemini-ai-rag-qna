import torch
from transformers import AutoTokenizer, AutoModel
    
def create_vector_store(total_text:list, tokenizer: AutoTokenizer ,model: AutoModel) -> list:
    vectorstore=[]

    for i in range(0, len(total_text)):
        res={}
        a=total_text[i]
        ascii_vector_id = a.encode('ascii', 'ignore').decode('ascii')
        res["id"]=ascii_vector_id
        input_ids = tokenizer(total_text[i], return_tensors="pt")["input_ids"]

        with torch.no_grad():
            embeddings = model(input_ids)["last_hidden_state"].mean(dim=1)
            
        res['values']= embeddings.numpy()[0].tolist()
        vectorstore.append(res)

    return vectorstore