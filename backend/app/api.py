from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from services import server

app = FastAPI()

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        contents = await file.read()
        '''
            Since we are sending the pdf file in form of Bytes from frontend, 
            therefore we need to send convert it into BytesIO format which PdfReader accepts!!
        '''

        status_stored=server.store_data(contents)

        return {"text": status_stored}
    else:
        return {"error": f"Invalid file format - {file}. Please upload a PDF file."}
    
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query(request: QueryRequest):
    query=request.query
    most_similar, llm_response = server.query_results(query)
    text_content = llm_response.text#._result['candidates'][0]['content']['parts'][0]['text']
    final_result = text_content # + str(most_similar)
    return {"text": f"{final_result}"}