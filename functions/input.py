import math
import random
import string
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
    
    print("List Nama Stasiun")
    for i in list_stasiun:
        print("- " + i) 
    
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

    daftar_jadwal.sort(key=lambda jadwal: jadwal["berangkat"])
    return daftar_jadwal

#Pilih Kereta
def PilihKereta(daftar_jadwal):
    Border()
    print("Jadwal keberangkatan:")
    nomor_valid = []
    for nomor in range(1, len(daftar_jadwal) + 1):
        jadwal = daftar_jadwal[nomor - 1]
        print(str(nomor) + ". " + jadwal["seri"] + "  berangkat " + jadwal["berangkat"])
        nomor_valid.append(str(nomor))

    while True:
        pilihan = input("Pilih kereta (1-" + str(len(daftar_jadwal)) + "): ").strip()
        if pilihan in nomor_valid:
            return daftar_jadwal[int(pilihan) - 1]
        print("Pilihan tidak valid, silahkan coba lagi.")

def PilihGerbongDanJumlahTiket():
    Border()
    while True:
        gerbong = int(input("Silahkan pilih gerbong kereta (1-7): "))   
        if type(gerbong)==int and gerbong >= 1 and gerbong <= 7:
            break
        else:
            gerbong = int(input("Gerbong tidak valid, masukkan angka 1 hingga 7 untuk nomor gerbong: "))
  
    while True:
        jumlah_tiket = int(input("Masukkan jumlah tiket: ").strip())
        if type(jumlah_tiket)==int and jumlah_tiket > 0 :
            break
        else:
            print("Jumlah tiket tidak valid, masukkan angka valid.")
    return gerbong, jumlah_tiket

def HitungTiket(jumlah_tiket, stasiun_asal, stasiun_tujuan, kereta_dipilih):
    Border()
    
    def ke_menit(jam):
        jam_str, menit_str = jam.split(".")
        return int(jam_str) * 60 + int(menit_str)

    waktu_perjalanan = (ke_menit(kereta_dipilih["tiba"]) - ke_menit(kereta_dipilih["berangkat"])) % 1440

    def ke_menit(jam):
        jam_str, menit_str = jam.split(".")
        return int(jam_str) * 60 + int(menit_str)
 
    waktu_perjalanan = (ke_menit(kereta_dipilih["tiba"]) - ke_menit(kereta_dipilih["berangkat"])) % 1440
 
 
    km_stasiun = {s["nama"]: s["km"] for s in data["stasiun"]}
    km_batas = km_stasiun[data["tarif"]["stasiun_batas"]]
 
    posisi_asal = km_stasiun[stasiun_asal] - km_batas
    posisi_tujuan = km_stasiun[stasiun_tujuan] - km_batas
    if posisi_asal * posisi_tujuan < 0:
        harga_per_tiket = data["tarif"]["lintas_penuh"]
    else:
        harga_per_tiket = data["tarif"]["satu_sisi"]
    harga_tiket = harga_per_tiket * jumlah_tiket
 
    karakter = string.ascii_uppercase + string.digits
    kode_unik_tiket = "TKT-" + "".join(random.choice(karakter) for _ in range(8))
 
    print("Rincian perjalanan:")
    print("Waktu perjalanan : " + str(waktu_perjalanan) + " menit")
    print("Harga per tiket  : Rp" + format(harga_per_tiket, ",").replace(",", "."))
    print("Jumlah tiket     : " + str(jumlah_tiket))
    print("Total harga      : Rp" + format(harga_tiket, ",").replace(",", "."))
 
    return waktu_perjalanan, harga_tiket, kode_unik_tiket
    
    return waktu_perjalanan, harga_tiket, kode_unik_tiket

def Pembayaran(harga_tiket):
    Border()
    daftar_bank = ["BCA", "Mandiri", "BNI", "BRI"]
    print("Total pembayaran: Rp" + format(harga_tiket, ",").replace(",", "."))
    print("Pilih bank untuk pembayaran:")
    for nomor in range(len(daftar_bank)):
        print(str(nomor + 1) + ". " + daftar_bank[nomor])

    while True:
        pilihan = input("Pilih bank (1-" + str(len(daftar_bank)) + "): ").strip()
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar_bank):
            break
        print("Pilihan tidak valid, silahkan coba lagi.")

    while True:
        no_rekening = input("Masukkan nomor rekening: ").strip()
        if no_rekening.isdigit() and 10 <= len(no_rekening) <= 16:
            break
        print("Nomor rekening tidak valid, silahkan coba lagi.")

    while True:
        pin = input("Masukkan PIN (6 digit): ").strip()
        if pin.isdigit() and len(pin) == 6:
            break
        print("PIN harus 6 digit angka, silahkan coba lagi.")

    print("\nMemproses pembayaran dari rekening " + "*"*(len(no_rekening)-4) + no_rekening[-4:] + " ...")
    print("Pembayaran sukses!")

def TampilkanTiket(pemesan_nama, pemesan_telp, pemesan_email, stasiun_asal, stasiun_tujuan, tanggal, gerbong, jumlah_tiket, waktu_perjalanan, harga_tiket, kode_unik_tiket, kereta_dipilih):
    
    Border()
    print("TIKET COMMUTER LINE BANDUNG RAYA")
    print("Kode tiket     : " + kode_unik_tiket)
    print("Nama pemesan   : " + pemesan_nama)
    print("No. telepon    : " + pemesan_telp)
    print("Email          : " + pemesan_email)
    print("Kereta         : " + kereta_dipilih["seri"] + " (" + kereta_dipilih["kode"] + ")")
    print("Tanggal        : " + tanggal)
    print("Rute           : " + stasiun_asal + " -> " + stasiun_tujuan)
    print("Berangkat      : " + kereta_dipilih["berangkat"])
    print("Tiba           : " + kereta_dipilih["tiba"])
    print("Waktu tempuh   : " + str(waktu_perjalanan) + " menit")
    print("Gerbong        : " + str(gerbong))
    print("Jumlah tiket   : " + str(jumlah_tiket))
    print("Total bayar    : Rp" + format(harga_tiket, ",").replace(",", "."))
    print("Status         : LUNAS")
    Border()
    Border()
    return