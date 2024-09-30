import os
from pinecone import Pinecone
from dotenv import load_dotenv
from pinecone import ServerlessSpec

load_dotenv()

def store_to_pinecone(vectorstore: list, index_name: str, namespace_name: str) -> str:
    try:
        pinecone_api_key=os.getenv('PINECONE_API_KEY')
        pc = Pinecone(api_key=pinecone_api_key)

        existing_indexes=pc.list_indexes()
        if index_name in existing_indexes:
            pc.delete_index(index_name)
        
        pc.create_index(
            name=index_name, 
            dimension=384, 
            metric="cosine", 
            spec=ServerlessSpec(cloud="aws",region="us-east-1")
        )

        index = pc.Index(index_name)
        index.upsert(
            vectors=vectorstore,
            namespace=namespace_name
        )
        
        return "success"
    
    except Exception as e:
        print(e)
        return "failed"
