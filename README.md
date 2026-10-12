# Academic Calculator

Website kalkulator akademik berbasis Python dan Streamlit.

## Fitur
- Kalkulator IPS berdasarkan nilai huruf dan SKS.
- Kalkulator IPK berdasarkan IPS serta total SKS setiap semester.
- Kalkulator nilai akhir berdasarkan nilai komponen dan bobot.
- Ekspor hasil ke CSV.
- Data tidak disimpan ke database.

## Menjalankan di komputer

1. Install Python 3.10 atau lebih baru.
2. Buka terminal/Command Prompt pada folder proyek.
3. Install dependensi:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

5. Buka alamat lokal yang ditampilkan terminal, biasanya `http://localhost:8501`.

## Publikasi gratis dengan Streamlit Community Cloud

1. Buat akun GitHub di https://github.com/ jika belum punya.
2. Buat repository baru, misalnya `academic-calculator`. Repository public paling sederhana untuk proses awal.
3. Unggah `app.py`, `requirements.txt`, dan `README.md` ke root repository.
4. Buka https://share.streamlit.io/ dan masuk menggunakan GitHub.
5. Klik **Create app**.
6. Pilih repository, branch `main`, dan file utama `app.py`.
7. Isi subdomain yang diinginkan jika tersedia, lalu klik **Deploy**.
8. Setelah deployment berhasil, aplikasi akan mendapat URL berakhiran `streamlit.app`. Bagikan URL itu kepada siapa saja.

## Catatan
- Skala nilai huruf pada kalkulator IPS adalah contoh: A=4.00, AB=3.50, B=3.00, BC=2.50, C=2.00, D=1.00, E=0.00. Sesuaikan jika aturan kampus berbeda.
- Batas nilai huruf pada kalkulator nilai akhir juga merupakan contoh, bukan aturan resmi kampus.
- Untuk menjaga konsistensi IPK, masukkan total SKS semester sesuai perhitungan akademik kampus.
