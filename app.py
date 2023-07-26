
from sqlalchemy import create_engine
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_engine("mysql://sql6634681:J1tAwUPb67@sql6.freemysqlhosting.net:3306/sql6634681")
@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    try:
     contents = await file.read()
     df = pd.read_excel(contents)
     print(df)
     df.to_sql("mytable",engine, if_exists="replace",index=False)
     return {"message": "File Uploaded Successfully"}
    except Exception as e:
       print(f"Error: {e}")
       return {"Error":e}
    

@app.get("/get_data/")
async def get_data():
   df = pd.read_sql_query("SELECT * FROM mytable",engine)
   data = df.to_dict(orient='records')
   return data