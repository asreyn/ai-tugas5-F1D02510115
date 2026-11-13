import json

# 1. Membaca aturan dari file JSON
with open("aturan.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data["judul"])
print("Jawab y/t.")

# 2. Mengumpulkan fakta awal dari user
fakta = set()
fakta_awal_list = []

for i, pertanyaan in enumerate(data["pertanyaan"], 1):
    while True:
        jawaban = input(f"{i}. {pertanyaan['teks']} (y/t) > ").lower().strip()
        if jawaban == 'y':
            fakta.add(pertanyaan["fakta"])
            fakta_awal_list.append(pertanyaan["fakta"])
            break
        elif jawaban == 't':
            break
        else:
            print("Jawaban tidak valid! Masukkan y atau t.")

# Tampilkan daftar fakta awal yang dijawab "y"
fakta_teks = ", ".join(fakta_awal_list) if fakta_awal_list else "Tidak ada"
print(f"\nFakta awal: {fakta_teks}\n")

# 3. Proses Forward Chaining
aturan_dipakai = []
aturan_yang_sudah_dijalankan = set()
siklus = 1

while True:
    aturan_baru_dieksekusi = False
    
    for aturan in data["aturan"]:
        # Skip jika aturan sudah pernah dipakai di siklus sebelumnya
        if aturan["id"] in aturan_yang_sudah_dijalankan:
            continue
            
        syarat = aturan["jika"]
        
        # Mengecek apakah syarat terpenuhi ("dan" atau "atau")
        if aturan["mode"] == "dan":
            cocok = all(item in fakta for item in syarat)
        else:
            cocok = any(item in fakta for item in syarat)
            
        # Jika cocok, masukkan hasil ke dalam fakta baru
        if cocok:
            hasil = aturan["maka"]
            aturan_yang_sudah_dijalankan.add(aturan["id"])
            aturan_dipakai.append(aturan)
            
            if hasil not in fakta:
                fakta.add(hasil)
            
            print(f"Siklus {siklus}: {aturan['id']} -> {hasil}")
            siklus += 1
            aturan_baru_dieksekusi = True
            break # Hentikan iterasi for, ulangi while dari awal untuk siklus selanjutnya
            
    # Jika loop selesai tapi tidak ada aturan yang terpicu, hentikan program
    if not aturan_baru_dieksekusi:
        print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
        break

# 4. Menampilkan Hasil dan Alasan
print("\nKesimpulan: ", end="")

# Memfilter hasil akhir (Fakta yang dihasilkan aturan, tapi tidak menjadi syarat di aturan lain)
semua_syarat_jika = set()
for r in data["aturan"]:
    semua_syarat_jika.update(r["jika"])

kesimpulan_akhir = [r["maka"] for r in aturan_dipakai if r["maka"] not in semua_syarat_jika]

if not kesimpulan_akhir:
    print("tidak ada kesimpulan yang sesuai.")
else:
    print(", ".join(kesimpulan_akhir))

print("Alasan:")
if not aturan_dipakai:
    print("  Tidak ada aturan yang terpenuhi dari fakta yang diberikan.")
else:
    # Print jejak mundur dari aturan yang terpakai
    for aturan in reversed(aturan_dipakai):
        # Cari mana syarat di aturan tersebut yang benar-benar ada di fakta kita (berlaku untuk mode "atau")
        syarat_terpenuhi = [s for s in aturan["jika"] if s in fakta]
        print(f"  {aturan['maka']} <- {aturan['id']} ({', '.join(syarat_terpenuhi)})")

print(f"\nCatatan: {data['batas']}")