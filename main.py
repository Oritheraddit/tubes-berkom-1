import json
from functions.input import InputStasiun,InputDataPemesan

print("Selamat datang di pemesanan tiket kereta Commuter Line Bandung Raya")

pemesan_nama, pemesan_telp, pemesan_email = InputDataPemesan()
stasiun_asal, stasiun_tujuan = InputStasiun()