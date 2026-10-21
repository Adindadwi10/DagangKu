import email

from flask import Flask, request, redirect, url_for, render_template_string, session
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_mydagang'

database_user = {}

DEFAULT_AKUN = [
    {"kode": "1-1100", "nama": "Kas", "level": "Akun biasa", "tipe": "Bank (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": True, "aktif": True},
    {"kode": "1-1110", "nama": "Kas Kecil", "level": "Akun biasa", "tipe": "Bank (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-1200", "nama": "Bank", "level": "Akun biasa", "tipe": "Bank (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-1300", "nama": "Piutang Usaha", "level": "Akun biasa", "tipe": "Piutang (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": True, "aktif": True},
    {"kode": "1-1400", "nama": "Persediaan Barang Dagang", "level": "Akun biasa", "tipe": "Persediaan (kontrol) (Debit) — khusus akun sistem", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": True, "aktif": True},
    {"kode": "1-1600", "nama": "Perlengkapan", "level": "Akun biasa", "tipe": "Aset Lancar Lainnya (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-1700", "nama": "Sewa Dibayar Dimuka", "level": "Akun biasa", "tipe": "Aset Lancar Lainnya (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-1800", "nama": "Asuransi Dibayar Dimuka", "level": "Akun biasa", "tipe": "Aset Lancar Lainnya (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2100", "nama": "Tanah", "level": "Akun biasa", "tipe": "Aset Tetap (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2200", "nama": "Gedung", "level": "Akun biasa", "tipe": "Aset Tetap (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2210", "nama": "Akumulasi Penyusutan Gedung", "level": "Akun biasa", "tipe": "Akumulasi Penyusutan (Kredit)", "dk": "K", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2300", "nama": "Kendaraan", "level": "Akun biasa", "tipe": "Aset Tetap (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2310", "nama": "Akumulasi Penyusutan Kendaraan", "level": "Akun biasa", "tipe": "Akumulasi Penyusutan (Kredit)", "dk": "K", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2400", "nama": "Peralatan Toko", "level": "Akun biasa", "tipe": "Aset Tetap (Debit)", "dk": "D", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    {"kode": "1-2410", "nama": "Akumulasi Penyusutan Peralatan", "level": "Akun biasa", "tipe": "Akumulasi Penyusutan (Kredit)", "dk": "K", "saldo": "-", "kategori": "1 — Aset", "sistem": False, "aktif": True},
    
    {"kode": "2-1100", "nama": "Utang Usaha", "level": "Akun biasa", "tipe": "Utang Dagang (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": True, "aktif": True},
    {"kode": "2-1200", "nama": "PPN Keluaran", "level": "Akun biasa", "tipe": "PPN Keluaran (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": True, "aktif": True},
    {"kode": "2-1300", "nama": "Utang Gaji", "level": "Akun biasa", "tipe": "Utang Jangka Pendek Lainnya (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": False, "aktif": True},
    {"kode": "2-1400", "nama": "Utang Pajak Penghasilan", "level": "Akun biasa", "tipe": "Utang Jangka Pendek Lainnya (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": False, "aktif": True},
    {"kode": "2-1500", "nama": "PPN Masukan", "level": "Akun biasa", "tipe": "PPN Masukan (Debit)", "dk": "D", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": True, "aktif": True},
    {"kode": "2-1600", "nama": "Utang Dividen", "level": "Akun biasa", "tipe": "Utang Jangka Pendek Lainnya (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": False, "aktif": True},
    {"kode": "2-2100", "nama": "Utang Bank Jangka Panjang", "level": "Akun biasa", "tipe": "Utang Jangka Panjang (Kredit)", "dk": "K", "saldo": "-", "kategori": "2 — Liabilitas", "sistem": False, "aktif": True},

    {"kode": "3-1100", "nama": "Modal Saham", "level": "Akun biasa", "tipe": "Modal (Kredit)", "dk": "K", "saldo": "-", "kategori": "3 — Ekuitas", "sistem": True, "aktif": True},
    {"kode": "3-1200", "nama": "Tambahan Modal Disetor", "level": "Akun biasa", "tipe": "Modal (Kredit)", "dk": "K", "saldo": "-", "kategori": "3 — Ekuitas", "sistem": False, "aktif": True},
    {"kode": "3-2100", "nama": "Laba Ditahan", "level": "Akun biasa", "tipe": "Laba Ditahan (Kredit)", "dk": "K", "saldo": "-", "kategori": "3 — Ekuitas", "sistem": True, "aktif": True},
    {"kode": "3-3100", "nama": "Dividen", "level": "Akun biasa", "tipe": "Dividen / Prive (Debit)", "dk": "D", "saldo": "-", "kategori": "3 — Ekuitas", "sistem": True, "aktif": True},
    {"kode": "3-9999", "nama": "Historical Balancing", "level": "Akun biasa", "tipe": "Historical Balancing", "dk": "D/K", "saldo": "-", "kategori": "3 — Ekuitas", "sistem": True, "aktif": True},

    {"kode": "4-1100", "nama": "Penjualan", "level": "Akun biasa", "tipe": "Penjualan (Kredit)", "dk": "K", "saldo": "-", "kategori": "4 — Pendapatan", "sistem": True, "aktif": True},
    {"kode": "4-1200", "nama": "Retur Penjualan", "level": "Akun biasa", "tipe": "Retur Penjualan (Debit)", "dk": "D", "saldo": "-", "kategori": "4 — Pendapatan", "sistem": True, "aktif": True},
    {"kode": "4-1300", "nama": "Potongan Penjualan", "level": "Akun biasa", "tipe": "Potongan Penjualan (Debit)", "dk": "D", "saldo": "-", "kategori": "4 — Pendapatan", "sistem": True, "aktif": True},
    {"kode": "4-1400", "nama": "Beban Angkut Penjualan", "level": "Akun biasa", "tipe": "Beban Angkut Penjualan (Debit)", "dk": "D", "saldo": "-", "kategori": "4 — Pendapatan", "sistem": True, "aktif": True},

    {"kode": "5-1100", "nama": "Harga Pokok Penjualan", "level": "Akun biasa", "tipe": "Harga Pokok Penjualan (Debit)", "dk": "D", "saldo": "-", "kategori": "5 — Harga Pokok Penjualan", "sistem": True, "aktif": True},
    {"kode": "5-1200", "nama": "Potongan Pembelian", "level": "Akun biasa", "tipe": "Potongan Pembelian (Kredit)", "dk": "K", "saldo": "-", "kategori": "5 — Harga Pokok Penjualan", "sistem": False, "aktif": False},
    {"kode": "5-1300", "nama": "Beban Angkut Pembelian", "level": "Akun biasa", "tipe": "Beban Angkut Pembelian (Debit)", "dk": "D", "saldo": "-", "kategori": "5 — Harga Pokok Penjualan", "sistem": True, "aktif": True},

    {"kode": "6-1100", "nama": "Beban Gaji", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1200", "nama": "Beban Sewa", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1300", "nama": "Beban Listrik, Air & Telepon", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1400", "nama": "Beban Perlengkapan", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1500", "nama": "Beban Penyusutan", "level": "Akun biasa", "tipe": "Beban Penyusutan (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1600", "nama": "Beban Pengiriman", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1700", "nama": "Beban Asuransi", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1800", "nama": "Beban Iklan & Promosi", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-1900", "nama": "Beban Operasional Lain-lain", "level": "Akun biasa", "tipe": "Beban Operasional (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},
    {"kode": "6-2000", "nama": "Beban Pajak Penghasilan", "level": "Akun biasa", "tipe": "Beban Pajak Penghasilan (Debit)", "dk": "D", "saldo": "-", "kategori": "6 — Beban Operasional", "sistem": False, "aktif": True},

    {"kode": "8-1100", "nama": "Pendapatan Bunga", "level": "Akun biasa", "tipe": "Pendapatan Lain-Lain (Kredit)", "dk": "K", "saldo": "-", "kategori": "8 — Pendapatan Lain-Lain", "sistem": False, "aktif": True},
    {"kode": "8-1200", "nama": "Pendapatan Lain-lain", "level": "Akun biasa", "tipe": "Pendapatan Lain-Lain (Kredit)", "dk": "K", "saldo": "-", "kategori": "8 — Pendapatan Lain-Lain", "sistem": False, "aktif": True},

    {"kode": "9-1100", "nama": "Beban Bunga", "level": "Akun biasa", "tipe": "Beban Lain-Lain (Debit)", "dk": "D", "saldo": "-", "kategori": "9 — Beban Lain-Lain", "sistem": False, "aktif": True},
    {"kode": "9-1200", "nama": "Beban Administrasi Bank", "level": "Akun biasa", "tipe": "Beban Lain-Lain (Debit)", "dk": "D", "saldo": "-", "kategori": "9 — Beban Lain-Lain", "sistem": False, "aktif": True},
    {"kode": "9-1300", "nama": "Beban Lain-lain", "level": "Akun biasa", "tipe": "Beban Lain-Lain (Debit)", "dk": "D", "saldo": "-", "kategori": "9 — Beban Lain-Lain", "sistem": False, "aktif": True},
]

def format_tanggal_indo(tanggal_str):
    try:
        parts = tanggal_str.split('-')
        if len(parts) == 3:
            tahun, bulan, hari = parts
            bulan_dict = {
                '01': 'Januari', '02': 'Februari', '03': 'Maret', '04': 'April',
                '05': 'Mei', '06': 'Juni', '07': 'Juli', '08': 'Agustus',
                '09': 'September', '10': 'Oktober', '11': 'November', '12': 'Desember'
            }
            nama_bulan = bulan_dict.get(bulan, 'Januari')
            return f"{int(hari)} {nama_bulan} {tahun}"
    except Exception:
        pass
    return "1 Januari 2026"

def format_tanggal_pendek_indo(tanggal_str):
    try:
        dt = datetime.strptime(tanggal_str, '%Y-%m-%d')
        bulan_dict = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
            7: 'Jul', 8: 'Agt', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
        }
        return f"{dt.day:02d} {bulan_dict[dt.month]} {dt.year}"
    except Exception:
        pass
    return tanggal_str

def sync_saldo_awal_penjualan(email):
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    tanggal_saldo = user_data.get('tanggal_saldo', '2026-01-01')
    
    try:
        dt_saldo = datetime.strptime(tanggal_saldo, '%Y-%m-%d')
        dt_jatuh_tempo = dt_saldo + timedelta(days=30)
        str_jatuh_tempo = dt_jatuh_tempo.strftime('%Y-%m-%d')
    except Exception:
        str_jatuh_tempo = tanggal_saldo

    penjualan_list = user_data.get('penjualan', [])
    penjualan_list = [p for p in penjualan_list if not p.get('is_saldo_awal', False)]

    for p in list_pelanggan:
        try:
            val = int(p.get('saldo_awal_piutang', 0) or 0)
            if val > 0:
                kode_plg = p.get('kode')
                formatted_val = f"{val:,.0f}".replace(',', '.')
                tr_baru = {
                    'tanggal': tanggal_saldo,
                    'tanggal_indo': format_tanggal_pendek_indo(tanggal_saldo),
                    'nomor': f"SA-{kode_plg}",
                    'pelanggan': p.get('nama'),
                    'status': 'Belum lunas',
                    'jatuh_tempo': format_tanggal_pendek_indo(str_jatuh_tempo),
                    'total': formatted_val,
                    'sisa': formatted_val,
                    'is_saldo_awal': True,
                    'details': [],
                    'dpp': val,
                    'ppn': 0,
                    'beban_angkut': 0,
                    'hpp': 0
                }
                penjualan_list.append(tr_baru)
        except Exception:
            pass

    database_user[email]['penjualan'] = penjualan_list

def hitung_sisa_piutang_pelanggan(user_data, nama_pelanggan):
    total = 0
    for tr in user_data.get('penjualan', []):
        if tr.get('pelanggan') == nama_pelanggan:
            try:
                sisa_str = str(tr.get('sisa', tr.get('total', '0'))).replace('.', '')
                total += int(sisa_str)
            except:
                pass
    return total

def hitung_total_piutang_pelanggan(user_data):
    total = 0
    for p in user_data.get('pelanggan', []):
        nama = p.get('nama')
        total += hitung_sisa_piutang_pelanggan(user_data, nama)
    return total

def hitung_total_utang_pemasok(user_data):
    total = 0
    for s in user_data.get('pemasok', []):
        try:
            val = int(s.get('saldo_awal_utang', 0) or 0)
            total += val
        except Exception:
            pass
    return total

def hitung_total_persediaan_barang(user_data):
    total = 0
    for b in user_data.get('barang', []):
        try:
            qty = float(b.get('qty_awal', 0) or 0)
            hp = float(b.get('harga_pokok', 0) or 0)
            total += int(qty * hp)
        except Exception:
            pass
    return total

def hitung_saldo_akun(user_data, kode_akun):
    """
    Menghitung saldo akun secara dinamis berdasarkan saldo awal, 
    penerimaan kas, pengeluaran kas, penjualan, pembelian, retur, dll.
    """
    akun_list = user_data.get('akun', [])
    target_akun = next((a for a in akun_list if a['kode'] == kode_akun), None)
    if not target_akun:
        return 0
    
    posisi_dk = target_akun.get('dk', 'D') # 'D' (Debit) atau 'K' (Kredit)
    
    # Ambil saldo awal dari form saldo awal
    saldo_awal_dict = user_data.get('saldo_awal', {})
    debit_awal = float(str(saldo_awal_dict.get(f"debit_{kode_akun}", "0")).replace('.', '') or 0)
    kredit_awal = float(str(saldo_awal_dict.get(f"kredit_{kode_akun}", "0")).replace('.', '') or 0)
    
    # Khusus akun sistem pengendali, ambil juga dari total kartu jika belum tersimpan di saldo_awal
    if kode_akun == "1-1300" and debit_awal == 0:
        debit_awal = float(hitung_total_piutang_pelanggan(user_data))
    elif kode_akun == "1-1400" and debit_awal == 0:
        debit_awal = float(hitung_total_persediaan_barang(user_data))
    elif kode_akun == "2-1100" and kredit_awal == 0:
        kredit_awal = float(hitung_total_utang_pemasok(user_data))

    total_debit = debit_awal
    total_kredit = kredit_awal

    # 1. Akumulasi dari Penjualan (Menambah Piutang di Debit, Menambah Penjualan/PPN di Kredit)
    for tr in user_data.get('penjualan', []):
        if tr.get('is_saldo_awal', False):
            continue
        t_val = float(str(tr.get('total', '0')).replace('.', '') or 0)
        dpp_val = float(str(tr.get('dpp', 0)).replace('.', '') or 0)
        ppn_val = float(str(tr.get('ppn', 0)).replace('.', '') or 0)
        hpp_val = float(str(tr.get('total_hpp', 0)).replace('.', '') or 0)

        if kode_akun == "1-1300":  # Piutang Usaha (Debit)
            total_debit += t_val
        elif kode_akun == "4-1100":  # Penjualan (Kredit)
            total_kredit += dpp_val
        elif kode_akun == "2-1200":  # PPN Keluaran (Kredit)
            total_kredit += ppn_val
        elif kode_akun == "5-1100":  # HPP (Debit)
            total_debit += hpp_val
        elif kode_akun == "1-1400":  # Persediaan (Kredit akibat penjualan)
            total_kredit += hpp_val

    # 2. Akumulasi dari Pembelian (Menambah Utang di Kredit, Menambah Persediaan di Debit)
    for tr in user_data.get('pembelian', []):
        t_val = float(str(tr.get('total', '0')).replace('.', '') or 0)
        sub_val = float(str(tr.get('subtotal', t_val)).replace('.', '') or 0)
        
        if kode_akun == "2-1100":  # Utang Usaha (Kredit)
            total_kredit += t_val
        elif kode_akun == "1-1400":  # Persediaan Barang Dagang (Debit)
            total_debit += sub_val

    # 3. Akumulasi dari Penerimaan Kas (Pelunasan Piutang mengurangi Piutang)
    for tr in user_data.get('penerimaan_kas', []):
        jumlah = float(str(tr.get('jumlah', 0)).replace('.', '') or 0)
        if tr.get('akun_kas') == kode_akun:
            total_debit += jumlah
        if tr.get('akun_lawan') == kode_akun:
            total_kredit += jumlah
        # Jika ada alokasi pelunasan piutang
        if kode_akun == "1-1300" and tr.get('jenis') == 'pelunasan_piutang':
            total_kredit += jumlah

    # Hitung saldo akhir berdasarkan posisi normal
    if posisi_dk == 'D':
        saldo_akhir = total_debit - total_kredit
    else:
        saldo_akhir = total_kredit - total_debit

    return int(saldo_akhir)

def render_dashboard_layout(active_menu, content_html, message=""):
    user_email = session.get('user_email', '')
    if not user_email or user_email not in database_user:
        return "<script>window.location.href = '/login';</script>"
    user_data = database_user[user_email]
    
    alert_html = ""
    if message:
        alert_html = f"""
        <div style="background-color: #d4edda; color: #155724; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; border: 1px solid #c3e6cb;">
            {message}
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>mydagang</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background-color: #f8f9fa;
                font-family: 'Poppins', sans-serif;
                margin: 0; display: flex; height: 100vh; overflow: hidden;
            }}
            .sidebar {{
                width: 260px; background-color: #111c2e; color: #94a3b8; display: flex; flex-direction: column; height: 100vh; overflow-y: auto;
            }}
            .sidebar-header {{ padding: 20px; display: flex; align-items: center; border-bottom: 1px solid #1e293b; }}
            .logo-box {{ background-color: #f28b9c; color: white; font-weight: bold; padding: 6px 10px; border-radius: 6px; font-size: 16px; margin-right: 10px; }}
            .logo-title {{ font-size: 16px; font-weight: bold; color: #ffffff; }}
            .logo-sub {{ font-size: 11px; color: #64748b; }}
            .sidebar-menu {{ padding: 15px 0; flex: 1; }}
            
            /* Dropdown Menu Header / Kategori */
            .menu-group {{ margin-bottom: 4px; }}
            .menu-dropdown-btn {{
                width: 100%; background: none; border: none; color: #64748b;
                padding: 10px 20px; text-align: left; font-size: 11px; font-weight: bold;
                cursor: pointer; display: flex; justify-content: space-between; align-items: center;
                text-transform: uppercase; letter-spacing: 0.5px; font-family: 'Poppins', sans-serif;
            }}
            .menu-dropdown-btn:hover {{ color: #ffffff; background-color: #1e293b; }}
            
            /* Animasi Ikon Panah */
            .arrow-icon {{ transition: transform 0.2s ease; font-size: 10px; }}
            .arrow-icon.rotate {{ transform: rotate(180deg); }}
            
            /* Kontainer Sub-menu */
            .submenu-content {{ display: none; flex-direction: column; padding-bottom: 5px; }}
            .submenu-content.show {{ display: flex; }}

            .menu-item {{ padding: 10px 20px 10px 30px; color: #cbd5e1; text-decoration: none; display: block; font-size: 14px; transition: 0.2s; }}
            .menu-item:hover {{ color: #ffffff; background-color: #1e293b; }}
            .menu-item.active {{ background-color: #d18a99; color: white; font-weight: 500; border-radius: 4px; margin: 0 10px; padding: 10px 15px; }}
            
            .main-container {{ flex: 1; display: flex; flex-direction: column; height: 100vh; overflow-y: auto; }}
            .topbar {{ background-color: #ffffff; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e5e7eb; }}
            .topbar-company {{ font-size: 16px; font-weight: 600; color: #1f2937; }}
            .topbar-user-area {{ display: flex; align-items: center; gap: 15px; }}
            .user-info {{ text-align: right; }}
            .user-name {{ font-size: 13px; font-weight: 600; color: #374151; }}
            .user-email {{ font-size: 12px; color: #6b7280; }}
            .btn-keluar {{ border: 1px solid #d1d5db; background-color: #ffffff; padding: 6px 14px; border-radius: 6px; font-size: 13px; cursor: pointer; color: #374151; text-decoration: none; }}
            .btn-keluar:hover {{ background-color: #f3f4f6; }}
            
            .content-body {{ padding: 30px; max-width: 1200px; padding-bottom: 100px; }}
            .page-title {{ font-size: 22px; font-weight: bold; color: #1f2937; margin-bottom: 5px; }}
            .page-desc {{ font-size: 13px; color: #6b7280; margin-bottom: 25px; }}
            
            .card-form {{ background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }}
            .form-group {{ margin-bottom: 20px; }}
            label {{ display: block; font-size: 13px; font-weight: 500; color: #374151; margin-bottom: 6px; }}
            .required {{ color: #e53e3e; }}
            input[type="text"], input[type="date"], select, textarea {{ width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; box-sizing: border-box; color: #1f2937; font-family: 'Poppins', sans-serif; background-color: #fff; }}
            input:focus, select:focus, textarea:focus {{ outline: none; border-color: #d18a99; box-shadow: 0 0 0 3px rgba(209, 138, 153, 0.15); }}
            .form-helper {{ font-size: 11px; color: #6b7280; margin-top: 4px; }}
            
            .btn-simpan {{ background-color: #d18a99; color: white; border: none; padding: 10px 24px; font-size: 14px; font-weight: 600; border-radius: 6px; cursor: pointer; font-family: 'Poppins', sans-serif; }}
            .btn-simpan:hover {{ background-color: #be7988; }}
            .btn-batal {{ background-color: #ffffff; color: #374151; border: 1px solid #d1d5db; padding: 10px 24px; font-size: 14px; font-weight: 500; border-radius: 6px; cursor: pointer; font-family: 'Poppins', sans-serif; text-decoration: none; display: inline-block; text-align: center; }}
            .btn-batal:hover {{ background-color: #f3f4f6; }}

            .account-card {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); overflow: hidden; }}
            table.account-table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
            table.account-table th {{ background-color: #f9fafb; color: #6b7280; font-weight: 600; padding: 10px 20px; border-bottom: 1px solid #e5e7eb; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
            table.account-table td {{ padding: 12px 20px; border-bottom: 1px solid #f3f4f6; color: #374151; }}
            
            .badge-header {{ background-color: #f3e8ff; color: #7e22ce; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; display: inline-block; margin-left: 6px; }}
            .badge-subheader {{ background-color: #fef3c7; color: #b45309; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; display: inline-block; margin-left: 6px; }}
            .badge-sistem {{ background-color: #fdf2f4; color: #d18a99; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; display: inline-block; margin-left: 6px; }}
            .badge-nonaktif {{ background-color: #f3f4f6; color: #6b7280; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; display: inline-block; margin-left: 6px; }}
            .badge-dk {{ background-color: #ecfdf5; color: #047857; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 11px; }}
            .badge-dk-k {{ background-color: #eff6ff; color: #1d4ed8; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 11px; }}
            .badge-belum-lunas {{ background-color: #fef3c7; color: #b45309; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; border: 1px solid #fde68a; display: inline-block; }}
            .badge-lunas {{ background-color: #ecfdf5; color: #047857; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; border: 1px solid #a7f3d0; display: inline-block; }}
            .badge-saldo-awal {{ background-color: #f3f4f6; color: #374151; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; margin-left: 6px; }}
            
            .action-container {{ display: flex; align-items: center; justify-content: flex-end; gap: 4px; white-space: nowrap; }}
            .btn-action {{ border: 1px solid #d1d5db; background: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; cursor: pointer; color: #374151; text-decoration: none; display: inline-block; }}
            .btn-action:hover {{ background: #f3f4f6; }}
            .btn-action-danger {{ border: 1px solid #fecaca; color: #dc2626; }}
            .btn-action-danger:hover {{ background: #fef2f2; }}
            
            .modal-backdrop {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }}
            .modal-box {{ background: white; width: 950px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }}
            .modal-header {{ padding: 20px 25px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }}
            .modal-body {{ padding: 25px; overflow-y: auto; flex: 1; }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <div class="sidebar-header">
                <div class="logo-box">MD</div>
                <div>
                    <div class="logo-title">mydagang</div>
                    <div class="logo-sub">Perusahaan Dagang</div>
                </div>
            </div>
            <div class="sidebar-menu">
                
                <!-- BERANDA -->
                <div class="menu-group">
                    <button class="menu-dropdown-btn" onclick="toggleMenu('menu-beranda', this)">
                        <span>Beranda</span>
                        <span class="arrow-icon">▼</span>
                    </button>
                    <div id="menu-beranda" class="submenu-content">
                        <a href="/dashboard" class="menu-item {'active' if active_menu == 'dashboard' else ''}">Dashboard</a>
                    </div>
                </div>
                
                <!-- SETUP -->
                <div class="menu-group" style="margin-top: 10px;">
                    <button class="menu-dropdown-btn" onclick="toggleMenu('menu-setup', this)">
                        <span>Setup</span>
                        <span class="arrow-icon">▼</span>
                    </button>
                    <div id="menu-setup" class="submenu-content">
                        <a href="/setup/perusahaan" class="menu-item {'active' if active_menu == 'perusahaan' else ''}">Data Perusahaan</a>
                        <a href="/setup/akun" class="menu-item {'active' if active_menu == 'akun' else ''}">Daftar Akun</a>
                        <a href="/setup/saldo-awal" class="menu-item {'active' if active_menu == 'saldo_awal' else ''}">Saldo Awal</a>
                    </div>
                </div>
                
                <!-- KARTU -->
                <div class="menu-group" style="margin-top: 10px;">
                    <button class="menu-dropdown-btn" onclick="toggleMenu('menu-kartu', this)">
                        <span>Kartu</span>
                        <span class="arrow-icon">▼</span>
                    </button>
                    <div id="menu-kartu" class="submenu-content">
                        <a href="/kartu/pelanggan" class="menu-item {'active' if active_menu == 'pelanggan' else ''}">Pelanggan</a>
                        <a href="/kartu/pemasok" class="menu-item {'active' if active_menu == 'pemasok' else ''}">Pemasok</a>
                        <a href="/kartu/barang" class="menu-item {'active' if active_menu == 'barang' else ''}">Barang</a>
                    </div>
                </div>
                
                <!-- TRANSAKSI -->
                <div class="menu-group" style="margin-top: 10px;">
                    <button class="menu-dropdown-btn" onclick="toggleMenu('menu-transaksi', this)">
                        <span>Transaksi</span>
                        <span class="arrow-icon">▼</span>
                    </button>
                    <div id="menu-transaksi" class="submenu-content">
                        <a href="/transaksi/penjualan" class="menu-item {'active' if active_menu == 'penjualan' else ''}">Penjualan</a>
                        <a href="/transaksi/retur-penjualan" class="menu-item {'active' if active_menu == 'retur_penjualan' else ''}">Retur Penjualan</a>
                        <a href="/transaksi/pembelian" class="menu-item {'active' if active_menu == 'pembelian' else ''}">Pembelian</a>
                        <a href="/transaksi/retur-pembelian" class="menu-item {'active' if active_menu == 'retur_pembelian' else ''}">Retur Pembelian</a>
                        <a href="/transaksi/penerimaan-kas" class="menu-item {'active' if active_menu == 'penerimaan_kas' else ''}">Penerimaan Kas</a>
                        <a href="/transaksi/pengeluaran-kas" class="menu-item {'active' if active_menu == 'pengeluaran_kas' else ''}">Pengeluaran Kas</a>
                        <a href="/transaksi/jurnal-umum" class="menu-item {'active' if active_menu == 'jurnal_umum' else ''}">Jurnal Umum</a>
                    </div>
                </div>

            </div>
        </div>

        <div class="main-container">
            <div class="topbar">
                <div class="topbar-company">{user_data.get('perusahaan', 'PT mydagang')}</div>
                <div class="topbar-user-area">
                    <div class="user-info">
                        <div class="user-name">{user_data.get('nama', 'adinda')}</div>
                        <div class="user-email">{user_email}</div>
                    </div>
                    <a href="/logout" class="btn-keluar">Keluar</a>
                </div>
            </div>

            <div class="content-body">
                {alert_html}
                {content_html}
            </div>
        </div>

        <script>
            function toggleMenu(menuId, btnEl) {{
                const content = document.getElementById(menuId);
                const arrow = btnEl.querySelector('.arrow-icon');
                
                if (content.classList.contains('show')) {{
                    content.classList.remove('show');
                    arrow.classList.remove('rotate');
                }} else {{
                    content.classList.add('show');
                    arrow.classList.add('rotate');
                }}
            }}

            // Otomatis buka menu dropdown & putar panah jika salah satu sub-menu di dalamnya sedang aktif/dikunjungi
            window.addEventListener('DOMContentLoaded', () => {{
                document.querySelectorAll('.menu-item.active').forEach(item => {{
                    const parentSub = item.closest('.submenu-content');
                    if (parentSub) {{
                        parentSub.classList.add('show');
                        const btn = parentSub.previousElementSibling;
                        if (btn && btn.querySelector('.arrow-icon')) {{
                            btn.querySelector('.arrow-icon').classList.add('rotate');
                        }}
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    msg = request.args.get('msg', '')
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Poppins', sans-serif; }}
            .password-container {{ position: relative; width: 100%; }}
            .password-container input {{ width: 100%; padding: 10px 40px 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box; }}
            .toggle-password {{ position: absolute; right: 12px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #9ca3af; display: flex; align-items: center; }}
        </style>
    </head>
    <body style="background-color: #fcfcfc; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div style="background: white; padding: 40px; border-radius: 12px; border: 1px solid #eaeaea; width: 400px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 25px;">
                <div style="background: #f28b9c; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-right: 8px;">MD</div>
                <div style="font-size: 20px; font-weight: bold; color: #1f2937;">mydagang</div>
            </div>
            {"<div style='background-color: #f8d7da; color: #721c24; padding: 8px; border-radius: 6px; margin-bottom: 15px; font-size: 13px;'>"+msg+"</div>" if msg else ""}
            <h2 style="color: #1f2937; margin-bottom: 20px; font-size: 24px;">Masuk</h2>
            <form action="/login" method="POST">
                <div style="margin-bottom: 15px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Email <span style="color:red">*</span></label>
                    <input type="text" name="email" required style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Password <span style="color:red">*</span></label>
                    <div class="password-container">
                        <input type="password" name="password" id="login_password" required>
                        <span class="toggle-password" onclick="togglePassword('login_password', this)">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        </span>
                    </div>
                </div>
                <button type="submit" style="width: 100%; background: #d18a99; color: white; padding: 10px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-family: 'Poppins', sans-serif;">Masuk</button>
            </form>
            <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #6b7280;">
                Belum punya akun? <a href="/register" style="color: #d18a99; text-decoration: none;">Daftar di sini</a>
            </div>
        </div>
        <script>
            function togglePassword(fieldId, el) {{
                const field = document.getElementById(fieldId);
                const svg = el.querySelector('svg');
                if (field.type === "password") {{
                    field.type = "text";
                    svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
                }} else {{
                    field.type = "password";
                    svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.route('/register')
def register():
    msg = request.args.get('msg', '')
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Poppins', sans-serif; }}
            .password-container {{ position: relative; width: 100%; }}
            .password-container input {{ width: 100%; padding: 10px 40px 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box; }}
            .toggle-password {{ position: absolute; right: 12px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #9ca3af; display: flex; align-items: center; }}
        </style>
    </head>
    <body style="background-color: #fcfcfc; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 40px 0;">
        <div style="background: white; padding: 40px; border-radius: 12px; border: 1px solid #eaeaea; width: 400px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 25px;">
                <div style="background: #f28b9c; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-right: 8px;">MD</div>
                <div style="font-size: 20px; font-weight: bold; color: #1f2937;">mydagang</div>
            </div>
            {"<div style='background-color: #f8d7da; color: #721c24; padding: 8px; border-radius: 6px; margin-bottom: 15px; font-size: 13px;'>"+msg+"</div>" if msg else ""}
            <h2 style="color: #1f2937; margin-bottom: 20px; font-size: 24px;">Daftar Akun Baru</h2>
            <form action="/register" method="POST">
                <div style="margin-bottom: 15px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Nama lengkap <span style="color:red">*</span></label>
                    <input type="text" name="nama_lengkap" required style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Email <span style="color:red">*</span></label>
                    <input type="text" name="email" required style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Password <span style="color:red">*</span></label>
                    <div class="password-container">
                        <input type="password" name="password" id="reg_password" required>
                        <span class="toggle-password" onclick="togglePassword('reg_password', this)">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">Minimal 6 karakter</div>
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Nama perusahaan <span style="color:red">*</span></label>
                    <input type="text" name="nama_perusahaan" placeholder="PT mydagang" required style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="font-size: 14px; display: block; margin-bottom: 6px;">Tanggal saldo awal</label>
                    <input type="date" name="tanggal_saldo" value="2026-01-01" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-family: 'Poppins', sans-serif; box-sizing: border-box;">
                    <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">Tanggal mulai pencatatan transaksi</div>
                </div>
                <button type="submit" style="width: 100%; background: #d18a99; color: white; padding: 10px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-family: 'Poppins', sans-serif;">Daftar & buat perusahaan</button>
            </form>
            <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #6b7280;">
                Sudah punya akun? <a href="/login" style="color: #d18a99; text-decoration: none;">Masuk</a>
            </div>
        </div>
        <script>
            function togglePassword(fieldId, el) {{
                const field = document.getElementById(fieldId);
                const svg = el.querySelector('svg');
                if (field.type === "password") {{
                    field.type = "text";
                    svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
                }} else {{
                    field.type = "password";
                    svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.route('/login', methods=['POST'])
def proses_login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email not in database_user:
        return redirect(url_for('login', msg="Akun belum terdaftar! Silakan daftar dulu."))
    if database_user[email]['password'] != password:
        return redirect(url_for('login', msg="Password salah!"))
    session['user_email'] = email
    return redirect(url_for('setup_perusahaan'))

@app.route('/register', methods=['POST'])
def proses_register():
    nama = request.form.get('nama_lengkap', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    perusahaan = request.form.get('nama_perusahaan', 'PT mydagang').strip()
    tanggal_saldo = request.form.get('tanggal_saldo', '2026-01-01')

    if '@' not in email:
        return redirect(url_for('register', msg="Format email tidak valid."))
    if len(password) < 6:
        return redirect(url_for('register', msg="Password minimal 6 karakter."))
    if email in database_user:
        return redirect(url_for('register', msg="Email sudah terdaftar! Silakan masuk."))

    database_user[email] = {
        'nama': nama,
        'password': password,
        'perusahaan': perusahaan,
        'alamat': '',
        'telepon': '',
        'tanggal_saldo': tanggal_saldo if tanggal_saldo else '2026-01-01',
        'akun': [dict(a) for a in DEFAULT_AKUN],
        'saldo_awal': {},
        'pelanggan': [],
        'pemasok': [],
        'barang': [],
        'penjualan': [],
        'retur_penjualan': [],
        'penerimaan_kas': []
    }
    session['user_email'] = email
    return redirect(url_for('setup_perusahaan'))

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    content = """
    <div class="page-title">Dashboard</div>
    <div class="page-desc">Selamat datang kembali di sistem pencatatan keuangan mydagang.</div>
    <div class="card-form">
        <p>Silakan pilih menu di sebelah kiri untuk mulai mengelola perusahaan Anda.</p>
    </div>
    """
    return render_dashboard_layout('dashboard', content)

@app.route('/setup/perusahaan', methods=['GET', 'POST'])
def setup_perusahaan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    msg = ""
    
    if request.method == 'POST':
        database_user[email]['perusahaan'] = request.form.get('nama_perusahaan')
        database_user[email]['alamat'] = request.form.get('alamat')
        database_user[email]['telepon'] = request.form.get('telepon')
        database_user[email]['tanggal_saldo'] = request.form.get('tanggal_saldo')
        sync_saldo_awal_penjualan(email)
        return redirect(url_for('daftar_akun'))
    
    user_data = database_user[email]
    
    content = f"""
    <div class="page-title">Data Perusahaan</div>
    <div class="page-desc">Tanggal saldo awal menjadi tanggal jurnal saldo awal.</div>
    
    <div class="card-form">
        <form action="/setup/perusahaan" method="POST">
            <div class="form-group">
                <label>Nama perusahaan <span class="required">*</span></label>
                <input type="text" name="nama_perusahaan" value="{user_data.get('perusahaan', '')}" required>
            </div>
            
            <div class="form-group">
                <label>Alamat</label>
                <textarea name="alamat">{user_data.get('alamat', '')}</textarea>
            </div>
            
            <div class="form-group">
                <label>Telepon</label>
                <input type="text" name="telepon" value="{user_data.get('telepon', '')}">
            </div>
            
            <div class="form-group">
                <label>Tanggal saldo awal <span class="required">*</span></label>
                <input type="date" name="tanggal_saldo" value="{user_data.get('tanggal_saldo', '2026-01-01')}" required>
                <div class="form-helper">Semua transaksi harus bertanggal sama atau setelah tanggal ini.</div>
            </div>
            
            <button type="submit" class="btn-simpan">Simpan</button>
        </form>
    </div>
    """
    return render_dashboard_layout('perusahaan', content, message=msg)


@app.route('/setup/akun')
def daftar_akun():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_akun = user_data.get('akun', DEFAULT_AKUN)
    list_akun = sorted(list_akun, key=lambda x: x['kode'])
    
    kategori_list = [
        "1 — Aset", 
        "2 — Liabilitas", 
        "3 — Ekuitas", 
        "4 — Pendapatan", 
        "5 — Harga Pokok Penjualan", 
        "6 — Beban Operasional", 
        "8 — Pendapatan Lain-Lain", 
        "9 — Beban Lain-Lain"
    ]
    
    html_cards = ""
    for kat in kategori_list:
        akun_kat = [a for a in list_akun if a['kategori'] == kat]
        if not akun_kat:
            continue
            
        rows_html = ""
        for acc in list_akun:
            if acc['kategori'] == kat:
                nama_style = "text-decoration: line-through; color: #9ca3af;" if not acc['aktif'] else ""
                badge_status = ""
                indent_html = ""
                
                if acc.get('level') == 'Header':
                    badge_status = '<span class="badge-header">Header</span>'
                    nama_style += " font-weight: 700; text-transform: uppercase;"
                elif acc.get('level') == 'Sub Header':
                    badge_status = '<span class="badge-subheader">Sub Header</span>'
                    nama_style += " font-weight: 600; text-transform: uppercase;"
                    indent_html = '<span style="color: #9ca3af; margin-right: 6px;">└</span>'
                else:
                    if acc.get('level') == 'Akun biasa' and acc.get('induk'):
                        indent_html = '<span style="color: #9ca3af; margin-right: 6px; margin-left: 15px;">└</span>'
                    
                    if acc['sistem']:
                        badge_status = '<span class="badge-sistem">Sistem</span>'
                    elif not acc['aktif']:
                        badge_status = '<span class="badge-nonaktif">Nonaktif</span>'
                
                btn_aktif_text = "Aktifkan" if not acc['aktif'] else "Nonaktifkan"
                
                aksi_html = '<div class="action-container">'
                if acc.get('level') in ['Header', 'Sub Header']:
                    target_level_anak = 'Sub Header' if acc.get('level') == 'Header' else 'Akun biasa'
                    aksi_html += f'<a href="/setup/akun/baru?level={target_level_anak}&induk={acc["kode"]}" class="btn-action">+ Anak</a>'
                
                aksi_html += f'<a href="/setup/akun/ubah/{acc["kode"]}" class="btn-action">Ubah</a>'
                
                if not acc['sistem']:
                    aksi_html += f'''
                        <a href="/setup/akun/toggle/{acc["kode"]}" class="btn-action">{btn_aktif_text}</a>
                        <a href="/setup/akun/hapus/{acc["kode"]}" class="btn-action btn-action-danger" onclick="return confirm(\'Apakah Anda yakin ingin menghapus akun {acc["nama"]}?\');">Hapus</a>
                    '''
                aksi_html += '</div>'
                
                dk_badge = f'<span class="badge-dk">{acc["dk"]}</span>' if acc["dk"] == 'D' else (f'<span class="badge-dk-k">{acc["dk"]}</span>' if acc["dk"] == 'K' else f'<span style="font-weight:600;">{acc["dk"]}</span>')

                rows_html += f"""
                <tr class="account-row" data-kode="{acc['kode'].lower()}" data-nama="{acc['nama'].lower()}">
                    <td><strong>{acc['kode']}</strong></td>
                    <td>{indent_html}<span style="{nama_style}">{acc['nama']}</span> {badge_status}</td>
                    <td>{acc['tipe']}</td>
                    <td>{dk_badge}</td>
                    <td>{acc['saldo']}</td>
                    <td style="text-align: right;">{aksi_html}</td>
                </tr>
                """
        
        html_cards += f"""
        <div class="account-card">
            <div class="account-header-title">{kat}</div>
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 15%;">Kode</th>
                        <th style="width: 32%;">Nama Akun</th>
                        <th style="width: 23%;">Tipe Akun (Subtipe)</th>
                        <th style="width: 8%;">D/K</th>
                        <th style="width: 8%;">Saldo</th>
                        <th style="width: 14%; text-align: right;">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Daftar Akun</div>
            <div class="page-desc" style="margin-bottom: 0;">Bagan akun. Header (1–9) menentukan kelompok utama. Sub Header / Tipe Akun untuk pengelompokan spesifik.<br>Pengguna dapat memilih posisi saldo normal (D/K) dan mengatur status aktif/nonaktif.</div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 10px;">
            <div style="font-size: 13px; color: #374151; display: flex; align-items: center; gap: 6px;">
                <input type="checkbox" checked style="width: 16px; height: 16px; accent-color: #d18a99;"> Tampilkan Nonaktif
            </div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="input_pencarian" placeholder="Cari kode / nama..." onkeyup="filterAkun()" style="padding: 7px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; width: 200px;">
                <a href="/setup/akun/baru" style="background-color: #d18a99; color: white; padding: 7px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; text-decoration: none; display: flex; align-items: center; gap: 4px;">+ Akun baru</a>
            </div>
        </div>
    </div>
    <div id="container_cards">
        {html_cards}
    </div>
    
    <script>
        function filterAkun() {{
            const input = document.getElementById('input_pencarian').value.toLowerCase();
            const rows = document.querySelectorAll('.account-row');
            
            rows.forEach(row => {{
                const kode = row.getAttribute('data-kode');
                const nama = row.getAttribute('data-nama');
                if (kode.includes(input) || nama.includes(input)) {{
                    row.style.display = "";
                }} else {{
                    row.style.display = "none";
                }}
            }});
        }}
    </script>
    """
    
    modal_html = session.pop('modal_akun', False)
    if modal_html:
        content += modal_html

    msg_error = session.pop('error_akun', '')
    if msg_error:
        content = f"""
        <div style="background-color: #f8d7da; color: #721c24; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; border: 1px solid #f5c6cb;">
            {msg_error}
        </div>
        """ + content

    return render_dashboard_layout('akun', content)

@app.route('/setup/akun/toggle/<path:kode>')
def toggle_akun(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    email = session['user_email']
    for acc in database_user[email]['akun']:
        if acc['kode'] == kode and not acc['sistem']:
            acc['aktif'] = not acc['aktif']
    return redirect(url_for('daftar_akun'))

@app.route('/setup/akun/hapus/<path:kode>')
def hapus_akun(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    email = session['user_email']
    database_user[email]['akun'] = [acc for acc in database_user[email]['akun'] if not (acc['kode'] == kode and not acc['sistem'])]
    return redirect(url_for('daftar_akun'))

@app.route('/setup/akun/baru', methods=['GET', 'POST'])
def tambah_akun():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    default_level = request.args.get('level', 'Akun biasa')
    default_induk = request.args.get('induk', '')
    
    if request.method == 'POST':
        level = request.form.get('level_akun', 'Akun biasa')
        kategori = request.form.get('header_akun')
        kode = request.form.get('kode_akun').strip()
        nama = request.form.get('nama_akun').strip()
        tipe = request.form.get('tipe_akun')
        induk = request.form.get('akun_induk')
        dk = "D" if request.form.get('saldo_normal') == "Debit" else "K"
        aktif = True if request.form.get('akun_aktif') else False
        
        user_akun_list = database_user[email]['akun']
        for acc in user_akun_list:
            if acc['kode'].lower() == kode.lower():
                session['error_akun'] = f"Gagal: Kode akun '{kode}' sudah terdaftar!"
                return redirect(url_for('daftar_akun'))
            if acc['nama'].lower() == nama.lower():
                session['error_akun'] = f"Gagal: Nama akun '{nama}' sudah terdaftar!"
                return redirect(url_for('daftar_akun'))

        new_acc = {
            "kode": kode,
            "nama": nama,
            "level": level,
            "tipe": tipe,
            "induk": induk if induk != "— Tanpa induk —" else "",
            "dk": dk,
            "saldo": "-",
            "kategori": kategori,
            "sistem": False,
            "aktif": aktif
        }
        database_user[email]['akun'].append(new_acc)
        return redirect(url_for('daftar_akun'))
        
    user_akun_list = database_user[email]['akun']
    
    border_h = "1px solid #d1d5db"; bg_h = "#fff"; color_h = "#1f2937"; shadow_h = "none";
    border_sh = "1px solid #d1d5db"; bg_sh = "#fff"; color_sh = "#1f2937"; shadow_sh = "none";
    border_b = "1px solid #d18a99"; bg_b = "#fffafb"; color_b = "#d18a99"; shadow_b = "0 0 0 1px #d18a99";
    
    if default_level == 'Header':
        border_h = "1px solid #d18a99"; bg_h = "#fffafb"; color_h = "#d18a99"; shadow_h = "0 0 0 1px #d18a99";
        border_b = "1px solid #d1d5db"; bg_b = "#fff"; color_b = "#1f2937"; shadow_b = "none";
    elif default_level == 'Sub Header':
        border_sh = "1px solid #d18a99"; bg_sh = "#fffafb"; color_sh = "#d18a99"; shadow_sh = "0 0 0 1px #d18a99";
        border_b = "1px solid #d1d5db"; bg_b = "#fff"; color_b = "#1f2937"; shadow_b = "none";

    # Convert list of dicts to safe JS array format
    import json
    js_akun_data = json.dumps([{ 'kode': a['kode'], 'nama': a['nama'], 'level': a.get('level', 'Akun biasa') } for a in user_akun_list])

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Akun Baru</div>
                <a href="/setup/akun" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/setup/akun/baru" method="POST" id="formAkunBaru">
                    
                    <input type="hidden" name="level_akun" id="input_level" value="{default_level}">
                    
                    <div class="form-group">
                        <label>Level Akun</label>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px;">
                            <div id="card_header" onclick="selectLevel('Header', this)" style="border: {border_h}; background-color: {bg_h}; border-radius: 8px; padding: 12px; cursor: pointer; text-align: center; box-shadow: {shadow_h};">
                                <div style="font-weight: 600; color: {color_h}; font-size: 13px;">Header</div>
                                <div style="font-size: 11px; color: #6b7280; margin-top: 2px;">Judul kelompok utama</div>
                            </div>
                            <div id="card_subheader" onclick="selectLevel('Sub Header', this)" style="border: {border_sh}; background-color: {bg_sh}; border-radius: 8px; padding: 12px; cursor: pointer; text-align: center; box-shadow: {shadow_sh};">
                                <div style="font-weight: 600; color: {color_sh}; font-size: 13px;">Sub Header</div>
                                <div style="font-size: 11px; color: #6b7280; margin-top: 2px;">Kelompok di bawah</div>
                            </div>
                            <div id="card_biasa" onclick="selectLevel('Akun biasa', this)" style="border: {border_b}; background-color: {bg_b}; border-radius: 8px; padding: 12px; cursor: pointer; text-align: center; box-shadow: {shadow_b};">
                                <div style="font-weight: 600; color: {color_b}; font-size: 13px;">Akun biasa</div>
                                <div style="font-size: 11px; color: #6b7280; margin-top: 2px;">Transaksi & saldo</div>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Header (Kelompok Akun)</label>
                        <select name="header_akun" id="select_header" onchange="updateKodeAkun(); filterAkunInduk();">
                            <option value="1 — Aset">1 — Aset</option>
                            <option value="2 — Liabilitas">2 — Liabilitas</option>
                            <option value="3 — Ekuitas">3 — Ekuitas</option>
                            <option value="4 — Pendapatan">4 — Pendapatan</option>
                            <option value="5 — Harga Pokok Penjualan">5 — Harga Pokok Penjualan</option>
                            <option value="6 — Beban Operasional">6 — Beban Operasional</option>
                            <option value="8 — Pendapatan Lain-Lain">8 — Pendapatan Lain-Lain</option>
                            <option value="9 — Beban Lain-Lain">9 — Beban Lain-Lain</option>
                        </select>
                        <div class="form-helper">Awalan nomor akun (1–9) menentukan kelompok utama akun.</div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode Akun <span class="required">*</span></label>
                            <input type="text" name="kode_akun" id="input_kode" value="1-" required oninput="filterAkunInduk()">
                            <div class="form-helper" id="helper_kode">Awalan harus '1'</div>
                        </div>
                        <div>
                            <label>Nama Akun <span class="required">*</span></label>
                            <input type="text" name="nama_akun" placeholder="mis. Kas Toko" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Tipe Akun (Sub Header / Subtipe)</label>
                        <select name="tipe_akun">
                            <option>Bank (Debit)</option>
                            <option>Piutang (Debit)</option>
                            <option>Aset Lancar (Debit)</option>
                            <option>Aset Tetap (Debit)</option>
                            <option>Aset Lancar Lainnya (Debit)</option>
                            <option>Aset Lainnya (Debit)</option>
                            <option value="Persediaan (kontrol) (Debit) — khusus akun sistem" disabled style="color: #9ca3af; background-color: #f3f4f6;">Persediaan (kontrol) (Debit) — khusus akun sistem (Tidak dapat dipilih)</option>
                            <option>Akumulasi Penyusutan (Kredit)</option>
                        </select>
                        <div class="form-helper">Menentukan pengelompokan akun di laporan keuangan.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo Normal (D / K)</label>
                        <div style="display: flex; gap: 15px; margin-top: 4px;">
                            <label style="border: 1px solid #d18a99; background: #fffafb; padding: 8px 16px; border-radius: 6px; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 13px;">
                                <input type="radio" name="saldo_normal" value="Debit" checked style="accent-color: #d18a99;"> Debit (D)
                            </label>
                            <label style="border: 1px solid #d1d5db; padding: 8px 16px; border-radius: 6px; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 13px;">
                                <input type="radio" name="saldo_normal" value="Kredit" style="accent-color: #d18a99;"> Kredit (K)
                            </label>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Akun Induk</label>
                        <select name="akun_induk" id="select_akun_induk">
                            <option value="— Tanpa induk —">— Tanpa induk —</option>
                        </select>
                        <div class="form-helper">Hanya menampilkan header atau sub header yang memiliki angka depan yang sama.</div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="akun_aktif" checked style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Akun aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/setup/akun" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        const allAkunData = {js_akun_data};

        function filterAkunInduk() {{
            const levelAkun = document.getElementById('input_level').value;
            const kodeInput = document.getElementById('input_kode').value.trim();
            const prefix = kodeInput.charAt(0);
            const selectInduk = document.getElementById('select_akun_induk');
            
            selectInduk.innerHTML = '<option value="— Tanpa induk —">— Tanpa induk —</option>';
            
            if (levelAkun === 'Header') return;

            let targetLevel = (levelAkun === 'Sub Header') ? 'Header' : 'Sub Header';

            allAkunData.forEach(acc => {{
                if (acc.level === targetLevel && acc.kode.charAt(0) === prefix) {{
                    let opt = document.createElement('option');
                    opt.value = acc.kode;
                    opt.text = acc.kode + " - " + acc.nama;
                    selectInduk.appendChild(opt);
                }}
            }});
        }}

        function selectLevel(levelName, el) {{
            document.getElementById('input_level').value = levelName;
            
            const cards = ['card_header', 'card_subheader', 'card_biasa'];
            cards.forEach(id => {{
                const c = document.getElementById(id);
                if(c) {{
                    c.style.border = "1px solid #d1d5db";
                    c.style.backgroundColor = "#fff";
                    c.style.boxShadow = "none";
                    c.querySelector('div').style.color = "#1f2937";
                }}
            }});
            
            el.style.border = "1px solid #d18a99";
            el.style.backgroundColor = "#fffafb";
            el.style.boxShadow = "0 0 0 1px #d18a99";
            el.querySelector('div').style.color = "#d18a99";

            filterAkunInduk();
        }}

        function updateKodeAkun() {{
            const select = document.getElementById('select_header');
            const inputKode = document.getElementById('input_kode');
            const helper = document.getElementById('helper_kode');
            const val = select.value;
            const angkaAwalan = val.charAt(0);
            
            inputKode.value = angkaAwalan + "-";
            helper.textContent = "Awalan harus '" + angkaAwalan + "'";
            filterAkunInduk();
        }}

        window.onload = function() {{
            filterAkunInduk();
        }};
    </script>
    """
    
    session['modal_akun'] = modal_content
    return redirect(url_for('daftar_akun'))

@app.route('/setup/akun/ubah/<path:kode>', methods=['GET', 'POST'])
def ubah_akun(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_akun_list = database_user[email]['akun']
    
    target_acc = None
    for acc in user_akun_list:
        if acc['kode'] == kode:
            target_acc = acc
            break
            
    if not target_acc:
        return redirect(url_for('daftar_akun'))
        
    if request.method == 'POST':
        new_nama = request.form.get('nama_akun').strip()
        new_kode = request.form.get('kode_akun').strip() if not target_acc['sistem'] else target_acc['kode']
        
        for acc in user_akun_list:
            if acc['kode'] != target_acc['kode'] and acc['kode'].lower() == new_kode.lower():
                session['error_akun'] = f"Gagal: Kode akun '{new_kode}' sudah terdaftar!"
                return redirect(url_for('daftar_akun'))
            if acc['nama'].lower() != target_acc['nama'].lower() and acc['nama'].lower() == new_nama.lower():
                session['error_akun'] = f"Gagal: Nama akun '{new_nama}' sudah terdaftar!"
                return redirect(url_for('daftar_akun'))

        if not target_acc['sistem']:
            target_acc['kategori'] = request.form.get('header_akun')
            target_acc['kode'] = new_kode
            target_acc['nama'] = new_nama
            target_acc['tipe'] = request.form.get('tipe_akun')
        
        target_acc['induk'] = request.form.get('akun_induk') if request.form.get('akun_induk') != "— Tanpa induk —" else ""
        target_acc['dk'] = "D" if request.form.get('saldo_normal') == "Debit" else "K"
        return redirect(url_for('daftar_akun'))
        
    kategori_options = ["1 — Aset", "2 — Liabilitas", "3 — Ekuitas", "4 — Pendapatan", "5 — Harga Pokok Penjualan", "6 — Beban Operasional", "8 — Pendapatan Lain-Lain", "9 — Beban Lain-Lain"]
    opt_header_html = ""
    for kat in kategori_options:
        selected = "selected" if kat == target_acc['kategori'] else ""
        opt_header_html += f'<option value="{kat}" {selected}>{kat}</option>'
        
    tipe_options = [
        "Bank (Debit)",
        "Piutang (Debit)",
        "Aset Lancar (Debit)",
        "Aset Tetap (Debit)",
        "Aset Lancar Lainnya (Debit)",
        "Aset Lainnya (Debit)",
        "Persediaan (kontrol) (Debit) — khusus akun sistem",
        "Akumulasi Penyusutan (Kredit)"
    ]
    opt_tipe_html = ""
    for t in tipe_options:
        selected = "selected" if t == target_acc['tipe'] else ""
        disabled_prop = "disabled style='color: #9ca3af; background-color: #f3f4f6;'" if "Persediaan" in t else ""
        opt_tipe_html += f'<option value="{t}" {selected} {disabled_prop}>{t}{" (Tidak dapat dipilih)" if "Persediaan" in t else ""}</option>'
        
    target_level = target_acc.get('level', 'Akun biasa')
    parent_level = 'Header' if target_level == 'Sub Header' else ('Sub Header' if target_level == 'Akun biasa' else '')
    target_prefix = target_acc['kode'][0] if target_acc['kode'] else '1'

    option_induk_html = '<option value="— Tanpa induk —">— Tanpa induk —</option>'
    for acc in user_akun_list:
        if parent_level and acc.get('level') == parent_level and acc['kode'].startswith(target_prefix):
            selected = "selected" if acc['kode'] == target_acc.get('induk') else ""
            option_induk_html += f'<option value="{acc["kode"]}" {selected}>{acc["kode"]} - {acc["nama"]}</option>'

    checked_d = "checked" if target_acc['dk'] == "D" else ""
    checked_k = "checked" if target_acc['dk'] == "K" else ""
    
    is_sistem = target_acc['sistem']
    disabled_attr = "disabled style='background-color: #f3f4f6; color: #6b7280; cursor: not-allowed;'" if is_sistem else ""
    catatan_sistem = '<div style="background-color: #fff3cd; color: #856404; padding: 10px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 15px; border: 1px solid #ffeeba;">Akun sistem. Anda hanya dapat mengubah Saldo Normal dan Akun Induk.</div>' if is_sistem else ''

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Ubah Akun</div>
                <a href="/setup/akun" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/setup/akun/ubah/{kode}" method="POST">
                    
                    {catatan_sistem}
                    <div class="form-group">
                        <label>Level Akun</label>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px;">
                            <div style="border: 1px solid #d1d5db; border-radius: 8px; padding: 12px; opacity: 0.5; text-align: center;">
                                <div style="font-weight: 600; color: #1f2937; font-size: 13px;">Header</div>
                            </div>
                            <div style="border: 1px solid #d1d5db; border-radius: 8px; padding: 12px; opacity: 0.5; text-align: center;">
                                <div style="font-weight: 600; color: #1f2937; font-size: 13px;">Sub Header</div>
                            </div>
                            <div style="border: 1px solid #d18a99; background-color: #fffafb; border-radius: 8px; padding: 12px; text-align: center; box-shadow: 0 0 0 1px #d18a99;">
                                <div style="font-weight: 600; color: #d18a99; font-size: 13px;">Akun biasa</div>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Header (Kelompok Akun)</label>
                        <select name="header_akun" id="select_header" onchange="updateKodeAkun()" {disabled_attr}>
                            {opt_header_html}
                        </select>
                        {'<input type="hidden" name="header_akun" value="'+target_acc['kategori']+'">' if is_sistem else ''}
                        <div class="form-helper">Awalan nomor akun (1–9) menentukan kelompok utama akun.</div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode Akun <span class="required">*</span></label>
                            <input type="text" name="kode_akun" id="input_kode" value="{target_acc['kode']}" {disabled_attr} required>
                            {'<input type="hidden" name="kode_akun" value="'+target_acc['kode']+'">' if is_sistem else ''}
                            <div class="form-helper" id="helper_kode">Awalan nomor akun</div>
                        </div>
                        <div>
                            <label>Nama Akun <span class="required">*</span></label>
                            <input type="text" name="nama_akun" value="{target_acc['nama']}" {disabled_attr} required>
                            {'<input type="hidden" name="nama_akun" value="'+target_acc['nama']+'">' if is_sistem else ''}
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Tipe Akun (Sub Header / Subtipe)</label>
                        <select name="tipe_akun" {disabled_attr}>
                            {opt_tipe_html}
                        </select>
                        {'<input type="hidden" name="tipe_akun" value="'+target_acc['tipe']+'">' if is_sistem else ''}
                        <div class="form-helper">Menentukan pengelompokan akun di laporan keuangan.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo Normal (D / K)</label>
                        <div style="display: flex; gap: 15px; margin-top: 4px;">
                            <label style="border: 1px solid {'#d18a99' if target_acc['dk']=='D' else '#d1d5db'}; background: {'#fffafb' if target_acc['dk']=='D' else '#fff'}; padding: 8px 16px; border-radius: 6px; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 13px;">
                                <input type="radio" name="saldo_normal" value="Debit" {checked_d} style="accent-color: #d18a99;"> Debit (D)
                            </label>
                            <label style="border: 1px solid {'#d18a99' if target_acc['dk']=='K' else '#d1d5db'}; background: {'#fffafb' if target_acc['dk']=='K' else '#fff'}; padding: 8px 16px; border-radius: 6px; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 13px;">
                                <input type="radio" name="saldo_normal" value="Kredit" {checked_k} style="accent-color: #d18a99;"> Kredit (K)
                            </label>
                        </div>
                        <div class="form-helper">Pengguna dapat menentukan saldo normal debit atau kredit secara fleksibel.</div>
                    </div>

                    <div class="form-group">
                        <label>Akun Induk</label>
                        <select name="akun_induk">
                            {option_induk_html}
                        </select>
                        <div class="form-helper">Pilih header atau sub header tempat akun ini dikelompokkan.</div>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/setup/akun" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function updateKodeAkun() {{
            const select = document.getElementById('select_header');
            const inputkode = document.getElementById('input_kode');
            if(!select || !inputkode) return;
            const val = select.value;
            const angkaAwalan = val.charAt(0);
            inputkode.value = angkaAwalan + "-";
        }}
    </script>
    """
    
    session['modal_akun'] = modal_content
    return redirect(url_for('daftar_akun'))


@app.route('/setup/saldo-awal', methods=['GET', 'POST'])
def saldo_awal():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_akun = user_data.get('akun', DEFAULT_AKUN)
    list_akun = sorted([a for a in list_akun if a.get('aktif', True)], key=lambda x: x['kode'])
    
    tanggal_perusahaan = user_data.get('tanggal_saldo', '2026-01-01')
    tanggal_format_indo = format_tanggal_indo(tanggal_perusahaan)
    
    if request.method == 'POST':
        saved_data = {}
        for key, val in request.form.items():
            saved_data[key] = val
        database_user[email]['saldo_awal'] = saved_data
        sync_saldo_awal_penjualan(email)
        return redirect(url_for('saldo_awal'))
        
    saved_saldo = user_data.get('saldo_awal', {})
    total_piutang_pelanggan = hitung_total_piutang_pelanggan(user_data)
    total_utang_pemasok = hitung_total_utang_pemasok(user_data)
    total_persediaan_barang = hitung_total_persediaan_barang(user_data)
    
    kategori_list = [
        "1 — Aset", 
        "2 — Liabilitas", 
        "3 — Ekuitas", 
        "4 — Pendapatan", 
        "5 — Harga Pokok Penjualan", 
        "6 — Beban Operasional", 
        "8 — Pendapatan Lain-Lain", 
        "9 — Beban Lain-Lain"
    ]
    
    html_cards = ""
    for kat in kategori_list:
        akun_kat = [a for a in list_akun if a['kategori'] == kat and a.get('level') == 'Akun biasa']
        if not akun_kat:
            continue
            
        rows_html = ""
        for acc in akun_kat:
            kode = acc['kode']
            val_debit = saved_saldo.get(f"debit_{kode}", "0")
            if val_debit == "": val_debit = "0"
            val_kredit = saved_saldo.get(f"kredit_{kode}", "0")
            if val_kredit == "": val_kredit = "0"
            
            is_piutang = (kode == "1-1300")
            is_persediaan = (kode == "1-1400")
            is_utang = (kode == "2-1100")
            is_historical = (kode == "3-9999")
            
            if is_piutang:
                formatted_val = f"{total_piutang_pelanggan:,.0f}".replace(',', '.') if total_piutang_pelanggan > 0 else "0"
                input_debit = f'<input type="text" id="debit_{kode}" name="debit_{kode}" value="{formatted_val}" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #374151; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;" oninput="hitungTotal()">'
                input_kredit = f'<input type="text" id="kredit_{kode}" name="kredit_{kode}" value="0" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #6b7280; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;">'
                info_kartu = ' <a href="/kartu/pelanggan" style="color: #d18a99; text-decoration: none; font-size: 11px;">(dari kartu pelanggan)</a>'
            elif is_persediaan:
                formatted_val = f"{total_persediaan_barang:,.0f}".replace(',', '.') if total_persediaan_barang > 0 else "0"
                input_debit = f'<input type="text" id="debit_{kode}" name="debit_{kode}" value="{formatted_val}" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #374151; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;" oninput="hitungTotal()">'
                input_kredit = f'<input type="text" id="kredit_{kode}" name="kredit_{kode}" value="0" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #6b7280; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;">'
                info_kartu = ' <a href="/kartu/barang" style="color: #d18a99; text-decoration: none; font-size: 11px;">(dari kartu barang)</a>'
            elif is_utang:
                formatted_val = f"{total_utang_pemasok:,.0f}".replace(',', '.') if total_utang_pemasok > 0 else "0"
                input_debit = f'<input type="text" id="debit_{kode}" name="debit_{kode}" value="0" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #6b7280; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;">'
                input_kredit = f'<input type="text" id="kredit_{kode}" name="kredit_{kode}" value="{formatted_val}" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #374151; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;" oninput="hitungTotal()">'
                info_kartu = ' <a href="/kartu/pemasok" style="color: #d18a99; text-decoration: none; font-size: 11px;">(dari kartu pemasok)</a>'
            elif is_historical:
                input_debit = f'<input type="text" id="debit_{kode}" name="debit_{kode}" value="{val_debit}" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #6b7280; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;">'
                input_kredit = f'<input type="text" id="kredit_{kode}" name="kredit_{kode}" value="{val_kredit}" readonly style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; background-color: #f3f4f6; color: #6b7280; border-radius: 4px; font-size: 13px; width: 140px; cursor: not-allowed;">'
                info_kartu = ' <span style="color: #d18a99; font-size: 11px; font-weight: 500;">(Otomatis)</span>'
            else:
                input_debit = f'<input type="text" id="debit_{kode}" name="debit_{kode}" value="{val_debit}" style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; width: 140px;" onfocus="clearZero(this)" onblur="restoreZero(this)" oninput="formatRupiah(this); hitungTotal()">'
                input_kredit = f'<input type="text" id="kredit_{kode}" name="kredit_{kode}" value="{val_kredit}" style="text-align: right; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; width: 140px;" onfocus="clearZero(this)" onblur="restoreZero(this)" oninput="formatRupiah(this); hitungTotal()">'
                info_kartu = ''

            rows_html += f"""
            <tr>
                <td style="width: 15%; padding: 10px 20px;"><strong>{kode}</strong></td>
                <td style="width: 45%; padding: 10px 20px;">{acc['nama']}{info_kartu}</td>
                <td style="width: 20%; padding: 10px 20px; text-align: right;">{input_debit}</td>
                <td style="width: 20%; padding: 10px 20px; text-align: right;">{input_kredit}</td>
            </tr>
            """
        
        html_cards += f"""
        <div class="account-card">
            <div style="padding: 12px 20px; font-weight: 600; font-size: 14px; background: #f9fafb; border-bottom: 1px solid #e5e7eb;">{kat.split('—')[1].strip()}</div>
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 15%;">Kode</th>
                        <th style="width: 45%;">Nama Akun</th>
                        <th style="width: 20%; text-align: right;">Debit</th>
                        <th style="width: 20%; text-align: right;">Kredit</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """

    content = f"""
    <div class="page-title">Saldo Awal</div>
    <div class="page-desc">Account Opening Balance per <strong>{tanggal_format_indo}</strong>. Isi debit/kredit saldo awal akun. Piutang, utang, dan persediaan dihitung dari kartu pelanggan, pemasok, dan barang.</div>
    
    <div id="bannerSelisih" style="display: none; background-color: #fef3c7; border: 1px solid #fde68a; color: #b45309; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; font-weight: 500;">
        <span id="textBannerSelisih">Selisih Rp 0 — sementara dimasukkan ke akun <strong>Historical Balancing</strong>. Lengkapi saldo awal sampai seimbang.</span>
    </div>

    <form action="/setup/saldo-awal" method="POST" id="formSaldoAwal" onsubmit="markSaved()">
        {html_cards}
        
        <div style="position: fixed; bottom: 0; left: 260px; right: 0; background: white; padding: 15px 30px; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 -4px 10px rgba(0,0,0,0.03); z-index: 99;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div id="statusSeimbang" style="background-color: #fef2f2; color: #dc2626; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 500; border: 1px solid #fecaca;">
                    ✕ Belum Seimbang
                </div>
                <div id="statusPerubahan" style="color: #ea580c; font-size: 13px; font-weight: 500; display: none;">
                    Ada perubahan yang belum disimpan
                </div>
            </div>
            <button type="submit" class="btn-simpan" style="background-color: #d18a99;">Simpan saldo awal</button>
        </div>
    </form>
    
    <script>
        let hasChanged = false;

        function clearZero(el) {{
            if (el.value === "0") {{ el.value = ""; }}
        }}
        
        function restoreZero(el) {{
            if (el.value === "") {{ el.value = "0"; }}
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
            hasChanged = true;
            document.getElementById('statusPerubahan').style.display = 'block';
            hitungTotal();
        }}

        function markSaved() {{ hasChanged = false; }}

        function hitungTotal() {{
            let totalDebit = 0;
            let totalKredit = 0;

            const inputs = document.querySelectorAll('#formSaldoAwal input[type="text"]');
            inputs.forEach(input => {{
                if(input.id === 'debit_3-9999' || input.id === 'kredit_3-9999') return;
                let val = parseInt(input.value.replace(/\./g, '')) || 0;
                if (input.name.startsWith('debit_')) {{
                    totalDebit += val;
                }} else if (input.name.startsWith('kredit_')) {{
                    totalKredit += val;
                }}
            }});

            const hbDebitInput = document.getElementById('debit_3-9999');
            const hbKreditInput = document.getElementById('kredit_3-9999');
            
            let selisihMurni = totalDebit - totalKredit;

            if(hbDebitInput && hbKreditInput) {{
                hbDebitInput.value = "0";
                hbKreditInput.value = "0";
                
                if (selisihMurni > 0) {{
                    hbKreditInput.value = new Intl.NumberFormat('id-ID').format(selisihMurni);
                }} else if (selisihMurni < 0) {{
                    hbDebitInput.value = new Intl.NumberFormat('id-ID').format(Math.abs(selisihMurni));
                }}
            }}

            const banner = document.getElementById('bannerSelisih');
            const textBanner = document.getElementById('textBannerSelisih');
            const statusBadge = document.getElementById('statusSeimbang');

            if (selisihMurni !== 0) {{
                banner.style.display = 'block';
                let formattedSelisih = new Intl.NumberFormat('id-ID').format(Math.abs(selisihMurni));
                let posisi = selisihMurni > 0 ? 'kredit' : 'debit';
                textBanner.innerHTML = `Selisih Rp ${{formattedSelisih}} — otomatis dimasukkan ke akun <strong>Historical Balancing</strong> (${{posisi}}). Saldo awal belum seimbang.`;
                
                statusBadge.style.backgroundColor = '#fef2f2';
                statusBadge.style.color = '#dc2626';
                statusBadge.style.borderColor = '#fecaca';
                statusBadge.innerHTML = '✕ Belum Seimbang (Selisih Rp ' + formattedSelisih + ')';
            }} else {{
                banner.style.display = 'none';
                statusBadge.style.backgroundColor = '#ecfdf5';
                statusBadge.style.color = '#047857';
                statusBadge.style.borderColor = '#a7f3d0';
                statusBadge.innerHTML = '✓ Seimbang';
            }}
        }}

        window.onload = function() {{ hitungTotal(); }};
    </script>
    """
    return render_dashboard_layout('saldo_awal', content)

@app.route('/kartu/pelanggan')
def kartu_pelanggan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    
    if not list_pelanggan:
        table_html = """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 60px 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="color: #6b7280; font-size: 14px;">Belum ada pelanggan. Klik “+ Pelanggan baru”.</div>
        </div>
        """
    else:
        rows = ""
        total_piutang = 0
        total_sisa_piutang = 0
        for p in list_pelanggan:
            saldo_piutang = int(p.get('saldo_awal_piutang', 0) or 0)
            total_piutang += saldo_piutang
            
            sisa_piutang_dyn = hitung_sisa_piutang_pelanggan(user_data, p.get('nama'))
            total_sisa_piutang += sisa_piutang_dyn

            formatted_piutang = f"{saldo_piutang:,.0f}".replace(',', '.')
            formatted_sisa = f"{sisa_piutang_dyn:,.0f}".replace(',', '.')
            
            rows += f"""
            <tr>
                <td style="padding: 12px 20px;"><strong>{p.get('kode')}</strong></td>
                <td style="padding: 12px 20px;">
                    <div style="font-weight: 600; color: #1f2937;">{p.get('nama')}</div>
                    <div style="font-size: 12px; color: #6b7280;">{p.get('alamat')}</div>
                </td>
                <td style="padding: 12px 20px;">{p.get('telepon')}</td>
                <td style="padding: 12px 20px;">{p.get('syarat_bayar_str')}</td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_piutang}</td>
                <td style="padding: 12px 20px; text-align: right; font-weight: 600; color: #b45309;">{formatted_sisa}</td>
                <td style="padding: 12px 20px; text-align: right;">
                    <div class="action-container">
                        <a href="/kartu/pelanggan/ubah/{p.get('kode')}" class="btn-action">Ubah</a>
                        <a href="/kartu/pelanggan/hapus/{p.get('kode')}" class="btn-action btn-action-danger" onclick="return confirm('Hapus pelanggan {p.get('nama')}?');">Hapus</a>
                    </div>
                </td>
            </tr>
            """
        formatted_total = f"{total_piutang:,.0f}".replace(',', '.')
        formatted_total_sisa = f"{total_sisa_piutang:,.0f}".replace(',', '.')
        table_html = f"""
        <div class="account-card">
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">KODE</th>
                        <th style="width: 25%;">NAMA</th>
                        <th style="width: 15%;">TELEPON</th>
                        <th style="width: 15%;">SYARAT BAYAR</th>
                        <th style="width: 12%; text-align: right;">SALDO AWAL</th>
                        <th style="width: 13%; text-align: right;">SISA PIUTANG</th>
                        <th style="width: 10%; text-align: right;">AKSI</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                    <tr style="background-color: #f9fafb; font-weight: 600;">
                        <td colspan="5" style="padding: 12px 20px;">Total sisa piutang</td>
                        <td style="padding: 12px 20px; text-align: right; color: #b45309;">{formatted_total_sisa}</td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
        <div>
            <div class="page-title">Pelanggan</div>
            <div class="page-desc" style="margin-bottom: 0;">Kartu pelanggan. Saldo awal & total sisa piutang berubah otomatis sesuai penjualan, retur, dan pelunasan.</div>
        </div>
        <div>
            <a href="/kartu/pelanggan/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Pelanggan baru</a>
        </div>
    </div>
    
    {table_html}
    """
    
    modal_html = session.pop('modal_pelanggan', '')
    if modal_html:
        content += modal_html

    return render_dashboard_layout('pelanggan', content)

@app.route('/kartu/pelanggan/baru', methods=['GET', 'POST'])
def tambah_pelanggan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    
    next_num = len(list_pelanggan) + 1
    next_kode = f"C{next_num:03d}"
    
    if request.method == 'POST':
        kode = request.form.get('kode').strip()
        nama = request.form.get('nama').strip()
        alamat = request.form.get('alamat')
        telepon = request.form.get('telepon')
        email_plg = request.form.get('email')
        syarat_pembayaran = request.form.get('syarat_pembayaran')
        
        if syarat_pembayaran == 'Kredit (dengan termin)':
            potongan = request.form.get('potongan', '').strip()
            jika_bayar = request.form.get('jika_bayar', '').strip()
            jatuh_tempo = request.form.get('jatuh_tempo', '30').strip()
            if potongan and jika_bayar:
                syarat_bayar_str = f"{potongan}/{jika_bayar}, n/{jatuh_tempo}"
            else:
                syarat_bayar_str = f"n/{jatuh_tempo}"
        else:
            syarat_bayar_str = "COD"
            potongan = ""
            jika_bayar = ""
            jatuh_tempo = ""
            
        saldo_awal_piutang = request.form.get('saldo_awal_piutang', '0').replace('.', '')
        aktif = True if request.form.get('aktif') else False
        
        new_plg = {
            'kode': kode,
            'nama': nama,
            'alamat': alamat,
            'telepon': telepon,
            'email': email_plg,
            'syarat_pembayaran': syarat_pembayaran,
            'syarat_bayar_str': syarat_bayar_str,
            'potongan': potongan,
            'jika_bayar': jika_bayar,
            'jatuh_tempo': jatuh_tempo,
            'saldo_awal_piutang': saldo_awal_piutang,
            'aktif': aktif
        }
        
        database_user[email]['pelanggan'].append(new_plg)
        sync_saldo_awal_penjualan(email)
        return redirect(url_for('kartu_pelanggan'))

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Pelanggan baru</div>
                <a href="/kartu/pelanggan" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/pelanggan/baru" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{next_kode}" required>
                        </div>
                        <div>
                            <label>Nama <span class="required">*</span></label>
                            <input type="text" name="nama" placeholder="Nama pelanggan" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Alamat</label>
                        <textarea name="alamat" rows="3" placeholder="Alamat lengkap pelanggan"></textarea>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Telepon</label>
                            <input type="text" name="telepon" placeholder="Nomor telepon">
                        </div>
                        <div>
                            <label>Email</label>
                            <input type="text" name="email" placeholder="Alamat email">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Syarat pembayaran</label>
                        <select name="syarat_pembayaran" id="selectSyarat" onchange="toggleTermin()">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="COD — tunai, tanpa termin">COD — tunai, tanpa termin</option>
                        </select>
                    </div>

                    <div id="wrapperTermin" style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px;">
                        <div id="labelTerminHeader" style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">Termin kredit — n/30</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                            <div>
                                <label style="font-size: 12px;">Potongan (%)</label>
                                <input type="text" name="potongan" id="inputPotongan" placeholder="mis. 2" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jika bayar &le; (hari)</label>
                                <input type="text" name="jika_bayar" id="inputJikaBayar" placeholder="mis. 10" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jatuh tempo (hari)</label>
                                <input type="text" name="jatuh_tempo" id="inputJatuhTempo" value="30" oninput="updateLabelTermin()">
                            </div>
                        </div>
                        <div style="font-size: 11px; color: #6b7280; margin-top: 6px;">Contoh 2/10, n/30: potongan 2% jika dibayar &le; 10 hari, jatuh tempo 30 hari.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo awal piutang (Rp)</label>
                        <input type="text" name="saldo_awal_piutang" placeholder="0" oninput="formatRupiah(this)">
                        <div class="form-helper">Per tanggal saldo awal perusahaan</div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" checked style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/pelanggan" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function toggleTermin() {{
            const val = document.getElementById('selectSyarat').value;
            const wrapper = document.getElementById('wrapperTermin');
            if(val.includes('COD')) {{
                wrapper.style.display = 'none';
            }} else {{
                wrapper.style.display = 'block';
            }}
        }}

        function updateLabelTermin() {{
            const pot = document.getElementById('inputPotongan').value.trim();
            const jb = document.getElementById('inputJikaBayar').value.trim();
            const jt = document.getElementById('inputJatuhTempo').value.trim() || '30';
            const header = document.getElementById('labelTerminHeader');
            
            if(pot !== '' && jb !== '') {{
                header.textContent = `Termin kredit — ${{pot}}/${{jb}}, n/${{jt}}`;
            }} else {{
                header.textContent = `Termin kredit — n/${{jt}}`;
            }}
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}
    </script>
    """
    
    session['modal_pelanggan'] = modal_content
    return redirect(url_for('kartu_pelanggan'))

@app.route('/kartu/pelanggan/ubah/<path:kode>', methods=['GET', 'POST'])
def ubah_pelanggan(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    
    target_plg = None
    for p in list_pelanggan:
        if p['kode'] == kode:
            target_plg = p
            break
            
    if not target_plg:
        return redirect(url_for('kartu_pelanggan'))

def hitung_total_piutang_pelanggan(user_data):
    total = 0
    for p in user_data.get('pelanggan', []):
        try:
            val = int(str(p.get('saldo_awal_piutang', 0)).replace('.', '').replace(',', '') or 0)
            total += val
        except Exception:
            pass
            
    # HINT: Jika murni hanya dari saldo awal kartu pelanggan tanpa ditambah 
    # transaksi penjualan berjalan, bagian bawah ini dikosongkan atau tidak usah 
    # menjumlahkan transaksi penjualan baru agar saldo awalnya tetap statis.
    
    return total
        
    if request.method == 'POST':
        target_plg['kode'] = request.form.get('kode').strip()
        target_plg['nama'] = request.form.get('nama').strip()
        target_plg['alamat'] = request.form.get('alamat')
        target_plg['telepon'] = request.form.get('telepon')
        target_plg['email'] = request.form.get('email')
        target_plg['syarat_pembayaran'] = request.form.get('syarat_pembayaran')
        
        if target_plg['syarat_pembayaran'] == 'Kredit (dengan termin)':
            potongan = request.form.get('potongan', '').strip()
            jika_bayar = request.form.get('jika_bayar', '').strip()
            jatuh_tempo = request.form.get('jatuh_tempo', '30').strip()
            target_plg['potongan'] = potongan
            target_plg['jika_bayar'] = jika_bayar
            target_plg['jatuh_tempo'] = jatuh_tempo
            if potongan and jika_bayar:
                target_plg['syarat_bayar_str'] = f"{potongan}/{jika_bayar}, n/{jatuh_tempo}"
            else:
                target_plg['syarat_bayar_str'] = f"n/{jatuh_tempo}"
        else:
            target_plg['syarat_bayar_str'] = "COD"
            target_plg['potongan'] = ""
            target_plg['jika_bayar'] = ""
            target_plg['jatuh_tempo'] = ""
            
        target_plg['saldo_awal_piutang'] = request.form.get('saldo_awal_piutang', '0').replace('.', '')
        target_plg['aktif'] = True if request.form.get('aktif') else False
        sync_saldo_awal_penjualan(email)
        return redirect(url_for('kartu_pelanggan'))

    selected_kredit = "selected" if target_plg.get('syarat_pembayaran') == 'Kredit (dengan termin)' else ""
    selected_cod = "selected" if 'COD' in target_plg.get('syarat_pembayaran', '') else ""
    display_termin = "none" if 'COD' in target_plg.get('syarat_pembayaran', '') else "block"
    checked_aktif = "checked" if target_plg.get('aktif', True) else ""
    
    pot_val = target_plg.get('potongan', '')
    jb_val = target_plg.get('jika_bayar', '')
    jt_val = target_plg.get('jatuh_tempo', '30')
    
    if pot_val and jb_val:
        termin_header_text = f"Termin kredit — {pot_val}/{jb_val}, n/{jt_val}"
    else:
        termin_header_text = f"Termin kredit — n/{jt_val}"

    formatted_piutang = f"{int(target_plg.get('saldo_awal_piutang', 0) or 0):,.0f}".replace(',', '.') if target_plg.get('saldo_awal_piutang') else ""

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Ubah pelanggan</div>
                <a href="/kartu/pelanggan" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/pelanggan/ubah/{kode}" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{target_plg.get('kode')}" required>
                        </div>
                        <div>
                            <label>Nama <span class="required">*</span></label>
                            <input type="text" name="nama" value="{target_plg.get('nama')}" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Alamat</label>
                        <textarea name="alamat" rows="3">{target_plg.get('alamat')}</textarea>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Telepon</label>
                            <input type="text" name="telepon" value="{target_plg.get('telepon')}">
                        </div>
                        <div>
                            <label>Email</label>
                            <input type="text" name="email" value="{target_plg.get('email', '')}">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Syarat pembayaran</label>
                        <select name="syarat_pembayaran" id="selectSyarat" onchange="toggleTermin()">
                            <option value="Kredit (dengan termin)" {selected_kredit}>Kredit (dengan termin)</option>
                            <option value="COD — tunai, tanpa termin" {selected_cod}>COD — tunai, tanpa termin</option>
                        </select>
                    </div>

                    <div id="wrapperTermin" style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px; display: {display_termin};">
                        <div id="labelTerminHeader" style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">{termin_header_text}</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                            <div>
                                <label style="font-size: 12px;">Potongan (%)</label>
                                <input type="text" name="potongan" id="inputPotongan" value="{pot_val}" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jika bayar &le; (hari)</label>
                                <input type="text" name="jika_bayar" id="inputJikaBayar" value="{jb_val}" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jatuh tempo (hari)</label>
                                <input type="text" name="jatuh_tempo" id="inputJatuhTempo" value="{jt_val}" oninput="updateLabelTermin()">
                            </div>
                        </div>
                        <div style="font-size: 11px; color: #6b7280; margin-top: 6px;">Contoh 2/10, n/30: potongan 2% jika dibayar &le; 10 hari, jatuh tempo 30 hari.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo awal piutang (Rp)</label>
                        <input type="text" name="saldo_awal_piutang" value="{formatted_piutang}" oninput="formatRupiah(this)">
                        <div class="form-helper">Per tanggal saldo awal perusahaan</div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" {checked_aktif} style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/pelanggan" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function toggleTermin() {{
            const val = document.getElementById('selectSyarat').value;
            const wrapper = document.getElementById('wrapperTermin');
            if(val.includes('COD')) {{
                wrapper.style.display = 'none';
            }} else {{
                wrapper.style.display = 'block';
            }}
        }}

        function updateLabelTermin() {{
            const pot = document.getElementById('inputPotongan').value.trim();
            const jb = document.getElementById('inputJikaBayar').value.trim();
            const jt = document.getElementById('inputJatuhTempo').value.trim() || '30';
            const header = document.getElementById('labelTerminHeader');
            
            if(pot !== '' && jb !== '') {{
                header.textContent = `Termin kredit — ${{pot}}/${{jb}}, n/${{jt}}`;
            }} else {{
                header.textContent = `Termin kredit — n/${{jt}}`;
            }}
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}
    </script>
    """
    
    session['modal_pelanggan'] = modal_content
    return redirect(url_for('kartu_pelanggan'))

@app.route('/kartu/pelanggan/hapus/<path:kode>')
def hapus_pelanggan(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    email = session['user_email']
    database_user[email]['pelanggan'] = [p for p in database_user[email]['pelanggan'] if p['kode'] != kode]
    sync_saldo_awal_penjualan(email)
    return redirect(url_for('kartu_pelanggan'))

@app.route('/kartu/pemasok')
def kartu_pemasok():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pemasok = user_data.get('pemasok', [])
    
    if not list_pemasok:
        table_html = """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 60px 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="color: #6b7280; font-size: 14px;">Belum ada pemasok. Klik “+ Pemasok baru”.</div>
        </div>
        """
    else:
        rows = ""
        total_utang = 0
        for s in list_pemasok:
            saldo_utang = int(s.get('saldo_awal_utang', 0) or 0)
            total_utang += saldo_utang
            formatted_utang = f"{saldo_utang:,.0f}".replace(',', '.')
            
            rows += f"""
            <tr>
                <td style="padding: 12px 20px;"><strong>{s.get('kode')}</strong></td>
                <td style="padding: 12px 20px;">
                    <div style="font-weight: 600; color: #1f2937;">{s.get('nama')}</div>
                    <div style="font-size: 12px; color: #6b7280;">{s.get('alamat')}</div>
                </td>
                <td style="padding: 12px 20px;">{s.get('telepon')}</td>
                <td style="padding: 12px 20px;">{s.get('syarat_bayar_str')}</td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_utang}</td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_utang}</td>
                <td style="padding: 12px 20px; text-align: right;">
                    <div class="action-container">
                        <a href="/kartu/pemasok/ubah/{s.get('kode')}" class="btn-action">Ubah</a>
                        <a href="/kartu/pemasok/hapus/{s.get('kode')}" class="btn-action btn-action-danger" onclick="return confirm('Hapus pemasok {s.get('nama')}?');">Hapus</a>
                    </div>
                </td>
            </tr>
            """
        formatted_total = f"{total_utang:,.0f}".replace(',', '.')
        table_html = f"""
        <div class="account-card">
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">KODE</th>
                        <th style="width: 25%;">NAMA</th>
                        <th style="width: 15%;">TELEPON</th>
                        <th style="width: 15%;">SYARAT BAYAR</th>
                        <th style="width: 12%; text-align: right;">SALDO AWAL</th>
                        <th style="width: 13%; text-align: right;">SISA UTANG</th>
                        <th style="width: 10%; text-align: right;">AKSI</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                    <tr style="background-color: #f9fafb; font-weight: 600;">
                        <td colspan="5" style="padding: 12px 20px;">Total sisa utang</td>
                        <td style="padding: 12px 20px; text-align: right;">{formatted_total}</td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
        <div>
            <div class="page-title">Pemasok</div>
            <div class="page-desc" style="margin-bottom: 0;">Kartu pemasok. Saldo awal utang menjadi faktur saldo awal SA-&lt;kode&gt; yang bisa dibayar.</div>
        </div>
        <div>
            <a href="/kartu/pemasok/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Pemasok baru</a>
        </div>
    </div>
    
    {table_html}
    """
    
    modal_html = session.pop('modal_pemasok', '')
    if modal_html:
        content += modal_html

    return render_dashboard_layout('pemasok', content)

@app.route('/kartu/pemasok/baru', methods=['GET', 'POST'])
def tambah_pemasok():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    
    # Pastikan key 'pemasok' ada di database user
    if email not in database_user:
        database_user[email] = {}
    if 'pemasok' not in database_user[email]:
        database_user[email]['pemasok'] = []
        
    list_pemasok = database_user[email]['pemasok']
    
    next_num = len(list_pemasok) + 1
    next_kode = f"S{next_num:03d}"
    
    if request.method == 'POST':
        kode = request.form.get('kode', '').strip()
        nama = request.form.get('nama', '').strip()
        alamat = request.form.get('alamat')
        telepon = request.form.get('telepon')
        email_pms = request.form.get('email')
        syarat_pembayaran = request.form.get('syarat_pembayaran')
        
        if syarat_pembayaran == 'Kredit (dengan termin)':
            potongan = request.form.get('potongan', '').strip()
            jika_bayar = request.form.get('jika_bayar', '').strip()
            jatuh_tempo = request.form.get('jatuh_tempo', '30').strip()
            if potongan and jika_bayar:
                syarat_bayar_str = f"{potongan}/{jika_bayar}, n/{jatuh_tempo}"
            else:
                syarat_bayar_str = f"n/{jatuh_tempo}"
        else:
            syarat_bayar_str = "COD"
            potongan = ""
            jika_bayar = ""
            jatuh_tempo = ""
            
        saldo_awal_utang = request.form.get('saldo_awal_utang', '0').replace('.', '')
        aktif = True if request.form.get('aktif') else False
        
        new_pms = {
            'kode': kode,
            'nama': nama,
            'alamat': alamat,
            'telepon': telepon,
            'email': email_pms,
            'syarat_pembayaran': syarat_pembayaran,
            'syarat_bayar_str': syarat_bayar_str,
            'potongan': potongan,
            'jika_bayar': jika_bayar,
            'jatuh_tempo': jatuh_tempo,
            'saldo_awal_utang': saldo_awal_utang,
            'aktif': aktif
        }
        
        database_user[email]['pemasok'].append(new_pms)
        
        # Jika Anda memiliki fungsi sinkronisasi saldo awal pembelian/utang, panggil di sini:
        # sync_saldo_awal_pembelian(email)
        
        return redirect(url_for('kartu_pemasok'))

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Pemasok baru</div>
                <a href="/kartu/pemasok" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/pemasok/baru" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{next_kode}" required>
                        </div>
                        <div>
                            <label>Nama <span class="required">*</span></label>
                            <input type="text" name="nama" placeholder="Nama pemasok" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Alamat</label>
                        <textarea name="alamat" rows="3" placeholder="Alamat lengkap pemasok"></textarea>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Telepon</label>
                            <input type="text" name="telepon" placeholder="Nomor telepon">
                        </div>
                        <div>
                            <label>Email</label>
                            <input type="text" name="email" placeholder="Alamat email">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Syarat pembayaran</label>
                        <select name="syarat_pembayaran" id="selectSyarat" onchange="toggleTermin()">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="COD — tunai, tanpa termin">COD — tunai, tanpa termin</option>
                        </select>
                    </div>

                    <div id="wrapperTermin" style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px;">
                        <div id="labelTerminHeader" style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">Termin kredit — n/30</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                            <div>
                                <label style="font-size: 12px;">Potongan (%)</label>
                                <input type="text" name="potongan" id="inputPotongan" placeholder="mis. 2" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jika bayar &le; (hari)</label>
                                <input type="text" name="jika_bayar" id="inputJikaBayar" placeholder="mis. 10" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jatuh tempo (hari)</label>
                                <input type="text" name="jatuh_tempo" id="inputJatuhTempo" value="30" oninput="updateLabelTermin()">
                            </div>
                        </div>
                        <div style="font-size: 11px; color: #6b7280; margin-top: 6px;">Contoh 2/10, n/30: potongan 2% jika dibayar &le; 10 hari, jatuh tempo 30 hari.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo awal utang (Rp)</label>
                        <input type="text" name="saldo_awal_utang" placeholder="0" oninput="formatRupiah(this)">
                        <div class="form-helper">Per tanggal saldo awal perusahaan</div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" checked style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/pemasok" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function toggleTermin() {{
            const val = document.getElementById('selectSyarat').value;
            const wrapper = document.getElementById('wrapperTermin');
            if(val.includes('COD')) {{
                wrapper.style.display = 'none';
            }} else {{
                wrapper.style.display = 'block';
            }}
        }}

        function updateLabelTermin() {{
            const pot = document.getElementById('inputPotongan').value.trim();
            const jb = document.getElementById('inputJikaBayar').value.trim();
            const jt = document.getElementById('inputJatuhTempo').value.trim() || '30';
            const header = document.getElementById('labelTerminHeader');
            
            if(pot !== '' && jb !== '') {{
                header.textContent = `Termin kredit — ${{pot}}/${{jb}}, n/${{jt}}`;
            }} else {{
                header.textContent = `Termin kredit — n/${{jt}}`;
            }}
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}
    </script>
    """
    
    session['modal_pemasok'] = modal_content
    return redirect(url_for('kartu_pemasok'))

@app.route('/kartu/pemasok/ubah/<path:kode>', methods=['GET', 'POST'])
def ubah_pemasok(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pemasok = user_data.get('pemasok', [])
    
    target_pms = None
    for p in list_pemasok:
        if p['kode'] == kode:
            target_pms = p
            break
            
    if not target_pms:
        return redirect(url_for('kartu_pemasok'))
    
    # Tambahkan logika ubah data pemasok di sini jika diperlukan
 
def hitung_total_utang_pemasok(user_data):
    total = 0
    for s in user_data.get('pemasok', []):
        try:
            val = int(s.get('saldo_awal_utang', 0) or 0)
            total += val
        except Exception:
            pass
    # Tambahkan dari transaksi pembelian kredit baru jika ada
    for tr in user_data.get('pembelian', []):
        try:
            if tr.get('status') != 'Lunas':
                total += int(str(tr.get('sisa', tr.get('total', 0))).replace('.', '') or 0)
        except:
            pass
    return total

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Pemasok baru</div>
                <a href="/kartu/pemasok" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/pemasok/baru" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{next_kode}" required>
                        </div>
                        <div>
                            <label>Nama <span class="required">*</span></label>
                            <input type="text" name="nama" placeholder="Nama pemasok" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Alamat</label>
                        <textarea name="alamat" rows="3" placeholder="Alamat lengkap pemasok"></textarea>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Telepon</label>
                            <input type="text" name="telepon" placeholder="Nomor telepon">
                        </div>
                        <div>
                            <label>Email</label>
                            <input type="text" name="email" placeholder="Alamat email">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Syarat pembayaran</label>
                        <select name="syarat_pembayaran" id="selectSyarat" onchange="toggleTermin()">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="COD — tunai, tanpa termin">COD — tunai, tanpa termin</option>
                        </select>
                    </div>

                    <div id="wrapperTermin" style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px;">
                        <div id="labelTerminHeader" style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">Termin kredit — n/30</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                            <div>
                                <label style="font-size: 12px;">Potongan (%)</label>
                                <input type="text" name="potongan" id="inputPotongan" placeholder="mis. 2" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jika bayar &le; (hari)</label>
                                <input type="text" name="jika_bayar" id="inputJikaBayar" placeholder="mis. 10" oninput="updateLabelTermin()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Jatuh tempo (hari)</label>
                                <input type="text" name="jatuh_tempo" id="inputJatuhTempo" value="30" oninput="updateLabelTermin()">
                            </div>
                        </div>
                        <div style="font-size: 11px; color: #6b7280; margin-top: 6px;">Contoh 2/10, n/30: potongan 2% jika dibayar &le; 10 hari, jatuh tempo 30 hari.</div>
                    </div>

                    <div class="form-group">
                        <label>Saldo awal utang (Rp)</label>
                        <input type="text" name="saldo_awal_utang" placeholder="0" oninput="formatRupiah(this)">
                        <div class="form-helper">Per tanggal saldo awal perusahaan</div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" checked style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/pemasok" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function toggleTermin() {{
            const val = document.getElementById('selectSyarat').value;
            const wrapper = document.getElementById('wrapperTermin');
            if(val.includes('COD')) {{
                wrapper.style.display = 'none';
            }} else {{
                wrapper.style.display = 'block';
            }}
        }}

        function updateLabelTermin() {{
            const pot = document.getElementById('inputPotongan').value.trim();
            const jb = document.getElementById('inputJikaBayar').value.trim();
            const jt = document.getElementById('inputJatuhTempo').value.trim() || '30';
            const header = document.getElementById('labelTerminHeader');
            
            if(pot !== '' && jb !== '') {{
                header.textContent = `Termin kredit — ${{pot}}/${{jb}}, n/${{jt}}`;
            }} else {{
                header.textContent = `Termin kredit — n/${{jt}}`;
            }}
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}
    </script>
    """
    
    session['modal_pemasok'] = modal_content
    return redirect(url_for('kartu_pemasok'))


@app.route('/kartu/pemasok/hapus/<path:kode>')
def hapus_pemasok(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    email = session['user_email']
    database_user[email]['pemasok'] = [s for s in database_user[email]['pemasok'] if s['kode'] != kode]
    return redirect(url_for('kartu_pemasok'))

@app.route('/kartu/barang')
def kartu_barang():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_barang = user_data.get('barang', [])
    
    if not list_barang:
        table_html = """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 60px 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="color: #6b7280; font-size: 14px;">Belum ada barang.</div>
        </div>
        """
    else:
        rows = ""
        total_nilai_persediaan = 0
        for b in list_barang:
            qty = float(b.get('qty_awal', 0) or 0)
            hp = float(b.get('harga_pokok', 0) or 0)
            hj = float(b.get('harga_jual', 0) or 0)
            nilai = int(qty * hp)
            total_nilai_persediaan += nilai
            
            formatted_hj = f"{hj:,.0f}".replace(',', '.') if hj > 0 else "0"
            formatted_hp = f"{hp:,.0f}".replace(',', '.') if hp > 0 else "0"
            formatted_nilai = f"{nilai:,.0f}".replace(',', '.')
            formatted_qty = f"{int(qty):,}".replace(',', '.') if qty.is_integer() else f"{qty:,.2f}".replace(',', '.')
            
            rows += f"""
            <tr>
                <td style="padding: 12px 20px;"><strong>{b.get('kode')}</strong></td>
                <td style="padding: 12px 20px;">
                    <div style="font-weight: 600; color: #1f2937;">{b.get('nama')}</div>
                    <div style="font-size: 12px; color: #6b7280;">Saldo awal: {formatted_qty} {b.get('satuan')} × {formatted_hp}</div>
                </td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_hj}</td>
                <td style="padding: 12px 20px;">{formatted_qty} {b.get('satuan')}</td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_hp}</td>
                <td style="padding: 12px 20px; text-align: right;">{formatted_nilai}</td>
                <td style="padding: 12px 20px; text-align: right;">
                    <div class="action-container">
                        <a href="/kartu/barang/stok/{b.get('kode')}" class="btn-action" style="background-color: #e5e7eb; color: #374151; padding: 6px 12px; border-radius: 4px; text-decoration: none;">Kartu stok</a>
                        <a href="/kartu/barang/ubah/{b.get('kode')}" class="btn-action">Ubah</a>
                        <a href="/kartu/barang/hapus/{b.get('kode')}" class="btn-action btn-action-danger" onclick="return confirm('Hapus barang {b.get('nama')}?');">Hapus</a>
                    </div>
                </td>
            </tr>
            """
        formatted_total = f"{total_nilai_persediaan:,.0f}".replace(',', '.')
        table_html = f"""
        <div class="account-card">
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">KODE</th>
                        <th style="width: 25%;">NAMA BARANG</th>
                        <th style="width: 12%; text-align: right;">HARGA JUAL</th>
                        <th style="width: 12%;">QTY</th>
                        <th style="width: 13%; text-align: right;">HARGA RATA-RATA</th>
                        <th style="width: 14%; text-align: right;">NILAI PERSEDIAAN</th>
                        <th style="width: 14%; text-align: right;">AKSI</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                    <tr style="background-color: #f9fafb; font-weight: 600;">
                        <td colspan="5" style="padding: 12px 20px;">Total nilai persediaan</td>
                        <td style="padding: 12px 20px; text-align: right;">{formatted_total}</td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
        <div>
            <div class="page-title">Barang</div>
            <div class="page-desc" style="margin-bottom: 0;">Kartu barang. Persediaan perpetual dengan metode rata-rata bergerak. Saldo awal = qty awal × harga pokok.</div>
        </div>
        <div>
            <a href="/kartu/barang/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Barang baru</a>
        </div>
    </div>
    
    {table_html}
    """
    
    modal_html = session.pop('modal_barang', '')
    if modal_html:
        content += modal_html

    return render_dashboard_layout('barang', content)

@app.route('/kartu/barang/baru', methods=['GET', 'POST'])
def tambah_barang():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_barang = user_data.get('barang', [])
    
    next_num = len(list_barang) + 1
    next_kode = f"B{next_num:03d}"
    
    if request.method == 'POST':
        kode = request.form.get('kode').strip()
        nama = request.form.get('nama').strip()
        satuan = request.form.get('satuan').strip()
        harga_jual = request.form.get('harga_jual', '0').replace('.', '')
        qty_awal = request.form.get('qty_awal', '0').replace('.', '')
        harga_pokok = request.form.get('harga_pokok', '0').replace('.', '')
        aktif = True if request.form.get('aktif') else False
        
        new_brg = {
            'kode': kode,
            'nama': nama,
            'satuan': satuan,
            'harga_jual': harga_jual,
            'qty_awal': qty_awal,
            'harga_pokok': harga_pokok,
            'aktif': aktif
        }
        
        database_user[email]['barang'].append(new_brg)
        return redirect(url_for('kartu_barang'))

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Barang baru</div>
                <a href="/kartu/barang" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/barang/baru" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{next_kode}" required>
                        </div>
                        <div>
                            <label>Nama barang <span class="required">*</span></label>
                            <input type="text" name="nama" placeholder="Nama barang" required>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Satuan</label>
                            <input type="text" name="satuan" value="pcs">
                        </div>
                        <div>
                            <label>Harga jual (Rp)</label>
                            <input type="text" name="harga_jual" placeholder="0" oninput="formatRupiah(this)">
                        </div>
                    </div>

                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px;">
                        <div style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">Saldo awal persediaan</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; align-items: center;">
                            <div>
                                <label style="font-size: 12px;">Qty awal</label>
                                <input type="text" name="qty_awal" id="inputQty" placeholder="0" oninput="hitungNilaiPersediaan()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Harga pokok / unit</label>
                                <input type="text" name="harga_pokok" id="inputHargaPokok" placeholder="0" oninput="formatRupiah(this); hitungNilaiPersediaan();">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Nilai</label>
                                <div id="displayNilai" style="font-weight: 600; font-size: 16px; color: #1f2937; padding: 8px 0;">0</div>
                            </div>
                        </div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" checked style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/barang" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}

        function hitungNilaiPersediaan() {{
            const qty = parseFloat(document.getElementById('inputQty').value.replace(/\./g, '')) || 0;
            const hp = parseFloat(document.getElementById('inputHargaPokok').value.replace(/\./g, '')) || 0;
            const total = qty * hp;
            document.getElementById('displayNilai').textContent = new Intl.NumberFormat('id-ID').format(total);
        }}
    </script>
    """
    
    session['modal_barang'] = modal_content
    return redirect(url_for('kartu_barang'))

@app.route('/kartu/barang/ubah/<path:kode>', methods=['GET', 'POST'])
def ubah_barang(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_barang = user_data.get('barang', [])
    
    target_brg = None
    for b in list_barang:
        if b['kode'] == kode:
            target_brg = b
            break
            
    if not target_brg:
        return redirect(url_for('kartu_barang'))
        
    if request.method == 'POST':
        target_brg['kode'] = request.form.get('kode').strip()
        target_brg['nama'] = request.form.get('nama').strip()
        target_brg['satuan'] = request.form.get('satuan').strip()
        target_brg['harga_jual'] = request.form.get('harga_jual', '0').replace('.', '')
        target_brg['qty_awal'] = request.form.get('qty_awal', '0').replace('.', '')
        target_brg['harga_pokok'] = request.form.get('harga_pokok', '0').replace('.', '')
        target_brg['aktif'] = True if request.form.get('aktif') else False
        return redirect(url_for('kartu_barang'))

    checked_aktif = "checked" if target_brg.get('aktif', True) else ""
    
    hj_val = f"{int(target_brg.get('harga_jual', 0) or 0):,.0f}".replace(',', '.') if target_brg.get('harga_jual') else ""
    qty_raw = float(target_brg.get('qty_awal', 0) or 0)
    qty_val = f"{int(qty_raw):,}".replace(',', '.') if qty_raw.is_integer() else f"{qty_raw}"
    hp_val = f"{float(target_brg.get('harga_pokok', 0) or 0):,.0f}".replace(',', '.') if target_brg.get('harga_pokok') else ""
    
    initial_nilai = int(qty_raw * (float(target_brg.get('harga_pokok', 0) or 0)))
    formatted_initial_nilai = f"{initial_nilai:,.0f}".replace(',', '.')

    modal_content = f"""
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 18px; font-weight: bold; color: #1f2937;">Ubah barang</div>
                <a href="/kartu/barang" style="color: #6b7280; font-size: 20px; text-decoration: none; font-weight: bold;">✕</a>
            </div>
            <div class="modal-body">
                <form action="/kartu/barang/ubah/{kode}" method="POST">
                    
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Kode <span class="required">*</span></label>
                            <input type="text" name="kode" value="{target_brg.get('kode')}" required>
                        </div>
                        <div>
                            <label>Nama barang <span class="required">*</span></label>
                            <input type="text" name="nama" value="{target_brg.get('nama')}" required>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;" class="form-group">
                        <div>
                            <label>Satuan</label>
                            <input type="text" name="satuan" value="{target_brg.get('satuan', 'pcs')}">
                        </div>
                        <div>
                            <label>Harga jual (Rp)</label>
                            <input type="text" name="harga_jual" value="{hj_val}" oninput="formatRupiah(this)">
                        </div>
                    </div>

                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 20px;">
                        <div style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 10px;">Saldo awal persediaan</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; align-items: center;">
                            <div>
                                <label style="font-size: 12px;">Qty awal</label>
                                <input type="text" name="qty_awal" id="inputQty" value="{qty_val}" oninput="hitungNilaiPersediaan()">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Harga pokok / unit</label>
                                <input type="text" name="harga_pokok" id="inputHargaPokok" value="{hp_val}" oninput="formatRupiah(this); hitungNilaiPersediaan();">
                            </div>
                            <div>
                                <label style="font-size: 12px;">Nilai</label>
                                <div id="displayNilai" style="font-weight: 600; font-size: 16px; color: #1f2937; padding: 8px 0;">{formatted_initial_nilai}</div>
                            </div>
                        </div>
                    </div>

                    <div class="form-group" style="display: flex; align-items: center; gap: 8px; margin-top: 10px;">
                        <input type="checkbox" name="aktif" {checked_aktif} style="width: 16px; height: 16px; accent-color: #d18a99;">
                        <label style="margin-bottom: 0; font-weight: 400; color: #1f2937;">Aktif</label>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <a href="/kartu/barang" class="btn-batal">Batal</a>
                        <button type="submit" class="btn-simpan">Simpan</button>
                    </div>

                </form>
            </div>
        </div>
    </div>
    
    <script>
        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{
                el.value = "";
            }} else {{
                let formatted = new Intl.NumberFormat('id-ID').format(angka);
                el.value = formatted;
            }}
        }}

        function hitungNilaiPersediaan() {{
            const qty = parseFloat(document.getElementById('inputQty').value.replace(/\./g, '')) || 0;
            const hp = parseFloat(document.getElementById('inputHargaPokok').value.replace(/\./g, '')) || 0;
            const total = qty * hp;
            document.getElementById('displayNilai').textContent = new Intl.NumberFormat('id-ID').format(total);
        }}
    </script>
    """
    
    session['modal_barang'] = modal_content
    return redirect(url_for('kartu_barang'))

def hitung_total_persediaan_barang(user_data):
    total = 0
    for b in user_data.get('barang', []):
        try:
            qty = float(b.get('qty_awal', 0) or 0)
            hp = float(b.get('harga_pokok', 0) or 0)
            # Anda bisa menyelaraskan dengan sisa qty di kartu stok berjalan jika sudah ada fungsi mutasinya
            total += int(qty * hp)
        except Exception:
            pass
    return total

@app.route('/kartu/barang/stok/<path:kode>')
def kartu_stok_barang(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_barang = user_data.get('barang', [])
    
    target_brg = None
    for b in list_barang:
        if b['kode'] == kode:
            target_brg = b
            break
            
    if not target_brg:
        return redirect(url_for('kartu_barang'))
        
    # Ambil data saldo awal
    qty_awal = float(target_brg.get('qty_awal', 0) or 0)
    harga_pokok_awal = float(target_brg.get('harga_pokok', 0) or 0)
    harga_jual = float(target_brg.get('harga_jual', 0) or 0)
    
    mutasi_list = []
    
    # State awal untuk perhitungan moving average
    current_qty = qty_awal
    current_rata = harga_pokok_awal
    current_nilai = int(current_qty * current_rata)
    
    # 1. Masukkan Saldo Awal sebagai baris pertama
    mutasi_list.append({
        'tanggal': '2026-01-01',
        'bukti': 'Saldo awal',
        'ket': 'Saldo awal persediaan',
        'masuk_qty': '', 'masuk_harga': '', 'masuk_jumlah': '',
        'keluar_qty': '', 'keluar_harga': '', 'keluar_jumlah': '',
        'saldo_qty': current_qty,
        'saldo_rata': current_rata,
        'saldo_nilai': current_nilai,
        'timestamp': '2026-01-01 00:00'
    })
    
    # 2. Tarik dan gabungkan seluruh transaksi (Penjualan, Pembelian, Retur Penjualan, Retur Pembelian)
    transaksi_barang = []

    # A. Penjualan (Mengurangi Stok)
    for trx in user_data.get('penjualan', []):
        if trx.get('is_saldo_awal', False):
            continue
        for det in trx.get('details', []):
            brg_str = det.get('barang', '')
            kode_brg_match = brg_str.split(' - ')[0].strip() if ' - ' in brg_str else brg_str
            if kode_brg_match == kode:
                transaksi_barang.append({
                    'tanggal': trx.get('tanggal'),
                    'no_bukti': trx.get('nomor'),
                    'jenis': 'penjualan',
                    'qty': float(det.get('qty', 0)),
                    'harga': float(det.get('harga', 0)),
                    'relasi': trx.get('pelanggan')
                })

    # B. Pembelian (Menambah Stok)
    for trx in user_data.get('pembelian', []):
        for det in trx.get('details', []):
            brg_str = det.get('barang', '')
            kode_brg_match = brg_str.split(' - ')[0].strip() if ' - ' in brg_str else brg_str
            if kode_brg_match == kode:
                transaksi_barang.append({
                    'tanggal': trx.get('tanggal'),
                    'no_bukti': trx.get('nomor'),
                    'jenis': 'pembelian',
                    'qty': float(det.get('qty', 0)),
                    'harga': float(det.get('harga', 0)),
                    'relasi': trx.get('pemasok')
                })

    # C. Retur Penjualan (Menambah Stok - Barang kembali dari pelanggan)
    for trx in user_data.get('retur_penjualan', []):
        for det in trx.get('details', []):
            brg_str = det.get('barang', '')
            kode_brg_match = brg_str.split(' - ')[0].strip() if ' - ' in brg_str else brg_str
            if kode_brg_match == kode:
                transaksi_barang.append({
                    'tanggal': trx.get('tanggal'),
                    'no_bukti': trx.get('nomor'),
                    'jenis': 'retur_penjualan',
                    'qty': float(det.get('qty', 0)),
                    'harga': float(det.get('harga', 0)),
                    'relasi': trx.get('pelanggan')
                })

    # D. Retur Pembelian (Mengurangi Stok - Barang dikembalikan ke pemasok)
    for trx in user_data.get('retur_pembelian', []):
        for det in trx.get('details', []):
            brg_str = det.get('barang', '')
            kode_brg_match = brg_str.split(' - ')[0].strip() if ' - ' in brg_str else brg_str
            if kode_brg_match == kode:
                transaksi_barang.append({
                    'tanggal': trx.get('tanggal'),
                    'no_bukti': trx.get('nomor'),
                    'jenis': 'retur_pembelian',
                    'qty': float(det.get('qty', 0)),
                    'harga': float(det.get('harga', 0)),
                    'relasi': trx.get('pemasok')
                })

    # Urutkan transaksi secara kronologis berdasarkan tanggal
    transaksi_barang = sorted(transaksi_barang, key=lambda x: x.get('tanggal', ''))

    # 3. Proses Mutasi Stok & Moving Average
    for trx in transaksi_barang:
        tgl = trx.get('tanggal', '')
        bukti = trx.get('no_bukti', '')
        relasi = trx.get('relasi', '')
        jenis = trx.get('jenis', '').lower()
        qty_trx = float(trx.get('qty', 0))
        harga_trx = float(trx.get('harga', 0))
        
        masuk_q, masuk_h, masuk_j = '', '', ''
        keluar_q, keluar_h, keluar_j = '', '', ''
        
        if jenis in ['pembelian', 'retur_penjualan']:
            # Barang Masuk Gudang (Menambah Stok)
            masuk_q = qty_trx
            masuk_h = harga_trx if jenis == 'pembelian' else current_rata
            masuk_j = int(masuk_q * masuk_h)
            
            total_qty_baru = current_qty + masuk_q
            if total_qty_baru > 0:
                total_nilai_baru = current_nilai + masuk_j
                current_rata = total_nilai_baru / total_qty_baru
                current_nilai = int(total_qty_baru * current_rata)
            current_qty = total_qty_baru
            
        elif jenis in ['penjualan', 'retur_pembelian']:
            # Barang Keluar Gudang (Mengurangi Stok)
            keluar_q = qty_trx
            keluar_h = current_rata # Menggunakan HPP rata-rata berjalan
            keluar_j = int(keluar_q * keluar_h)
            
            current_qty -= keluar_q
            current_nilai = int(current_qty * current_rata)
            if current_qty <= 0:
                current_qty = 0
                current_nilai = 0
                current_rata = 0

        mutasi_list.append({
            'tanggal': tgl,
            'bukti': bukti,
            'ket': relasi,
            'masuk_qty': masuk_q if masuk_q != '' else '',
            'masuk_harga': masuk_h if masuk_h != '' else '',
            'masuk_jumlah': masuk_j if masuk_j != '' else '',
            'keluar_qty': keluar_q if keluar_q != '' else '',
            'keluar_harga': keluar_h if keluar_h != '' else '',
            'keluar_jumlah': keluar_j if keluar_j != '' else '',
            'saldo_qty': current_qty,
            'saldo_rata': current_rata,
            'saldo_nilai': current_nilai
        })

    # Render baris tabel HTML
    rows_mutasi = ""
    for m in mutasi_list:
        m_qty_in = f"{int(m['masuk_qty']):,}".replace(',', '.') if isinstance(m['masuk_qty'], (int, float)) and m['masuk_qty'] > 0 else ""
        m_harga_in = f"{m['masuk_harga']:,.0f}".replace(',', '.') if isinstance(m['masuk_harga'], (int, float)) and m['masuk_harga'] > 0 else ""
        m_jml_in = f"{m['masuk_jumlah']:,.0f}".replace(',', '.') if isinstance(m['masuk_jumlah'], (int, float)) and m['masuk_jumlah'] > 0 else ""
        
        m_qty_out = f"{int(m['keluar_qty']):,}".replace(',', '.') if isinstance(m['keluar_qty'], (int, float)) and m['keluar_qty'] > 0 else ""
        m_harga_out = f"{m['keluar_harga']:,.0f}".replace(',', '.') if isinstance(m['keluar_harga'], (int, float)) and m['keluar_harga'] > 0 else ""
        m_jml_out = f"{m['keluar_jumlah']:,.0f}".replace(',', '.') if isinstance(m['keluar_jumlah'], (int, float)) and m['keluar_jumlah'] > 0 else ""
        
        s_qty = f"{int(m['saldo_qty']):,}".replace(',', '.') if isinstance(m['saldo_qty'], (int, float)) else "0"
        s_rata = f"{m['saldo_rata']:,.0f}".replace(',', '.') if isinstance(m['saldo_rata'], (int, float)) else "0"
        s_nilai = f"{m['saldo_nilai']:,.0f}".replace(',', '.') if isinstance(m['saldo_nilai'], (int, float)) else "0"
        
        rows_mutasi += f"""
        <tr>
            <td style="padding: 12px 15px;">{m['tanggal']}</td>
            <td style="padding: 12px 15px;"><strong>{m['bukti']}</strong><br><span style="font-size: 11px; color: #6b7280;">{m['ket']}</span></td>
            <td style="padding: 12px 15px; text-align: right;">{m_qty_in}</td>
            <td style="padding: 12px 15px; text-align: right;">{m_harga_in}</td>
            <td style="padding: 12px 15px; text-align: right;">{m_jml_in}</td>
            <td style="padding: 12px 15px; text-align: right;">{m_qty_out}</td>
            <td style="padding: 12px 15px; text-align: right;">{m_harga_out}</td>
            <td style="padding: 12px 15px; text-align: right;">{m_jml_out}</td>
            <td style="padding: 12px 15px; text-align: right; font-weight: 600;">{s_qty}</td>
            <td style="padding: 12px 15px; text-align: right;">{s_rata}</td>
            <td style="padding: 12px 15px; text-align: right; font-weight: 600;">{s_nilai}</td>
        </tr>
        """

    formatted_hj_Header = f"Rp {harga_jual:,.0f}".replace(',', '.') if harga_jual > 0 else "Rp 0"
    formatted_rata_Header = f"Rp {current_rata:,.0f}".replace(',', '.')
    formatted_nilai_Header = f"Rp {current_nilai:,.0f}".replace(',', '.')
    formatted_qty_Header = f"{int(current_qty):,} {target_brg.get('satuan', 'pcs')}".replace(',', '.')

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title" style="font-size: 20px; font-weight: bold;">Kartu Persediaan — {target_brg.get('nama').upper()}</div>
            <div class="page-desc" style="color: #6b7280; font-size: 13px; margin-top: 4px;">Metode rata-rata bergerak (moving average). Terhubung otomatis dengan Penjualan, Pembelian, Retur Penjualan, dan Retur Pembelian.</div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/kartu/barang" style="background-color: #ffffff; border: 1px solid #d1d5db; color: #374151; padding: 8px 14px; border-radius: 6px; font-size: 13px; text-decoration: none; font-weight: 500;">← Daftar barang</a>
            <button onclick="window.print()" style="background-color: #ffffff; border: 1px solid #d1d5db; color: #374151; padding: 8px 14px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: 500;">Cetak</button>
        </div>
    </div>

    <!-- Kotak Ringkasan Atas -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
        <div style="background: #ffffff; padding: 15px 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Qty akhir</div>
            <div style="font-size: 18px; font-weight: 700; color: #1f2937;">{formatted_qty_Header}</div>
        </div>
        <div style="background: #ffffff; padding: 15px 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Harga rata-rata</div>
            <div style="font-size: 18px; font-weight: 700; color: #1f2937;">{formatted_rata_Header}</div>
        </div>
        <div style="background: #ffffff; padding: 15px 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Nilai persediaan</div>
            <div style="font-size: 18px; font-weight: 700; color: #1f2937;">{formatted_nilai_Header}</div>
        </div>
        <div style="background: #ffffff; padding: 15px 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Harga jual</div>
            <div style="font-size: 18px; font-weight: 700; color: #1f2937;">{formatted_hj_Header}</div>
        </div>
    </div>

    <!-- Tabel Rinci Kartu Stok -->
    <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="background-color: #f9fafb; border-bottom: 1px solid #e5e7eb; color: #4b5563; text-align: left;">
                    <th style="padding: 12px 15px; width: 10%;">TANGGAL</th>
                    <th style="padding: 12px 15px; width: 18%;">BUKTI</th>
                    <th style="padding: 12px 15px; text-align: right;" colspan="3">MASUK</th>
                    <th style="padding: 12px 15px; text-align: right;" colspan="3">KELUAR (HPP)</th>
                    <th style="padding: 12px 15px; text-align: right;" colspan="3">SALDO</th>
                </tr>
                <tr style="background-color: #fdfdfd; border-bottom: 1px solid #e5e7eb; color: #6b7280; font-size: 11px;">
                    <th style="padding: 6px 15px;"></th>
                    <th style="padding: 6px 15px;"></th>
                    <th style="padding: 6px 15px; text-align: right;">QTY</th>
                    <th style="padding: 6px 15px; text-align: right;">HARGA</th>
                    <th style="padding: 6px 15px; text-align: right;">JUMLAH</th>
                    <th style="padding: 6px 15px; text-align: right;">QTY</th>
                    <th style="padding: 6px 15px; text-align: right;">HARGA</th>
                    <th style="padding: 6px 15px; text-align: right;">JUMLAH</th>
                    <th style="padding: 6px 15px; text-align: right;">QTY</th>
                    <th style="padding: 6px 15px; text-align: right;">RATA-RATA</th>
                    <th style="padding: 6px 15px; text-align: right;">NILAI</th>
                </tr>
            </thead>
            <tbody>
                {rows_mutasi}
            </tbody>
        </table>
    </div>
    """

    return render_dashboard_layout('barang', content)

@app.route('/kartu/barang/hapus/<path:kode>')
def hapus_barang(kode):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    email = session['user_email']
    database_user[email]['barang'] = [b for b in database_user[email]['barang'] if b['kode'] != kode]
    return redirect(url_for('kartu_barang'))

@app.route('/transaksi/penjualan')
def transaksi_penjualan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    sync_saldo_awal_penjualan(email)
    list_penjualan = user_data.get('penjualan', [])

    if not list_penjualan:
        table_penjualan_html = """
        <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
            Tidak ada transaksi pada periode ini.
        </div>
        """
        table_jurnal_html = """
        <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
            Belum ada jurnal pada periode ini.
        </div>
        """
    else:
        rows_p = ""
        rows_j = ""
        total_nilai_trx = 0
        total_nilai_sisa = 0
        count_trx = 0
        count_jurnal = 0
        
        sum_piutang = 0
        sum_hpp = 0
        sum_persediaan = 0
        sum_ppn = 0
        sum_penjualan = 0

        for tr in list_penjualan:
            count_trx += 1
            try:
                t_val = int(tr.get('total', '0').replace('.', ''))
            except:
                t_val = 0
            total_nilai_trx += t_val
            
            sisa_str = tr.get('sisa', tr.get('total'))
            try:
                s_val = int(str(sisa_str).replace('.', ''))
            except:
                s_val = t_val
            total_nilai_sisa += s_val

            no_faktur_display = tr.get('nomor')
            if tr.get('is_saldo_awal', False):
                no_faktur_display += ' <span class="badge-saldo-awal">Saldo awal</span>'

            detail_url = f"/transaksi/penjualan/ubah/{tr.get('nomor')}"
            
            status_badge_html = f'<span class="badge-lunas">Lunas</span>' if s_val == 0 else f'<span class="badge-belum-lunas">{tr.get("status", "Belum lunas")}</span>'

            rows_p += f"""
            <tr>
                <td style="padding: 12px 20px;">{tr.get('tanggal_indo', tr.get('tanggal'))}</td>
                <td style="padding: 12px 20px;"><a href="{detail_url}" style="color: #d18a99; font-weight: 600; text-decoration: none;">{no_faktur_display}</a></td>
                <td style="padding: 12px 20px;">{tr.get('pelanggan')}</td>
                <td style="padding: 12px 20px;">{status_badge_html}</td>
                <td style="padding: 12px 20px;">{tr.get('jatuh_tempo', '-')}</td>
                <td style="padding: 12px 20px; text-align: right;">{tr.get('total')}</td>
                <td style="padding: 12px 20px; text-align: right; color: #b45309; font-weight: 500;">{f"{s_val:,.0f}".replace(',', '.')}</td>
            </tr>
            """
            
            if tr.get('is_saldo_awal', False):
                continue

            count_jurnal += 1
            piutang_val = t_val
            hpp_val = int(tr.get('total_hpp', 0) or 0)
            persediaan_val = hpp_val
            
            dpp_val = int(tr.get('dpp', 0) or 0)
            ppn_val = int(tr.get('ppn', 0) or 0)
            if dpp_val == 0 and ppn_val == 0:
                ppn_persen = float(tr.get('ppn_persen', 0) or 0)
                if ppn_persen > 0:
                    dpp_val = int(piutang_val / (1 + ppn_persen / 100))
                    ppn_val = piutang_val - dpp_val
                else:
                    dpp_val = piutang_val
                    ppn_val = 0

            sum_piutang += piutang_val
            sum_hpp += hpp_val
            sum_persediaan += persediaan_val
            sum_ppn += ppn_val
            sum_penjualan += dpp_val

            ket_jurnal = f"Penjualan kredit - {tr.get('pelanggan')}"
            if tr.get('memo'):
                ket_jurnal += f" ({tr.get('memo')})"

            rows_j += f"""
            <tr>
                <td style="padding: 12px 20px; white-space: nowrap;">{tr.get('tanggal_indo', tr.get('tanggal'))}</td>
                <td style="padding: 12px 20px;"><a href="{detail_url}" style="color: #d18a99; font-weight: 600; text-decoration: none;">{tr.get('nomor')}</a></td>
                <td style="padding: 12px 20px;">{ket_jurnal}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{piutang_val:,.0f}".replace(',', '.') if piutang_val > 0 else '-'}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{hpp_val:,.0f}".replace(',', '.') if hpp_val > 0 else '-'}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{persediaan_val:,.0f}".replace(',', '.') if persediaan_val > 0 else '-'}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{ppn_val:,.0f}".replace(',', '.') if ppn_val > 0 else '-'}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{dpp_val:,.0f}".replace(',', '.') if dpp_val > 0 else '-'}</td>
            </tr>
            """
            
        formatted_total_trx = f"{total_nilai_trx:,.0f}".replace(',', '.')
        formatted_total_sisa = f"{total_nilai_sisa:,.0f}".replace(',', '.')
        
        table_penjualan_html = f"""
        <table class="account-table">
            <thead>
                <tr>
                    <th style="width: 13%;">TANGGAL</th>
                    <th style="width: 20%;">NO. FAKTUR</th>
                    <th style="width: 25%;">PELANGGAN</th>
                    <th style="width: 12%;">STATUS</th>
                    <th style="width: 12%;">JATUH TEMPO</th>
                    <th style="width: 13%; text-align: right;">TOTAL</th>
                    <th style="width: 13%; text-align: right;">SISA</th>
                </tr>
            </thead>
            <tbody>
                {rows_p}
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="5" style="padding: 12px 20px;">Total ({count_trx} transaksi)</td>
                    <td style="padding: 12px 20px; text-align: right;">{formatted_total_trx}</td>
                    <td style="padding: 12px 20px; text-align: right; color: #b45309;">{formatted_total_sisa}</td>
                </tr>
            </tbody>
        </table>
        """

        if count_jurnal == 0:
            table_jurnal_html = """
            <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
                Belum ada transaksi penjualan baru (saldo awal pelanggan tidak dimasukkan ke jurnal penjualan).
            </div>
            """
        else:
            table_jurnal_html = f"""
            <div style="overflow-x: auto;">
            <table class="account-table" style="min-width: 950px;">
                <thead>
                    <tr>
                        <th rowspan="2" style="width: 12%; vertical-align: middle;">TANGGAL</th>
                        <th rowspan="2" style="width: 15%; vertical-align: middle;">NO. BUKTI</th>
                        <th rowspan="2" style="width: 23%; vertical-align: middle;">KETERANGAN</th>
                        <th style="width: 10%; text-align: right; background: #f3f4f6;">Piutang Usaha</th>
                        <th style="width: 10%; text-align: right; background: #f3f4f6;">Harga Pokok Penjualan</th>
                        <th style="width: 10%; text-align: right; background: #f3f4f6;">Persediaan Barang Dagang</th>
                        <th style="width: 10%; text-align: right; background: #f3f4f6;">PPN Keluaran</th>
                        <th style="width: 10%; text-align: right; background: #f3f4f6;">Penjualan</th>
                    </tr>
                    <tr>
                        <th style="text-align: right; font-size: 10px; color: #047857;">DEBIT</th>
                        <th style="text-align: right; font-size: 10px; color: #047857;">DEBIT</th>
                        <th style="text-align: right; font-size: 10px; color: #1d4ed8;">KREDIT</th>
                        <th style="text-align: right; font-size: 10px; color: #1d4ed8;">KREDIT</th>
                        <th style="text-align: right; font-size: 10px; color: #1d4ed8;">KREDIT</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_j}
                    <tr style="background-color: #f9fafb; font-weight: 600;">
                        <td colspan="3" style="padding: 12px 20px;">Total ({count_jurnal} bukti)</td>
                        <td style="padding: 12px 20px; text-align: right;">{f"{sum_piutang:,.0f}".replace(',', '.')}</td>
                        <td style="padding: 12px 20px; text-align: right;">{f"{sum_hpp:,.0f}".replace(',', '.')}</td>
                        <td style="padding: 12px 20px; text-align: right;">{f"{sum_persediaan:,.0f}".replace(',', '.')}</td>
                        <td style="padding: 12px 20px; text-align: right;">{f"{sum_ppn:,.0f}".replace(',', '.')}</td>
                        <td style="padding: 12px 20px; text-align: right;">{f"{sum_penjualan:,.0f}".replace(',', '.')}</td>
                    </tr>
                </tbody>
            </table>
            </div>
            """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Penjualan</div>
            <div class="page-desc" style="margin-bottom: 0;">Transaksi penjualan tunai & kredit. Jurnal penjualan dan HPP (perpetual) terbentuk otomatis. Saldo awal dari kartu pelanggan tercatat di jurnal atas.</div>
        </div>
        <div>
            <a href="/transaksi/penjualan/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Tambah Transaksi</a>
        </div>
    </div>

    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px 20px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <input type="date" value="2026-01-01" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            <span style="font-size: 13px; color: #6b7280;">s.d.</span>
            <input type="date" value="2026-10-31" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
        </div>
        <div>
            <select style="padding: 6px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                <option>Semua status</option>
                <option>Tunai</option>
                <option>Lunas</option>
                <option>Sebagian</option>
                <option>Belum lunas</option>
            </select>
        </div>
    </div>

    <div class="account-card" style="margin-bottom: 25px;">
        {table_penjualan_html}
    </div>

    <div class="account-card">
        <div style="padding: 15px 20px; font-weight: 600; font-size: 15px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal Penjualan</div>
        {table_jurnal_html}
    </div>
    """
    
    return render_dashboard_layout('penjualan', content)

@app.route('/transaksi/penjualan/baru', methods=['GET', 'POST'])
def tambah_transaksi_penjualan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    list_barang = user_data.get('barang', [])
    
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        pelanggan = request.form.get('pelanggan')
        no_faktur = request.form.get('no_faktur').strip()
        if not no_faktur:
            no_faktur = f"BKM-{len(user_data.get('penjualan', [])) + 1:02d}"
        
        pembayaran = request.form.get('pembayaran')
        termin_pot = request.form.get('termin_pot', '')
        termin_hari = request.form.get('termin_hari', '')
        termin_jt = request.form.get('termin_jt', '30')
        termin = f"{termin_pot}/{termin_hari}, n/{termin_jt}" if termin_pot and termin_hari else f"n/{termin_jt}"
        memo = request.form.get('memo', '')
        
        item_barangs = request.form.getlist('item_barang[]')
        item_qtys = request.form.getlist('item_qty[]')
        item_hargas = request.form.getlist('item_harga[]')
        
        ppn_persen_raw = request.form.get('ppn_persen', '0')
        ppn_persen = float(ppn_persen_raw) if ppn_persen_raw != '' and ppn_persen_raw != '-' else 0.0
        
        diskon_jenis = request.form.get('diskon_jenis', 'Rp')
        diskon_nilai = float(request.form.get('diskon_nilai', 0) or 0)
        
        beban_angkut = True if request.form.get('beban_angkut') else False
        beban_angkut_nilai = float(request.form.get('beban_angkut_nilai', 0) or 0) if beban_angkut else 0.0
        
        subtotal = 0
        total_hpp_transaksi = 0
        details = []
        for i in range(len(item_barangs)):
            brg_str = item_barangs[i]
            if not brg_str:
                continue
            qty_raw = float(item_qtys[i].replace('.', '') or 0)
            qty = int(qty_raw) if qty_raw.is_integer() else qty_raw
            harga = float(item_hargas[i].replace('.', '') or 0)
            jumlah = qty * harga
            subtotal += jumlah
            
            hpp_unit = 0
            kode_brg_match = brg_str.split(' - ')[0].strip()
            for b in list_barang:
                if b.get('kode') == kode_brg_match:
                    hpp_unit = float(b.get('harga_pokok', 0) or 0)
                    break
            total_hpp_transaksi += (qty * hpp_unit)

            details.append({
                'barang': brg_str, 
                'qty': qty, 
                'harga': harga, 
                'jumlah': jumlah,
                'hpp_unit': hpp_unit,
                'total_hpp': qty * hpp_unit
            })
            
        diskon_nominal = diskon_nilai if diskon_jenis == 'Rp' else (subtotal * diskon_nilai / 100)
        dpp = subtotal - diskon_nominal
        ppn_nominal = dpp * (ppn_persen / 100)
        total_transaksi = dpp + ppn_nominal + beban_angkut_nilai
        
        formatted_total = f"{int(total_transaksi):,.0f}".replace(',', '.')
        
        try:
            dt_trx = datetime.strptime(tanggal, '%Y-%m-%d')
            dt_jt = dt_trx + timedelta(days=int(termin_jt or 30))
            str_jt = format_tanggal_pendek_indo(dt_jt.strftime('%Y-%m-%d'))
        except:
            str_jt = "-"

        transaksi = {
            'tanggal': tanggal,
            'tanggal_indo': format_tanggal_pendek_indo(tanggal),
            'nomor': no_faktur,
            'pelanggan': pelanggan,
            'status': 'Belum lunas',
            'jatuh_tempo': str_jt,
            'total': formatted_total,
            'sisa': formatted_total,
            'pembayaran': pembayaran,
            'termin': termin,
            'termin_pot': termin_pot,
            'termin_hari': termin_hari,
            'termin_jt': termin_jt,
            'memo': memo,
            'ppn_persen': ppn_persen,
            'diskon_jenis': diskon_jenis,
            'diskon_nilai': diskon_nilai,
            'beban_angkut': beban_angkut,
            'beban_angkut_nilai': beban_angkut_nilai,
            'total_hpp': total_hpp_transaksi,
            'dpp': dpp,
            'ppn': ppn_nominal,
            'is_saldo_awal': False,
            'details': details
        }
        database_user[email]['penjualan'].append(transaksi)
        
        return redirect(url_for('ubah_transaksi_penjualan_detail', nomor=no_faktur))

    today_date = datetime.now().strftime('%Y-%m-%d')

    options_pelanggan = ""
    pelanggan_termin_map = {}
    for p in list_pelanggan:
        p_nama = p.get('nama')
        pot = p.get('potongan', '')
        jb = p.get('jika_bayar', '')
        jt = p.get('jatuh_tempo', '30') or '30'
        pelanggan_termin_map[p_nama] = {'pot': pot, 'jb': jb, 'jt': jt}
        options_pelanggan += f'<option value="{p_nama}">{p.get("kode")} — {p_nama}</option>'
    
    options_barang = "".join([f'<option value="{b.get("kode")} - {b.get("nama")}" data-harga="{b.get("harga_jual", 0)}" data-hpp="{b.get("harga_pokok", 0)}">{b.get("kode")} {b.get("nama")} (Stok: {b.get("qty_awal", 0)})</option>' for b in list_barang])
    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div>
                <div class="page-title" style="display: flex; align-items: center; gap: 10px;">
                    Transaksi Penjualan Baru
                </div>
                <div style="font-size: 13px; color: #6b7280; margin-top: 4px;">
                    Buat transaksi penjualan barang dagang
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/transaksi/penjualan" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
            <a href="/transaksi/penjualan/baru" class="btn-action" style="padding: 8px 16px; font-weight: 500; background: #fff; border-color: #d18a99; color: #d18a99;">+ Baru</a>
        </div>
    </div>

    <div class="card-form" style="margin-bottom: 25px;">
        <form action="/transaksi/penjualan/baru" method="POST" id="formPenjualan">
            
            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Tanggal <span class="required">*</span></label>
                    <input type="date" name="tanggal" value="{today_date}" required>
                </div>
                <div>
                    <label>Pelanggan (kode / nama) <span class="required">*</span></label>
                    <select name="pelanggan" id="selectPelanggan" onchange="muatTerminPelanggan(this)" required>
                        <option value="">-- Pilih Pelanggan --</option>
                        {options_pelanggan}
                    </select>
                </div>
                <div>
                    <label>No. faktur</label>
                    <input type="text" name="no_faktur" value="" placeholder="(kosong = otomatis)">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Pembayaran</label>
                    <select name="pembayaran" id="selectPembayaran">
                        <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                        <option value="Tunai">Tunai</option>
                    </select>
                </div>
                <div>
                    <label>Termin</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                        <input type="text" name="termin_pot" id="inputTerminPot" value="" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_hari" id="inputTerminHari" value="" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_jt" id="inputTerminJt" value="30" style="text-align: center;">
                    </div>
                </div>
                <div>
                    <label>Memo</label>
                    <input type="text" name="memo" placeholder="Keterangan">
                </div>
            </div>

            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table" id="tabelItem">
                    <thead>
                        <tr>
                            <th style="width: 5%;">#</th>
                            <th style="width: 45%;">Barang (kode / nama)</th>
                            <th style="width: 15%;">Qty</th>
                            <th style="width: 20%; text-align: right;">Harga jual</th>
                            <th style="width: 15%; text-align: right;">Jumlah</th>
                            <th style="width: 5%; text-align: center;"></th>
                        </tr>
                    </thead>
                    <tbody id="tbodyItem">
                        <tr>
                            <td>1</td>
                            <td>
                                <select name="item_barang[]" onchange="updateHarga(this)" style="border:none; width:100%; background:transparent;">
                                    <option value="">-- Pilih Barang --</option>
                                    {options_barang}
                                </select>
                            </td>
                            <td><input type="text" name="item_qty[]" value="" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:left;"></td>
                            <td><input type="text" name="item_harga[]" value="" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:right;"></td>
                            <td style="text-align: right;" class="col-jumlah">-</td>
                            <td style="text-align: center;"><a href="#" onclick="hapusBaris(this); return false;" style="color: #dc2626; text-decoration: none;">✕</a></td>
                        </tr>
                    </tbody>
                </table>
                <div style="padding: 10px 20px; background: #f9fafb; display: flex; justify-content: space-between; align-items: center;">
                    <button type="button" onclick="tambahBaris()" style="background: none; border: none; color: #d18a99; font-weight: 600; cursor: pointer; font-size: 13px;">+ Tambah baris</button>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px; margin-bottom: 25px; font-size: 13px;">
                <div style="display: flex; width: 420px; justify-content: space-between; padding: 4px 0;">
                    <span style="color: #6b7280;">Subtotal</span>
                    <span id="displaySubtotal" style="font-weight: 600; min-width: 120px; text-align: right;">-</span>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">Diskon dagang / rabat</span>
                    <div style="display: flex; gap: 5px; align-items: center;">
                        <select name="diskon_jenis" onchange="hitungTotalSemua()" style="padding: 4px; font-size: 12px; width: 55px;">
                            <option value="Rp">Rp</option>
                            <option value="%">%</option>
                        </select>
                        <input type="text" name="diskon_nilai" value="" placeholder="-" oninput="hitungTotalSemua()" style="padding: 4px; text-align: right; font-size: 12px; width: 95px;">
                        <span id="displayDiskonNominal" style="min-width: 100px; text-align: right; font-weight: 500; color: #374151;">-</span>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; width: 420px; padding: 4px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <label style="display: flex; align-items: center; gap: 8px; margin-bottom: 0; color: #6b7280; font-weight: normal; cursor: pointer;">
                            <input type="checkbox" name="beban_angkut" id="checkboxBebanAngkut" onclick="toggleBebanAngkutPanel()" style="width: 14px; height: 14px; accent-color: #d18a99;"> Beban Angkut
                        </label>
                        <span id="displayBebanAngkutNominal" style="min-width: 120px; text-align: right; font-weight: 500; color: #374151;">-</span>
                    </div>
                    <div id="panelBebanAngkut" style="display: none; background: #f9fafb; padding: 10px; border-radius: 6px; border: 1px solid #e5e7eb; margin-top: 8px;">
                        <label style="font-size: 11px; margin-bottom: 4px;">Nilai Beban Angkut (Rp)</label>
                        <input type="text" name="beban_angkut_nilai" id="inputBebanAngkutNilai" value="" placeholder="-" oninput="formatRupiah(this); hitungTotalSemua();" style="padding: 6px; font-size: 13px;">
                    </div>
                </div>

                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">PPN Keluaran</span>
                    <div style="display: flex; gap: 5px; align-items: center;">
                        <input type="text" name="ppn_persen" value="-" onfocus="if(this.value==='-') this.value='';" onblur="if(this.value==='') this.value='-';" oninput="hitungTotalSemua()" style="width: 65px; padding: 4px; text-align: right; font-size: 12px;">
                        <span style="margin-right: 15px;">%</span>
                        <span id="displayPpnNominal" style="min-width: 100px; text-align: right; font-weight: 500; color: #374151;">-</span>
                    </div>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; border-top: 2px solid #e5e7eb; padding-top: 10px; font-size: 15px; font-weight: bold; color: #1f2937;">
                    <span>Total</span>
                    <span id="displayTotal" style="min-width: 120px; text-align: right;">-</span>
                </div>
            </div>

            <div style="display: flex; justify-content: flex-end; align-items: center; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                <button type="submit" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan transaksi</button>
            </div>

        </form>
    </div>
    
    <script>
        const pelangganTerminMap = {json.dumps(pelanggan_termin_map)};

        function muatTerminPelanggan(selectEl) {{
            const namaPlg = selectEl.value;
            if (pelangganTerminMap[namaPlg]) {{
                const t = pelangganTerminMap[namaPlg];
                document.getElementById('inputTerminPot').value = t.pot || '';
                document.getElementById('inputTerminHari').value = t.jb || '';
                document.getElementById('inputTerminJt').value = t.jt || '30';
            }} else {{
                document.getElementById('inputTerminPot').value = '';
                document.getElementById('inputTerminHari').value = '';
                document.getElementById('inputTerminJt').value = '30';
            }}
        }}

        function toggleBebanAngkutPanel() {{
            const chk = document.getElementById('checkboxBebanAngkut');
            const panel = document.getElementById('panelBebanAngkut');
            if(chk.checked) {{ panel.style.display = 'block'; }}
            else {{
                panel.style.display = 'none';
                document.getElementById('inputBebanAngkutNilai').value = '';
                hitungTotalSemua();
            }}
        }}

        function updateHarga(selectEl) {{
            const row = selectEl.closest('tr');
            const selectedOpt = selectEl.options[selectEl.selectedIndex];
            const harga = selectedOpt.getAttribute('data-harga') || 0;
            const hargaInput = row.querySelector('input[name="item_harga[]"]');
            hargaInput.value = harga > 0 ? new Intl.NumberFormat('id-ID').format(harga) : '';
            hitungBaris(hargaInput);
        }}

        function hitungBaris(el) {{
            const row = el.closest('tr');
            const qty = parseFloat(row.querySelector('input[name="item_qty[]"]').value.replace(/\./g, '')) || 0;
            const harga = parseFloat(row.querySelector('input[name="item_harga[]"]').value.replace(/\./g, '')) || 0;
            const jumlah = qty * harga;
            row.querySelector('.col-jumlah').textContent = jumlah > 0 ? new Intl.NumberFormat('id-ID').format(jumlah) : '-';
            hitungTotalSemua();
        }}

        function formatRupiah(el) {{
            let angka = el.value.replace(/[^\d]/g, '');
            if (angka === "") {{ el.value = ""; }}
            else {{ el.value = new Intl.NumberFormat('id-ID').format(angka); }}
        }}

        function hitungTotalSemua() {{
            let subtotal = 0;
            document.querySelectorAll('#tbodyItem tr').forEach(row => {{
                const qty = parseFloat(row.querySelector('input[name="item_qty[]"]').value.replace(/\./g, '')) || 0;
                const harga = parseFloat(row.querySelector('input[name="item_harga[]"]').value.replace(/\./g, '')) || 0;
                subtotal += (qty * harga);
            }});
            
            document.getElementById('displaySubtotal').textContent = subtotal > 0 ? new Intl.NumberFormat('id-ID').format(subtotal) : '-';

            const diskonJenis = document.querySelector('select[name="diskon_jenis"]').value;
            const diskonNilai = parseFloat(document.querySelector('input[name="diskon_nilai"]').value.replace(/\./g, '')) || 0;
            let diskonNominal = diskonJenis === 'Rp' ? diskonNilai : (subtotal * diskonNilai / 100);
            
            const elDiskon = document.getElementById('displayDiskonNominal');
            elDiskon.textContent = diskonNominal > 0 ? '(Rp ' + new Intl.NumberFormat('id-ID').format(diskonNominal) + ')' : '-';

            const dpp = subtotal - diskonNominal;
            const ppnPersenRaw = document.querySelector('input[name="ppn_persen"]').value;
            const ppnPersen = (ppnPersenRaw === '' || ppnPersenRaw === '-') ? 0 : (parseFloat(ppnPersenRaw.replace(/\./g, '')) || 0);
            const ppnNominal = dpp * (ppnPersen / 100);

            document.getElementById('displayPpnNominal').textContent = ppnNominal > 0 ? new Intl.NumberFormat('id-ID').format(ppnNominal) : '-';

            let bebanAngkutNilai = 0;
            const chk = document.getElementById('checkboxBebanAngkut');
            if(chk && chk.checked) {{
                bebanAngkutNilai = parseFloat(document.getElementById('inputBebanAngkutNilai').value.replace(/\./g, '')) || 0;
            }}
            document.getElementById('displayBebanAngkutNominal').textContent = bebanAngkutNilai > 0 ? new Intl.NumberFormat('id-ID').format(bebanAngkutNilai) : '-';

            const total = dpp + ppnNominal + bebanAngkutNilai;
            document.getElementById('displayTotal').textContent = total > 0 ? new Intl.NumberFormat('id-ID').format(total) : '-';
        }}

        function tambahBaris() {{
            const tbody = document.getElementById('tbodyItem');
            const rowCount = tbody.rows.length + 1;
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${{rowCount}}</td>
                <td>
                    <select name="item_barang[]" onchange="updateHarga(this)" style="border:none; width:100%; background:transparent;">
                        <option value="">-- Pilih Barang --</option>
                        {options_barang}
                    </select>
                </td>
                <td><input type="text" name="item_qty[]" value="" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:left;"></td>
                <td><input type="text" name="item_harga[]" value="" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:right;"></td>
                <td style="text-align: right;" class="col-jumlah">-</td>
                <td style="text-align: center;"><a href="#" onclick="hapusBaris(this); return false;" style="color: #dc2626; text-decoration: none;">✕</a></td>
            `;
            tbody.appendChild(newRow);
        }}

        function hapusBaris(el) {{
            const row = el.closest('tr');
            if(document.querySelectorAll('#tbodyItem tr').length > 1) {{
                row.remove();
                hitungTotalSemua();
            }}
        }}
    </script>
    """
    
    return render_dashboard_layout('penjualan', content)

@app.route('/transaksi/penjualan/ubah/<path:nomor>')
def ubah_transaksi_penjualan_detail(nomor):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_penjualan = user_data.get('penjualan', [])
    list_pelanggan = user_data.get('pelanggan', [])
    list_barang = user_data.get('barang', [])
    
    target_trx = None
    for tr in list_penjualan:
        if tr.get('nomor') == nomor:
            target_trx = tr
            break
            
    if not target_trx:
        return redirect(url_for('transaksi_penjualan'))

    options_pelanggan = "".join([f'<option value="{p.get("nama")}" {"selected" if p.get("nama") == target_trx.get("pelanggan") else ""}>{p.get("kode")} — {p.get("nama")}</option>' for p in list_pelanggan])

    rows_item_html = ""
    details = target_trx.get('details', [])
    if not details:
        details = [{'barang': '', 'qty': '', 'harga': 0, 'jumlah': 0, 'hpp_unit': 0, 'total_hpp': 0}]

    total_hpp_trx = 0
    rows_hpp_baris_html = ""

    for idx, det in enumerate(details):
        r_num = idx + 1
        q_raw = float(det.get('qty', 0) or 0)
        q_val = f"{int(q_raw)}" if q_raw.is_integer() else f"{q_raw}"
        h_val = f"{int(det.get('harga', 0)):,.0f}".replace(',', '.') if det.get('harga') else ''
        j_val = f"{int(det.get('jumlah', 0)):,.0f}".replace(',', '.') if det.get('jumlah') else '-'
        
        hpp_u = float(det.get('hpp_unit', 0) or 0)
        tot_hpp = float(det.get('total_hpp', 0) or 0)
        total_hpp_trx += tot_hpp

        formatted_hpp_u = f"{hpp_u:,.0f}".replace(',', '.')
        formatted_tot_hpp = f"{tot_hpp:,.0f}".replace(',', '.')
        nama_brg_bersih = det.get('barang', '-')
        
        rows_hpp_baris_html += f"""
        <tr>
            <td>{nama_brg_bersih}</td>
            <td>{q_val}</td>
            <td style="text-align: right;">{formatted_hpp_u}</td>
            <td style="text-align: right; font-weight: 500;">{formatted_tot_hpp}</td>
        </tr>
        """
        
        opt_brg_html = '<option value="">-- Pilih Barang --</option>'
        for b in list_barang:
            b_str = f"{b.get('kode')} - {b.get('nama')}"
            sel = "selected" if b_str == det.get('barang') else ""
            opt_brg_html += f'<option value="{b_str}" data-harga="{b.get("harga_jual", 0)}" data-hpp="{b.get("harga_pokok", 0)}" {sel}>{b.get("kode")} {b.get("nama")}</option>'

        rows_item_html += f"""
        <tr>
            <td>{r_num}</td>
            <td>
                <select name="item_barang[]" onchange="updateHarga(this)" style="border:none; width:100%; background:transparent;">
                    {opt_brg_html}
                </select>
            </td>
            <td><input type="text" name="item_qty[]" value="{q_val}" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:left;"></td>
            <td><input type="text" name="item_harga[]" value="{h_val}" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:right;"></td>
            <td style="text-align: right;" class="col-jumlah">{j_val}</td>
            <td style="text-align: center;"><a href="#" onclick="hapusBaris(this); return false;" style="color: #dc2626; text-decoration: none;">✕</a></td>
        </tr>
        """

    total_trx_str = target_trx.get('total', '0')
    subtotal_str = total_trx_str
    formatted_total_hpp_trx = f"{total_hpp_trx:,.0f}".replace(',', '.') if total_hpp_trx > 0 else '0'
    ppn_persen_val = target_trx.get('ppn_persen', 0)
    ppn_persen_str = f"{int(ppn_persen_val)}" if float(ppn_persen_val).is_integer() else (f"{ppn_persen_val}" if ppn_persen_val else "-")

    diskon_nilai_val = target_trx.get('diskon_nilai', 0)
    diskon_display_str = f"(Rp {int(diskon_nilai_val):,.0f})".replace(',', '.') if diskon_nilai_val and float(diskon_nilai_val) > 0 else "-"
    is_saldo_awal = target_trx.get('is_saldo_awal', False)

    bottom_journals_html = ""
    if not is_saldo_awal:
        bottom_journals_html = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px;">
            <div>
                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal penjualan</div>
                    <table class="account-table">
                        <thead>
                            <tr>
                                <th>KODE</th>
                                <th>AKUN</th>
                                <th style="text-align: right;">DEBIT</th>
                                <th style="text-align: right;">KREDIT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1-1300</td>
                                <td>Piutang Usaha</td>
                                <td style="text-align: right;">{total_trx_str}</td>
                                <td style="text-align: right;"></td>
                            </tr>
                            <tr>
                                <td>4-1100</td>
                                <td>Penjualan</td>
                                <td style="text-align: right;"></td>
                                <td style="text-align: right;">{total_trx_str}</td>
                            </tr>
                            <tr style="background-color: #f9fafb; font-weight: 600;">
                                <td colspan="2">Total</td>
                                <td style="text-align: right;">{total_trx_str}</td>
                                <td style="text-align: right;">{total_trx_str}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="account-card">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal HPP (persediaan berkurang)</div>
                    <table class="account-table">
                        <thead>
                            <tr>
                                <th>KODE</th>
                                <th>AKUN</th>
                                <th style="text-align: right;">DEBIT</th>
                                <th style="text-align: right;">KREDIT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>5-1100</td>
                                <td>Harga Pokok Penjualan</td>
                                <td style="text-align: right;">{formatted_total_hpp_trx}</td>
                                <td style="text-align: right;"></td>
                            </tr>
                            <tr>
                                <td>1-1400</td>
                                <td>Persediaan Barang Dagang</td>
                                <td style="text-align: right;"></td>
                                <td style="text-align: right;">{formatted_total_hpp_trx}</td>
                            </tr>
                            <tr style="background-color: #f9fafb; font-weight: 600;">
                                <td colspan="2">Total</td>
                                <td style="text-align: right;">{formatted_total_hpp_trx}</td>
                                <td style="text-align: right;">{formatted_total_hpp_trx}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                        <span>Retur penjualan</span>
                        <a href="/transaksi/retur-penjualan/baru" class="btn-action" style="padding: 4px 10px; font-size: 12px;">+ Buat retur</a>
                    </div>
                    <div style="padding: 30px; text-align: center; color: #6b7280; font-size: 13px;">
                        Belum ada retur.
                    </div>
                </div>

                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">HPP per baris (rata-rata bergerak)</div>
                    <table class="account-table">
                        <thead>
                            <tr>
                                <th>BARANG</th>
                                <th>QTY</th>
                                <th style="text-align: right;">HPP / UNIT</th>
                                <th style="text-align: right;">TOTAL HPP</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_hpp_baris_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """
    else:
        bottom_journals_html = f"""
        <div class="account-card" style="padding: 30px; text-align: center; color: #6b7280; font-size: 13px;">
            Transaksi ini bersumber dari <strong>Saldo Awal Pelanggan (Kartu Pelanggan)</strong>.
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div>
                <div class="page-title" style="display: flex; align-items: center; gap: 10px;">
                    Transaksi Penjualan {target_trx.get('nomor')} {"<span class='badge-saldo-awal'>Saldo Awal</span>" if is_saldo_awal else ""}
                </div>
                <div style="font-size: 13px; color: #6b7280; margin-top: 4px; display: flex; align-items: center; gap: 8px;">
                    Status: <span class="badge-belum-lunas">{target_trx.get('status', 'Belum lunas')}</span> &nbsp; Sisa tagihan Rp {target_trx.get('sisa', total_trx_str)}
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/transaksi/penjualan" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
            <a href="/transaksi/penjualan/baru" class="btn-action" style="padding: 8px 16px; font-weight: 500; background: #fff; border-color: #d18a99; color: #d18a99;">+ Baru</a>
        </div>
    </div>

    <div class="card-form" style="margin-bottom: 25px;">
        <form action="/transaksi/penjualan/baru" method="POST" id="formPenjualan">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Tanggal <span class="required">*</span></label>
                    <input type="date" name="tanggal" value="{target_trx.get('tanggal')}" required>
                </div>
                <div>
                    <label>Pelanggan (kode / nama) <span class="required">*</span></label>
                    <select name="pelanggan" required>{options_pelanggan}</select>
                </div>
                <div>
                    <label>No. faktur</label>
                    <input type="text" name="no_faktur" value="{target_trx.get('nomor')}">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Pembayaran</label>
                    <select name="pembayaran">
                        <option value="Kredit (dengan termin)" {"selected" if target_trx.get('pembayaran') != 'Tunai' else ""}>Kredit (dengan termin)</option>
                        <option value="Tunai" {"selected" if target_trx.get('pembayaran') == 'Tunai' else ""}>Tunai</option>
                    </select>
                </div>
                <div>
                    <label>Termin</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                        <input type="text" name="termin_pot" value="{target_trx.get('termin_pot', '')}" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_hari" value="{target_trx.get('termin_hari', '')}" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_jt" value="{target_trx.get('termin_jt', '30')}" style="text-align: center;">
                    </div>
                </div>
                <div>
                    <label>Memo</label>
                    <input type="text" name="memo" value="{target_trx.get('memo', '')}" placeholder="Keterangan">
                </div>
            </div>

            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table" id="tabelItem">
                    <thead>
                        <tr>
                            <th style="width: 5%;">#</th>
                            <th style="width: 45%;">Barang (kode / nama)</th>
                            <th style="width: 15%;">Qty</th>
                            <th style="width: 20%; text-align: right;">Harga jual</th>
                            <th style="width: 15%; text-align: right;">Jumlah</th>
                            <th style="width: 5%; text-align: center;"></th>
                        </tr>
                    </thead>
                    <tbody id="tbodyItem">{rows_item_html}</tbody>
                </table>
            </div>

            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px; margin-bottom: 25px; font-size: 13px;">
                <div style="display: flex; width: 420px; justify-content: space-between; padding: 4px 0;">
                    <span style="color: #6b7280;">Subtotal</span>
                    <span id="displaySubtotal" style="font-weight: 600; min-width: 120px; text-align: right;">{subtotal_str}</span>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">Diskon dagang / rabat</span>
                    <span id="displayDiskonNominal">{diskon_display_str}</span>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">PPN Keluaran</span>
                    <div style="display: flex; gap: 5px; align-items: center;">
                        <input type="text" name="ppn_persen" value="{ppn_persen_str}" onfocus="if(this.value==='-') this.value='';" onblur="if(this.value==='') this.value='-';" style="width: 65px; padding: 4px; text-align: right; font-size: 12px;">
                        <span>%</span>
                    </div>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; border-top: 2px solid #e5e7eb; padding-top: 10px; font-size: 15px; font-weight: bold; color: #1f2937;">
                    <span>Total</span>
                    <span id="displayTotal" style="min-width: 120px; text-align: right;">{total_trx_str}</span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                <button type="button" class="btn-action btn-action-danger" style="padding: 10px 20px; font-weight: 500;">Hapus transaksi</button>
                <button type="submit" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan perubahan</button>
            </div>
        </form>
    </div>

    {bottom_journals_html}
    """
    return render_dashboard_layout('penjualan', content)

    if 'transaksi' not in database_user[email]:
        database_user[email]['transaksi'] = []
    
    database_user[email]['transaksi'].append({
        'tanggal': request.form.get('tanggal'),
        'no_bukti': request.form.get('no_bukti'),
        'jenis': 'penjualan', # <--- Jenis transaksi
        'kode_barang': request.form.get('kode_barang'),
        'qty': float(request.form.get('qty', 0)),
        'harga': float(request.form.get('harga', 0)),
        'relasi': request.form.get('pelanggan')
    })
    return redirect(url_for('kartu_barang'))

# --- RETUR PENJUALAN ROUTES ---
@app.route('/transaksi/retur-penjualan')
def transaksi_retur_penjualan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_retur = user_data.get('retur_penjualan', [])

    rows = ""
    for r in list_retur:
        rows += f"""
        <tr>
            <td style="padding: 12px 20px;">{r.get('tanggal')}</td>
            <td style="padding: 12px 20px; font-weight: 600; color: #d18a99;">{r.get('nomor')}</td>
            <td style="padding: 12px 20px;">{r.get('pelanggan')}</td>
            <td style="padding: 12px 20px;">{r.get('keterangan', '-')}</td>
            <td style="padding: 12px 20px; text-align: right;">{r.get('total')}</td>
        </tr>
        """

    table_html = f"""
    <table class="account-table">
        <thead>
            <tr>
                <th>TANGGAL</th>
                <th>NO. RETUR</th>
                <th>PELANGGAN</th>
                <th>KETERANGAN</th>
                <th style="text-align: right;">TOTAL</th>
            </tr>
        </thead>
        <tbody>
            {rows if rows else '<tr><td colspan="5" style="text-align:center; padding:30px; color:#6b7280;">Belum ada retur penjualan.</td></tr>'}
        </tbody>
    </table>
    """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Retur Penjualan</div>
            <div class="page-desc" style="margin-bottom: 0;">Penerimaan kembali barang dari pelanggan. Mengurangi piutang/kas dan **menambah kembali stok** di kartu stok.</div>
        </div>
        <div>
            <a href="/transaksi/retur-penjualan/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none;">+ Tambah Retur Penjualan</a>
        </div>
    </div>
    <div class="account-card">{table_html}</div>
    """
    return render_dashboard_layout('retur_penjualan', content)


@app.route('/transaksi/retur-penjualan/baru', methods=['GET', 'POST'])
def tambah_retur_penjualan():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    list_barang = user_data.get('barang', [])
    
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        pelanggan = request.form.get('pelanggan')
        no_retur = request.form.get('no_retur').strip() or f"RP-{len(user_data.get('retur_penjualan', [])) + 1:02d}"
        keterangan = request.form.get('keterangan', '')
        
        item_barangs = request.form.getlist('item_barang[]')
        item_qtys = request.form.getlist('item_qty[]')
        item_hargas = request.form.getlist('item_harga[]')
        
        subtotal = 0
        details = []
        for i in range(len(item_barangs)):
            brg_str = item_barangs[i]
            if not brg_str:
                continue
            qty = float(item_qtys[i].replace('.', '') or 0)
            harga = float(item_hargas[i].replace('.', '') or 0)
            jumlah = qty * harga
            subtotal += jumlah
            details.append({'barang': brg_str, 'qty': qty, 'harga': harga, 'jumlah': jumlah})

        formatted_total = f"{int(subtotal):,.0f}".replace(',', '.')
        retur_data = {
            'tanggal': tanggal,
            'nomor': no_retur,
            'pelanggan': pelanggan,
            'keterangan': keterangan,
            'total': formatted_total,
            'details': details
        }
        
        if 'retur_penjualan' not in user_data:
            database_user[email]['retur_penjualan'] = []
        database_user[email]['retur_penjualan'].append(retur_data)
        
        return redirect(url_for('transaksi_retur_penjualan'))

    options_pelanggan = "".join([f'<option value="{p.get("nama")}">{p.get("nama")}</option>' for p in list_pelanggan])
    options_barang = "".join([f'<option value="{b.get("kode")} - {b.get("nama")}">{b.get("kode")} {b.get("nama")}</option>' for b in list_barang])
    today_date = datetime.now().strftime('%Y-%m-%d')

    content = f"""
    <div class="page-title">Tambah Retur Penjualan Baru</div>
    <div class="page-desc">Barang yang diretur oleh pelanggan akan otomatis masuk kembali ke kartu stok.</div>
    <div class="card-form">
        <form action="/transaksi/retur-penjualan/baru" method="POST">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 20px;" class="form-group">
                <div><label>Tanggal</label><input type="date" name="tanggal" value="{today_date}" required></div>
                <div><label>Pelanggan</label><select name="pelanggan" required><option value="">-- Pilih --</option>{options_pelanggan}</select></div>
                <div><label>No. Retur</label><input type="text" name="no_retur" placeholder="Otomatis"></div>
            </div>
            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table">
                    <thead>
                        <tr>
                            <th>Barang</th>
                            <th style="width: 15%;">Qty Retur</th>
                            <th style="width: 20%; text-align: right;">Harga Satuan</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><select name="item_barang[]" style="border:none; width:100%;"><option value="">-- Pilih --</option>{options_barang}</select></td>
                            <td><input type="text" name="item_qty[]" value="1" style="border:none; width:100%;"></td>
                            <td><input type="text" name="item_harga[]" value="0" style="border:none; width:100%; text-align:right;"></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="display: flex; justify-content: flex-end;"><button type="submit" class="btn-simpan">Simpan Retur Penjualan</button></div>
        </form>
    </div>
    """
    return render_dashboard_layout('retur_penjualan', content)

@app.route('/transaksi/retur-penjualan/ubah/<path:no_retur>')
def ubah_retur_penjualan_detail(no_retur):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_retur = user_data.get('retur_penjualan', [])
    
    target_retur = None
    for rt in list_retur:
        if rt.get('no_retur') == no_retur:
            target_retur = rt
            break
            
    if not target_retur:
        return redirect(url_for('retur_penjualan'))

    sub_retur = float(target_retur.get('subtotal_retur', 0) or 0)
    ppn_kor = float(target_retur.get('ppn_koreksi', 0) or 0)
    tot_retur = float(target_retur.get('total_retur', 0) or 0)
    tot_hpp_retur = float(target_retur.get('total_hpp_retur', 0) or 0)

    formatted_sub = f"{int(sub_retur):,.0f}".replace(',', '.') if sub_retur > 0 else '0'
    formatted_ppn = f"{int(ppn_kor):,.0f}".replace(',', '.') if ppn_kor > 0 else '0'
    formatted_tot = f"{int(tot_retur):,.0f}".replace(',', '.') if tot_retur > 0 else '0'
    formatted_hpp = f"{int(tot_hpp_retur):,.0f}".replace(',', '.') if tot_hpp_retur > 0 else '0'

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Retur Penjualan {target_retur.get('no_retur')}</div>
            <div style="font-size: 13px; color: #6b7280; margin-top: 4px;">
                Faktur Asal: <strong>{target_retur.get('faktur_asal')}</strong> | Pelanggan: <strong>{target_retur.get('pelanggan_nama')}</strong>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/transaksi/retur-penjualan" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
        </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <a href="#" class="btn-action btn-action-danger" style="padding: 10px 20px; font-weight: 500;">Hapus retur</a>
        <button type="button" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan perubahan</button>
    </div>

    <div class="account-card" style="margin-bottom: 25px;">
        <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal retur penjualan</div>
        <table class="account-table">
            <thead>
                <tr>
                    <th style="width: 15%;">KODE</th>
                    <th style="width: 45%;">AKUN</th>
                    <th style="width: 20%; text-align: right;">DEBIT</th>
                    <th style="width: 20%; text-align: right;">KREDIT</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>4-1200</td>
                    <td>Retur Penjualan</td>
                    <td style="text-align: right;">{formatted_sub}</td>
                    <td style="text-align: right;"></td>
                </tr>
                <tr>
                    <td>2-1200</td>
                    <td>PPN Keluaran</td>
                    <td style="text-align: right;">{formatted_ppn}</td>
                    <td style="text-align: right;"></td>
                </tr>
                <tr>
                    <td>1-1300</td>
                    <td>Piutang Usaha</td>
                    <td style="text-align: right;"></td>
                    <td style="text-align: right;">{formatted_tot}</td>
                </tr>
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="2">Total</td>
                    <td style="text-align: right;">{formatted_tot}</td>
                    <td style="text-align: right;">{formatted_tot}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="account-card">
        <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal HPP (persediaan kembali)</div>
        <table class="account-table">
            <thead>
                <tr>
                    <th style="width: 15%;">KODE</th>
                    <th style="width: 45%;">AKUN</th>
                    <th style="width: 20%; text-align: right;">DEBIT</th>
                    <th style="width: 20%; text-align: right;">KREDIT</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1-1400</td>
                    <td>Persediaan Barang Dagang</td>
                    <td style="text-align: right;">{formatted_hpp}</td>
                    <td style="text-align: right;"></td>
                </tr>
                <tr>
                    <td>5-1100</td>
                    <td>Harga Pokok Penjualan</td>
                    <td style="text-align: right;"></td>
                    <td style="text-align: right;">{formatted_hpp}</td>
                </tr>
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="2">Total</td>
                    <td style="text-align: right;">{formatted_hpp}</td>
                    <td style="text-align: right;">{formatted_hpp}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    return render_dashboard_layout('retur_penjualan', content)

# Contoh Dummy Database Pelanggan & Piutang Belum Lunas (Faktur)
DATABASE_PELANGGAN = [
    {
        'kode': 'C001', 
        'nama': 'PT JAYA', 
        'piutang': [
            {'no_faktur': 'INV/2026/1001', 'tanggal': '01/10/2026', 'jatuh_tempo': '15/10/2026', 'total': 5000000, 'sisa': 2500000},
            {'no_faktur': 'INV/2026/1015', 'tanggal': '10/10/2026', 'jatuh_tempo': '24/10/2026', 'total': 3000000, 'sisa': 3000000}
        ]
    },
    {
        'kode': 'C002', 
        'nama': 'CV MAKMUR ABADI', 
        'piutang': [
            {'no_faktur': 'INV/2026/1008', 'tanggal': '05/10/2026', 'jatuh_tempo': '20/10/2026', 'total': 4500000, 'sisa': 4500000}
        ]
    }
]

# --- PENERIMAAN KAS ROUTES
@app.route('/transaksi/penerimaan-kas', methods=['GET', 'POST'])
def penerimaan_kas():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pelanggan = user_data.get('pelanggan', [])
    list_akun = user_data.get('akun', DEFAULT_AKUN)
    list_penjualan = user_data.get('penjualan', [])
    list_penerimaan = user_data.get('penerimaan_kas', [])

    active_tab = request.args.get('tab', 'pelunasan') # 'pelunasan' atau 'lain'

    if request.method == 'POST':
        jenis_transaksi = request.form.get('jenis_transaksi', 'pelunasan')
        tanggal = request.form.get('tanggal')
        akun_kas_input = request.form.get('akun_kas')
        no_bukti = request.form.get('no_bukti', '').strip()
        memo_utama = request.form.get('memo', '').strip()
        
        nama_akun_kas_bersih = akun_kas_input.split(' - ')[1] if ' - ' in akun_kas_input else akun_kas_input

        if jenis_transaksi == 'pelunasan':
            pelanggan = request.form.get('pelanggan')
            if not no_bukti:
                no_bukti = f"BKM-{len(list_penerimaan) + 1:03d}"
            
            jumlah_diterima = float(request.form.get('jumlah_diterima', '0').replace('.', '') or 0)
            potongan = float(request.form.get('potongan', '0').replace('.', '') or 0)
            
            faktur_terpilih = request.form.getlist('faktur_terpilih[]')
            bayar_list = request.form.getlist('bayar_alokasi[]')

            alokasi_faktur = []
            for idx, fak_no in enumerate(faktur_terpilih):
                val_bayar = float(bayar_list[idx].replace('.', '') or 0) if idx < len(bayar_list) else 0
                if val_bayar > 0:
                    alokasi_faktur.append(fak_no)
                    for tr in list_penjualan:
                        if tr.get('nomor') == fak_no:
                            try:
                                sisa_lama = float(str(tr.get('sisa', tr.get('total'))).replace('.', '') or 0)
                                total_hapus = val_bayar + (potongan / len(faktur_terpilih) if potongan > 0 else 0)
                                sisa_baru = max(0, sisa_lama - total_hapus)
                                tr['sisa'] = f"{int(sisa_baru):,.0f}".replace(',', '.')
                                if sisa_baru == 0:
                                    tr['status'] = 'Lunas'
                                else:
                                    tr['status'] = 'Sebagian'
                            except:
                                pass

            total_pengaruh_piutang = jumlah_diterima + potongan
            for acc in list_akun:
                acc_str = f"{acc.get('kode')} - {acc.get('nama')}"
                if acc_str == akun_kas_input or acc.get('kode') in akun_kas_input:
                    try:
                        saldo_lama = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(saldo_lama + jumlah_diterima):,.0f}".replace(',', '.')
                    except:
                        pass
                if 'Piutang Usaha' in acc.get('nama'):
                    try:
                        saldo_piutang = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(max(0, saldo_piutang - total_pengaruh_piutang)):,.0f}".replace(',', '.')
                    except:
                        pass

            keterangan_final = memo_utama if memo_utama else f"Pelunasan piutang - {pelanggan}"

            penerimaan_obj = {
                'jenis': 'pelunasan',
                'no_bukti': no_bukti,
                'tanggal': tanggal,
                'dari': pelanggan,
                'akun_kas': nama_akun_kas_bersih,
                'akun_tabel': 'Piutang Usaha', # Hanya nama akun kredit saja
                'memo': keterangan_final,
                'jumlah_pembayaran': jumlah_diterima,
                'potongan': potongan,
                'kredit_akun': 'Piutang Usaha',
                'alokasi': alokasi_faktur
            }
            user_data.setdefault('penerimaan_kas', []).append(penerimaan_obj)
            return redirect(url_for('penerimaan_kas', tab='pelunasan'))

        else:
            # Penerimaan Lain
            if not no_bukti:
                no_bukti = f"BKM-Lain-{len(list_penerimaan) + 1:03d}"
            
            diterima_dari = request.form.get('diterima_dari', '-')
            akun_baris = request.form.getlist('akun_baris[]')
            jumlah_baris = request.form.getlist('jumlah_baris[]')
            keterangan_baris = request.form.getlist('keterangan_baris[]')

            total_jumlah_lain = 0
            detail_item_lain = []
            akun_kredit_list = []

            for idx, ak in enumerate(akun_baris):
                if ak and idx < len(jumlah_baris):
                    val_jml = float(jumlah_baris[idx].replace('.', '') or 0)
                    if val_jml > 0:
                        total_jumlah_lain += val_jml
                        nama_akun_lawan = ak.split(' - ')[1] if ' - ' in ak else ak
                        akun_kredit_list.append(nama_akun_lawan)
                        detail_item_lain.append({
                            'akun': nama_akun_lawan,
                            'jumlah': val_jml,
                            'keterangan': keterangan_baris[idx] if idx < len(keterangan_baris) else ''
                        })

            for acc in list_akun:
                acc_str = f"{acc.get('kode')} - {acc.get('nama')}"
                if acc_str == akun_kas_input or acc.get('kode') in akun_kas_input:
                    try:
                        saldo_lama = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(saldo_lama + total_jumlah_lain):,.0f}".replace(',', '.')
                    except:
                        pass

            keterangan_final = memo_utama if memo_utama else f"Penerimaan lain dari {diterima_dari}"
            str_akun_kredit = ", ".join(akun_kredit_list)

            penerimaan_obj = {
                'jenis': 'lain',
                'no_bukti': no_bukti,
                'tanggal': tanggal,
                'dari': diterima_dari,
                'akun_kas': nama_akun_kas_bersih,
                'akun_tabel': str_akun_kredit, # Hanya nama akun kredit saja
                'memo': keterangan_final,
                'jumlah_pembayaran': total_jumlah_lain,
                'potongan': 0,
                'kredit_akun': str_akun_kredit,
                'detail_lain': detail_item_lain
            }
            user_data.setdefault('penerimaan_kas', []).append(penerimaan_obj)
            return redirect(url_for('penerimaan_kas', tab='lain'))

    today_date = datetime.now().strftime('%Y-%m-%d')
    current_date_formatted = datetime.now().strftime('%d %b %Y')

    # Dropdown Pelanggan
    options_pelanggan = '<option value="">ketik kode atau nama...</option>'
    for p in list_pelanggan:
        p_nama = p.get('nama')
        options_pelanggan += f'<option value="{p_nama}">{p.get("kode")} — {p_nama}</option>'

    # Dropdown Akun Kas / Bank / Kas Kecil
    options_akun_kas = ""
    for acc in list_akun:
        if acc.get('kategori') == '1 — Aset' and ('Kas' in acc.get('nama') or 'Bank' in acc.get('nama')):
            selected = 'selected' if '1-1100' in acc.get('kode') else ''
            options_akun_kas += f'<option value="{acc.get("kode")} - {acc.get("nama")}" {selected}>{acc.get("kode")} — {acc.get("nama")}</option>'

    # Dropdown Semua Akun untuk Penerimaan Lain
    options_semua_akun = '<option value="">-- Pilih Akun --</option>'
    for acc in list_akun:
        options_semua_akun += f'<option value="{acc.get("kode")} - {acc.get("nama")}">{acc.get("kode")} — {acc.get("nama")}</option>'

    # Render Tabel Daftar & Jurnal
    if not list_penerimaan:
        table_penerimaan_html = '<div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">Belum ada data pada periode ini.</div>'
        table_jurnal_html = '<div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">Belum ada jurnal pada periode ini.</div>'
    else:
        rows_pk = ""
        rows_jpk = ""
        sum_kas_debit = 0
        sum_pot_debit = 0
        sum_kredit_total = 0

        for pk in list_penerimaan:
            val_jumlah = float(pk.get('jumlah_pembayaran', 0) or 0)
            val_potongan = float(pk.get('potongan', 0) or 0)
            total_kredit = val_jumlah + val_potongan

            sum_kas_debit += val_jumlah
            sum_pot_debit += val_potongan
            sum_kredit_total += total_kredit

            tgl_raw = pk.get('tanggal', '')
            try:
                dt_obj = datetime.strptime(tgl_raw, '%Y-%m-%d')
                months_id = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des']
                tgl_formatted = f"{dt_obj.day} {months_id[dt_obj.month]} {dt_obj.year}"
            except:
                tgl_formatted = tgl_raw

            formatted_jumlah = f"{int(val_jumlah):,.0f}".replace(',', '.')
            formatted_potongan = f"{int(val_potongan):,.0f}".replace(',', '.') if val_potongan > 0 else '-'
            formatted_kredit = f"{int(total_kredit):,.0f}".replace(',', '.')

            rows_pk += f"""
            <tr>
                <td style="padding: 12px 16px;">{tgl_formatted}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #d18a99;">{pk.get('no_bukti')}</td>
                <td style="padding: 12px 16px;">{pk.get('dari')}</td>
                <td style="padding: 12px 16px; font-weight: 500; color: #374151;">{pk.get('akun_tabel')}</td>
                <td style="padding: 12px 16px;">{pk.get('akun_kas')}</td>
                <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #047857;">{formatted_jumlah}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_potongan}</td>
            </tr>
            """

            rows_jpk += f"""
            <tr>
                <td style="padding: 12px 16px;">{tgl_formatted}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #d18a99;">{pk.get('no_bukti')}</td>
                <td style="padding: 12px 16px;">{pk.get('memo')}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_jumlah}</td>
                <td style="padding: 12px 16px; text-align: right;">{f"{int(val_potongan):,.0f}".replace(',', '.') if val_potongan > 0 else '-'}</td>
                <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #b45309;">{pk.get('kredit_akun')}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_kredit}</td>
            </tr>
            """

        table_penerimaan_html = f"""
        <table class="account-table">
            <thead>
                <tr>
                    <th>TANGGAL</th>
                    <th>NO. BUKTI</th>
                    <th>DARI</th>
                    <th>AKUN</th>
                    <th>AKUN KAS</th>
                    <th style="text-align: right;">JUMLAH</th>
                    <th style="text-align: right;">POTONGAN</th>
                </tr>
            </thead>
            <tbody>{rows_pk}</tbody>
        </table>
        """

        table_jurnal_html = f"""
        <div style="overflow-x: auto;">
        <table class="account-table" style="min-width: 950px;">
            <thead>
                <tr>
                    <th rowspan="2" style="vertical-align: middle;">TANGGAL</th>
                    <th rowspan="2" style="vertical-align: middle;">NO. BUKTI</th>
                    <th rowspan="2" style="vertical-align: middle;">KETERANGAN</th>
                    <th style="text-align: right; background: #f3f4f6;">Kas / Bank</th>
                    <th style="text-align: right; background: #f3f4f6;">Potongan Penjualan</th>
                    <th rowspan="2" style="text-align: right; vertical-align: middle; background: #fef3c7;">AKUN KREDIT</th>
                    <th style="text-align: right; background: #f3f4f6;">Jumlah Kredit</th>
                </tr>
                <tr>
                    <th style="text-align: right; font-size: 10px; color: #047857;">DEBIT</th>
                    <th style="text-align: right; font-size: 10px; color: #047857;">DEBIT</th>
                    <th style="text-align: right; font-size: 10px; color: #b45309;">KREDIT</th>
                </tr>
            </thead>
            <tbody>
                {rows_jpk}
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="3" style="padding: 12px 16px;">Total ({len(list_penerimaan)} bukti)</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_kas_debit):,.0f}".replace(',', '.')}</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_pot_debit):,.0f}".replace(',', '.') if sum_pot_debit > 0 else '-'}</td>
                    <td style="text-align: right;">-</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_kredit_total):,.0f}".replace(',', '.')}</td>
                </tr>
            </tbody>
        </table>
        </div>
        """

    # Form Content Berdasarkan Tab Aktif
    if active_tab == 'pelunasan':
        form_tab_content = f"""
        <input type="hidden" name="jenis_transaksi" value="pelunasan">
        <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr 1fr; gap: 20px; margin-bottom: 20px;" class="form-group">
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Tanggal <span style="color: #ef4444;">*</span></label>
                <input type="date" name="tanggal" id="inputTanggalPK" value="{today_date}" onchange="hitungDiskonTerminOtomatis()" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Pelanggan (kode / nama) <span style="color: #ef4444;">*</span></label>
                <select name="pelanggan" id="selectPelangganPK" onchange="muatTagihanPelanggan(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_pelanggan}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Setor ke akun <span style="color: #ef4444;">*</span></label>
                <select name="akun_kas" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_akun_kas}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">No. bukti</label>
                <input type="text" name="no_bukti" placeholder="BKM-otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                <span style="font-size: 11px; color: #6b7280; margin-top: 2px; display: block;">Kosong = otomatis</span>
            </div>
        </div>

        <!-- 3 KOTAK DI BAWAH PELANGGAN -->
        <div id="wrapperDetailPelanggan" style="display: none;">
            <div style="display: grid; grid-template-columns: 220px 1fr 1fr 200px; gap: 20px; align-items: start; background: #fdf2f4; border: 1px solid #fce7ec; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #f5d0d8;">
                    <div style="font-size: 11px; color: #6b7280;">Sisa piutang per {current_date_formatted}</div>
                    <div id="labelSisaPiutangTotal" style="font-size: 18px; font-weight: 700; color: #1f2937; margin-top: 4px;">Rp 0</div>
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Jumlah diterima <span style="color: #ef4444;">*</span></label>
                    <input type="text" name="jumlah_diterima" id="inputJumlahDiterima" value="0" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;">
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Potongan</label>
                    <input type="text" name="potongan" id="inputPotongan" value="0" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;">
                    <div style="font-size: 11px; color: #6b7280; margin-top: 3px;">Otomatis: diskon termin untuk faktur yang lunas dalam masa diskon</div>
                </div>
                <div style="padding-top: 22px;">
                    <button type="button" onclick="lunasiSeluruhPiutang()" style="background: white; border: 1px solid #d18a99; color: #d18a99; padding: 8px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; width: 100%;">Lunasi seluruh piutang</button>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Memo (Keterangan)</label>
                <input type="text" name="memo" placeholder="Kosongkan jika ingin otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>

            <!-- TABEL ALOKASI FAKTUR -->
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; margin-top: 15px; background: white;">
                <div style="padding: 12px 16px; background: #f9fafb; font-size: 13px; font-weight: 500; color: #374151; border-bottom: 1px solid #e5e7eb;">
                    Alokasi faktur (klik baris untuk memilih faktur tertentu)
                </div>
                <div id="containerTagihan" style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
                    Pilih pelanggan untuk melihat sisa piutang.
                </div>
            </div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 12px;">
                Cukup isi jumlah yang diterima: saldo piutang pelanggan berkurang, dan pembayaran otomatis dicatat ke transaksi terlama lebih dulu (termasuk transaksi bulan sebelumnya).
            </div>
        </div>
        """
    else:
        form_tab_content = f"""
        <input type="hidden" name="jenis_transaksi" value="lain">
        <div style="display: grid; grid-template-columns: 1fr 2fr 2fr 1fr; gap: 20px; margin-bottom: 20px;" class="form-group">
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Tanggal <span style="color: #ef4444;">*</span></label>
                <input type="date" name="tanggal" value="{today_date}" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;" required>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Masuk ke akun <span style="color: #ef4444;">*</span></label>
                <select name="akun_kas" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_akun_kas}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Diterima dari</label>
                <input type="text" name="diterima_dari" placeholder="Sumber penerimaan" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">No. bukti</label>
                <input type="text" name="no_bukti" placeholder="BKM-otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                <span style="font-size: 11px; color: #6b7280; margin-top: 2px; display: block;">Kosong = otomatis</span>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="font-size: 13px; color: #374151; font-weight: 500;">Memo</label>
            <input type="text" name="memo" placeholder="Keterangan" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
        </div>

        <!-- TABEL BARIS PENERIMAAN LAIN -->
        <div style="border: 1px solid #e5e7eb; border-radius: 8px; background: white; overflow: hidden; margin-top: 20px;">
            <table class="account-table" style="margin-bottom: 0;">
                <thead>
                    <tr>
                        <th style="width: 6%;">#</th>
                        <th style="width: 44%;">Akun (kode / nama)</th>
                        <th style="width: 20%; text-align: right;">Jumlah</th>
                        <th style="width: 24%;">Keterangan</th>
                        <th style="width: 6%; text-align: center;"></th>
                    </tr>
                </thead>
                <tbody id="tbodyPenerimaanLain">
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">1</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLain(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">2</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLain(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">3</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLain(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div style="padding: 10px 16px; background: #f9fafb; border-top: 1px solid #e5e7eb;">
                <button type="button" onclick="tambahBarisLain()" style="background: none; border: none; color: #d18a99; font-weight: 600; font-size: 13px; cursor: pointer;">+ Tambah baris</button>
            </div>
        </div>
        """

    content = f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div class="page-title">Penerimaan Kas</div>
                <div class="page-desc" style="margin-bottom: 15px; color: #6b7280; font-size: 13px;">
                    Pelunasan piutang pelanggan (BKM) dan penerimaan kas lain-lain seperti pendapatan bunga atau setoran modal.
                </div>
            </div>
            <div>
                <button type="submit" form="formPenerimaanKas" style="background-color: #d18a99; color: white; border: none; padding: 10px 24px; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer;">Simpan</button>
            </div>
        </div>

        <!-- TABS -->
        <div style="display: flex; border-bottom: 1px solid #e5e7eb; gap: 30px; margin-bottom: 20px;">
            <a href="/transaksi/penerimaan-kas?tab=pelunasan" style="padding-bottom: 10px; font-size: 14px; font-weight: 600; text-decoration: none; color: {'#d18a99' if active_tab == 'pelunasan' else '#6b7280'}; border-bottom: 2px solid {'#d18a99' if active_tab == 'pelunasan' else 'transparent'};">Pelunasan Piutang</a>
            <a href="/transaksi/penerimaan-kas?tab=lain" style="padding-bottom: 10px; font-size: 14px; font-weight: 600; text-decoration: none; color: {'#d18a99' if active_tab == 'lain' else '#6b7280'}; border-bottom: 2px solid {'#d18a99' if active_tab == 'lain' else 'transparent'};">Penerimaan Lain</a>
        </div>
    </div>

    <div class="card-form" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 30px; position: relative;">
        <form action="/transaksi/penerimaan-kas?tab={active_tab}" method="POST" id="formPenerimaanKas">
            {form_tab_content}
        </form>
    </div>

    <!-- LIST & JURNAL DI BAWAH -->
    <div class="account-card" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="font-weight: 600; font-size: 15px; color: #1f2937;">Daftar pelunasan / penerimaan kas</div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <input type="date" value="2026-01-01" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 12px;">
                <span style="font-size: 12px; color: #6b7280;">s.d.</span>
                <input type="date" value="2026-10-31" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 12px;">
            </div>
        </div>
        {table_penerimaan_html}
    </div>

    <div class="account-card" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px;">
        <div style="font-weight: 600; font-size: 15px; color: #1f2937; margin-bottom: 15px;">Jurnal Penerimaan Kas</div>
        {table_jurnal_html}
    </div>

    <script>
        const daftarPenjualanPK = {json.dumps(list_penjualan)};
        let activeTagihanPelanggan = [];

        function muatTagihanPelanggan(selectEl) {{
            const namaPelanggan = selectEl.value;
            const wrapperDetail = document.getElementById('wrapperDetailPelanggan');
            const labelSisa = document.getElementById('labelSisaPiutangTotal');
            
            if(!namaPelanggan) {{
                if(wrapperDetail) wrapperDetail.style.display = 'none';
                activeTagihanPelanggan = [];
                return;
            }}

            if(wrapperDetail) wrapperDetail.style.display = 'block';

            activeTagihanPelanggan = daftarPenjualanPK.filter(tr => tr.pelanggan.toLowerCase() === namaPelanggan.toLowerCase());
            
            let totalSisaPiutang = 0;
            activeTagihanPelanggan.forEach(tr => {{
                let sisaVal = parseFloat(String(tr.sisa || tr.total).replace(/[^\\d]/g, '') || 0);
                totalSisaPiutang += sisaVal;
            }});

            if(labelSisa) {{
                labelSisa.innerText = 'Rp ' + new Intl.NumberFormat('id-ID').format(totalSisaPiutang);
            }}

            renderTabelAlokasi([]);
        }}

        function renderTabelAlokasi(selectedFakturs = []) {{
            const container = document.getElementById('containerTagihan');
            if(activeTagihanPelanggan.length === 0) {{
                container.innerHTML = 'Tidak ada tagihan/faktur untuk pelanggan ini.';
                return;
            }}

            let rowsHtml = '';
            activeTagihanPelanggan.forEach((tr, idx) => {{
                let isChecked = selectedFakturs.includes(tr.nomor) ? 'checked' : '';
                let sisaStr = tr.sisa || tr.total;
                let dibayarVal = selectedFakturs.includes(tr.nomor) ? sisaStr : '0';

                rowsHtml += `
                <tr onclick="togglePilihFaktur('${{tr.nomor}}')" style="cursor: pointer;">
                    <td style="padding: 12px 16px;"><input type="checkbox" name="faktur_terpilih[]" value="${{tr.nomor}}" data-sisa="${{sisaStr}}" data-tanggal="${{tr.tanggal}}" ${{isChecked}} onclick="event.stopPropagation(); updateJumlahDiterimaOtomatis();" style="cursor: pointer;"></td>
                    <td style="padding: 12px 16px;"><strong>${{tr.nomor}}</strong> ${{tr.status === 'Saldo Awal' || idx === 0 ? '<span style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 11px; color: #4b5563; margin-left: 6px;">Saldo awal</span>' : ''}}</td>
                    <td style="padding: 12px 16px;">${{tr.tanggal_indo || tr.tanggal}}<br><span style="font-size: 11px; color: #6b7280;">JT ${{tr.jatuh_tempo || '-'}}</span></td>
                    <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #1f2937;">Rp ${{sisaStr}}</td>
                    <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #047857;" id="bayar_disp_${{tr.nomor}}">Rp ${{selectedFakturs.includes(tr.nomor) ? sisaStr : '0'}}</td>
                    <td style="padding: 12px 16px; text-align: right; color: #6b7280;" id="potongan_disp_${{tr.nomor}}">Rp 0</td>
                    <input type="hidden" name="bayar_alokasi[]" id="bayar_val_${{tr.nomor}}" value="${{dibayarVal}}">
                </tr>
                `;
            }});

            container.innerHTML = `
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 8%;">PILIH</th>
                        <th style="width: 25%;">NO. FAKTUR</th>
                        <th style="width: 22%;">TANGGAL</th>
                        <th style="width: 15%; text-align: right;">SISA</th>
                        <th style="width: 15%; text-align: right;">DIBAYAR</th>
                        <th style="width: 15%; text-align: right;">POTONGAN</th>
                    </tr>
                </thead>
                <tbody>${{rowsHtml}}</tbody>
            </table>
            `;
        }}

        function togglePilihFaktur(nomorFaktur) {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            checkboxes.forEach(cb => {{
                if(cb.value === nomorFaktur) {{
                    cb.checked = !cb.checked;
                }}
            }});
            updateJumlahDiterimaOtomatis();
        }}

        function lunasiSeluruhPiutang() {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            checkboxes.forEach(cb => {{
                cb.checked = true;
            }});
            updateJumlahDiterimaOtomatis();
        }}

        function updateJumlahDiterimaOtomatis() {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            const inputDiterima = document.getElementById('inputJumlahDiterima');
            const inputPotongan = document.getElementById('inputPotongan');
            const tglBayarStr = document.getElementById('inputTanggalPK').value;
            const tglBayar = new Date(tglBayarStr);

            let totalDibayar = 0;
            let totalPotongan = 0;

            checkboxes.forEach(cb => {{
                let nomor = cb.value;
                let sisaStr = cb.getAttribute('data-sisa');
                let tglFakturStr = cb.getAttribute('data-tanggal');
                let sisaNum = parseFloat(sisaStr.replace(/[^\\d]/g, '') || 0);
                
                let dispEl = document.getElementById('bayar_disp_' + nomor);
                let hiddenEl = document.getElementById('bayar_val_' + nomor);
                let potDispEl = document.getElementById('potongan_disp_' + nomor);

                if(cb.checked) {{
                    let diskonFaktur = 0;
                    if(tglFakturStr) {{
                        let tglFak = new Date(tglFakturStr);
                        let selisihHari = Math.floor((tglBayar - tglFak) / (1000 * 60 * 60 * 24));
                        if(selisihHari >= 0 && selisihHari <= 10) {{
                            diskonFaktur = Math.round(sisaNum * 0.01); 
                        }}
                    }}

                    let bayarBersih = sisaNum - diskonFaktur;
                    totalDibayar += bayarBersih;
                    totalPotongan += diskonFaktur;

                    dispEl.innerText = 'Rp ' + new Intl.NumberFormat('id-ID').format(bayarBersih);
                    hiddenEl.value = new Intl.NumberFormat('id-ID').format(bayarBersih);
                    potDispEl.innerText = diskonFaktur > 0 ? 'Rp ' + new Intl.NumberFormat('id-ID').format(diskonFaktur) : 'Rp 0';
                }} else {{
                    dispEl.innerText = 'Rp 0';
                    hiddenEl.value = '0';
                    potDispEl.innerText = 'Rp 0';
                }}
            }});

            inputDiterima.value = new Intl.NumberFormat('id-ID').format(totalDibayar);
            inputPotongan.value = new Intl.NumberFormat('id-ID').format(totalPotongan);
        }}

        function hitungDiskonTerminOtomatis() {{
            updateJumlahDiterimaOtomatis();
        }}

        function tambahBarisLain() {{
            const tbody = document.getElementById('tbodyPenerimaanLain');
            const rowCount = tbody.rows.length + 1;
            const newRow = tbody.insertRow();
            newRow.innerHTML = `
                <td style="padding: 10px 16px; text-align: center; color: #6b7280;">${{rowCount}}</td>
                <td style="padding: 10px 16px;">
                    <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                        {options_semua_akun}
                    </select>
                </td>
                <td style="padding: 10px 16px;">
                    <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahPK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                </td>
                <td style="padding: 10px 16px;">
                    <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                </td>
                <td style="padding: 10px 16px; text-align: center;">
                    <button type="button" onclick="hapusBarisLain(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                </td>
            `;
        }}

        function hapusBarisLain(btn) {{
            const row = btn.closest('tr');
            if(row.parentNode.rows.length > 1) {{
                row.remove();
                const rows = document.getElementById('tbodyPenerimaanLain').rows;
                for(let i=0; i<rows.length; i++) {{
                    rows[i].cells[0].innerText = i + 1;
                }}
            }}
        }}

        function formatRupiahPK(el) {{
            let angka = el.value.replace(/[^\\d]/g, '');
            if (angka === "") {{ el.value = "0"; }}
            else {{ el.value = new Intl.NumberFormat('id-ID').format(angka); }}
        }}
    </script>
    """
    return render_dashboard_layout('penerimaan_kas', content)

# --- HALAMAN PEMBELIAN ---
@app.route('/transaksi/pembelian')
def transaksi_pembelian():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pembelian = user_data.get('pembelian', [])

    if not list_pembelian:
        table_pembelian_html = """
        <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
            Tidak ada transaksi pembelian pada periode ini.
        </div>
        """
        table_jurnal_html = """
        <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
            Belum ada jurnal pembelian.
        </div>
        """
    else:
        rows_p = ""
        rows_j = ""
        total_nilai_trx = 0
        count_trx = 0
        sum_persediaan = 0
        sum_ppn = 0
        sum_utang = 0

        for tr in list_pembelian:
            count_trx += 1
            try:
                t_val = int(str(tr.get('total', '0')).replace('.', ''))
            except:
                t_val = 0
            total_nilai_trx += t_val

            no_faktur_display = tr.get('nomor')
            detail_url = f"/transaksi/pembelian/ubah/{tr.get('nomor')}"
            status_badge_html = f'<span class="badge-lunas">Lunas</span>' if tr.get('status') == 'Lunas' else f'<span class="badge-belum-lunas">{tr.get("status", "Belum lunas")}</span>'

            rows_p += f"""
            <tr>
                <td style="padding: 12px 20px;">{tr.get('tanggal_indo', tr.get('tanggal'))}</td>
                <td style="padding: 12px 20px;"><a href="{detail_url}" style="color: #d18a99; font-weight: 600; text-decoration: none;">{no_faktur_display}</a></td>
                <td style="padding: 12px 20px;">{tr.get('pemasok')}</td>
                <td style="padding: 12px 20px;">{status_badge_html}</td>
                <td style="padding: 12px 20px;">{tr.get('jatuh_tempo', '-')}</td>
                <td style="padding: 12px 20px; text-align: right;">{tr.get('total')}</td>
            </tr>
            """

            dpp_val = int(tr.get('dpp', 0) or t_val)
            ppn_val = int(tr.get('ppn', 0) or 0)
            utang_val = t_val

            sum_persediaan += dpp_val
            sum_ppn += ppn_val
            sum_utang += utang_val

            rows_j += f"""
            <tr>
                <td style="padding: 12px 20px; white-space: nowrap;">{tr.get('tanggal_indo', tr.get('tanggal'))}</td>
                <td style="padding: 12px 20px;"><a href="{detail_url}" style="color: #d18a99; font-weight: 600; text-decoration: none;">{tr.get('nomor')}</a></td>
                <td style="padding: 12px 20px;">Pembelian barang dari {tr.get('pemasok')}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{dpp_val:,.0f}".replace(',', '.')}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{ppn_val:,.0f}".replace(',', '.') if ppn_val > 0 else '-'}</td>
                <td style="padding: 12px 20px; text-align: right;">{f"{utang_val:,.0f}".replace(',', '.')}</td>
            </tr>
            """

        formatted_total_trx = f"{total_nilai_trx:,.0f}".replace(',', '.')
        table_pembelian_html = f"""
        <table class="account-table">
            <thead>
                <tr>
                    <th style="width: 15%;">TANGGAL</th>
                    <th style="width: 20%;">NO. FAKTUR</th>
                    <th style="width: 25%;">PEMASOK</th>
                    <th style="width: 12%;">STATUS</th>
                    <th style="width: 13%;">JATUH TEMPO</th>
                    <th style="width: 15%; text-align: right;">TOTAL</th>
                </tr>
            </thead>
            <tbody>
                {rows_p}
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="5" style="padding: 12px 20px;">Total ({count_trx} transaksi)</td>
                    <td style="padding: 12px 20px; text-align: right;">{formatted_total_trx}</td>
                </tr>
            </tbody>
        </table>
        """

        table_jurnal_html = f"""
        <div style="overflow-x: auto;">
        <table class="account-table">
            <thead>
                <tr>
                    <th>TANGGAL</th>
                    <th>NO. BUKTI</th>
                    <th>KETERANGAN</th>
                    <th style="text-align: right;">Persediaan (D)</th>
                    <th style="text-align: right;">PPN Masukan (D)</th>
                    <th style="text-align: right;">Utang Usaha (K)</th>
                </tr>
            </thead>
            <tbody>
                {rows_j}
            </tbody>
        </table>
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Pembelian</div>
            <div class="page-desc" style="margin-bottom: 0;">Pencatatan pembelian barang dagang. Otomatis memperbarui Kartu Stok (menambah qty) dan Kartu Pemasok.</div>
        </div>
        <div>
            <a href="/transaksi/pembelian/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Tambah Pembelian</a>
        </div>
    </div>
    <div class="account-card" style="margin-bottom: 25px;">
        {table_pembelian_html}
    </div>
    <div class="account-card">
        <div style="padding: 15px 20px; font-weight: 600; font-size: 15px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal Pembelian</div>
        {table_jurnal_html}
    </div>
    """
    return render_dashboard_layout('pembelian', content)


@app.route('/transaksi/pembelian/baru', methods=['GET', 'POST'])
def tambah_transaksi_pembelian():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pemasok = user_data.get('pemasok', [])
    list_barang = user_data.get('barang', [])
    
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        pemasok = request.form.get('pemasok')
        no_faktur = request.form.get('no_faktur').strip()
        if not no_faktur:
            no_faktur = f"PB-{len(user_data.get('pembelian', [])) + 1:02d}"
        
        item_barangs = request.form.getlist('item_barang[]')
        item_qtys = request.form.getlist('item_qty[]')
        item_hargas = request.form.getlist('item_harga[]')
        ppn_persen = float(request.form.get('ppn_persen', 0) or 0)
        
        subtotal = 0
        details = []
        for i in range(len(item_barangs)):
            brg_str = item_barangs[i]
            if not brg_str:
                continue
            qty = float(item_qtys[i].replace('.', '') or 0)
            harga = float(item_hargas[i].replace('.', '') or 0)
            jumlah = qty * harga
            subtotal += jumlah
            details.append({'barang': brg_str, 'qty': qty, 'harga': harga, 'jumlah': jumlah})

        dpp = subtotal
        ppn_nominal = dpp * (ppn_persen / 100)
        total_transaksi = dpp + ppn_nominal
        formatted_total = f"{int(total_transaksi):,.0f}".replace(',', '.')

        transaksi = {
            'tanggal': tanggal,
            'tanggal_indo': format_tanggal_pendek_indo(tanggal),
            'nomor': no_faktur,
            'pemasok': pemasok,
            'status': 'Belum lunas',
            'jatuh_tempo': '30 hari',
            'total': formatted_total,
            'dpp': dpp,
            'ppn': ppn_nominal,
            'details': details
        }
        
        if 'pembelian' not in user_data:
            database_user[email]['pembelian'] = []
        database_user[email]['pembelian'].append(transaksi)
        
        return redirect(url_for('transaksi_pembelian'))

    options_pemasok = "".join([f'<option value="{p.get("nama")}">{p.get("kode")} — {p.get("nama")}</option>' for p in list_pemasok])
    options_barang = "".join([f'<option value="{b.get("kode")} - {b.get("nama")}" data-harga="{b.get("harga_pokok", 0)}">{b.get("kode")} {b.get("nama")}</option>' for b in list_barang])
    today_date = datetime.now().strftime('%Y-%m-%d')

    content = f"""
    <div class="page-title">Transaksi Pembelian Baru</div>
    <div class="page-desc">Catat pembelian barang dari pemasok. Stok barang di kartu stok akan bertambah otomatis.</div>
    <div class="card-form">
        <form action="/transaksi/pembelian/baru" method="POST">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 20px;" class="form-group">
                <div>
                    <label>Tanggal <span class="required">*</span></label>
                    <input type="date" name="tanggal" value="{today_date}" required>
                </div>
                <div>
                    <label>Pemasok <span class="required">*</span></label>
                    <select name="pemasok" required>
                        <option value="">-- Pilih Pemasok --</option>
                        {options_pemasok}
                    </select>
                </div>
                <div>
                    <label>No. Faktur</label>
                    <input type="text" name="no_faktur" placeholder="Otomatis jika kosong">
                </div>
            </div>
            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table">
                    <thead>
                        <tr>
                            <th style="width: 5%;">#</th>
                            <th style="width: 45%;">Barang</th>
                            <th style="width: 15%;">Qty</th>
                            <th style="width: 20%; text-align: right;">Harga Beli / Pokok</th>
                            <th style="width: 15%; text-align: right;">Jumlah</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyItemBeli">
                        <tr>
                            <td>1</td>
                            <td><select name="item_barang[]" style="border:none; width:100%;"><option value="">-- Pilih --</option>{options_barang}</select></td>
                            <td><input type="text" name="item_qty[]" value="1" style="border:none; width:100%;"></td>
                            <td><input type="text" name="item_harga[]" value="0" style="border:none; width:100%; text-align:right;"></td>
                            <td style="text-align: right;">0</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="display: flex; justify-content: flex-end;">
                <button type="submit" class="btn-simpan">Simpan Pembelian</button>
            </div>
        </form>
    </div>
    """
    return render_dashboard_layout('pembelian', content)
    
@app.route('/transaksi/pembelian/ubah/<path:nomor>')
def ubah_transaksi_pembelian_detail(nomor):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pembelian = user_data.get('pembelian', [])
    list_pemasok = user_data.get('pemasok', [])
    list_barang = user_data.get('barang', [])
    
    target_trx = None
    for tr in list_pembelian:
        if tr.get('nomor') == nomor:
            target_trx = tr
            break
            
    if not target_trx:
        return redirect(url_for('transaksi_pembelian'))

    options_pemasok = "".join([f'<option value="{p.get("nama")}" {"selected" if p.get("nama") == target_trx.get("pemasok") else ""}>{p.get("kode")} — {p.get("nama")}</option>' for p in list_pemasok])

    rows_item_html = ""
    details = target_trx.get('details', [])
    if not details:
        details = [{'barang': '', 'qty': '', 'harga': 0, 'jumlah': 0}]

    for idx, det in enumerate(details):
        r_num = idx + 1
        q_raw = float(det.get('qty', 0) or 0)
        q_val = f"{int(q_raw)}" if q_raw.is_integer() else f"{q_raw}"
        h_val = f"{int(det.get('harga', 0)):,.0f}".replace(',', '.') if det.get('harga') else ''
        j_val = f"{int(det.get('jumlah', 0)):,.0f}".replace(',', '.') if det.get('jumlah') else '-'
        
        nama_brg_bersih = det.get('barang', '-')
        
        opt_brg_html = '<option value="">-- Pilih Barang --</option>'
        for b in list_barang:
            b_str = f"{b.get('kode')} — {b.get('nama')}"
            sel = "selected" if b_str == det.get('barang') else ""
            opt_brg_html += f'<option value="{b_str}" data-harga="{b.get("harga_beli", b.get("harga_pokok", 0))}" {sel}>{b.get("kode")} {b.get("nama")}</option>'

        rows_item_html += f"""
        <tr>
            <td>{r_num}</td>
            <td>
                <select name="item_barang[]" onchange="updateHargaBeli(this)" style="border:none; width:100%; background:transparent;">
                    {opt_brg_html}
                </select>
            </td>
            <td><input type="text" name="item_qty[]" value="{q_val}" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:left;"></td>
            <td><input type="text" name="item_harga[]" value="{h_val}" oninput="hitungBaris(this)" style="border:none; width:100%; background:transparent; text-align:right;"></td>
            <td style="text-align: right;" class="col-jumlah">{j_val}</td>
            <td style="text-align: center;"><a href="#" onclick="hapusBaris(this); return false;" style="color: #dc2626; text-decoration: none;">✕</a></td>
        </tr>
        """

    total_trx_str = target_trx.get('total', '0')
    subtotal_str = f"{int(target_trx.get('dpp', 0)):,.0f}".replace(',', '.') if target_trx.get('dpp') else total_trx_str
    
    # Menghitung nilai komponen untuk jurnal
    dpp_val = float(target_trx.get('dpp', 0) or 0)
    ppn_val = float(target_trx.get('ppn', 0) or 0)
    beban_angkut_val = float(target_trx.get('beban_angkut_nilai', 0) or 0)
    persediaan_val = dpp_val + beban_angkut_val
    total_val = dpp_val + ppn_val + beban_angkut_val

    formatted_persediaan = f"{int(persediaan_val):,.0f}".replace(',', '.')
    formatted_ppn = f"{int(ppn_val):,.0f}".replace(',', '.') if ppn_val > 0 else ""
    formatted_total_trx = f"{int(total_val):,.0f}".replace(',', '.')

    ppn_persen_val = target_trx.get('ppn_persen', 0)
    ppn_persen_str = f"{int(ppn_persen_val)}" if float(ppn_persen_val).is_integer() else (f"{ppn_persen_val}" if ppn_persen_val else "0")

    diskon_nilai_val = target_trx.get('diskon_nilai', 0)
    diskon_display_str = f"(Rp {int(diskon_nilai_val):,.0f})".replace(',', '.') if diskon_nilai_val and float(diskon_nilai_val) > 0 else "-"
    is_saldo_awal = target_trx.get('is_saldo_awal', False)

    bottom_journals_html = ""
    if not is_saldo_awal:
        # Baris PPN Masukan hanya akan muncul jika nilai PPN > 0
        ppn_row_html = ""
        if ppn_val > 0:
            ppn_row_html = f"""
                            <tr>
                                <td>2-1500</td>
                                <td>PPN Masukan</td>
                                <td style="text-align: right;">{formatted_ppn}</td>
                                <td style="text-align: right;"></td>
                            </tr>
            """

        bottom_journals_html = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px;">
            <div>
                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal</div>
                    <table class="account-table">
                        <thead>
                            <tr>
                                <th>KODE</th>
                                <th>AKUN</th>
                                <th style="text-align: right;">DEBIT</th>
                                <th style="text-align: right;">KREDIT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1-1400</td>
                                <td>Persediaan Barang Dagang</td>
                                <td style="text-align: right;">{formatted_persediaan}</td>
                                <td style="text-align: right;"></td>
                            </tr>
                            {ppn_row_html}
                            <tr>
                                <td>2-1100</td>
                                <td>Utang Usaha</td>
                                <td style="text-align: right;"></td>
                                <td style="text-align: right;">{formatted_total_trx}</td>
                            </tr>
                            <tr style="background-color: #f9fafb; font-weight: 600;">
                                <td colspan="2">Total</td>
                                <td style="text-align: right;">{formatted_total_trx}</td>
                                <td style="text-align: right;">{formatted_total_trx}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                        <span>Retur pembelian</span>
                        <a href="/transaksi/retur-pembelian/baru" class="btn-action" style="padding: 4px 10px; font-size: 12px;">+ Buat retur</a>
                    </div>
                    <div style="padding: 30px; text-align: center; color: #6b7280; font-size: 13px;">
                        Belum ada retur.
                    </div>
                </div>

                <div class="account-card" style="margin-bottom: 25px;">
                    <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Riwayat pelunasan</div>
                    <div style="padding: 30px; text-align: center; color: #6b7280; font-size: 13px;">
                        Belum ada pelunasan.
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        bottom_journals_html = f"""
        <div class="account-card" style="padding: 30px; text-align: center; color: #6b7280; font-size: 13px;">
            Transaksi ini bersumber dari <strong>Saldo Awal Pemasok (Kartu Pemasok)</strong>.
        </div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div>
                <div class="page-title" style="display: flex; align-items: center; gap: 10px;">
                    Transaksi Pembelian {target_trx.get('nomor')} {"<span class='badge-saldo-awal'>Saldo Awal</span>" if is_saldo_awal else ""}
                </div>
                <div style="font-size: 13px; color: #6b7280; margin-top: 4px; display: flex; align-items: center; gap: 8px;">
                    Status: <span class="badge-belum-lunas">{target_trx.get('status', 'Belum lunas')}</span> &nbsp; Sisa tagihan Rp {target_trx.get('sisa', formatted_total_trx)}
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/transaksi/pembelian" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
            <a href="/transaksi/pembelian/baru" class="btn-action" style="padding: 8px 16px; font-weight: 500; background: #fff; border-color: #d18a99; color: #d18a99;">+ Baru</a>
        </div>
    </div>

    <div class="card-form" style="margin-bottom: 25px;">
        <form action="/transaksi/pembelian/baru" method="POST" id="formPembelian">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Tanggal <span class="required">*</span></label>
                    <input type="date" name="tanggal" value="{target_trx.get('tanggal')}" required>
                </div>
                <div>
                    <label>Pemasok (kode / nama) <span class="required">*</span></label>
                    <select name="pemasok" required>{options_pemasok}</select>
                </div>
                <div>
                    <label>No. bukti</label>
                    <input type="text" name="no_faktur" value="{target_trx.get('nomor')}">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px;" class="form-group">
                <div>
                    <label>Pembayaran</label>
                    <select name="pembayaran">
                        <option value="Kredit (dengan termin)" {"selected" if target_trx.get('pembayaran') != 'Tunai' else ""}>Kredit (dengan termin)</option>
                        <option value="Tunai" {"selected" if target_trx.get('pembayaran') == 'Tunai' else ""}>Tunai</option>
                    </select>
                </div>
                <div>
                    <label>Termin</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                        <input type="text" name="termin_pot" value="{target_trx.get('termin_pot', '')}" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_hari" value="{target_trx.get('termin_hari', '')}" placeholder="-" style="text-align: center;">
                        <input type="text" name="termin_jt" value="{target_trx.get('termin_jt', '30')}" style="text-align: center;">
                    </div>
                </div>
                <div>
                    <label>Memo</label>
                    <input type="text" name="memo" value="{target_trx.get('memo', '')}" placeholder="Keterangan">
                </div>
            </div>

            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table" id="tabelItem">
                    <thead>
                        <tr>
                            <th style="width: 5%;">#</th>
                            <th style="width: 45%;">Barang (kode / nama)</th>
                            <th style="width: 15%;">Qty</th>
                            <th style="width: 20%; text-align: right;">Harga beli</th>
                            <th style="width: 15%; text-align: right;">Jumlah</th>
                            <th style="width: 5%; text-align: center;"></th>
                        </tr>
                    </thead>
                    <tbody id="tbodyItem">{rows_item_html}</tbody>
                </table>
            </div>

            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px; margin-bottom: 25px; font-size: 13px;">
                <div style="display: flex; width: 420px; justify-content: space-between; padding: 4px 0;">
                    <span style="color: #6b7280;">Subtotal</span>
                    <span id="displaySubtotal" style="font-weight: 600; min-width: 120px; text-align: right;">{subtotal_str}</span>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">Diskon dagang / rabat</span>
                    <span id="displayDiskonNominal">{diskon_display_str}</span>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="color: #6b7280;">PPN Masukan</span>
                    <div style="display: flex; gap: 5px; align-items: center;">
                        <input type="text" name="ppn_persen" value="{ppn_persen_str}" onfocus="if(this.value==='0') this.value='';" onblur="if(this.value==='') this.value='0';" style="width: 65px; padding: 4px; text-align: right; font-size: 12px;">
                        <span>%</span>
                    </div>
                </div>
                <div style="display: flex; width: 420px; justify-content: space-between; border-top: 2px solid #e5e7eb; padding-top: 10px; font-size: 15px; font-weight: bold; color: #1f2937;">
                    <span>Total</span>
                    <span id="displayTotal" style="min-width: 120px; text-align: right;">{formatted_total_trx}</span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                <button type="button" class="btn-action btn-action-danger" style="padding: 10px 20px; font-weight: 500;">Hapus transaksi</button>
                <button type="submit" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan perubahan</button>
            </div>
        </form>
    </div>

    {bottom_journals_html}
    """
    return render_dashboard_layout('pembelian', content)

@app.route('/transaksi/retur-pembelian')
def transaksi_retur_pembelian():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_retur = user_data.get('retur_pembelian', [])

    rows = ""
    for r in list_retur:
        rows += f"""
        <tr>
            <td style="padding: 12px 20px;">{r.get('tanggal')}</td>
            <td style="padding: 12px 20px; font-weight: 600; color: #d18a99;">{r.get('nomor')}</td>
            <td style="padding: 12px 20px;">{r.get('pemasok')}</td>
            <td style="padding: 12px 20px;">{r.get('keterangan', '-')}</td>
            <td style="padding: 12px 20px; text-align: right;">{r.get('total')}</td>
        </tr>
        """

    table_html = f"""
    <table class="account-table">
        <thead>
            <tr>
                <th>TANGGAL</th>
                <th>NO. RETUR</th>
                <th>PEMASOK</th>
                <th>KETERANGAN</th>
                <th style="text-align: right;">TOTAL</th>
            </tr>
        </thead>
        <tbody>
            {rows if rows else '<tr><td colspan="5" style="text-align:center; padding:30px; color:#6b7280;">Belum ada retur pembelian.</td></tr>'}
        </tbody>
    </table>
    """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Retur Pembelian</div>
            <div class="page-desc" style="margin-bottom: 0;">Pengembalian barang kepada pemasok. Mengurangi utang dan **mengurangi stok** di kartu stok.</div>
        </div>
        <div>
            <a href="/transaksi/retur-pembelian/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none;">+ Tambah Retur Pembelian</a>
        </div>
    </div>
    <div class="account-card">{table_html}</div>
    """
    return render_dashboard_layout('retur_pembelian', content)


@app.route('/transaksi/retur-pembelian/baru', methods=['GET', 'POST'])
def tambah_retur_pembelian():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pemasok = user_data.get('pemasok', [])
    list_barang = user_data.get('barang', [])
    
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        pemasok = request.form.get('pemasok')
        no_retur = request.form.get('no_retur').strip() or f"RB-{len(user_data.get('retur_pembelian', [])) + 1:02d}"
        keterangan = request.form.get('keterangan', '')
        
        item_barangs = request.form.getlist('item_barang[]')
        item_qtys = request.form.getlist('item_qty[]')
        item_hargas = request.form.getlist('item_harga[]')
        
        subtotal = 0
        details = []
        for i in range(len(item_barangs)):
            brg_str = item_barangs[i]
            if not brg_str:
                continue
            qty = float(item_qtys[i].replace('.', '') or 0)
            harga = float(item_hargas[i].replace('.', '') or 0)
            jumlah = qty * harga
            subtotal += jumlah
            details.append({'barang': brg_str, 'qty': qty, 'harga': harga, 'jumlah': jumlah})

        formatted_total = f"{int(subtotal):,.0f}".replace(',', '.')
        retur_data = {
            'tanggal': tanggal,
            'nomor': no_retur,
            'pemasok': pemasok,
            'keterangan': keterangan,
            'total': formatted_total,
            'details': details
        }
        
        if 'retur_pembelian' not in user_data:
            database_user[email]['retur_pembelian'] = []
        database_user[email]['retur_pembelian'].append(retur_data)
        
        return redirect(url_for('transaksi_retur_pembelian'))

    options_pemasok = "".join([f'<option value="{p.get("nama")}">{p.get("nama")}</option>' for p in list_pemasok])
    options_barang = "".join([f'<option value="{b.get("kode")} - {b.get("nama")}">{b.get("kode")} {b.get("nama")}</option>' for b in list_barang])
    today_date = datetime.now().strftime('%Y-%m-%d')

    content = f"""
    <div class="page-title">Tambah Retur Pembelian Baru</div>
    <div class="page-desc">Barang yang dikembalikan ke pemasok akan otomatis mengurangi stok di kartu stok.</div>
    <div class="card-form">
        <form action="/transaksi/retur-pembelian/baru" method="POST">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 20px;" class="form-group">
                <div><label>Tanggal</label><input type="date" name="tanggal" value="{today_date}" required></div>
                <div><label>Pemasok</label><select name="pemasok" required><option value="">-- Pilih --</option>{options_pemasok}</select></div>
                <div><label>No. Retur</label><input type="text" name="no_retur" placeholder="Otomatis"></div>
            </div>
            <div class="account-card" style="margin: 20px 0;">
                <table class="account-table">
                    <thead>
                        <tr>
                            <th>Barang</th>
                            <th style="width: 15%;">Qty Retur</th>
                            <th style="width: 20%; text-align: right;">Harga Satuan</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><select name="item_barang[]" style="border:none; width:100%;"><option value="">-- Pilih --</option>{options_barang}</select></td>
                            <td><input type="text" name="item_qty[]" value="1" style="border:none; width:100%;"></td>
                            <td><input type="text" name="item_harga[]" value="0" style="border:none; width:100%; text-align:right;"></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="display: flex; justify-content: flex-end;"><button type="submit" class="btn-simpan">Simpan Retur Pembelian</button></div>
        </form>
    </div>
    """
    return render_dashboard_layout('retur_pembelian', content)


@app.route('/transaksi/retur-pembelian/ubah/<path:no_retur>')
def ubah_retur_pembelian_detail(no_retur):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_retur = user_data.get('retur_pembelian', [])
    
    target_retur = None
    for rt in list_retur:
        if rt.get('no_retur') == no_retur:
            target_retur = rt
            break
            
    if not target_retur:
        return redirect(url_for('retur_pembelian'))

    sub_retur = float(target_retur.get('subtotal_retur', 0) or 0)
    ppn_kor = float(target_retur.get('ppn_koreksi', 0) or 0)
    tot_retur = float(target_retur.get('total_retur', 0) or 0)

    formatted_sub = f"{int(sub_retur):,.0f}".replace(',', '.') if sub_retur > 0 else '0'
    formatted_ppn = f"{int(ppn_kor):,.0f}".replace(',', '.') if ppn_kor > 0 else '0'
    formatted_tot = f"{int(tot_retur):,.0f}".replace(',', '.') if tot_retur > 0 else '0'

    ppn_row_html = ""
    if ppn_kor > 0:
        ppn_row_html = f"""
                <tr>
                    <td>2-1500</td>
                    <td>PPN Masukan</td>
                    <td style="text-align: right;"></td>
                    <td style="text-align: right;">{formatted_ppn}</td>
                </tr>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Retur Pembelian {target_retur.get('no_retur')}</div>
            <div style="font-size: 13px; color: #6b7280; margin-top: 4px;">
                Faktur Asal: <strong>{target_retur.get('faktur_asal')}</strong> | Pemasok: <strong>{target_retur.get('pemasok_nama')}</strong>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/transaksi/retur-pembelian" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
        </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <a href="#" class="btn-action btn-action-danger" style="padding: 10px 20px; font-weight: 500;">Hapus retur</a>
        <button type="button" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan perubahan</button>
    </div>

    <div class="account-card" style="margin-bottom: 25px;">
        <div style="padding: 15px 20px; font-weight: 600; font-size: 14px; color: #1f2937; border-bottom: 1px solid #e5e7eb;">Jurnal retur pembelian</div>
        <table class="account-table">
            <thead>
                <tr>
                    <th style="width: 15%;">KODE</th>
                    <th style="width: 45%;">AKUN</th>
                    <th style="width: 20%; text-align: right;">DEBIT</th>
                    <th style="width: 20%; text-align: right;">KREDIT</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>2-1100</td>
                    <td>Utang Usaha</td>
                    <td style="text-align: right;">{formatted_tot}</td>
                    <td style="text-align: right;"></td>
                </tr>
                {ppn_row_html}
                <tr>
                    <td>1-1400</td>
                    <td>Persediaan Barang Dagang</td>
                    <td style="text-align: right;"></td>
                    <td style="text-align: right;">{formatted_sub}</td>
                </tr>
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="2">Total</td>
                    <td style="text-align: right;">{formatted_tot}</td>
                    <td style="text-align: right;">{formatted_tot}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    return render_dashboard_layout('retur_pembelian', content)

@app.route('/transaksi/pengeluaran-kas', methods=['GET', 'POST'])
def pengeluaran_kas():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_pemasok = user_data.get('pemasok', [])
    list_akun = user_data.get('akun', DEFAULT_AKUN)
    list_pembelian = user_data.get('pembelian', [])
    list_pengeluaran = user_data.get('pengeluaran_kas', [])

    active_tab = request.args.get('tab', 'pembayaran') # 'pembayaran' atau 'lain'

    if request.method == 'POST':
        jenis_transaksi = request.form.get('jenis_transaksi', 'pembayaran')
        tanggal = request.form.get('tanggal')
        akun_kas_input = request.form.get('akun_kas')
        no_bukti = request.form.get('no_bukti', '').strip()
        memo_utama = request.form.get('memo', '').strip()
        
        nama_akun_kas_bersih = akun_kas_input.split(' - ')[1] if ' - ' in akun_kas_input else akun_kas_input

        if jenis_transaksi == 'pembayaran':
            pemasok = request.form.get('pemasok')
            if not no_bukti:
                no_bukti = f"BKK-{len(list_pengeluaran) + 1:03d}"
            
            jumlah_dibayar = float(request.form.get('jumlah_dibayar', '0').replace('.', '') or 0)
            potongan = float(request.form.get('potongan', '0').replace('.', '') or 0)
            
            faktur_terpilih = request.form.getlist('faktur_terpilih[]')
            bayar_list = request.form.getlist('bayar_alokasi[]')

            alokasi_faktur = []
            for idx, fak_no in enumerate(faktur_terpilih):
                val_bayar = float(bayar_list[idx].replace('.', '') or 0) if idx < len(bayar_list) else 0
                if val_bayar > 0:
                    alokasi_faktur.append(fak_no)
                    for tr in list_pembelian:
                        if tr.get('nomor') == fak_no:
                            try:
                                sisa_lama = float(str(tr.get('sisa', tr.get('total'))).replace('.', '') or 0)
                                total_hapus = val_bayar + (potongan / len(faktur_terpilih) if potongan > 0 else 0)
                                sisa_baru = max(0, sisa_lama - total_hapus)
                                tr['sisa'] = f"{int(sisa_baru):,.0f}".replace(',', '.')
                                if sisa_baru == 0:
                                    tr['status'] = 'Lunas'
                                else:
                                    tr['status'] = 'Sebagian'
                            except:
                                pass

            total_pengaruh_utang = jumlah_dibayar + potongan
            for acc in list_akun:
                acc_str = f"{acc.get('kode')} — {acc.get('nama')}"
                if acc_str == akun_kas_input or acc.get('kode') in akun_kas_input:
                    try:
                        saldo_lama = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(saldo_lama - jumlah_dibayar):,.0f}".replace(',', '.')
                    except:
                        pass
                if 'Utang Usaha' in acc.get('nama'):
                    try:
                        saldo_utang = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(max(0, saldo_utang - total_pengaruh_utang)):,.0f}".replace(',', '.')
                    except:
                        pass

            keterangan_final = memo_utama if memo_utama else f"Pembayaran utang - {pemasok}"

            pengeluaran_obj = {
                'jenis': 'pembayaran',
                'no_bukti': no_bukti,
                'tanggal': tanggal,
                'kepada': pemasok,
                'akun_kas': nama_akun_kas_bersih,
                'akun_tabel': 'Utang Usaha',
                'memo': keterangan_final,
                'jumlah_pembayaran': jumlah_dibayar,
                'potongan': potongan,
                'debit_akun': 'Utang Usaha',
                'alokasi': alokasi_faktur
            }
            user_data.setdefault('pengeluaran_kas', []).append(pengeluaran_obj)
            return redirect(url_for('pengeluaran_kas', tab='pembayaran'))

        else:
            # Pengeluaran Lain
            if not no_bukti:
                no_bukti = f"BKK-Lain-{len(list_pengeluaran) + 1:03d}"
            
            dibayar_kepada = request.form.get('dibayar_kepada', '-')
            akun_baris = request.form.getlist('akun_baris[]')
            jumlah_baris = request.form.getlist('jumlah_baris[]')
            keterangan_baris = request.form.getlist('keterangan_baris[]')

            total_jumlah_lain = 0
            detail_item_lain = []
            akun_debit_list = []

            for idx, ak in enumerate(akun_baris):
                if ak and idx < len(jumlah_baris):
                    val_jml = float(jumlah_baris[idx].replace('.', '') or 0)
                    if val_jml > 0:
                        total_jumlah_lain += val_jml
                        nama_akun_lawan = ak.split(' — ')[1] if ' — ' in ak else (ak.split(' - ')[1] if ' - ' in ak else ak)
                        akun_debit_list.append(nama_akun_lawan)
                        detail_item_lain.append({
                            'akun': nama_akun_lawan,
                            'jumlah': val_jml,
                            'keterangan': keterangan_baris[idx] if idx < len(keterangan_baris) else ''
                        })

            for acc in list_akun:
                acc_str = f"{acc.get('kode')} — {acc.get('nama')}"
                if acc_str == akun_kas_input or acc.get('kode') in akun_kas_input:
                    try:
                        saldo_lama = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                        acc['saldo'] = f"{int(saldo_lama - total_jumlah_lain):,.0f}".replace(',', '.')
                    except:
                        pass

            keterangan_final = memo_utama if memo_utama else f"Pengeluaran lain kepada {dibayar_kepada}"
            str_akun_debit = ", ".join(akun_debit_list)

            pengeluaran_obj = {
                'jenis': 'lain',
                'no_bukti': no_bukti,
                'tanggal': tanggal,
                'kepada': dibayar_kepada,
                'akun_kas': nama_akun_kas_bersih,
                'akun_tabel': str_akun_debit,
                'memo': keterangan_final,
                'jumlah_pembayaran': total_jumlah_lain,
                'potongan': 0,
                'debit_akun': str_akun_debit,
                'detail_lain': detail_item_lain
            }
            user_data.setdefault('pengeluaran_kas', []).append(pengeluaran_obj)
            return redirect(url_for('pengeluaran_kas', tab='lain'))

    today_date = datetime.now().strftime('%Y-%m-%d')
    current_date_formatted = datetime.now().strftime('%d %b %Y')

    # Dropdown Pemasok
    options_pemasok = '<option value="">ketik kode atau nama...</option>'
    for p in list_pemasok:
        p_nama = p.get('nama')
        options_pemasok += f'<option value="{p_nama}">{p.get("kode")} — {p_nama}</option>'

    # Dropdown Akun Kas / Bank / Kas Kecil
    options_akun_kas = ""
    for acc in list_akun:
        if acc.get('kategori') == '1 — Aset' and ('Kas' in acc.get('nama') or 'Bank' in acc.get('nama')):
            selected = 'selected' if '1-1100' in acc.get('kode') else ''
            options_akun_kas += f'<option value="{acc.get("kode")} — {acc.get("nama")}" {selected}>{acc.get("kode")} — {acc.get("nama")}</option>'

    # Dropdown Semua Akun untuk Pengeluaran Lain (Kecuali akun kontrol Piutang, Utang, Persediaan)
    options_semua_akun = '<option value="">-- Pilih Akun --</option>'
    for acc in list_akun:
        nama_acc = acc.get('nama', '')
        if not any(k in nama_acc for k in ['Piutang', 'Utang', 'Persediaan']):
            options_semua_akun += f'<option value="{acc.get("kode")} — {nama_acc}">{acc.get("kode")} — {nama_acc}</option>'

    # Render Tabel Daftar & Jurnal
    if not list_pengeluaran:
        table_pengeluaran_html = '<div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">Belum ada data pada periode ini.</div>'
        table_jurnal_html = '<div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">Belum ada jurnal pada periode ini.</div>'
    else:
        rows_pk = ""
        rows_jpk = ""
        sum_kas_kredit = 0
        sum_pot_kredit = 0
        sum_debit_total = 0

        for pk in list_pengeluaran:
            val_jumlah = float(pk.get('jumlah_pembayaran', 0) or 0)
            val_potongan = float(pk.get('potongan', 0) or 0)
            total_debit = val_jumlah + val_potongan

            sum_kas_kredit += val_jumlah
            sum_pot_kredit += val_potongan
            sum_debit_total += total_debit

            tgl_raw = pk.get('tanggal', '')
            try:
                dt_obj = datetime.strptime(tgl_raw, '%Y-%m-%d')
                months_id = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des']
                tgl_formatted = f"{dt_obj.day} {months_id[dt_obj.month]} {dt_obj.year}"
            except:
                tgl_formatted = tgl_raw

            formatted_jumlah = f"{int(val_jumlah):,.0f}".replace(',', '.')
            formatted_potongan = f"{int(val_potongan):,.0f}".replace(',', '.') if val_potongan > 0 else '-'
            formatted_debit = f"{int(total_debit):,.0f}".replace(',', '.')

            rows_pk += f"""
            <tr>
                <td style="padding: 12px 16px;">{tgl_formatted}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #d18a99;">{pk.get('no_bukti')}</td>
                <td style="padding: 12px 16px;">{pk.get('kepada')}</td>
                <td style="padding: 12px 16px; font-weight: 500; color: #374151;">{pk.get('akun_tabel')}</td>
                <td style="padding: 12px 16px;">{pk.get('akun_kas')}</td>
                <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #047857;">{formatted_jumlah}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_potongan}</td>
            </tr>
            """

            rows_jpk += f"""
            <tr>
                <td style="padding: 12px 16px;">{tgl_formatted}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #d18a99;">{pk.get('no_bukti')}</td>
                <td style="padding: 12px 16px;">{pk.get('memo')}</td>
                <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #b45309;">{pk.get('debit_akun')}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_debit}</td>
                <td style="padding: 12px 16px; text-align: right;">{f"{int(val_potongan):,.0f}".replace(',', '.') if val_potongan > 0 else '-'}</td>
                <td style="padding: 12px 16px; text-align: right;">{formatted_jumlah}</td>
            </tr>
            """

        table_pengeluaran_html = f"""
        <table class="account-table">
            <thead>
                <tr>
                    <th>TANGGAL</th>
                    <th>NO. BUKTI</th>
                    <th>KEPADA</th>
                    <th>AKUN</th>
                    <th>AKUN KAS</th>
                    <th style="text-align: right;">JUMLAH</th>
                    <th style="text-align: right;">POTONGAN</th>
                </tr>
            </thead>
            <tbody>{rows_pk}</tbody>
        </table>
        """

        table_jurnal_html = f"""
        <div style="overflow-x: auto;">
        <table class="account-table" style="min-width: 950px;">
            <thead>
                <tr>
                    <th rowspan="2" style="vertical-align: middle;">TANGGAL</th>
                    <th rowspan="2" style="vertical-align: middle;">NO. BUKTI</th>
                    <th rowspan="2" style="vertical-align: middle;">KETERANGAN</th>
                    <th rowspan="2" style="text-align: right; vertical-align: middle; background: #fef3c7;">AKUN DEBIT</th>
                    <th style="text-align: right; background: #f3f4f6;">Jumlah Debit</th>
                    <th style="text-align: right; background: #f3f4f6;">Potongan Pembelian</th>
                    <th style="text-align: right; background: #f3f4f6;">Kas / Bank</th>
                </tr>
                <tr>
                    <th style="text-align: right; font-size: 10px; color: #b45309;">DEBIT</th>
                    <th style="text-align: right; font-size: 10px; color: #047857;">KREDIT</th>
                    <th style="text-align: right; font-size: 10px; color: #047857;">KREDIT</th>
                </tr>
            </thead>
            <tbody>
                {rows_jpk}
                <tr style="background-color: #f9fafb; font-weight: 600;">
                    <td colspan="4" style="padding: 12px 16px;">Total ({len(list_pengeluaran)} bukti)</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_debit_total):,.0f}".replace(',', '.')}</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_pot_kredit):,.0f}".replace(',', '.') if sum_pot_kredit > 0 else '-'}</td>
                    <td style="padding: 12px 16px; text-align: right;">{f"{int(sum_kas_kredit):,.0f}".replace(',', '.')}</td>
                </tr>
            </tbody>
        </table>
        </div>
        """

    # Form Content Berdasarkan Tab Aktif
    if active_tab == 'pembayaran':
        form_tab_content = f"""
        <input type="hidden" name="jenis_transaksi" value="pembayaran">
        <div style="font-size: 15px; font-weight: 600; color: #1f2937; margin-bottom: 15px;">Pembayaran utang baru</div>
        <div style="display: grid; grid-template-columns: 1fr 2fr 1.5fr 1fr; gap: 20px; margin-bottom: 20px;" class="form-group">
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Tanggal <span style="color: #ef4444;">*</span></label>
                <input type="date" name="tanggal" id="inputTanggalEK" value="{today_date}" onchange="hitungDiskonTerminOtomatis()" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Pemasok (kode / nama) <span style="color: #ef4444;">*</span></label>
                <select name="pemasok" id="selectPemasokEK" onchange="muatTagihanPemasok(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_pemasok}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Bayar dari akun <span style="color: #ef4444;">*</span></label>
                <select name="akun_kas" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_akun_kas}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">No. bukti</label>
                <input type="text" name="no_bukti" placeholder="BKK-otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                <span style="font-size: 11px; color: #6b7280; margin-top: 2px; display: block;">Kosong = otomatis</span>
            </div>
        </div>

        <!-- 3 KOTAK DI BAWAH PEMASOK -->
        <div id="wrapperDetailPemasok" style="display: none;">
            <div style="display: grid; grid-template-columns: 220px 1fr 1fr 200px; gap: 20px; align-items: start; background: #fdf2f4; border: 1px solid #fce7ec; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #f5d0d8;">
                    <div style="font-size: 11px; color: #6b7280;">Sisa utang per {current_date_formatted}</div>
                    <div id="labelSisaUtangTotal" style="font-size: 18px; font-weight: 700; color: #1f2937; margin-top: 4px;">Rp 0</div>
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Jumlah dibayar <span style="color: #ef4444;">*</span></label>
                    <input type="text" name="jumlah_dibayar" id="inputJumlahDibayar" value="0" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;">
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Potongan</label>
                    <input type="text" name="potongan" id="inputPotonganEK" value="0" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;">
                    <div style="font-size: 11px; color: #6b7280; margin-top: 3px;">Otomatis: diskon termin untuk faktur yang lunas dalam masa diskon</div>
                </div>
                <div style="padding-top: 22px;">
                    <button type="button" onclick="lunasiSeluruhUtang()" style="background: white; border: 1px solid #d18a99; color: #d18a99; padding: 8px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; width: 100%;">Lunasi seluruh utang</button>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Memo (Keterangan)</label>
                <input type="text" name="memo" placeholder="Kosongkan jika ingin otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>

            <!-- TABEL ALOKASI FAKTUR PEMBELIAN -->
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; margin-top: 15px; background: white;">
                <div style="padding: 12px 16px; background: #f9fafb; font-size: 13px; font-weight: 500; color: #374151; border-bottom: 1px solid #e5e7eb;">
                    Alokasi faktur (klik baris untuk memilih faktur tertentu)
                </div>
                <div id="containerTagihanPemasok" style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
                    Pilih pemasok untuk melihat sisa utang.
                </div>
            </div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 12px;">
                Cukup isi jumlah yang dibayar: saldo utang pemasok berkurang, dan pembayaran otomatis dicatat ke transaksi terlama lebih dulu (termasuk transaksi bulan sebelumnya).
            </div>
        </div>
        """
    else:
        form_tab_content = f"""
        <input type="hidden" name="jenis_transaksi" value="lain">
        <div style="font-size: 15px; font-weight: 600; color: #1f2937; margin-bottom: 15px;">Pengeluaran kas lain baru</div>
        <div style="display: grid; grid-template-columns: 1fr 2fr 2fr 1fr; gap: 20px; margin-bottom: 20px;" class="form-group">
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Tanggal <span style="color: #ef4444;">*</span></label>
                <input type="date" name="tanggal" value="{today_date}" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;" required>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Keluar dari akun <span style="color: #ef4444;">*</span></label>
                <select name="akun_kas" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;" required>
                    {options_akun_kas}
                </select>
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">Dibayar kepada</label>
                <input type="text" name="dibayar_kepada" placeholder="Penerima pengeluaran" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            </div>
            <div>
                <label style="font-size: 13px; color: #374151; font-weight: 500;">No. bukti</label>
                <input type="text" name="no_bukti" placeholder="BKK-otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                <span style="font-size: 11px; color: #6b7280; margin-top: 2px; display: block;">Kosong = otomatis</span>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="font-size: 13px; color: #374151; font-weight: 500;">Memo</label>
            <input type="text" name="memo" placeholder="Keterangan" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
        </div>

        <!-- TABEL BARIS PENGELUARAN LAIN -->
        <div style="border: 1px solid #e5e7eb; border-radius: 8px; background: white; overflow: hidden; margin-top: 20px;">
            <table class="account-table" style="margin-bottom: 0;">
                <thead>
                    <tr>
                        <th style="width: 6%;">#</th>
                        <th style="width: 44%;">Akun (kode / nama)</th>
                        <th style="width: 20%; text-align: right;">Jumlah</th>
                        <th style="width: 24%;">Keterangan</th>
                        <th style="width: 6%; text-align: center;"></th>
                    </tr>
                </thead>
                <tbody id="tbodyPengeluaranLain">
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">1</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLainEK(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">2</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLainEK(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 16px; text-align: center; color: #6b7280;">3</td>
                        <td style="padding: 10px 16px;">
                            <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                                {options_semua_akun}
                            </select>
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                        </td>
                        <td style="padding: 10px 16px;">
                            <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                        </td>
                        <td style="padding: 10px 16px; text-align: center;">
                            <button type="button" onclick="hapusBarisLainEK(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div style="padding: 10px 16px; background: #f9fafb; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                <button type="button" onclick="tambahBarisLainEK()" style="background: none; border: none; color: #d18a99; font-weight: 600; font-size: 13px; cursor: pointer;">+ Tambah baris</button>
                <span style="font-size: 11px; color: #6b7280;">Enter/↓ bawah · ↑ atas · Tab kanan · Esc batal · Ctrl+V tempel dari Excel</span>
            </div>
        </div>
        <div style="font-size: 12px; color: #6b7280; margin-top: 12px;">
            Akun kontrol (Piutang, Utang, Persediaan) tidak dapat dipakai di sini — gunakan menu penjualan, pembelian, atau pelunasan. Jurnal: Dr akun-akun lawan / Cr Kas.
        </div>
        """

    content = f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div class="page-title">Pengeluaran Kas</div>
                <div class="page-desc" style="margin-bottom: 15px; color: #6b7280; font-size: 13px;">
                    Pembayaran utang ke pemasok (BKK) dan pengeluaran kas lain-lain seperti beban, pembelian aset, atau prive/dividen.
                </div>
            </div>
            <div>
                <button type="submit" form="formPengeluaranKas" style="background-color: #d18a99; color: white; border: none; padding: 10px 24px; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer;">Simpan</button>
            </div>
        </div>

        <!-- TABS -->
        <div style="display: flex; border-bottom: 1px solid #e5e7eb; gap: 30px; margin-bottom: 20px;">
            <a href="/transaksi/pengeluaran-kas?tab=pembayaran" style="padding-bottom: 10px; font-size: 14px; font-weight: 600; text-decoration: none; color: {'#d18a99' if active_tab == 'pembayaran' else '#6b7280'}; border-bottom: 2px solid {'#d18a99' if active_tab == 'pembayaran' else 'transparent'};">Pembayaran Utang</a>
            <a href="/transaksi/pengeluaran-kas?tab=lain" style="padding-bottom: 10px; font-size: 14px; font-weight: 600; text-decoration: none; color: {'#d18a99' if active_tab == 'lain' else '#6b7280'}; border-bottom: 2px solid {'#d18a99' if active_tab == 'lain' else 'transparent'};">Pengeluaran Lain</a>
        </div>
    </div>

    <div class="card-form" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 30px; position: relative;">
        <form action="/transaksi/pengeluaran-kas?tab={active_tab}" method="POST" id="formPengeluaranKas">
            {form_tab_content}
        </form>
    </div>

    <!-- LIST & JURNAL DI BAWAH -->
    <div class="account-card" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="font-weight: 600; font-size: 15px; color: #1f2937;">Daftar pembayaran utang / pengeluaran</div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <input type="date" value="2026-01-01" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 12px;">
                <span style="font-size: 12px; color: #6b7280;">s.d.</span>
                <input type="date" value="2026-10-31" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 12px;">
            </div>
        </div>
        {table_pengeluaran_html}
    </div>

    <div class="account-card" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px;">
        <div style="font-weight: 600; font-size: 15px; color: #1f2937; margin-bottom: 15px;">Jurnal Pengeluaran Kas</div>
        {table_jurnal_html}
    </div>

    <script>
        const daftarPembelianEK = {json.dumps(list_pembelian)};
        let activeTagihanPemasok = [];

        function muatTagihanPemasok(selectEl) {{
            const namaPemasok = selectEl.value;
            const wrapperDetail = document.getElementById('wrapperDetailPemasok');
            const labelSisa = document.getElementById('labelSisaUtangTotal');
            
            if(!namaPemasok) {{
                if(wrapperDetail) wrapperDetail.style.display = 'none';
                activeTagihanPemasok = [];
                return;
            }}

            if(wrapperDetail) wrapperDetail.style.display = 'block';

            activeTagihanPemasok = daftarPembelianEK.filter(tr => tr.pemasok.toLowerCase() === namaPemasok.toLowerCase());
            
            let totalSisaUtang = 0;
            activeTagihanPemasok.forEach(tr => {{
                let sisaVal = parseFloat(String(tr.sisa || tr.total).replace(/[^\\d]/g, '') || 0);
                totalSisaUtang += sisaVal;
            }});

            if(labelSisa) {{
                labelSisa.innerText = 'Rp ' + new Intl.NumberFormat('id-ID').format(totalSisaUtang);
            }}

            renderTabelAlokasiPemasok([]);
        }}

        function renderTabelAlokasiPemasok(selectedFakturs = []) {{
            const container = document.getElementById('containerTagihanPemasok');
            if(activeTagihanPemasok.length === 0) {{
                container.innerHTML = 'Tidak ada tagihan/faktur untuk pemasok ini.';
                return;
            }}

            let rowsHtml = '';
            activeTagihanPemasok.forEach((tr, idx) => {{
                let isChecked = selectedFakturs.includes(tr.nomor) ? 'checked' : '';
                let sisaStr = tr.sisa || tr.total;
                let dibayarVal = selectedFakturs.includes(tr.nomor) ? sisaStr : '0';

                rowsHtml += `
                <tr onclick="togglePilihFakturPemasok('${{tr.nomor}}')" style="cursor: pointer;">
                    <td style="padding: 12px 16px;"><input type="checkbox" name="faktur_terpilih[]" value="${{tr.nomor}}" data-sisa="${{sisaStr}}" data-tanggal="${{tr.tanggal}}" ${{isChecked}} onclick="event.stopPropagation(); updateJumlahDibayarOtomatis();" style="cursor: pointer;"></td>
                    <td style="padding: 12px 16px;"><strong>${{tr.nomor}}</strong> ${{tr.status === 'Saldo Awal' || idx === 0 ? '<span style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 11px; color: #4b5563; margin-left: 6px;">Saldo awal</span>' : ''}}</td>
                    <td style="padding: 12px 16px;">${{tr.tanggal_indo || tr.tanggal}}<br><span style="font-size: 11px; color: #6b7280;">JT ${{tr.jatuh_tempo || '-'}}</span></td>
                    <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #1f2937;">Rp ${{sisaStr}}</td>
                    <td style="padding: 12px 16px; text-align: right; font-weight: 600; color: #047857;" id="bayar_pemasok_disp_${{tr.nomor}}">Rp ${{selectedFakturs.includes(tr.nomor) ? sisaStr : '0'}}</td>
                    <td style="padding: 12px 16px; text-align: right; color: #6b7280;" id="potongan_pemasok_disp_${{tr.nomor}}">Rp 0</td>
                    <input type="hidden" name="bayar_alokasi[]" id="bayar_pemasok_val_${{tr.nomor}}" value="${{dibayarVal}}">
                </tr>
                `;
            }});

            container.innerHTML = `
            <table class="account-table">
                <thead>
                    <tr>
                        <th style="width: 8%;">PILIH</th>
                        <th style="width: 25%;">NO. FAKTUR</th>
                        <th style="width: 22%;">TANGGAL</th>
                        <th style="width: 15%; text-align: right;">SISA</th>
                        <th style="width: 15%; text-align: right;">DIBAYAR</th>
                        <th style="width: 15%; text-align: right;">POTONGAN</th>
                    </tr>
                </thead>
                <tbody>${{rowsHtml}}</tbody>
            </table>
            `;
        }}

        function togglePilihFakturPemasok(nomorFaktur) {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            checkboxes.forEach(cb => {{
                if(cb.value === nomorFaktur) {{
                    cb.checked = !cb.checked;
                }}
            }});
            updateJumlahDibayarOtomatis();
        }}

        function lunasiSeluruhUtang() {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            checkboxes.forEach(cb => {{
                cb.checked = true;
            }});
            updateJumlahDibayarOtomatis();
        }}

        function updateJumlahDibayarOtomatis() {{
            const checkboxes = document.querySelectorAll('input[name="faktur_terpilih[]"]');
            const inputDibayar = document.getElementById('inputJumlahDibayar');
            const inputPotongan = document.getElementById('inputPotonganEK');
            const tglBayarStr = document.getElementById('inputTanggalEK').value;
            const tglBayar = new Date(tglBayarStr);

            let totalDibayar = 0;
            let totalPotongan = 0;

            checkboxes.forEach(cb => {{
                let nomor = cb.value;
                let sisaStr = cb.getAttribute('data-sisa');
                let tglFakturStr = cb.getAttribute('data-tanggal');
                let sisaNum = parseFloat(sisaStr.replace(/[^\\d]/g, '') || 0);
                
                let dispEl = document.getElementById('bayar_pemasok_disp_' + nomor);
                let hiddenEl = document.getElementById('bayar_pemasok_val_' + nomor);
                let potDispEl = document.getElementById('potongan_pemasok_disp_' + nomor);

                if(cb.checked) {{
                    let diskonFaktur = 0;
                    if(tglFakturStr) {{
                        let tglFak = new Date(tglFakturStr);
                        let selisihHari = Math.floor((tglBayar - tglFak) / (1000 * 60 * 60 * 24));
                        if(selisihHari >= 0 && selisihHari <= 10) {{
                            diskonFaktur = Math.round(sisaNum * 0.01); 
                        }}
                    }}

                    let bayarBersih = sisaNum - diskonFaktur;
                    totalDibayar += bayarBersih;
                    totalPotongan += diskonFaktur;

                    dispEl.innerText = 'Rp ' + new Intl.NumberFormat('id-ID').format(bayarBersih);
                    hiddenEl.value = new Intl.NumberFormat('id-ID').format(bayarBersih);
                    potDispEl.innerText = diskonFaktur > 0 ? 'Rp ' + new Intl.NumberFormat('id-ID').format(diskonFaktur) : 'Rp 0';
                }} else {{
                    dispEl.innerText = 'Rp 0';
                    hiddenEl.value = '0';
                    potDispEl.innerText = 'Rp 0';
                }}
            }});

            inputDibayar.value = new Intl.NumberFormat('id-ID').format(totalDibayar);
            inputPotongan.value = new Intl.NumberFormat('id-ID').format(totalPotongan);
        }}

        function hitungDiskonTerminOtomatis() {{
            updateJumlahDibayarOtomatis();
        }}

        function tambahBarisLainEK() {{
            const tbody = document.getElementById('tbodyPengeluaranLain');
            const rowCount = tbody.rows.length + 1;
            const newRow = tbody.insertRow();
            newRow.innerHTML = `
                <td style="padding: 10px 16px; text-align: center; color: #6b7280;">${{rowCount}}</td>
                <td style="padding: 10px 16px;">
                    <select name="akun_baris[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">
                        {options_semua_akun}
                    </select>
                </td>
                <td style="padding: 10px 16px;">
                    <input type="text" name="jumlah_baris[]" value="" placeholder="0" oninput="formatRupiahEK(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;">
                </td>
                <td style="padding: 10px 16px;">
                    <input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan baris" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;">
                </td>
                <td style="padding: 10px 16px; text-align: center;">
                    <button type="button" onclick="hapusBarisLainEK(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button>
                </td>
            `;
        }}

        function hapusBarisLainEK(btn) {{
            const row = btn.closest('tr');
            if(row.parentNode.rows.length > 1) {{
                row.remove();
                const rows = document.getElementById('tbodyPengeluaranLain').rows;
                for(let i=0; i<rows.length; i++) {{
                    rows[i].cells[0].innerText = i + 1;
                }}
            }}
        }}

        function formatRupiahEK(el) {{
            let angka = el.value.replace(/[^\\d]/g, '');
            if (angka === "") {{ el.value = "0"; }}
            else {{ el.value = new Intl.NumberFormat('id-ID').format(angka); }}
        }}
    </script>
    """
    return render_dashboard_layout('pengeluaran_kas', content)

@app.route('/transaksi/jurnal-umum')
def jurnal_umum():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_jurnal = user_data.get('jurnal_umum', [])

    if not list_jurnal:
        table_jurnal_html = """
        <div style="padding: 40px 20px; text-align: center; color: #6b7280; font-size: 13px;">
            Belum ada jurnal umum pada periode ini.
        </div>
        """
    else:
        rows_html = ""
        for ju in list_jurnal:
            tgl_raw = ju.get('tanggal', '')
            try:
                dt_obj = datetime.strptime(tgl_raw, '%Y-%m-%d')
                months_id = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des']
                tgl_formatted = f"{dt_obj.day} {months_id[dt_obj.month]} {dt_obj.year}"
            except:
                tgl_formatted = tgl_raw

            details = ju.get('details', [])
            detail_rows = ""
            tot_debit = 0
            tot_kredit = 0

            for d in details:
                deb = float(d.get('debit', 0) or 0)
                kre = float(d.get('kredit', 0) or 0)
                tot_debit += deb
                tot_kredit += kre

                deb_str = f"{int(deb):,.0f}".replace(',', '.') if deb > 0 else '-'
                kre_str = f"{int(kre):,.0f}".replace(',', '.') if kre > 0 else '-'

                detail_rows += f"""
                <tr>
                    <td style="padding: 8px 16px; color: #374151;">{d.get('akun')}</td>
                    <td style="padding: 8px 16px; color: #6b7280; font-size: 12px;">{d.get('keterangan', '')}</td>
                    <td style="padding: 8px 16px; text-align: right; color: #047857;">{deb_str}</td>
                    <td style="padding: 8px 16px; text-align: right; color: #1d4ed8;">{kre_str}</td>
                </tr>
                """

            rows_html += f"""
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 15px; overflow: hidden;">
                <div style="padding: 12px 20px; background: #f9fafb; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <span style="font-weight: 600; color: #d18a99;">{ju.get('no_bukti')}</span>
                        <span style="font-size: 13px; color: #6b7280;">{tgl_formatted}</span>
                        <span style="background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500;">{ju.get('jenis_jurnal', 'Jurnal Umum')}</span>
                    </div>
                    <div style="font-size: 13px; color: #4b5563; font-style: italic;">{ju.get('memo', '')}</div>
                </div>
                <table class="account-table" style="margin-bottom: 0;">
                    <thead>
                        <tr>
                            <th style="width: 50%; padding: 8px 16px;">Akun</th>
                            <th style="width: 20%; padding: 8px 16px;">Keterangan Baris</th>
                            <th style="width: 15%; padding: 8px 16px; text-align: right;">Debit</th>
                            <th style="width: 15%; padding: 8px 16px; text-align: right;">Kredit</th>
                        </tr>
                    </thead>
                    <tbody>
                        {detail_rows}
                    </tbody>
                </table>
            </div>
            """

        table_jurnal_html = f"""
        <div>{rows_html}</div>
        """

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Jurnal Umum</div>
            <div class="page-desc" style="margin-bottom: 0;">Untuk transaksi di luar menu lain: jurnal umum (dividen, retur), jurnal penyesuaian (penyusutan, akrual), dan jurnal penutup.</div>
        </div>
        <div>
            <a href="/transaksi/jurnal-umum/baru" style="background-color: #d18a99; color: white; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; text-decoration: none; display: inline-block;">+ Jurnal umum baru</a>
        </div>
    </div>

    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px 20px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <input type="date" value="2026-01-01" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
            <span style="font-size: 13px; color: #6b7280;">s.d.</span>
            <input type="date" value="2026-10-31" style="padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
        </div>
    </div>

    {table_jurnal_html}
    """
    return render_dashboard_layout('jurnal_umum', content)


@app.route('/transaksi/jurnal-umum/baru', methods=['GET', 'POST'])
def tambah_jurnal_umum():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    email = session['user_email']
    user_data = database_user.get(email, {})
    list_akun = user_data.get('akun', DEFAULT_AKUN)
    list_jurnal = user_data.get('jurnal_umum', [])

    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        no_bukti = request.form.get('no_bukti', '').strip()
        if not no_bukti:
            no_bukti = f"JU-{len(list_jurnal) + 1:03d}"
        
        memo = request.form.get('memo', '').strip()
        jenis_jurnal = request.form.get('jenis_jurnal', 'Jurnal Umum')

        akun_list = request.form.getlist('akun[]')
        debit_list = request.form.getlist('debit[]')
        kredit_list = request.form.getlist('kredit[]')
        keterangan_baris = request.form.getlist('keterangan_baris[]')

        details = []
        total_debit_trx = 0
        total_kredit_trx = 0

        for idx, ak in enumerate(akun_list):
            if ak:
                deb_val = float(debit_list[idx].replace('.', '') or 0) if idx < len(debit_list) else 0
                kre_val = float(kredit_list[idx].replace('.', '') or 0) if idx < len(kredit_list) else 0
                
                if deb_val > 0 or kre_val > 0:
                    total_debit_trx += deb_val
                    total_kredit_trx += kre_val
                    
                    nama_akun_bersih = ak.split(' — ')[1] if ' — ' in ak else (ak.split(' - ')[1] if ' - ' in ak else ak)
                    
                    # Update saldo akun secara otomatis di master akun
                    for acc in list_akun:
                        acc_str = f"{acc.get('kode')} — {acc.get('nama')}"
                        if acc_str == ak or acc.get('kode') in ak:
                            try:
                                saldo_lama = float(str(acc.get('saldo', '0')).replace('.', '') or 0)
                                kategori = acc.get('kategori', '')
                                
                                # Tentukan penambahan saldo berdasarkan posisi normal akun
                                if kategori in ['1 — Aset', '5 — Beban']:
                                    perubahan = deb_val - kre_val
                                else:
                                    perubahan = kre_val - deb_val
                                    
                                saldo_baru = saldo_lama + perubahan
                                acc['saldo'] = f"{int(saldo_baru):,.0f}".replace(',', '.')
                            except:
                                pass

                    details.append({
                        'akun': nama_akun_bersih,
                        'debit': deb_val,
                        'kredit': kre_val,
                        'keterangan': keterangan_baris[idx] if idx < len(keterangan_baris) else ''
                    })

        jurnal_obj = {
            'no_bukti': no_bukti,
            'tanggal': tanggal,
            'memo': memo,
            'jenis_jurnal': jenis_jurnal,
            'total_debit': total_debit_trx,
            'total_kredit': total_kredit_trx,
            'details': details
        }

        user_data.setdefault('jurnal_umum', []).append(jurnal_obj)
        return redirect(url_for('jurnal_umum'))

    today_date = datetime.now().strftime('%Y-%m-%d')

    options_semua_akun = '<option value="">-- Pilih Akun --</option>'
    for acc in list_akun:
        options_semua_akun += f'<option value="{acc.get("kode")} — {acc.get("nama")}">{acc.get("kode")} — {acc.get("nama")}</option>'

    content = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
        <div>
            <div class="page-title">Jurnal Umum Baru</div>
            <div class="page-desc" style="margin-bottom: 0;">Satu baris hanya boleh berisi debit ATAU kredit. Bisa tempel (Ctrl+V) dari Excel: Kode akun | Debit | Kredit | Keterangan.</div>
        </div>
        <div>
            <a href="/transaksi/jurnal-umum" class="btn-action" style="padding: 8px 16px; font-weight: 500;">← Daftar</a>
        </div>
    </div>

    <div class="card-form" style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
        <form action="/transaksi/jurnal-umum/baru" method="POST" id="formJurnalUmum">
            <div style="display: grid; grid-template-columns: 1fr 1.5fr 2fr 1fr; gap: 20px; margin-bottom: 20px;" class="form-group">
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Tanggal <span style="color: #ef4444;">*</span></label>
                    <input type="date" name="tanggal" value="{today_date}" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;" required>
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">No. bukti</label>
                    <input type="text" name="no_bukti" placeholder="JU-otomatis" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                    <span style="font-size: 11px; color: #6b7280; margin-top: 2px; display: block;">Kosong = otomatis (JU-xxxx)</span>
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Memo / keterangan</label>
                    <input type="text" name="memo" placeholder="mis. Penyusutan peralatan Januari" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px;">
                </div>
                <div>
                    <label style="font-size: 13px; color: #374151; font-weight: 500;">Jenis jurnal</label>
                    <select name="jenis_jurnal" style="width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; background: white;">
                        <option value="Jurnal Umum">Jurnal Umum</option>
                        <option value="Penyesuaian">Penyesuaian</option>
                        <option value="Penutup">Penutup</option>
                    </select>
                </div>
            </div>

            <!-- TABEL BARIS JURNAL UMUM -->
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; background: white; overflow: hidden; margin-top: 20px;">
                <table class="account-table" style="margin-bottom: 0;">
                    <thead>
                        <tr>
                            <th style="width: 5%;">#</th>
                            <th style="width: 40%;">Akun (kode / nama)</th>
                            <th style="width: 18%; text-align: right;">Debit</th>
                            <th style="width: 18%; text-align: right;">Kredit</th>
                            <th style="width: 13%;">Keterangan</th>
                            <th style="width: 6%; text-align: center;"></th>
                        </tr>
                    </thead>
                    <tbody id="tbodyJurnalUmum">
                        <!-- 4 Baris Awal Default -->
                        <tr>
                            <td style="padding: 10px 16px; text-align: center; color: #6b7280;">1</td>
                            <td style="padding: 10px 16px;"><select name="akun[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">{options_semua_akun}</select></td>
                            <td style="padding: 10px 16px;"><input type="text" name="debit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="kredit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;"></td>
                            <td style="padding: 10px 16px; text-align: center;"><button type="button" onclick="hapusBarisJU(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 16px; text-align: center; color: #6b7280;">2</td>
                            <td style="padding: 10px 16px;"><select name="akun[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">{options_semua_akun}</select></td>
                            <td style="padding: 10px 16px;"><input type="text" name="debit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="kredit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;"></td>
                            <td style="padding: 10px 16px; text-align: center;"><button type="button" onclick="hapusBarisJU(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 16px; text-align: center; color: #6b7280;">3</td>
                            <td style="padding: 10px 16px;"><select name="akun[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">{options_semua_akun}</select></td>
                            <td style="padding: 10px 16px;"><input type="text" name="debit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="kredit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;"></td>
                            <td style="padding: 10px 16px; text-align: center;"><button type="button" onclick="hapusBarisJU(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 16px; text-align: center; color: #6b7280;">4</td>
                            <td style="padding: 10px 16px;"><select name="akun[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">{options_semua_akun}</select></td>
                            <td style="padding: 10px 16px;"><input type="text" name="debit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="kredit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                            <td style="padding: 10px 16px;"><input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;"></td>
                            <td style="padding: 10px 16px; text-align: center;"><button type="button" onclick="hapusBarisJU(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button></td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr style="background-color: #f9fafb; font-weight: 600;">
                            <td colspan="2" style="padding: 12px 16px; text-align: center;">
                                <span id="statusBalance" style="background: #fee2e2; color: #991b1b; padding: 3px 10px; border-radius: 4px; font-size: 12px;">✕ Selisih</span>
                                <span style="margin-left: 10px;">Total</span>
                            </td>
                            <td style="padding: 12px 16px; text-align: right;" id="totalDebitJU">-</td>
                            <td style="padding: 12px 16px; text-align: right;" id="totalKreditJU">-</td>
                            <td colspan="2"></td>
                        </tr>
                    </tfoot>
                </table>
                <div style="padding: 10px 16px; background: #f9fafb; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                    <button type="button" onclick="tambahBarisJU()" style="background: none; border: none; color: #d18a99; font-weight: 600; font-size: 13px; cursor: pointer;">+ Tambah baris</button>
                    <span style="font-size: 11px; color: #6b7280;">Enter/↓ bawah · ↑ atas · Tab kanan · Esc batal</span>
                </div>
            </div>

            <div style="display: flex; justify-content: flex-end; align-items: center; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px;">
                <button type="submit" class="btn-simpan" style="background-color: #d18a99; padding: 10px 28px;">Simpan jurnal umum</button>
            </div>
        </form>
    </div>

    <script>
        function tambahBarisJU() {{
            const tbody = document.getElementById('tbodyJurnalUmum');
            const rowCount = tbody.rows.length + 1;
            const newRow = tbody.insertRow();
            newRow.innerHTML = `
                <td style="padding: 10px 16px; text-align: center; color: #6b7280;">${{rowCount}}</td>
                <td style="padding: 10px 16px;"><select name="akun[]" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; background: white;">{options_semua_akun}</select></td>
                <td style="padding: 10px 16px;"><input type="text" name="debit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                <td style="padding: 10px 16px;"><input type="text" name="kredit[]" value="" placeholder="0" oninput="formatRupiahJU(this)" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px; text-align: right;"></td>
                <td style="padding: 10px 16px;"><input type="text" name="keterangan_baris[]" value="" placeholder="Keterangan" style="width: 100%; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 13px;"></td>
                <td style="padding: 10px 16px; text-align: center;"><button type="button" onclick="hapusBarisJU(this)" style="background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 16px;">×</button></td>
            `;
        }}

        function hapusBarisJU(btn) {{
            const row = btn.closest('tr');
            if(row.parentNode.rows.length > 1) {{
                row.remove();
                const rows = document.getElementById('tbodyJurnalUmum').rows;
                for(let i=0; i<rows.length; i++) {{
                    rows[i].cells[0].innerText = i + 1;
                }}
                hitungTotalJU();
            }}
        }}

        function formatRupiahJU(el) {{
            let angka = el.value.replace(/[^\\d]/g, '');
            if (angka === "") {{ el.value = ""; }}
            else {{ el.value = new Intl.NumberFormat('id-ID').format(angka); }}
            hitungTotalJU();
        }}

        function hitungTotalJU() {{
            let totalDebit = 0;
            let totalKredit = 0;

            document.querySelectorAll('#tbodyJurnalUmum tr').forEach(row => {{
                const inpDeb = row.querySelector('input[name="debit[]"]');
                const inpKre = row.querySelector('input[name="kredit[]"]');
                
                if(inpDeb && inpDeb.value) {{
                    totalDebit += parseFloat(inpDeb.value.replace(/\\./g, '')) || 0;
                }}
                if(inpKre && inpKre.value) {{
                    totalKredit += parseFloat(inpKre.value.replace(/\\./g, '')) || 0;
                }}
            }});

            document.getElementById('totalDebitJU').innerText = totalDebit > 0 ? 'Rp ' + new Intl.NumberFormat('id-ID').format(totalDebit) : '-';
            document.getElementById('totalKreditJU').innerText = totalKredit > 0 ? 'Rp ' + new Intl.NumberFormat('id-ID').format(totalKredit) : '-';

            const statusBadge = document.getElementById('statusBalance');
            if(totalDebit > 0 && totalDebit === totalKredit) {{
                statusBadge.style.backgroundColor = '#d1fae5';
                statusBadge.style.color = '#065f46';
                statusBadge.innerText = '✓ Seimbang';
            }} else {{
                statusBadge.style.backgroundColor = '#fee2e2';
                statusBadge.style.color = '#991b1b';
                statusBadge.innerText = '✕ Selisih';
            }}
        }}
    </script>
    """
    return render_dashboard_layout('jurnal_umum', content)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

