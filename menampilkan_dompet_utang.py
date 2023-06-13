import submodules

def menampilkan_dompet_utang():
    # Akses file domept dan file utang
    hd_dompet , ls_dompet = submodules.open_read_csv("dompet.csv")
    hd_utang , ls_utang = submodules.open_read_csv("utang.csv")

    # Penyesuaian konten nominal dengan mata uang rupiah
    ls_dompet = [ [ele[0], f"Rp{int(ele[1]):>10,}"] for ele in ls_dompet ]
    ls_utang = [ [ele[0], f"Rp{int(ele[1]):>10,}"] for ele in ls_utang ]

    # Tampilkan dompet
    if len(ls_dompet) >= 1:
        print("Daftar Dompet Pengguna :")
        submodules.display_table(ls_dompet, hd_dompet)
        print()
    else:
        print("\nKamu belum memiliki dompet")

    # Tampilkan utang
    if len(ls_utang) >= 1:
        print("Daftar Utang Pengguna :")
        submodules.display_table(ls_utang, hd_utang)
    else:
        print("Selamat, Kamu tidak memiliki utang!")

if __name__ == "__main__":
    menampilkan_dompet_utang()