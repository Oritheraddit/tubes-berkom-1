import math
from datetime import datetime
import json
data = json.load(open("data/data_commuter_bandung_raya.json", encoding="utf-8"))


#Menginput stasiun
def InputStasiun():
    list_stasiun = [stasiun["nama"] for stasiun in data["stasiun"]]
    list_stasiun_lower = [nama.lower() for nama in list_stasiun] 

    while True:
        stasiun_asal_input = input("Masukkan stasiun asal: ").strip().lower()
        if stasiun_asal_input in list_stasiun_lower:
            i = list_stasiun_lower.index(stasiun_asal_input)
            stasiun_asal = list_stasiun[i]
            break
        print("Stasiun tersebut tidak ada, silahkan coba lagi")

    while True:
        stasiun_tujuan_input = input("Masukkan stasiun tujuan: ").strip().lower()
        if stasiun_tujuan_input not in list_stasiun_lower:
            print("Stasiun tersebut tidak ada, silahkan coba lagi.")
        elif stasiun_tujuan_input == stasiun_asal_input:
            print("Stasiun tujuan tidak boleh sama dengan stasiun asal, silahkan coba lagi.")
        else:
            i = list_stasiun_lower.index(stasiun_tujuan_input)
            stasiun_tujuan = list_stasiun[i]
            break
    return        

#Cari Jadwal
def CariJadwal():
    
    return

#Pilih Kereta
def PilihKereta():
    
    return

#Generate Kursi
def GenerateKursi():

    return
