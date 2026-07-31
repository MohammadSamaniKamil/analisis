"""
Estimasi Harga Rumah Kecamatan Cidahu
Aplikasi untuk pengguna umum — sederhana, modern, dan mudah dipahami.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ─────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────
st.set_page_config(
    page_title="Estimasi Harga Rumah Cidahu",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────
# CUSTOM CSS — tampilan modern & bersih
# ─────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sembunyikan menu dan footer default Streamlit, tapi biarkan header (tombol sidebar) */
    #MainMenu, footer { visibility: hidden; }

    /* Background utama */
    .main { background-color: #F8F9FA; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] * { color: #E8E8E8 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #E8E8E8 !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }

    /* Card umum */
    .card {
        background: white;
        border-radius: 16px;
        padding: 28px 32px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    /* Card hero (judul halaman) */
    .hero-card {
        background: linear-gradient(135deg, #0f4c75 0%, #1b6ca8 100%);
        border-radius: 20px;
        padding: 36px 32px;
        margin-bottom: 24px;
        color: white;
        text-align: center;
    }
    .hero-icon { font-size: 48px; margin-bottom: 12px; }
    .hero-title {
        font-size: 26px;
        font-weight: 700;
        color: white;
        margin: 0 0 8px 0;
        line-height: 1.3;
    }
    .hero-sub {
        font-size: 15px;
        color: rgba(255,255,255,0.82);
        margin: 0;
        line-height: 1.6;
    }

    /* Section label */
    .section-label {
        font-size: 13px;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 16px;
    }

    /* Card input */
    .input-card-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 4px 0;
    }
    .input-card-sub {
        font-size: 14px;
        color: #6B7280;
        margin: 0 0 24px 0;
    }

    /* Divider tipis */
    .thin-divider {
        border: none;
        border-top: 1px solid #F3F4F6;
        margin: 20px 0;
    }

    /* Tombol estimasi */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0f4c75 0%, #1b6ca8 100%);
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 14px 24px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(15,76,117,0.3);
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(15,76,117,0.4);
    }
    .stButton > button:active { transform: translateY(0); }

    /* Card hasil prediksi */
    .result-card {
        background: linear-gradient(135deg, #f0f9f4 0%, #e8f5f0 100%);
        border: 1.5px solid #6FCF97;
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        margin: 24px 0 20px 0;
    }
    .result-label {
        font-size: 14px;
        font-weight: 500;
        color: #27AE60;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0 0 8px 0;
    }
    .result-harga {
        font-size: 36px;
        font-weight: 700;
        color: #1a5c35;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .result-range {
        font-size: 13px;
        color: #6B9E80;
        margin: 0;
    }

    /* Badge status harga */
    .badge-murah {
        display: inline-block;
        background: #ECFDF5;
        color: #065F46;
        border: 1px solid #6EE7B7;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 12px;
    }
    .badge-menengah {
        display: inline-block;
        background: #FFFBEB;
        color: #92400E;
        border: 1px solid #FCD34D;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 12px;
    }
    .badge-tinggi {
        display: inline-block;
        background: #FFF5F5;
        color: #9B1C1C;
        border: 1px solid #FCA5A5;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 12px;
    }

    /* Perbandingan harga */
    .compare-card {
        background: white;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
    .compare-label {
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 10px;
    }
    .compare-values {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 13px;
    }
    .compare-you { color: #1b6ca8; font-weight: 600; }
    .compare-avg { color: #6B7280; }

    /* Info box */
    .info-box {
        background: #F0F9FF;
        border-left: 3px solid #38BDF8;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 16px 0;
        font-size: 14px;
        color: #0C4A6E;
        line-height: 1.6;
    }

    /* Disclaimer */
    .disclaimer {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 13px;
        color: #92400E;
        line-height: 1.6;
        margin-top: 16px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 24px 0 8px;
        color: #9CA3AF;
        font-size: 13px;
        line-height: 1.8;
    }

    /* Input field styling */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 1.5px solid #E5E7EB;
        font-size: 15px;
        padding: 10px 14px;
        transition: border-color 0.2s;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #1b6ca8;
        box-shadow: 0 0 0 3px rgba(27,108,168,0.1);
    }

    /* Label input */
    .stNumberInput label, .stSelectbox label {
        font-size: 14px;
        font-weight: 500;
        color: #374151;
    }

    /* Tentang halaman */
    .about-section {
        background: white;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .about-title {
        font-size: 17px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 10px 0;
    }
    .about-body {
        font-size: 14px;
        color: #4B5563;
        line-height: 1.75;
        margin: 0;
    }

    /* Fitur highlight */
    .fitur-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #F9FAFB;
        font-size: 14px;
        color: #374151;
    }
    .fitur-row:last-child { border-bottom: none; }
    .fitur-icon { font-size: 20px; width: 32px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """Muat model Random Forest (model terbaik hasil penelitian)."""
    base = os.path.dirname(os.path.abspath(__file__))
    try:
        model = joblib.load(os.path.join(base, "model_rfr.pkl"))
        return model, True
    except Exception:
        return None, False


@st.cache_data(show_spinner=False)
def load_metadata():
    """Muat statistik dataset untuk perbandingan harga pasar."""
    base = os.path.dirname(os.path.abspath(__file__))
    try:
        df = pd.read_csv(os.path.join(base, "dataset_clean.csv"))
        return {
            "mean":   float(df["harga_jual"].mean()),
            "median": float(df["harga_jual"].median()),
            "min":    float(df["harga_jual"].min()),
            "max":    float(df["harga_jual"].max()),
            "q1":     float(df["harga_jual"].quantile(0.25)),
            "q3":     float(df["harga_jual"].quantile(0.75)),
            "n":      len(df),
        }
    except Exception:
        return {
            "mean": 554_532_609, "median": 355_000_000,
            "min": 35_000_000,   "max": 1_800_000_000,
            "q1": 166_000_000,   "q3": 750_000_000, "n": 46,
        }


# ─────────────────────────────────────
# FUNGSI PREDIKSI
# ─────────────────────────────────────
FITUR = ["jumlah_kamar_tidur", "jumlah_kamar_mandi", "luas_tanah", "luas_bangunan"]
MARGIN_TETAP = 413_399_134   # 1.96 × RMSE latih (dihitung dari notebook)


def predict_price(model, kt: int, km: int, lt: float, lb: float) -> dict:
    """
    Prediksi harga menggunakan model RFR terbaik.
    Input di-log1p → prediksi → expm1 kembali ke Rupiah.
    Mengembalikan dict berisi harga prediksi dan rentang estimasi.
    """
    X = pd.DataFrame(
        [[kt, km, lt, lb]],
        columns=FITUR
    )
    pred_log = model.predict(X)[0]
    pred_rp  = float(np.expm1(pred_log))
    bawah    = max(0.0, pred_rp - MARGIN_TETAP)
    atas     = pred_rp + MARGIN_TETAP

    return {
        "harga":  pred_rp,
        "bawah":  bawah,
        "atas":   atas,
        "margin": MARGIN_TETAP,
    }


# ─────────────────────────────────────
# FORMAT RUPIAH
# ─────────────────────────────────────
def format_rupiah(angka: float, singkat: bool = False) -> str:
    """Format angka ke format mata uang Rupiah Indonesia."""
    if singkat:
        if angka >= 1_000_000_000:
            return f"Rp {angka / 1_000_000_000:.2f} M"
        if angka >= 1_000_000:
            return f"Rp {angka / 1_000_000:.0f} Jt"
        return f"Rp {angka:,.0f}"
    # Format lengkap
    return "Rp {:,.0f}".format(angka).replace(",", ".")


# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────
def render_sidebar() -> str:
    """Render sidebar dan kembalikan nama halaman aktif."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 24px 0 20px;">
            <div style="font-size:44px; margin-bottom:8px;">🏠</div>
            <div style="font-size:17px; font-weight:700; color:white; line-height:1.4;">
                Estimasi Harga<br>Rumah Cidahu
            </div>
            <div style="font-size:12px; color:rgba(255,255,255,0.5); margin-top:6px;">
                Kecamatan Cidahu, Sukabumi
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:0 0 20px'>",
                    unsafe_allow_html=True)

        halaman = st.radio(
            "Menu",
            ["🏡  Estimasi Harga", "ℹ️  Tentang Aplikasi"],
            label_visibility="collapsed",
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

    return halaman


# ─────────────────────────────────────
# HALAMAN ESTIMASI HARGA
# ─────────────────────────────────────
def show_home(model, meta: dict):
    """Halaman utama: form input dan hasil prediksi."""

    # ── Hero ──────────────────────────────
    st.markdown("""
    <div class="hero-card">
        <div class="hero-icon">🏠</div>
        <p class="hero-title">Estimasi Harga Rumah<br>Kecamatan Cidahu</p>
        <p class="hero-sub">
            Masukkan spesifikasi rumah untuk mendapatkan<br>
            perkiraan harga penawaran secara instan.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Card Input ────────────────────────
    with st.container():
        st.markdown('<p class="input-card-title">Spesifikasi Rumah</p>', unsafe_allow_html=True)

        # Baris 1: Luas Tanah & Luas Bangunan
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            lt = st.number_input(
                "📐 Luas Tanah (m²)",
                min_value=0,
                max_value=9999,
                value=None,
                placeholder="Contoh: 120",
                step=1,
                help="Luas tanah dalam meter persegi"
            )
        with col2:
            lb = st.number_input(
                "🏗️ Luas Bangunan (m²)",
                min_value=0,
                max_value=9999,
                value=None,
                placeholder="Contoh: 90",
                step=1,
                help="Luas bangunan dalam meter persegi"
            )

        # Baris 2: Kamar Tidur & Kamar Mandi
        col3, col4 = st.columns(2, gap="medium")
        with col3:
            kt = st.number_input(
                "🛏️ Jumlah Kamar Tidur",
                min_value=0,
                max_value=20,
                value=None,
                placeholder="Contoh: 3",
                step=1,
                help="Jumlah kamar tidur"
            )
        with col4:
            km = st.number_input(
                "🚿 Jumlah Kamar Mandi",
                min_value=0,
                max_value=10,
                value=None,
                placeholder="Contoh: 2",
                step=1,
                help="Jumlah kamar mandi"
            )

        st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

        # Tombol estimasi
        tombol = st.button("🔍  Estimasi Harga Sekarang", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Validasi & Prediksi ───────────────
    if tombol:
        # Validasi: semua harus diisi
        if any(v is None for v in [lt, lb, kt, km]):
            st.warning("⚠️ Mohon isi semua kolom spesifikasi rumah terlebih dahulu.")
            return

        # Validasi: nilai harus positif
        if lt <= 0 or lb <= 0 or kt <= 0 or km <= 0:
            st.error("❌ Semua nilai harus lebih dari 0. Periksa kembali input Anda.")
            return

        # Validasi logis: luas bangunan tidak boleh melebihi luas tanah
        if lb > lt:
            st.warning("⚠️ Luas bangunan tidak boleh lebih besar dari luas tanah.")
            return

        # Proses prediksi
        with st.spinner("⏳ Sedang menghitung estimasi harga..."):
            import time
            time.sleep(0.8)   # animasi singkat agar terasa proses
            hasil = predict_price(model, int(kt), int(km), float(lt), float(lb))

        harga   = hasil["harga"]
        bawah   = hasil["bawah"]
        atas    = hasil["atas"]

        # ── Card Hasil ────────────────────
        st.markdown(f"""
        <div class="result-card">
            <p class="result-label">💰 Estimasi Harga Rumah</p>
            <p class="result-harga">{format_rupiah(harga)}</p>
            <p class="result-range">
                Perkiraan kisaran: {format_rupiah(bawah, singkat=True)} — {format_rupiah(atas, singkat=True)}
            </p>
            {_badge_harga(harga, meta)}
        </div>
        """, unsafe_allow_html=True)

        # ── Perbandingan dengan Pasar ──────
        _show_perbandingan(harga, meta)


        # ── Disclaimer ────────────────────
        st.markdown("""
        <div class="disclaimer">
            ⚠️ <strong>Catatan Penting:</strong>
            Hasil estimasi merupakan perkiraan berdasarkan data harga penawaran rumah
            di Kecamatan Cidahu, harga aktual dapat berbeda 
            tergantung kondisi fisik, lokasi spesifik, dan negosiasi.
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────
    _render_footer()


def _badge_harga(harga: float, meta: dict) -> str:
    """Kembalikan HTML badge berdasarkan posisi harga vs pasar."""
    q1, q3 = meta["q1"], meta["q3"]
    if harga < q1:
        return '<span class="badge-murah">✅ Di bawah rata-rata pasar</span>'
    elif harga <= q3:
        return '<span class="badge-menengah">🟡 Harga menengah pasar</span>'
    else:
        return '<span class="badge-tinggi">🔴 Di atas rata-rata pasar</span>'


def _show_perbandingan(harga: float, meta: dict):
    """Tampilkan perbandingan harga estimasi vs rata-rata pasar dengan progress bar."""
    rata_rata = meta["mean"]
    harga_max = meta["max"]

    # Hitung posisi dalam skala 0–100%
    pct_kamu = min(100, int(harga / harga_max * 100))
    pct_rata = min(100, int(rata_rata / harga_max * 100))

    st.markdown("""
    <div class="compare-card">
        <p class="compare-label">📊 Posisi harga estimasi vs rata-rata pasar Kecamatan Cidahu</p>
        <div class="compare-values">
            <span class="compare-you">🏠 Estimasi Anda</span>
            <span class="compare-you">""" + format_rupiah(harga, singkat=True) + """</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("**🏠 Estimasi Anda**")
        st.progress(pct_kamu / 100)
        st.markdown("**📈 Rata-rata Pasar**")
        st.progress(pct_rata / 100)
    with col_b:
        st.markdown(f"<br><strong style='color:#1b6ca8'>{format_rupiah(harga, singkat=True)}</strong>",
                    unsafe_allow_html=True)
        st.markdown(f"<strong style='color:#6B7280'>{format_rupiah(rata_rata, singkat=True)}</strong>",
                    unsafe_allow_html=True)

    # Kalimat perbandingan
    selisih = harga - rata_rata
    if selisih > 0:
        kalimat = f"Estimasi harga **{format_rupiah(abs(selisih), singkat=True)} lebih tinggi** dari rata-rata pasar."
    elif selisih < 0:
        kalimat = f"Estimasi harga **{format_rupiah(abs(selisih), singkat=True)} lebih rendah** dari rata-rata pasar."
    else:
        kalimat = "Estimasi harga **sama dengan** rata-rata pasar."

    st.caption(kalimat)


# ─────────────────────────────────────
# HALAMAN TENTANG APLIKASI
# ─────────────────────────────────────
def show_about():
    """Halaman tentang aplikasi."""

    st.markdown("""
    <div class="hero-card">
        <div class="hero-icon">ℹ️</div>
        <p class="hero-title">Tentang Aplikasi</p>
        <p class="hero-sub">Pelajari bagaimana aplikasi ini bekerja</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Apa itu aplikasi ini ──────────────
    st.markdown("""
    <div class="about-section">
        <p class="about-title">🏠 Apa itu aplikasi ini?</p>
        <p class="about-body">
            Aplikasi <strong>Estimasi Harga Rumah Kecamatan Cidahu</strong> membantu Anda
            memperkirakan harga penawaran rumah di Kecamatan Cidahu, Kabupaten Sukabumi
            berdasarkan spesifikasi properti yang Anda masukkan.
            <br><br>
            Cukup masukkan luas tanah, luas bangunan, jumlah kamar tidur, dan jumlah kamar mandi —
            aplikasi akan langsung memberikan estimasi harga dalam hitungan detik.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # ── Cara kerja ────────────────────────
    st.markdown("""
    <div class="about-section">
        <p class="about-title">⚙️ Bagaimana Cara Kerjanya?</p>
        <p class="about-body">
            Aplikasi menggunakan model <strong>Machine Learning</strong> terbaik hasil penelitian
            untuk memprediksi harga berdasarkan 4 faktor utama:
        </p>
    </div>
    """, unsafe_allow_html=True)

    fitur_info = [
        ("📐", "Luas Tanah", "Semakin luas tanah, semakin tinggi nilai properti"),
        ("🏗️", "Luas Bangunan", "Ukuran fisik bangunan yang berdiri di atas tanah"),
        ("🛏️", "Kamar Tidur", "Jumlah kamar tidur yang tersedia"),
        ("🚿", "Kamar Mandi", "Jumlah kamar mandi yang tersedia"),
    ]
    for icon, nama, deskripsi in fitur_info:
        st.markdown(f"""
        <div class="fitur-row">
            <span class="fitur-icon">{icon}</span>
            <div>
                <strong style="font-size:14px;color:#111827">{nama}</strong><br>
                <span style="font-size:13px;color:#6B7280">{deskripsi}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tujuan aplikasi ───────────────────
    st.markdown("""
    <div class="about-section">
        <p class="about-title">🎯 Tujuan Aplikasi</p>
        <p class="about-body">
            Aplikasi ini ditujukan sebagai <strong>alat bantu referensi awal</strong> bagi:
            <br><br>
            • Calon pembeli rumah yang ingin mengetahui kisaran harga wajar<br>
            • Pemilik properti yang ingin menetapkan harga penawaran<br>
            • Masyarakat umum yang membutuhkan informasi harga properti di Kecamatan Cidahu
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Disclaimer:</strong>
        Hasil estimasi merupakan perkiraan berdasarkan data penelitian dalam transaksi properti.
        Harga aktual dipengaruhi oleh kondisi fisik bangunan, lokasi spesifik,
        kondisi pasar, dan kesepakatan antara penjual dan pembeli.
    </div>
    """, unsafe_allow_html=True)

    _render_footer()


# ─────────────────────────────────────
# FOOTER
# ─────────────────────────────────────
def _render_footer():
    st.markdown("""
    <div class="footer">
        Estimasi Harga Rumah Kecamatan Cidahu<br>
        <span style="color:#D1D5DB">Powered by</span>
        <strong style="color:#6B7280"> Streamlit</strong>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────
def main():
    inject_css()

    model, ok = load_model()
    meta      = load_metadata()
    halaman   = render_sidebar()

    if not ok:
        st.error("⚠️ Model tidak ditemukan. Pastikan file `model_rfr.pkl` tersedia di folder yang sama.")
        return

    if "Estimasi" in halaman:
        show_home(model, meta)
    else:
        show_about()


if __name__ == "__main__":
    main()
