import json
from functions.input import (InputStasiun,InputDataPemesan,CariJadwal,CariTanggal,PilihKereta,PilihGerbongDanJumlahTiket,HitungTiket,Pembayaran,TampilkanTiket)

print("Selamat datang di pemesanan tiket kereta Commuter Line Bandung Raya")

pemesan_nama, pemesan_telp, pemesan_email = InputDataPemesan()
stasiun_asal, stasiun_tujuan = InputStasiun()

while True:
    tanggal = CariTanggal()
    jadwal = CariJadwal(stasiun_asal, stasiun_tujuan, tanggal)
    if len(jadwal) == 0:
        print("Tidak ada jadwal untuk tanggal itu, silahkan pilih tanggal lain.")
    else:
        break

kereta_dipilih = PilihKereta(jadwal)
gerbong, jumlah_tiket = PilihGerbongDanJumlahTiket()

waktu_perjalanan, harga_tiket, kode_unik_tiket = HitungTiket(jumlah_tiket, stasiun_asal, stasiun_tujuan, kereta_dipilih)

Pembayaran(harga_tiket)

TampilkanTiket(pemesan_nama, pemesan_telp, pemesan_email, stasiun_asal, stasiun_tujuan, tanggal, gerbong, jumlah_tiket, waktu_perjalanan, harga_tiket, kode_unik_tiket, kereta_dipilih)
