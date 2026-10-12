import streamlit as st
import pandas as pd

# -----------------------------
# Academic Calculator
# Built with Python + Streamlit
# -----------------------------

st.set_page_config(
    page_title="Academic Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

GRADE_POINTS = {
    "A": 4.00,
    "AB": 3.50,
    "B": 3.00,
    "BC": 2.50,
    "C": 2.00,
    "D": 1.00,
    "E": 0.00,
}

# Modern, responsive styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f7f9ff 0%, #eef3ff 55%, #f8fbff 100%); }
    [data-testid="stSidebar"] { background: #111b35; }
    [data-testid="stSidebar"] * { color: #f5f7ff !important; }
    .hero {
        padding: 1.6rem 1.8rem; border-radius: 22px;
        background: linear-gradient(120deg, #172554, #2563eb);
        color: white; margin-bottom: 1.2rem;
        box-shadow: 0 14px 35px rgba(37, 99, 235, .18);
    }
    .hero h1 { color: white; font-size: 2.15rem; margin: 0 0 .35rem 0; }
    .hero p { color: #dbeafe; margin: 0; font-size: 1rem; }
    .metric-card {
        padding: 1rem 1.1rem; border-radius: 16px;
        background: white; border: 1px solid #e4eaf7;
        box-shadow: 0 5px 18px rgba(15, 23, 42, .04);
    }
    .small-muted { color: #64748b; font-size: .88rem; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e4eaf7;
        padding: 1rem; border-radius: 16px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0; padding: 10px 16px;
        background: rgba(255,255,255,.75);
    }
    div.stButton > button {
        border-radius: 10px; font-weight: 600; min-height: 2.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "ips_rows" not in st.session_state:
    st.session_state.ips_rows = pd.DataFrame({
        "Mata kuliah": ["Matematika", "Fisika", "Pemrograman"],
        "Nilai huruf": ["A", "AB", "B"],
        "SKS": [3, 2, 3],
    })

if "ipk_rows" not in st.session_state:
    st.session_state.ipk_rows = pd.DataFrame({
        "Semester": ["Semester 1", "Semester 2"],
        "IPS": [3.50, 3.65],
        "Total SKS semester": [20, 22],
    })

st.markdown(
    """
    <div class="hero">
      <h1>🎓 Academic Calculator</h1>
      <p>Hitung IPS, IPK, dan nilai akhir mata kuliah dalam satu tempat.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🎓 Academic Calculator")
    st.caption("Alat bantu perhitungan akademik mahasiswa")
    st.markdown("---")
    st.markdown("### Panduan singkat")
    st.write("1. Pilih fitur melalui tab.")
    st.write("2. Masukkan nilai dan SKS.")
    st.write("3. Hasil dihitung otomatis.")
    st.markdown("---")
    st.caption("Versi 1.0 • Python + Streamlit")
    st.caption("Data yang dimasukkan tidak disimpan ke database oleh aplikasi ini.")

tab_ips, tab_ipk, tab_final, tab_info = st.tabs([
    "📘 Kalkulator IPS",
    "🎓 Kalkulator IPK",
    "🧮 Nilai Akhir",
    "ℹ️ Panduan",
])

with tab_ips:
    st.subheader("Kalkulator IPS")
    st.write("Masukkan mata kuliah, nilai huruf, dan jumlah SKS pada semester yang sedang dihitung.")
    st.info("Skala default: A = 4,00; AB = 3,50; B = 3,00; BC = 2,50; C = 2,00; D = 1,00; E = 0,00. Sesuaikan dengan aturan kampusmu.")

    edited_ips = st.data_editor(
        st.session_state.ips_rows,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mata kuliah": st.column_config.TextColumn("Mata kuliah", required=True),
            "Nilai huruf": st.column_config.SelectboxColumn(
                "Nilai huruf", options=list(GRADE_POINTS.keys()), required=True
            ),
            "SKS": st.column_config.NumberColumn("SKS", min_value=1, max_value=12, step=1, required=True),
        },
        key="ips_editor",
    )
    st.session_state.ips_rows = edited_ips

    valid_ips = edited_ips.dropna(subset=["Mata kuliah", "Nilai huruf", "SKS"]).copy()
    valid_ips = valid_ips[valid_ips["Mata kuliah"].astype(str).str.strip() != ""]
    if not valid_ips.empty:
        valid_ips["SKS"] = pd.to_numeric(valid_ips["SKS"], errors="coerce")
        valid_ips = valid_ips.dropna(subset=["SKS"])
        valid_ips = valid_ips[valid_ips["SKS"] > 0]
        valid_ips["Bobot nilai"] = valid_ips["Nilai huruf"].map(GRADE_POINTS)
        valid_ips["Nilai mutu"] = valid_ips["Bobot nilai"] * valid_ips["SKS"]
        total_sks = float(valid_ips["SKS"].sum())
        total_mutu = float(valid_ips["Nilai mutu"].sum())
        ips = total_mutu / total_sks if total_sks else 0.0

        c1, c2, c3 = st.columns(3)
        c1.metric("IPS", f"{ips:.2f}")
        c2.metric("Total SKS", f"{total_sks:g}")
        c3.metric("Total nilai mutu", f"{total_mutu:.2f}")
        with st.expander("Lihat rincian perhitungan"):
            st.dataframe(valid_ips[["Mata kuliah", "Nilai huruf", "SKS", "Bobot nilai", "Nilai mutu"]], use_container_width=True, hide_index=True)
            st.latex(r"\mathrm{IPS} = \frac{\sum(\mathrm{bobot\ nilai}\times\mathrm{SKS})}{\sum\mathrm{SKS}}")
            st.write(f"IPS = {total_mutu:.2f} ÷ {total_sks:g} = **{ips:.2f}**")
        csv = valid_ips.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Unduh rincian IPS (CSV)", csv, "rincian_ips.csv", "text/csv")
    else:
        st.warning("Tambahkan setidaknya satu mata kuliah dengan nilai dan SKS yang valid.")

with tab_ipk:
    st.subheader("Kalkulator IPK")
    st.write("Masukkan IPS dan total SKS dari setiap semester yang sudah ditempuh.")
    st.info("IPK dihitung dengan pembobotan SKS: jumlah (IPS semester × SKS semester) dibagi total SKS kumulatif.")

    edited_ipk = st.data_editor(
        st.session_state.ipk_rows,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Semester": st.column_config.TextColumn("Semester", required=True),
            "IPS": st.column_config.NumberColumn("IPS", min_value=0.0, max_value=4.0, step=0.01, format="%.2f", required=True),
            "Total SKS semester": st.column_config.NumberColumn("Total SKS semester", min_value=1, max_value=60, step=1, required=True),
        },
        key="ipk_editor",
    )
    st.session_state.ipk_rows = edited_ipk

    valid_ipk = edited_ipk.dropna(subset=["Semester", "IPS", "Total SKS semester"]).copy()
    valid_ipk = valid_ipk[valid_ipk["Semester"].astype(str).str.strip() != ""]
    valid_ipk["IPS"] = pd.to_numeric(valid_ipk["IPS"], errors="coerce")
    valid_ipk["Total SKS semester"] = pd.to_numeric(valid_ipk["Total SKS semester"], errors="coerce")
    valid_ipk = valid_ipk.dropna(subset=["IPS", "Total SKS semester"])
    valid_ipk = valid_ipk[
        (valid_ipk["IPS"] >= 0) & (valid_ipk["IPS"] <= 4) & (valid_ipk["Total SKS semester"] > 0)
    ]
    if not valid_ipk.empty:
        valid_ipk["Nilai mutu semester"] = valid_ipk["IPS"] * valid_ipk["Total SKS semester"]
        total_sks_ipk = float(valid_ipk["Total SKS semester"].sum())
        total_mutu_ipk = float(valid_ipk["Nilai mutu semester"].sum())
        ipk = total_mutu_ipk / total_sks_ipk if total_sks_ipk else 0.0
        c1, c2, c3 = st.columns(3)
        c1.metric("IPK kumulatif", f"{ipk:.2f}")
        c2.metric("Total SKS", f"{total_sks_ipk:g}")
        c3.metric("Total nilai mutu", f"{total_mutu_ipk:.2f}")
        with st.expander("Lihat rincian perhitungan"):
            st.dataframe(valid_ipk, use_container_width=True, hide_index=True)
            st.latex(r"\mathrm{IPK} = \frac{\sum(\mathrm{IPS\ semester}\times\mathrm{SKS\ semester})}{\sum\mathrm{SKS}}")
            st.write(f"IPK = {total_mutu_ipk:.2f} ÷ {total_sks_ipk:g} = **{ipk:.2f}**")
        st.download_button("⬇️ Unduh riwayat IPK (CSV)", valid_ipk.to_csv(index=False).encode("utf-8"), "riwayat_ipk.csv", "text/csv")
    else:
        st.warning("Masukkan setidaknya satu semester dengan IPS 0–4 dan total SKS lebih dari 0.")

with tab_final:
    st.subheader("Kalkulator Nilai Akhir")
    st.write("Masukkan nilai tiap komponen dan bobotnya. Total bobot harus 100%.")
    st.caption("Gunakan bobot sesuai RPS atau ketentuan dosen. Nilai komponen menggunakan skala 0–100.")

    default_components = pd.DataFrame({
        "Komponen": ["Tugas", "Kuis", "UTS", "UAS"],
        "Nilai (0–100)": [85.0, 80.0, 78.0, 90.0],
        "Bobot (%)": [20.0, 10.0, 30.0, 40.0],
    })
    components = st.data_editor(
        default_components,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Komponen": st.column_config.TextColumn("Komponen", required=True),
            "Nilai (0–100)": st.column_config.NumberColumn("Nilai (0–100)", min_value=0.0, max_value=100.0, step=1.0, format="%.2f", required=True),
            "Bobot (%)": st.column_config.NumberColumn("Bobot (%)", min_value=0.0, max_value=100.0, step=1.0, format="%.2f", required=True),
        },
        key="final_editor",
    )

    valid_final = components.dropna(subset=["Komponen", "Nilai (0–100)", "Bobot (%)"]).copy()
    valid_final = valid_final[valid_final["Komponen"].astype(str).str.strip() != ""]
    valid_final["Nilai (0–100)"] = pd.to_numeric(valid_final["Nilai (0–100)"], errors="coerce")
    valid_final["Bobot (%)"] = pd.to_numeric(valid_final["Bobot (%)"], errors="coerce")
    valid_final = valid_final.dropna(subset=["Nilai (0–100)", "Bobot (%)"])
    valid_final = valid_final[
        (valid_final["Nilai (0–100)"] >= 0) & (valid_final["Nilai (0–100)"] <= 100) &
        (valid_final["Bobot (%)"] >= 0) & (valid_final["Bobot (%)"] <= 100)
    ]
    total_weight = float(valid_final["Bobot (%)"].sum()) if not valid_final.empty else 0.0
    weighted_sum = float((valid_final["Nilai (0–100)"] * valid_final["Bobot (%)"] / 100).sum()) if not valid_final.empty else 0.0

    c1, c2 = st.columns(2)
    c1.metric("Total bobot", f"{total_weight:.2f}%")
    if abs(total_weight - 100.0) < 0.001 and not valid_final.empty:
        final_grade = weighted_sum
        c2.metric("Nilai akhir", f"{final_grade:.2f} / 100")
        if final_grade >= 85:
            letter = "A"
        elif final_grade >= 80:
            letter = "AB"
        elif final_grade >= 70:
            letter = "B"
        elif final_grade >= 65:
            letter = "BC"
        elif final_grade >= 60:
            letter = "C"
        elif final_grade >= 50:
            letter = "D"
        else:
            letter = "E"
        st.success(f"Nilai akhir: **{final_grade:.2f}**. Perkiraan nilai huruf berdasarkan contoh skala bawaan: **{letter}**.")
        st.caption("Batas nilai huruf di atas hanya contoh dan tidak mewakili semua perguruan tinggi. Sesuaikan dengan aturan kampus.")
        with st.expander("Lihat rincian perhitungan"):
            valid_final["Kontribusi nilai"] = valid_final["Nilai (0–100)"] * valid_final["Bobot (%)"] / 100
            st.dataframe(valid_final, use_container_width=True, hide_index=True)
            st.write("Nilai akhir = jumlah (nilai komponen × bobot komponen ÷ 100).")
            st.write(f"Nilai akhir = **{final_grade:.2f}**")
        st.download_button("⬇️ Unduh rincian nilai akhir (CSV)", valid_final.to_csv(index=False).encode("utf-8"), "rincian_nilai_akhir.csv", "text/csv")
    else:
        c2.metric("Nilai akhir", "—")
        st.warning("Pastikan total bobot seluruh komponen tepat 100% agar nilai akhir dapat dihitung.")

with tab_info:
    st.subheader("Panduan penggunaan")
    st.markdown(
        """
        **1. IPS (Indeks Prestasi Semester)**  
        Pilih nilai huruf dan SKS setiap mata kuliah. Aplikasi mengubah nilai huruf menjadi bobot angka, kemudian menghitung rata-rata berbobot SKS.

        **2. IPK (Indeks Prestasi Kumulatif)**  
        Masukkan IPS dan total SKS setiap semester. IPK dihitung sebagai rata-rata IPS yang dibobot dengan SKS semester.

        **3. Nilai akhir mata kuliah**  
        Masukkan nilai komponen dan bobot sesuai RPS. Total bobot harus 100%.

        **Catatan penting**
        - Skala nilai huruf dan batas kelulusan dapat berbeda antaruniversitas atau program studi.
        - Untuk perhitungan resmi, gunakan aturan akademik kampus masing-masing.
        - Aplikasi ini tidak meminta nama, NIM, kata sandi, atau data pribadi.
        - Data input tidak disimpan ke database. Unduh CSV jika ingin menyimpan salinan.
        """
    )
    st.markdown("### Rumus utama")
    st.latex(r"\mathrm{IPS}=\frac{\sum(\mathrm{bobot\ nilai}\times\mathrm{SKS})}{\sum\mathrm{SKS}}")
    st.latex(r"\mathrm{IPK}=\frac{\sum(\mathrm{IPS\ semester}\times\mathrm{SKS\ semester})}{\sum\mathrm{SKS}}")
    st.latex(r"\mathrm{Nilai\ akhir}=\sum(\mathrm{nilai\ komponen}\times\mathrm{bobot\ komponen})")
    st.caption("Academic Calculator • Dibuat dengan Python dan Streamlit")
