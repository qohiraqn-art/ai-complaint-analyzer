import os
import json 
import pandas as pd 
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=api_key)

class HasilAnalisis(BaseModel) :
    rating : int
    bermasalah : bool

def analisis_review(review) :
    percobaan_maksimal = 3
    for percobaan in range (percobaan_maksimal) :
        try :
            response = client.models.generate_content(
                model = 'gemini-3.6-flash',
                contents = f""" tolong analisa review dari pelanggan berikut 

                review = "{review}"

                balas HANYA dengan format JSON, tanpa kalimat pembuka, dan kalimat penutup, tanpa tanda backtick markdown :
                {{"rating" : 1-5, "bermasalah" : true/false }}
                """,
                config = types.GenerateContentConfig(
                    temperature=0
                )
            )
            data = json.loads(response.text)
            hasil = HasilAnalisis(**data)
            return hasil
        except Exception as masalah :
            print(f"percobaan : {percobaan + 1}, gagal ", masalah)
            time.sleep(5)
    return None

df = pd.read_csv("review.csv")
df.columns = df.columns.str.strip()

hasil_analisa_review = []
yang_bermasalah = 0
total_rating = 0


for index, row in df.iterrows() :
    review = row["Review"]
    hasil = analisis_review(review)
    hasil_analisa_review.append(hasil)
    print(hasil)


for item in hasil_analisa_review :
    if item is not None:
        if item.bermasalah == True :
            yang_bermasalah = yang_bermasalah + 1
        total_rating = total_rating + item.rating

rata_rata = total_rating / len(hasil_analisa_review)
print(rata_rata)

data_untuk_tabel = [item.model_dump() for item in hasil_analisa_review if item is not None]
df_hasil = pd.DataFrame(data_untuk_tabel)
df_final = pd.concat([df,df_hasil], axis=1)
df_final.to_csv("hasil_analisis_review.csv", index=False)

print(df_final) 