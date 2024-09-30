import toml
from models import load_model
from utils import vectorstore_embeddings, gemini_response, pdf_util, store_to_pinecone, query_to_pinecone

config = toml.load('config.toml')
index=config['pinecone']['index']
namespace=config['pinecone']['namespace']
top_k=config['pinecone']['top_k']

chunk_size = config['text_splitter']['CHUNK_SIZE']
chunk_overlap = config['text_splitter']['CHUNK_OVERLAP']

model_name=config['model']['MODEL_NAME']
tokenizer, model = load_model.load_model(model_name)

def store_data(contents):
    # return "PDF Stored in Pinecone"
    total_text=pdf_util.extract_text_from_pdf(contents, chunk_size, chunk_overlap)

    vectorstore=vectorstore_embeddings.create_vector_store(total_text, tokenizer, model)

    storing_pinecone_status=store_to_pinecone.store_to_pinecone(vectorstore, index, namespace)

    if(storing_pinecone_status): return "PDF Stored in Pinecone"
    else: return "Not Stored"


def query_results(query):
    
    pinecone_results=query_to_pinecone.query_pinecone(tokenizer, model, query, index, namespace, top_k)
    llm_response=gemini_response.gemini_response(query, pinecone_results)

    return pinecone_results, llm_response
