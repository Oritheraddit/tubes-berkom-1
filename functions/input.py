import math
from datetime import datetime, timedelta
import json
data = json.load(open("data/data_commuter_bandung_raya.json", encoding="utf-8"))

def Border():
    print("\n","="*40,"\n")

#menginput data pemesan
def InputDataPemesan():
    while True:
        pemesan_nama = input("Masukkan nama pemesan tiket: ")
        pemesan_telp = input("Masukkan nomor telepon pemesan tiket: ")
        pemesan_email = input("Masukkan email pemesan tiket: ")
        confirm = input("Data pemesan sudah benar? (y/n): ").strip().lower()
        if confirm == "y":
            break
    return pemesan_nama, pemesan_telp, pemesan_email

#Menginput stasiun
def InputStasiun():
    Border()
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
    return stasiun_asal, stasiun_tujuan

#Input Tanggal
def CariTanggal():
    hari_ini = datetime.now()
    Border()
    hari_ini_str = hari_ini.strftime("%Y-%m-%d")
    pilihan_tanggal = []
    print("Pilih tanggal keberangkatan:")
    for i in range(4):
        hari = hari_ini = datetime.now() + timedelta(days=i)
        pilihan_tanggal.append(hari.strftime("%Y-%m-%d"))
        print(str(i+1) + ". " + hari.strftime("%Y-%m-%d"))
    print("5. Tanggal lain")
    
    while True:
        pilihan = input("Pilih (1-5): ").strip()
        if pilihan in ["1", "2", "3", "4"]:
            return pilihan_tanggal[int(pilihan) - 1]
        elif pilihan == "5":
            tanggal = input("Masukkan tanggal (YYYY-MM-DD): ").strip()
            if len(tanggal) != 10 or tanggal[4] != "-" or tanggal[7] != "-":
                print("Format salah, contoh: 2026-11-27")
            elif tanggal < hari_ini_str:
                print("Tanggal sudah lewat, silahkan coba lagi.")
            else:
                return tanggal
        else:
            print("Pilihan tidak valid, silahkan coba lagi.")     
    #return tanggal

#Cari Jadwal
def CariJadwal(asal, tujuan, tanggal):
    waktu_sekarang = datetime.now()
    tanggal_hari_ini = waktu_sekarang.strftime("%Y-%m-%d")
    jam_sekarang = waktu_sekarang.strftime("%H.%M")

    daftar_jadwal = []

    for kode_kereta in data["jadwal"].get(tanggal, []):
        data_kereta = data["kereta"][kode_kereta]
        daftar_perhentian = data_kereta["perhentian"]

        daftar_nama_stasiun = [perhentian[0] for perhentian in daftar_perhentian]
        posisi_asal = daftar_nama_stasiun.index(asal)
        posisi_tujuan = daftar_nama_stasiun.index(tujuan)
        searah = posisi_asal < posisi_tujuan

        if searah:
            jam_berangkat = daftar_perhentian[posisi_asal][2]
            jam_tiba = daftar_perhentian[posisi_tujuan][1]
            bukan_hari_ini = tanggal != tanggal_hari_ini
            belum_berangkat = jam_berangkat > jam_sekarang

            if bukan_hari_ini or belum_berangkat:
                daftar_jadwal.append({
                    "kode": kode_kereta,
                    "seri": data_kereta["seri"],
                    "berangkat": jam_berangkat,
                    "tiba": jam_tiba,
                })
                #if len(daftar_jadwal) == 3:
                #    break

    return daftar_jadwal

#Pilih Kereta
def PilihKereta(daftar_jadwal):
    Border()
    print("Jadwal keberangkatan:")
    nomor_valid = []
    for nomor in range(1, len(daftar_jadwal) + 1):
        jadwal = daftar_jadwal[nomor - 1]
        print(str(nomor) + ". " + jadwal["seri"] + "  berangkat " + jadwal["berangkat"] + "  tiba " + jadwal["tiba"])
        nomor_valid.append(str(nomor))

    while True:
        pilihan = input("Pilih kereta (1-" + str(len(daftar_jadwal)) + "): ").strip()
        if pilihan in nomor_valid:
            return daftar_jadwal[int(pilihan) - 1]
        print("Pilihan tidak valid, silahkan coba lagi.")

#Generate Kursi
def GenerateKursi():

    return
