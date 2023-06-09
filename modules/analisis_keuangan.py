from . import submodules as sdl
from datetime import date, timedelta

def analisis_keuangan():
    # Identitas subprogram
    print("\n"+" ANALISIS KEUANGAN ".center(50,"=")+"\n")

    # Buka dan baca file sejarah_transaksi dan dompet
    hd_dp, ls_dp = sdl.open_read_csv("dompet.csv")
    _, ls_tr = sdl.open_read_csv("sejarah_transaksi.csv")

    # Restriksi 30 hari yg lalu
    hari_ini = date.today()
    hari_30_belakang = (hari_ini - timedelta(days=30)).strftime("%Y/%m/%d")
    ls_tr_new = [] # list untuk menampung list transaksi 30 hari ke belakang
    for ele in ls_tr:
        if ele[0] < hari_30_belakang:
            break
        ls_tr_new.append(ele)

    # Cek transaksi 30 hari apakah ada
    if len(ls_tr_new) == 0:
        print("Kamu belum membuat transaksi 30 hari ini!")
        print("Tidak bisa melakukan analisis keuangan")
        return # Mengakhiri program karena tidak ada transaksi

    # Pertambahan/pengurangan dompet
    hd_dp.append("Perubahan") # kolom untuk perubahan dompet
    for i in range(len(ls_tr_new)):
        # Akses setiap kolom pada list transaksi
        _, kode, _, dompet, nominal = ls_tr_new[i] 
        nominal = int(nominal)
        tr_index = -1 # Index -1
        for j in range(len(ls_dp)):
            if dompet == ls_dp[j][0]: # cari index untuk tr_index
                tr_index = j
                break
        try: # Tambahkan nominal pada transaksi apabila index 2 ls_dp ada
            ls_dp[tr_index][2] = ls_dp[tr_index][2] + nominal if kode == "1" else ls_dp[tr_index][2] - nominal
        except IndexError: # Jika ls_dp index 2 tidak ada
            (ls_dp[tr_index]).append(nominal) if kode == "1" else (ls_dp[tr_index]).append(-nominal)
    
    # Ganti warna untuk perubahan dompet 
    for ele in ls_dp:
        try:
            ele[1] = f"Rp{int(ele[1]):>10,}"
            color2 = "green" if ele[2] >= 0 else "red"
            ele[2] = sdl.ch_color_style(f"Rp{ele[2]:>10,}",color2)
        except IndexError: # Apabila index 1/2 tidak ada
            pass

    # Jumlahkan pendapatan berdasarkan tipe dan jumlahkan pengeluaran berdasarkan tipe
    hd_in = ["Pemasukan", "Subtotal"] # Header distribusi pendapatan
    ls_in = []
    hd_ex = ["Pengeluaran", "SubTotal", "% Thd pemasukan"] # Header distribusi pengeluaran
    ls_ex = []

    for i in range(len(ls_tr_new)):
        code = ls_tr_new[i][1]
        tipe = ls_tr_new[i][2]
        amount = int(ls_tr_new[i][4])
        
        if tipe == "transfer_akun":
            continue # Mengabaikan tipe transfer akun
        
        if code == "1": # Jumlahkan pendapatan berdasarkan tipe pada blok ini
            in_index = -1 # index -1
            for p in range(len(ls_in)):
                if ls_in[p][0] == tipe: # cari index untuk in_index
                    in_index = p
                    break
            if in_index != -1: # Tambahkan nominal jika index bukan -1
                ls_in[in_index][1] += amount
            else: # Append tipe, nominal jika index -1
                ls_in.append([tipe, amount])

        else: # Penjumlahan pengeluaran berdasarkan tipe pada blok ini
            ex_index = -1 # index -1
            for j in range(len(ls_ex)):
                if ls_ex[j][0] == tipe:
                    ex_index = j
                    break
            if ex_index != -1: # cari index untuk ex_index
                ls_ex[ex_index][1] += amount
            else: # Append tipe, nominal jika index -1
                ls_ex.append([tipe, amount])

    # Penambahan total semua tipe pendapatan
    total_in = sum([ ele[1] for ele in ls_in ])
    ls_in.append(["Total Seluruh", total_in])

    # Penambahan total semua tipe pengeluaran
    total_ex = sum([ ele[1] for ele in ls_ex ])
    ls_ex.append(["Total Seluruh", total_ex])

    for ele1 in ls_in:
        ele1[1] = f"Rp{int(ele1[1]):>10,}"
    
    # Presentase pengeluaran pada blok ini
    # Ambil batas presentase pada file tipe_pengeluaran 
    _, ls_tpex = sdl.open_read_csv("tipe_pengeluaran.csv")
    notes = [] # Catatan peringatan di sini

    for j in range(len(ls_ex)-1): # Mengecualikan total seluruh ex
        amount = int(ls_ex[j][1])
        tipe = ls_ex[j][0]
        
        # Default batas presentase pengeluaran per tipe 25 % oleh seluruh pendapatan
        # Ubah presentase tipe apabila ada
        prc = 25 # Default presentase 25%
        for k in range(len(ls_tpex)): # Akses apabila ada presentase kustom
            if ls_tpex[k][0] == tipe:
                prc = float(ls_tpex[k][1])

        # Hitung presentase pengeluaran per tipe thd pendapatan
        by_in = round(amount/total_in*100,2)
        ls_ex[j].append(f"{by_in}%")

        ls_ex[j][1] = f"Rp{amount:>10,}"

        if tipe == "bayar utang":
            continue
        
        if by_in > prc:
            for i in range(len(ls_ex[j])):
                ls_ex[j][i] = sdl.ch_color_style(ls_ex[j][i],"red")
            notes.append(f"Pengeluaran tipe {ls_ex[j][0]} berada di atas {prc}% pendapatan 30 hari ke belakang")
    
    # Untuk total pengeluaran, batas presentase 70% thd seluruh pendapatan
    all_amount = int(ls_ex[-1][1])
    prc_all = 70 # Presentase seluruh pengeluaran dgn batas 70% thd pendapatan

    by_in = round(all_amount/total_in*100,2)
    ls_ex[-1].append(f"{by_in}%")

    ls_ex[-1][1] = f"Rp{all_amount:>10,}"
    if by_in > prc_all:
        for i in range(len(ls_ex[-1])):
            ls_ex[-1][i] = sdl.ch_color_style(ls_ex[-1][i],"red")
        notes.append(f"Pengeluaran total berada di atas {prc_all}% pendapatan 30 hari ke belakang")
    
    # Tampilkan update dompet
    print("Analisis Dompet 30 hari ke belakang :")
    sdl.display_table(ls_dp, hd_dp)
    print()

    # Tampilkan pendapatan berdasarkan tipe
    print("Analisis Pendapatan berdasarkan tipe 30 hari ke belakang :")
    sdl.display_table(ls_in, hd_in)
    print()

    # Tampilkan pengeluaran berdasarkan tipe
    print("Analisis Pengeluaran berdasarkan tipe 30 hari ke belakang :")
    sdl.display_table(ls_ex, hd_ex)
    print()

    # Tampilkan peringatan
    print("Catatan:")
    if len(notes) == 0:
        print("Selamat, tidak ada catatan untuk pengeluaranmu!")
        print("Tetap gunakan uang dengan bijak")
    else:
        for ele in notes:
            print(ele) # Tampilkan setiap peringatan yang ada

if __name__ == "__main__":
    analisis_keuangan()