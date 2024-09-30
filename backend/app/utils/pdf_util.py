import io
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(contents, chunk_size: str, chunk_overlap:str) -> list:
    text_splitter= RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    pdf=io.BytesIO(contents)
    reader=PdfReader(pdf)
    total_text=[]
    for i in range(len(reader.pages)):
        page=reader.pages[i]
        texts=page.extract_text()
        if texts:
            text_chunks = text_splitter.split_text(texts)
            total_text.extend(text_chunks)

    return total_text