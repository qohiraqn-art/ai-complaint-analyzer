import json
import os 
import pandas as pd
import time

from dotenv import load_dotenv 
from google import genai
from google.genai import types
load_dotenv()

api_key = os.getenv('gemini_api_key')
client = genai.Client(api_key=api_key)

def analisis_complaint(text_complaint) :
    percobaan_maksimal = 3
    for percobaan in range (percobaan_maksimal) :
        try:
            response = client.models.generate_content(
            model = 'gemini-3.5-flash',
            contents = f"""tolong analisa komplain berikut 
            komplain = "{text_complaint}"

            Balas HANYA dengan JSON persis format ini, tanpa kalimat pembuka atau penutup, tanpa tanda backtick markdown :
            {{"sentiment" : "positive/negative/neutral", "category" : "billing/technical/general", "urgent" : true/false }}
            """,
            config = types.GenerateContentConfig(
                temperature = 0
            )
            )
            data = json.loads(response.text) 
            return data
        except Exception as e :
            print(f"percobaan {percobaan + 1} gagal :", e)
            time.sleep(5)
    return None


df = pd.read_csv("data_complaint.csv")
df.columns = df.columns.str.strip()

semua_hasil= []
urgent = 0

for index, row in df.iterrows() :
    complaint = row["Complaint"]
    hasil = analisis_complaint(complaint)
    semua_hasil.append(hasil)
    print(hasil)

for item in semua_hasil :
    if item is not None :
        if item["urgent"] == True :
             urgent = urgent + 1



df_hasil = pd.DataFrame(semua_hasil)
df_final = pd.concat([df,df_hasil], axis=1)
df_final.to_csv("hasil_analisis_complaint.csv", index=False)

print(semua_hasil)
print('yang urgent :', urgent)
print(df_final)