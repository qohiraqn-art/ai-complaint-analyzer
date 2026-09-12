import asyncio
import time
from pydantic import BaseModel 
import json
from pydantic import ValidationError


class HasilAnalisis(BaseModel) :
    sentiment : str
    confidence : float 
    kategori : str = ""




response_gemini_mentah = '{"sentiment": "negative", "confidence": 0.7, "kategori": "pengiriman"}'

def proses_response_gemini(response) : 
    try :
        hasil4 = HasilAnalisis.model_validate_json(response)
        return(hasil4)
    except ValidationError as e :
        print("ada yang salah :", e)
        return None

response_valid = '{"sentiment": "positive", "confidence": 0.9, "kategori": "harga"}'
response_lain = '{"sentiment": "negative", "confidence": 0.3, "kategori": "pengiriman"}'
response_rusak = "bukan json"


hasil = proses_response_gemini(response_valid)
hasil2 = proses_response_gemini(response_rusak)

if hasil is None :
    print("gagal memproses, coba lagi")
else : 
    print(hasil)

if hasil2 is None:
    print("gagal memproses, coba lagi")
else:
    print(hasil2)



