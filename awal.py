import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk hitung biaya
def hitung_biaya(jumlah_stasiun):
    scanner = jumlah_stasiun * 10 * 1000          # 10 unit scanner/stasiun, $1000/unit
    software = 500000 if jumlah_stasiun >= 100 else 50000
    integrasi = 250000 if jumlah_stasiun >= 100 else 25000
    server = 200000 if jumlah_stasiun >= 100 else 15000
    total = scanner + software + integrasi + server
    return {
        "Scanner": scanner,
        "Software & Lisensi": software,
        "Integrasi & Training": integrasi,
        "Server": server,
        "Total": total
    }

# UI Streamlit
st.title("💳 Dashboard Estimasi Biaya Palm Recognition KAI")

st.sidebar.header("Pengaturan")
jumlah_stasiun = st.sidebar.slider("Pilih Jumlah Stasiun", 1, 300, 100)

# Hitung biaya
biaya = hitung_biaya(jumlah_stasiun)
biaya_idr = {k: v*17000 for k, v in biaya.items()}  # konversi ke Rupiah (kurs 17.000)

# Tampilkan tabel
st.subheader(f"Estimasi Biaya untuk {jumlah_stasiun} Stasiun")
df = pd.DataFrame({
    "Komponen": list(biaya.keys()),
    "Biaya (USD)": list(biaya.values()),
    "Biaya (IDR)": [f"Rp {x:,.0f}" for x in biaya_idr.values()]
})
st.dataframe(df)

# Pie Chart proporsi biaya
st.subheader("Proporsi Biaya (USD)")
fig1, ax1 = plt.subplots()
ax1.pie(
    [biaya["Scanner"], biaya["Software & Lisensi"], biaya["Integrasi & Training"], biaya["Server"]],
    labels=["Scanner", "Software & Lisensi", "Integrasi", "Server"],
    autopct='%1.1f%%',
    startangle=90
)
ax1.axis("equal")
st.pyplot(fig1)

# Line Chart simulasi scaling
st.subheader("Simulasi Scaling Biaya (USD)")
st.caption("Perbandingan biaya total untuk jumlah stasiun berbeda")

jumlah_list = [50, 100, 150, 200, 250, 300]
biaya_scaling = [hitung_biaya(j)["Total"] for j in jumlah_list]

fig2, ax2 = plt.subplots()
ax2.plot(jumlah_list, biaya_scaling, marker="o")
ax2.set_xlabel("Jumlah Stasiun")
ax2.set_ylabel("Total Biaya (USD)")
ax2.set_title("Pertumbuhan Biaya terhadap Jumlah Stasiun")
st.pyplot(fig2)

# Maintenance tahunan
st.subheader("Biaya Maintenance Tahunan")
maintenance_usd = biaya["Total"] * 0.1
maintenance_idr = maintenance_usd * 17000
st.info(f"Perkiraan biaya maintenance tahunan: **USD {maintenance_usd:,.0f} (~Rp {maintenance_idr:,.0f})**")

