from flask import Flask, request, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)

user_session = {"logged_in": False, "username": "", "active_menu": "data-perusahaan"}

profil_perusahaan = {
    "nama": "",
    "alamat": "",
    "telepon": "",
    "periode": "2026-01-01"
}

daftar_akun = [
    # Aset
    {"kategori": "Aset", "kode": "1-1100", "nama": "Kas", "induk": "Kas & Bank", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1110", "nama": "Kas Kecil", "induk": "Kas & Bank", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1200", "nama": "Bank", "induk": "Kas & Bank", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1300", "nama": "Piutang Usaha", "induk": "Piutang Usaha", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1400", "nama": "Persediaan Barang Dagang", "induk": "Persediaan", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1500", "nama": "PPN Masukan", "induk": "PPN Masukan", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1600", "nama": "Perlengkapan", "induk": "Aset Lancar Lainnya", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1700", "nama": "Sewa Dibayar Dimuka", "induk": "Aset Lancar Lainnya", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-1800", "nama": "Asuransi Dibayar Dimuka", "induk": "Aset Lancar Lainnya", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2100", "nama": "Tanah", "induk": "Aset Tetap", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2200", "nama": "Gedung", "induk": "Aset Tetap", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2210", "nama": "Akumulasi Penyusutan Gedung", "induk": "Akumulasi Penyusutan", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2300", "nama": "Kendaraan", "induk": "Aset Tetap", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2310", "nama": "Akumulasi Penyusutan Kendaraan", "induk": "Akumulasi Penyusutan", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2400", "nama": "Peralatan Toko", "induk": "Aset Tetap", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Aset", "kode": "1-2410", "nama": "Akumulasi Penyusutan Peralatan", "induk": "Akumulasi Penyusutan", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},

    # Liabilitas
    {"kategori": "Liabilitas", "kode": "2-1100", "nama": "Utang Usaha", "induk": "Utang Usaha", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Liabilitas", "kode": "2-1200", "nama": "PPN Keluaran", "induk": "PPN Keluaran", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Liabilitas", "kode": "2-1300", "nama": "Utang Gaji", "induk": "Liabilitas Lancar Lainnya", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Liabilitas", "kode": "2-1400", "nama": "Utang Pajak Penghasilan", "induk": "Liabilitas Lancar Lainnya", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Liabilitas", "kode": "2-1500", "nama": "Utang Dividen", "induk": "Liabilitas Lancar Lainnya", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Liabilitas", "kode": "2-2100", "nama": "Utang Bank Jangka Panjang", "induk": "Liabilitas Jangka Panjang", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},

    # Ekuitas
    {"kategori": "Ekuitas", "kode": "3-1100", "nama": "Modal Saham", "induk": "Modal", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Ekuitas", "kode": "3-1200", "nama": "Tambahan Modal Disetor", "induk": "Modal", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Ekuitas", "kode": "3-2100", "nama": "Laba Ditahan", "induk": "Laba Ditahan", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Ekuitas", "kode": "3-3100", "nama": "Dividen", "induk": "Dividen / Prive", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Ekuitas", "kode": "3-9999", "nama": "Historical Balancing", "induk": "Historical Balancing", "dk": "D/K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},

    # Pendapatan
    {"kategori": "Pendapatan", "kode": "4-1100", "nama": "Penjualan", "induk": "Penjualan", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Pendapatan", "kode": "4-1200", "nama": "Retur Penjualan", "induk": "Retur Penjualan", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Pendapatan", "kode": "4-1300", "nama": "Potongan Penjualan", "induk": "Potongan Penjualan", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},

    # Harga Pokok Penjualan
    {"kategori": "Harga Pokok Penjualan", "kode": "5-1100", "nama": "Harga Pokok Penjualan", "induk": "Harga Pokok Penjualan", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Harga Pokok Penjualan", "kode": "5-1200", "nama": "Potongan Pembelian", "induk": "Potongan Pembelian", "dk": "K", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Harga Pokok Penjualan", "kode": "5-1300", "nama": "Beban Angkut Pembelian", "induk": "Beban Angkut Pembelian", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},

    # Beban
    {"kategori": "Beban", "kode": "6-1100", "nama": "Beban Gaji", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1200", "nama": "Beban Sewa", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1300", "nama": "Beban Listrik, Air & Telepon", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1400", "nama": "Beban Perlengkapan", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1500", "nama": "Beban Penyusutan", "induk": "Beban Penyusutan", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1600", "nama": "Beban Pengiriman", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1610", "nama": "Beban Angkut Penjualan", "induk": "Beban Angkut Penjualan", "dk": "D", "sistem": True, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1700", "nama": "Beban Asuransi", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1800", "nama": "Beban Iklan & Promosi", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "6-1900", "nama": "Beban Operasional Lain-lain", "induk": "Beban Operasional", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban", "kode": "9-1100", "nama": "Beban Pajak Penghasilan", "induk": "Beban Pajak Penghasilan", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},

    # Pendapatan Lain-lain
    {"kategori": "Pendapatan Lain-lain", "kode": "7-1100", "nama": "Pendapatan Bunga", "induk": "Pendapatan Lain-lain", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Pendapatan Lain-lain", "kode": "7-1200", "nama": "Pendapatan Lain-lain", "induk": "Pendapatan Lain-lain", "dk": "K", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},

    # Beban Lain-lain
    {"kategori": "Beban Lain-lain", "kode": "8-1100", "nama": "Beban Bunga", "induk": "Beban Lain-lain", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"},
    {"kategori": "Beban Lain-lain", "kode": "8-1200", "nama": "Beban Administrasi Bank", "induk": "Beban Lain-lain", "dk": "D", "sistem": False, "debit": "", "kredit": "", "saldo": "-"}
]

daftar_pelanggan = []
daftar_pemasok = []
daftar_barang = []
daftar_penjualan = []
daftar_pembelian = []
daftar_penerimaan_kas = []
daftar_pengeluaran_kas = []
daftar_jurnal_umum = []

def format_tanggal_indo(periode_str):
    bulan_dict = {
        "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
        "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
        "09": "September", "10": "Oktober", "11": "November", "12": "Desember"
    }
    try:
        dt = datetime.strptime(periode_str, "%Y-%m-%d")
        return f"{dt.day} {bulan_dict.get(dt.strftime('%m'), dt.strftime('%m'))} {dt.year}"
    except:
        pass
    return periode_str

@app.route('/')
def index():
    if not user_session["logged_in"]:
        page = request.args.get('page', 'login')
        
        if page == 'register':
            return render_template_string('''
            <h2>Daftar Akun Baru</h2>
            <form method="POST" action="/auth-submit">
                <input type="hidden" name="mode" value="register">
                <p>Nama lengkap:<br><input type="text" name="nama_lengkap" placeholder="Contoh: Adinda" required></p>
                <p>Email:<br><input type="email" name="email" placeholder="emailperusahaan@gmail.com" required></p>
                <p>Password:<br><input type="password" name="password" required></p>
                <p>Nama perusahaan:<br><input type="text" name="nama_perusahaan" placeholder="PT Dagang" required></p>
                <p>Tanggal saldo awal:<br><input type="date" name="tanggal" value="2026-01-01"></p>
                <button type="submit">Daftar & buat perusahaan</button>
            </form>
            <p>Sudah punya akun? <a href="/?page=login">Masuk</a></p>
            ''')
        else:
            return render_template_string('''
            <h2>Masuk</h2>
            <form method="POST" action="/auth-submit">
                <input type="hidden" name="mode" value="login">
                <p>Email:<br><input type="email" name="email" placeholder="emailperusahaan@gmail.com" required></p>
                <p>Password:<br><input type="password" name="password" required></p>
                <button type="submit">Masuk</button>
            </form>
            <p>Belum punya akun? <a href="/?page=register">Daftar di sini</a></p>
            ''')
    else:
        return redirect(url_for('menu_handler', menu_name=user_session["active_menu"]))

@app.route('/auth-submit', methods=['POST'])
def auth_submit():
    mode = request.form.get('mode')
    email = request.form.get('email')
    
    user_session["logged_in"] = True
    user_session["username"] = email
    user_session["active_menu"] = "data-perusahaan"
    
    if mode == 'register':
        nama_pt = request.form.get('nama_perusahaan')
        tanggal = request.form.get('tanggal')
        if nama_pt:
            profil_perusahaan["nama"] = nama_pt
        if tanggal:
            profil_perusahaan["periode"] = tanggal
            
    return redirect(url_for('menu_handler', menu_name="data-perusahaan"))

@app.route('/logout')
def logout():
    user_session["logged_in"] = False
    user_session["username"] = ""
    return redirect(url_for('index'))

@app.route('/app/<menu_name>')
def menu_handler(menu_name):
    if not user_session["logged_in"]:
        return redirect(url_for('index'))
    
    user_session["active_menu"] = menu_name
    content_html = ""
    
    if menu_name == 'data-perusahaan':
        content_html = f'''
        <h2>Data Perusahaan</h2>
        <form method="POST" action="/update-perusahaan">
            <p>Nama Perusahaan:<br><input type="text" name="nama" value="{profil_perusahaan['nama']}" placeholder="PT Dagang"></p>
            <p>Alamat:<br><input type="text" name="alamat" value="{profil_perusahaan['alamat']}" placeholder="Contoh: Jl. Pemuda No. 15, Semarang"></p>
            <p>Nomor Telepon:<br><input type="text" name="telepon" value="{profil_perusahaan['telepon']}" placeholder="Contoh: 081234567890"></p>
            <p>Periode Akuntansi (Tanggal Saldo Awal):<br><input type="date" name="periode" value="{profil_perusahaan['periode']}"></p>
            <button type="submit">Simpan Perubahan</button>
        </form>
        '''
    elif menu_name == 'daftar-akun':
        search_query = request.args.get('q', '').lower()
        kategori_list = ["Aset", "Liabilitas", "Ekuitas", "Pendapatan", "Harga Pokok Penjualan", "Beban", "Pendapatan Lain-lain", "Beban Lain-lain"]
        
        tables_html = "<h2>Daftar Akun</h2>"
        tables_html += '<p>Bagan akun. Akun bertanda Sistem adalah linked account: tidak bisa dihapus dan subtipenya terkunci.</p>'
        
        tables_html += f'''
        <form method="GET" action="/app/daftar-akun">
            <p><input type="text" name="q" value="{search_query}" placeholder="Cari kode / nama..."> <button type="submit">Cari</button>
            <a href="/app/akun-baru"><button type="button">+ Akun baru</button></a></p>
        </form>
        <hr>
        '''
        
        for kat in kategori_list:
            filtered_akun = [a for a in daftar_akun if a['kategori'] == kat and (not search_query or search_query in a['kode'].lower() or search_query in a['nama'].lower())]
            
            if search_query and not filtered_akun:
                continue
                
            tables_html += f'<h3>{kat}</h3>'
            tables_html += '<table border="1" cellpadding="6" cellspacing="0">'
            tables_html += '<tr><th>KODE</th><th>NAMA AKUN</th><th>AKUN INDUK</th><th>D/K</th><th>SALDO</th><th>AKSI</th></tr>'
            
            if filtered_akun:
                for akun in filtered_akun:
                    nama_tampilan = f"{akun['nama']} <b>[Sistem]</b>" if akun['sistem'] else akun['nama']
                    
                    if akun['sistem']:
                        aksi_html = f'<a href="/app/ubah-akun?kode={akun["kode"]}"><button type="button">Ubah</button></a>'
                    else:
                        aksi_html = f'''
                        <a href="/app/ubah-akun?kode={akun["kode"]}"><button type="button">Ubah</button></a>
                        <a href="/hapus-akun?kode={akun["kode"]}" onclick="return confirm(\'Apakah benar-benar ingin dihapus?\');"><button type="button">Hapus</button></a>
                        '''
                        
                    tables_html += f'''
                    <tr>
                        <td>{akun['kode']}</td>
                        <td>{nama_tampilan}</td>
                        <td>{akun['induk']}</td>
                        <td>{akun['dk']}</td>
                        <td>{akun['saldo']}</td>
                        <td>{aksi_html}</td>
                    </tr>
                    '''
            else:
                tables_html += '<tr><td colspan="6" align="center">Tidak ada akun ditemukan</td></tr>'
            tables_html += '</table>'
            
        content_html = tables_html
        
    elif menu_name == 'saldo-awal':
        total_piutang = 0
        for p in daftar_pelanggan:
            try:
                total_piutang += float(str(p['saldo_awal']).replace('.', '').replace(',', '.'))
            except:
                pass

        total_utang = 0
        for s in daftar_pemasok:
            try:
                total_utang += float(str(s['saldo_awal']).replace('.', '').replace(',', '.'))
            except:
                pass

        total_persediaan_kartu = 0
        for b in daftar_barang:
            try:
                total_persediaan_kartu += float(str(b['nilai']).replace('.', '').replace(',', '.'))
            except:
                pass

        total_persediaan_otomatis = total_persediaan_kartu + total_utang - total_piutang
        if total_persediaan_otomatis < 0:
            total_persediaan_otomatis = 0

        total_debit = total_piutang + total_persediaan_otomatis
        total_kredit = total_utang

        for a in daftar_akun:
            if 'debit' not in a: a['debit'] = ''
            if 'kredit' not in a: a['kredit'] = ''
            
            if a['kode'] == '1-1300':
                a['debit'] = f"{total_piutang:,.0f}".replace(',', '.') if total_piutang > 0 else ""
                a['kredit'] = ""
                a['saldo'] = a['debit'] if a['debit'] else "-"
            elif a['kode'] == '1-1400':
                a['debit'] = f"{total_persediaan_otomatis:,.0f}".replace(',', '.') if total_persediaan_otomatis > 0 else ""
                a['kredit'] = ""
                a['saldo'] = a['debit'] if a['debit'] else "-"
            elif a['kode'] == '2-1100':
                a['kredit'] = f"{total_utang:,.0f}".replace(',', '.') if total_utang > 0 else ""
                a['debit'] = ""
                a['saldo'] = a['kredit'] if a['kredit'] else "-"

            if a['kode'] != '3-9999':
                try:
                    total_debit += float(str(a['debit']).replace('.', '').replace(',', '.')) if a['kode'] not in ['1-1300', '1-1400', '2-1100'] else 0
                except:
                    pass
                try:
                    total_kredit += float(str(a['kredit']).replace('.', '').replace(',', '.')) if a['kode'] not in ['1-1300', '1-1400', '2-1100'] else 0
                except:
                    pass

        selisih = total_debit - total_kredit
        
        hb_debit = 0
        hb_kredit = 0
        if selisih > 0:
            hb_kredit = selisih
            total_kredit += selisih
        elif selisih < 0:
            hb_debit = abs(selisih)
            total_debit += abs(selisih)
            
        status_seimbang = "Seimbang" if selisih == 0 else "Tidak Seimbang"
        tanggal_format = format_tanggal_indo(profil_perusahaan['periode'])
        
        tables_html = "<h2>Saldo Awal</h2>"
        tables_html += f'<p>Account Opening Balance per <b>{tanggal_format}</b>. Piutang, utang, dan persediaan bersumber otomatis dari kartu masing-masing.</p>'
        tables_html += '<form method="POST" action="/simpan-saldo-awal">'
        
        kategori_list = ["Aset", "Liabilitas", "Ekuitas", "Pendapatan", "Harga Pokok Penjualan", "Beban", "Pendapatan Lain-lain", "Beban Lain-lain"]
        
        for kat in kategori_list:
            tables_html += f'<h3>{kat}</h3>'
            tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
            tables_html += '<tr><th>KODE</th><th>NAMA AKUN</th><th>DEBIT</th><th>KREDIT</th></tr>'
            
            for akun in daftar_akun:
                if 'debit' not in akun: akun['debit'] = ''
                if 'kredit' not in akun: akun['kredit'] = ''

                if akun['kategori'] == kat:
                    if akun['kode'] == '3-9999':
                        hb_d_str = f"{hb_debit:,.0f}".replace(',', '.') if hb_debit > 0 else "-"
                        hb_k_str = f"{hb_kredit:,.0f}".replace(',', '.') if hb_kredit > 0 else "-"
                        tables_html += f'''
                        <tr>
                            <td>{akun['kode']}</td>
                            <td>{akun['nama']} (Otomatis)</td>
                            <td align="right">{hb_d_str}</td>
                            <td align="right">{hb_k_str}</td>
                        </tr>
                        '''
                    elif akun['kode'] == '1-1300':
                        d_str = akun['debit'] if akun['debit'] else "-"
                        tables_html += f'''
                        <tr>
                            <td>{akun['kode']}</td>
                            <td>{akun['nama']} (<a href="/app/pelanggan">dari Kartu Pelanggan</a>)</td>
                            <td align="right">{d_str}</td>
                            <td align="right">-</td>
                        </tr>
                        '''
                    elif akun['kode'] == '1-1400':
                        d_str = akun['debit'] if akun['debit'] else "-"
                        tables_html += f'''
                        <tr>
                            <td>{akun['kode']}</td>
                            <td>{akun['nama']} (<a href="/app/barang">dari Kartu Barang</a>)</td>
                            <td align="right">{d_str}</td>
                            <td align="right">-</td>
                        </tr>
                        '''
                    elif akun['kode'] == '2-1100':
                        k_str = akun['kredit'] if akun['kredit'] else "-"
                        tables_html += f'''
                        <tr>
                            <td>{akun['kode']}</td>
                            <td>{akun['nama']} (<a href="/app/pemasok">dari Kartu Pemasok</a>)</td>
                            <td align="right">-</td>
                            <td align="right">{k_str}</td>
                        </tr>
                        '''
                    else:
                        d_val = akun['debit'] if akun['debit'] and akun['debit'] != '0' else ''
                        k_val = akun['kredit'] if akun['kredit'] and akun['kredit'] != '0' else ''
                        tables_html += f'''
                        <tr>
                            <td>{akun['kode']}</td>
                            <td>{akun['nama']}</td>
                            <td><input type="text" name="debit_{akun['kode']}" value="{d_val}" placeholder="0" style="width: 100px;"></td>
                            <td><input type="text" name="kredit_{akun['kode']}" value="{k_val}" placeholder="0" style="width: 100px;"></td>
                        </tr>
                        '''
            tables_html += '</table>'
            
        tables_html += f'''
        <hr>
        <p><b>Total Debit:</b> {total_debit:,.0f} | <b>Total Kredit:</b> {total_kredit:,.0f} | <b>Status:</b> {status_seimbang}</p>
        <button type="submit">Simpan saldo awal</button>
        </form>
        '''
        content_html = tables_html

    elif menu_name == 'pelanggan':
        total_sisa_piutang = 0
        for p in daftar_pelanggan:
            try:
                total_sisa_piutang += float(str(p['saldo_awal']).replace('.', '').replace(',', '.'))
            except:
                pass

        tables_html = "<h2>Pelanggan</h2>"
        tables_html += '<p>Kartu pelanggan. Saldo awal piutang masuk ke saldo awal piutang usaha.</p>'
        tables_html += '<p><a href="/app/pelanggan-baru"><button type="button">+ Pelanggan baru</button></a></p>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>KODE</th><th>NAMA</th><th>TELEPON</th><th>SYARAT BAYAR</th><th>SALDO AWAL</th><th>SISA PIUTANG</th><th>AKSI</th></tr>'
        
        if daftar_pelanggan:
            for p in daftar_pelanggan:
                tables_html += f'''
                <tr>
                    <td>{p['kode']}</td>
                    <td>{p['nama']}</td>
                    <td>{p['telepon']}</td>
                    <td>{p['syarat_bayar']}</td>
                    <td align="right">{p['saldo_awal']}</td>
                    <td align="right">{p['saldo_awal']}</td>
                    <td>
                        <a href="/app/ubah-pelanggan?kode={p['kode']}"><button type="button">Ubah</button></a>
                        <a href="/hapus-pelanggan?kode={p['kode']}" onclick="return confirm(\'Apakah benar-benar ingin dihapus?\');"><button type="button">Hapus</button></a>
                    </td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="7" align="center">Belum ada pelanggan</td></tr>'
            
        tables_html += f'''
        <tr>
            <td colspan="5" align="right"><b>Total sisa piutang</b></td>
            <td colspan="2" align="right"><b>{total_sisa_piutang:,.0f}".replace(',', '.') if total_sisa_piutang > 0 else "-"</b></td>
        </tr>
        </table>
        '''
        content_html = tables_html

    elif menu_name == 'pelanggan-baru':
        next_code = f"C{str(len(daftar_pelanggan) + 1).zfill(3)}"
        content_html = f'''
        <h2>Pelanggan baru</h2>
        <form method="POST" action="/tambah-pelanggan-submit">
            <table width="100%" cellpadding="4" cellspacing="0">
                <tr>
                    <td>Kode *<br><input type="text" name="kode" value="{next_code}" required style="width: 250px;"></td>
                    <td>Nama *<br><input type="text" name="nama" required style="width: 350px;"></td>
                </tr>
                <tr>
                    <td colspan="2">Alamat<br><textarea name="alamat" rows="3" style="width: 100%;"></textarea></td>
                </tr>
                <tr>
                    <td>Telepon<br><input type="text" name="telepon" style="width: 250px;"></td>
                    <td>Email<br><input type="email" name="email" style="width: 350px;"></td>
                </tr>
                <tr>
                    <td colspan="2">
                        Syarat pembayaran<br>
                        <select name="syarat_bayar" style="width: 100%;">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="Tunai">Tunai</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <fieldset>
                            <legend>Termin kredit — n/30</legend>
                            <table>
                                <tr>
                                    <td>Potongan (%)<br><input type="text" name="potongan" placeholder="0" style="width: 100px;"></td>
                                    <td>Jika bayar ≤ (hari)<br><input type="text" name="hari_diskon" placeholder="0" style="width: 150px;"></td>
                                    <td>Jatuh tempo (hari)<br><input type="text" name="jatuh_tempo" value="30" style="width: 150px;"></td>
                                </tr>
                            </table>
                            <small>Contoh 2/10, n/30: potongan 2% jika dibayar ≤ 10 hari, jatuh tempo 30 hari.</small>
                        </fieldset>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        Saldo awal piutang (Rp)<br>
                        <input type="text" name="saldo_awal" placeholder="0" style="width: 250px;">
                        <br><small>Per tanggal saldo awal perusahaan</small>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <label><input type="checkbox" name="aktif" checked> Aktif</label>
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/pelanggan"><button type="button">Batal</button></a>
            <button type="submit">Simpan</button>
        </form>
        '''

    elif menu_name == 'pemasok':
        total_sisa_utang = 0
        for s in daftar_pemasok:
            try:
                total_sisa_utang += float(str(s['saldo_awal']).replace('.', '').replace(',', '.'))
            except:
                pass

        tables_html = "<h2>Pemasok</h2>"
        tables_html += '<p>Kartu pemasok. Saldo awal utang masuk ke saldo awal utang usaha.</p>'
        tables_html += '<p><a href="/app/pemasok-baru"><button type="button">+ Pemasok baru</button></a></p>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>KODE</th><th>NAMA</th><th>TELEPON</th><th>SYARAT BAYAR</th><th>SALDO AWAL</th><th>SISA UTANG</th><th>AKSI</th></tr>'
        
        if daftar_pemasok:
            for s in daftar_pemasok:
                tables_html += f'''
                <tr>
                    <td>{s['kode']}</td>
                    <td>{s['nama']}</td>
                    <td>{s['telepon']}</td>
                    <td>{s['syarat_bayar']}</td>
                    <td align="right">{s['saldo_awal']}</td>
                    <td align="right">{s['saldo_awal']}</td>
                    <td>
                        <a href="/app/ubah-pemasok?kode={s['kode']}"><button type="button">Ubah</button></a>
                        <a href="/hapus-pemasok?kode={s['kode']}" onclick="return confirm(\'Apakah benar-benar ingin dihapus?\');"><button type="button">Hapus</button></a>
                    </td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="7" align="center">Belum ada pemasok</td></tr>'
            
        tables_html += f'''
        <tr>
            <td colspan="5" align="right"><b>Total sisa utang</b></td>
            <td colspan="2" align="right"><b>{total_sisa_utang:,.0f}".replace(',', '.') if total_sisa_utang > 0 else "-"</b></td>
        </tr>
        </table>
        '''
        content_html = tables_html

    elif menu_name == 'pemasok-baru':
        next_code = f"S{str(len(daftar_pemasok) + 1).zfill(3)}"
        content_html = f'''
        <h2>Pemasok baru</h2>
        <form method="POST" action="/tambah-pemasok-submit">
            <table width="100%" cellpadding="4" cellspacing="0">
                <tr>
                    <td>Kode *<br><input type="text" name="kode" value="{next_code}" required style="width: 250px;"></td>
                    <td>Nama *<br><input type="text" name="nama" required style="width: 350px;"></td>
                </tr>
                <tr>
                    <td colspan="2">Alamat<br><textarea name="alamat" rows="3" style="width: 100%;"></textarea></td>
                </tr>
                <tr>
                    <td>Telepon<br><input type="text" name="telepon" style="width: 250px;"></td>
                    <td>Email<br><input type="email" name="email" style="width: 350px;"></td>
                </tr>
                <tr>
                    <td colspan="2">
                        Syarat pembayaran<br>
                        <select name="syarat_bayar" style="width: 100%;">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="Tunai">Tunai</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <fieldset>
                            <legend>Termin kredit — n/30</legend>
                            <table>
                                <tr>
                                    <td>Potongan (%)<br><input type="text" name="potongan" placeholder="0" style="width: 100px;"></td>
                                    <td>Jika bayar ≤ (hari)<br><input type="text" name="hari_diskon" placeholder="0" style="width: 150px;"></td>
                                    <td>Jatuh tempo (hari)<br><input type="text" name="jatuh_tempo" value="30" style="width: 150px;"></td>
                                </tr>
                            </table>
                            <small>Contoh 2/10, n/30: potongan 2% jika dibayar ≤ 10 hari, jatuh tempo 30 hari.</small>
                        </fieldset>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        Saldo awal utang (Rp)<br>
                        <input type="text" name="saldo_awal" placeholder="0" style="width: 250px;">
                        <br><small>Per tanggal saldo awal perusahaan</small>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <label><input type="checkbox" name="aktif" checked> Aktif</label>
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/pemasok"><button type="button">Batal</button></a>
            <button type="submit">Simpan</button>
        </form>
        '''

    elif menu_name == 'barang':
        total_nilai_persediaan = 0
        for b in daftar_barang:
            try:
                total_nilai_persediaan += float(str(b['nilai']).replace('.', '').replace(',', '.'))
            except:
                pass

        tables_html = "<h2>Barang</h2>"
        tables_html += '<p>Kartu barang. Persediaan perpetual dengan metode rata-rata bergerak. Saldo awal = qty awal × harga pokok.</p>'
        tables_html += '<p><a href="/app/barang-baru"><button type="button">+ Barang baru</button></a></p>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>KODE</th><th>NAMA BARANG</th><th>HARGA JUAL</th><th>QTY</th><th>HARGA RATA-RATA</th><th>NILAI PERSEDIAAN</th><th>AKSI</th></tr>'
        
        if daftar_barang:
            for b in daftar_barang:
                tables_html += f'''
                <tr>
                    <td>{b['kode']}</td>
                    <td>{b['nama']}</td>
                    <td align="right">{b['harga_jual']}</td>
                    <td>{b['qty']} {b['satuan']}</td>
                    <td align="right">{b['harga_pokok']}</td>
                    <td align="right">{b['nilai']}</td>
                    <td>
                        <a href="/app/ubah-barang?kode={b['kode']}"><button type="button">Ubah</button></a>
                        <a href="/hapus-barang?kode={b['kode']}" onclick="return confirm(\'Apakah benar-benar ingin dihapus?\');"><button type="button">Hapus</button></a>
                    </td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="7" align="center">Tidak ada barang</td></tr>'
            
        tables_html += f'''
        <tr>
            <td colspan="5" align="right"><b>Total nilai persediaan</b></td>
            <td colspan="2" align="right"><b>{total_nilai_persediaan:,.0f}".replace(',', '.') if total_nilai_persediaan > 0 else "-"</b></td>
        </tr>
        </table>
        '''
        content_html = tables_html

    elif menu_name == 'barang-baru':
        next_code = f"B0{str(len(daftar_barang) + 1).zfill(3)}"
        content_html = f'''
        <h2>Barang baru</h2>
        <form method="POST" action="/tambah-barang-submit">
            <table width="100%" cellpadding="4" cellspacing="0">
                <tr>
                    <td>Kode *<br><input type="text" name="kode" value="{next_code}" required style="width: 250px;"></td>
                    <td>Nama barang *<br><input type="text" name="nama" required style="width: 350px;"></td>
                </tr>
                <tr>
                    <td>Satuan<br><input type="text" name="satuan" value="pcs" style="width: 250px;"></td>
                    <td>Harga jual (Rp)<br><input type="text" name="harga_jual" placeholder="0" style="width: 350px;"></td>
                </tr>
                <tr>
                    <td colspan="2">
                        <fieldset>
                            <legend>Saldo awal persediaan</legend>
                            <table>
                                <tr>
                                    <td>Qty awal<br><input type="text" name="qty" id="qty_awal" placeholder="0" style="width: 120px;" oninput="hitungNilaiPersediaan()"></td>
                                    <td>Harga pokok / unit<br><input type="text" name="harga_pokok" id="hpp_awal" placeholder="0" style="width: 150px;" oninput="hitungNilaiPersediaan()"></td>
                                    <td>Nilai<br><b id="label_nilai" style="font-size: 16px;">0</b><input type="hidden" name="nilai" id="input_nilai" value="0"></td>
                                </tr>
                            </table>
                        </fieldset>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <label><input type="checkbox" name="aktif" checked> Aktif</label>
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/barang"><button type="button">Batal</button></a>
            <button type="submit">Simpan</button>
        </form>
        <script>
        function hitungNilaiPersediaan() {{
            var qty = parseFloat(document.getElementById('qty_awal').value) || 0;
            var hpp = parseFloat(document.getElementById('hpp_awal').value) || 0;
            var totalNilai = qty * hpp;
            
            document.getElementById('label_nilai').innerText = totalNilai.toLocaleString('id-ID');
            document.getElementById('input_nilai').value = totalNilai;
        }}
        </script>
        '''

    elif menu_name == 'penjualan':
        tables_html = "<h2>Penjualan</h2>"
        tables_html += '<p>Transaksi penjualan tunai & kredit. Jurnal penjualan dan HPP (perpetual) terbentuk otomatis.</p>'
        tables_html += '<p><a href="/app/tambah-penjualan"><button type="button">+ Tambah Transaksi</button></a></p>'
        tables_html += '''
        <p>
            Dari: <input type="date" value="2026-01-01"> s.d. <input type="date" value="2026-10-31">
            <select><option>Semua status</option></select>
        </p>
        '''
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>TANGGAL</th><th>NO. FAKTUR</th><th>PELANGGAN</th><th>STATUS</th><th>JATUH TEMPO</th><th>TOTAL</th><th>SISA</th></tr>'
        
        jurnal_penjualan_riil = [trx for trx in daftar_penjualan if not trx['no_faktur'].startswith("SA-")]
        if jurnal_penjualan_riil:
            for trx in jurnal_penjualan_riil:
                status_badge = f'<span style="background: #e6ffed; color: #006600; padding: 2px 6px; border-radius: 4px;">{trx["status"]}</span>'
                tables_html += f'''
                <tr>
                    <td>{trx['tanggal']}</td>
                    <td><b><a href="#" style="color: #800000; text-decoration: none;">{trx['no_faktur']}</a></b></td>
                    <td>{trx['pelanggan']}</td>
                    <td>{status_badge}</td>
                    <td>{trx['jatuh_tempo']}</td>
                    <td align="right">{trx['total']}</td>
                    <td align="right">{trx['sisa']}</td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="7" align="center">Belum ada transaksi penjualan</td></tr>'
        tables_html += '</table>'
        
        tables_html += '<br><h3>Jurnal Penjualan</h3>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%; font-size: 13px;">'
        tables_html += '<tr><th>TANGGAL</th><th>NO. BUKTI</th><th>KETERANGAN</th><th>PIUTANG USAHA (Dr)</th><th>HPP (Dr)</th><th>PERSEDIAAN (Cr)</th><th>PPN KELUARAN (Cr)</th><th>PENJUALAN (Cr)</th></tr>'
        
        if jurnal_penjualan_riil:
            for trx in jurnal_penjualan_riil:
                tables_html += f'''
                <tr>
                    <td>{trx['tanggal']}</td>
                    <td>{trx['no_faktur']}</td>
                    <td>Penjualan - {trx['pelanggan']}</td>
                    <td align="right">{trx['total']}</td>
                    <td align="right">-</td>
                    <td align="right">-</td>
                    <td align="right">-</td>
                    <td align="right">{trx['total']}</td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="8" align="center">Belum ada jurnal penjualan</td></tr>'
            
        tables_html += '</table>'
        content_html = tables_html

    elif menu_name == 'tambah-penjualan':
        today_str = datetime.now().strftime('%d/%m/%Y')
        options_pelanggan = "".join([f'<option value="{p["nama"]}">{p["kode"]} - {p["nama"]}</option>' for p in daftar_pelanggan])
        options_barang = "".join([f'<option value="{b["kode"]} - {b["nama"]}" data-harga="{b["harga_jual"]}">{b["kode"]} - {b["nama"]} (Stok: {b["qty"]})</option>' for b in daftar_barang])

        content_html = f'''
        <h2>Tambah Transaksi Penjualan</h2>
        <p>Nomor dibuat otomatis bila dikosongkan. Grid bisa diisi dengan tempel (Ctrl+V) dari Excel: Kode barang | Qty | Harga.</p>
        <form method="POST" action="/tambah-penjualan-submit">
            <table width="100%" cellpadding="6">
                <tr>
                    <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required style="width: 200px;"></td>
                    <td>Pelanggan (kode / nama) *<br>
                        <select name="pelanggan" style="width: 100%;" required>
                            <option value="">-- Pilih Pelanggan --</option>
                            {options_pelanggan}
                        </select>
                    </td>
                    <td>No. faktur<br><input type="text" name="no_faktur" placeholder="FJ-otomatis" style="width: 200px;"></td>
                </tr>
                <tr>
                    <td>Pembayaran<br>
                        <select name="pembayaran" style="width: 100%;">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="Tunai">Tunai</option>
                        </select>
                    </td>
                    <td colspan="2">Termin / Memo<br>
                        <input type="text" name="memo" placeholder="Keterangan transaksi" style="width: 100%;">
                    </td>
                </tr>
            </table>
            <br>
            <table border="1" cellpadding="6" cellspacing="0" width="100%">
                <tr>
                    <th>#</th>
                    <th>Barang (kode / nama)</th>
                    <th>Qty</th>
                    <th>Harga jual</th>
                    <th>Jumlah</th>
                    <th>Aksi</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>
                        <select name="barang_1" id="barang_1" style="width: 100%;" onchange="pilihBarang(1)">
                            <option value="">-- Pilih Barang --</option>
                            {options_barang}
                        </select>
                    </td>
                    <td><input type="text" name="qty_1" id="qty_1" value="0" style="width: 80px;" oninput="hitungTotal()"></td>
                    <td><input type="text" name="harga_1" id="harga_1" value="0" style="width: 120px;" oninput="hitungTotal()"></td>
                    <td><span id="jumlah_1">0</span><input type="hidden" name="jumlah_hidden_1" id="jumlah_hidden_1" value="0"></td>
                    <td><button type="button">X</button></td>
                </tr>
            </table>
            <p><a href="#">+ Tambah baris</a></p>
            <table width="100%">
                <tr>
                    <td align="right">
                        <b>Subtotal: <span id="label_subtotal">0</span></b><br>
                        <b>PPN Keluaran: <input type="text" name="ppn" id="input_ppn" value="0" style="width: 60px;" oninput="hitungTotal()"> %</b><br>
                        <hr style="width: 200px;">
                        <b style="font-size: 16px;">Total: <span id="label_total">0</span></b>
                        <input type="hidden" name="total_hidden" id="input_total_hidden" value="0">
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/penjualan"><button type="button">Daftar</button></a>
            <button type="submit">Simpan transaksi</button>
        </form>
        <script>
        function pilihBarang(row) {{
            var selectEl = document.getElementById('barang_' + row);
            var selectedOption = selectEl.options[selectEl.selectedIndex];
            var harga = selectedOption.getAttribute('data-harga') || '0';
            document.getElementById('harga_' + row).value = harga;
            document.getElementById('qty_' + row).value = '1';
            hitungTotal();
        }}
        function hitungTotal() {{
            var qty = parseFloat(document.getElementById('qty_1').value) || 0;
            var harga = parseFloat(document.getElementById('harga_1').value) || 0;
            var subtotal = qty * harga;
            var ppnPersen = parseFloat(document.getElementById('input_ppn').value) || 0;
            var nilaiPpn = subtotal * (ppnPersen / 100);
            var total = subtotal + nilaiPpn;

            document.getElementById('jumlah_1').innerText = subtotal.toLocaleString('id-ID');
            document.getElementById('jumlah_hidden_1').value = subtotal;
            document.getElementById('label_subtotal').innerText = subtotal.toLocaleString('id-ID');
            document.getElementById('label_total').innerText = total.toLocaleString('id-ID');
            document.getElementById('input_total_hidden').value = total.toLocaleString('id-ID');
        }}
        </script>
        '''

    elif menu_name == 'pembelian':
        tables_html = "<h2>Pembelian</h2>"
        tables_html += '<p>Transaksi pembelian tunai & kredit. Persediaan bertambah dan harga rata-rata diperbarui otomatis.</p>'
        tables_html += '<p><a href="/app/tambah-pembelian"><button type="button">+ Tambah Transaksi</button></a></p>'
        tables_html += '''
        <p>
            Dari: <input type="date" value="2026-01-01"> s.d. <input type="date" value="2026-10-31">
            <select><option>Semua status</option></select>
        </p>
        '''
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>TANGGAL</th><th>NO BUKTI</th><th>PEMASOK</th><th>STATUS</th><th>JATUH TEMPO</th><th>TOTAL</th><th>SISA</th><th>AKSI</th></tr>'
        
        jurnal_pembelian_riil = [trx for trx in daftar_pembelian if not trx['no_faktur'].startswith("SA-")]
        if jurnal_pembelian_riil:
            for trx in jurnal_pembelian_riil:
                status_badge = f'<span style="background: #e6ffed; color: #006600; padding: 2px 6px; border-radius: 4px;">{trx["status"]}</span>'
                tables_html += f'''
                <tr>
                    <td>{trx['tanggal']}</td>
                    <td><b><a href="#" style="color: #800000; text-decoration: none;">{trx['no_faktur']}</a></b></td>
                    <td>{trx['pemasok']}</td>
                    <td>{status_badge}</td>
                    <td>{trx['jatuh_tempo']}</td>
                    <td align="right">{trx['total']}</td>
                    <td align="right">{trx['sisa']}</td>
                    <td>
                        <a href="/hapus-pembelian?no_faktur={trx['no_faktur']}" onclick="return confirm(\'Hapus transaksi ini?\');"><button type="button">Hapus</button></a>
                    </td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="8" align="center">Belum ada transaksi pembelian</td></tr>'
        tables_html += '</table>'

        tables_html += '<br><h3>Jurnal Pembelian</h3>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%; font-size: 13px;">'
        tables_html += '<tr><th>TANGGAL</th><th>NO. BUKTI</th><th>KETERANGAN</th><th>PERSEDIAAN (Dr)</th><th>PPN MASUKAN (Dr)</th><th>KAS/UTANG (Cr)</th></tr>'

        if jurnal_pembelian_riil:
            for trx in jurnal_pembelian_riil:
                tables_html += f'''
                <tr>
                    <td>{trx['tanggal']}</td>
                    <td>{trx['no_faktur']}</td>
                    <td>Pembelian - {trx['pemasok']}</td>
                    <td align="right">{trx['total']}</td>
                    <td align="right">-</td>
                    <td align="right">{trx['total']}</td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="6" align="center">Belum ada jurnal pembelian</td></tr>'
        tables_html += '</table>'

        content_html = tables_html

    elif menu_name == 'tambah-pembelian':
        today_str = datetime.now().strftime('%d/%m/%Y')
        options_pemasok = "".join([f'<option value="{s["nama"]}">{s["kode"]} - {s["nama"]}</option>' for s in daftar_pemasok])
        options_barang = "".join([f'<option value="{b["kode"]} - {b["nama"]}" data-harga="{b["harga_pokok"]}">{b["kode"]} - {b["nama"]} (Stok: {b["qty"]})</option>' for b in daftar_barang])

        content_html = f'''
        <h2>Tambah Transaksi Pembelian</h2>
        <p>Nomor dibuat otomatis bila dikosongkan. Grid bisa diisi dengan tempel (Ctrl+V) dari Excel: Kode barang | Qty | Harga.</p>
        <form method="POST" action="/tambah-pembelian-submit">
            <table width="100%" cellpadding="6">
                <tr>
                    <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required style="width: 200px;"></td>
                    <td>Pemasok (kode / nama) *<br>
                        <select name="pemasok" style="width: 100%;" required>
                            <option value="">-- Pilih Pemasok --</option>
                            {options_pemasok}
                        </select>
                    </td>
                    <td>No. bukti<br><input type="text" name="no_faktur" placeholder="FB-otomatis" style="width: 200px;"></td>
                </tr>
                <tr>
                    <td>Pembayaran<br>
                        <select name="pembayaran" style="width: 100%;">
                            <option value="Kredit (dengan termin)">Kredit (dengan termin)</option>
                            <option value="Tunai">Tunai</option>
                        </select>
                    </td>
                    <td colspan="2">Termin / Memo<br>
                        <input type="text" name="memo" placeholder="Keterangan transaksi" style="width: 100%;">
                    </td>
                </tr>
            </table>
            <br>
            <table border="1" cellpadding="6" cellspacing="0" width="100%">
                <tr>
                    <th>#</th>
                    <th>Barang (kode / nama)</th>
                    <th>Qty</th>
                    <th>Harga beli</th>
                    <th>Jumlah</th>
                    <th>Aksi</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>
                        <select name="barang_1" id="barang_1" style="width: 100%;" onchange="pilihBarangBeli(1)">
                            <option value="">-- Pilih Barang --</option>
                            {options_barang}
                        </select>
                    </td>
                    <td><input type="text" name="qty_1" id="qty_1" value="0" style="width: 80px;" oninput="hitungTotalBeli()"></td>
                    <td><input type="text" name="harga_1" id="harga_1" value="0" style="width: 120px;" oninput="hitungTotalBeli()"></td>
                    <td><span id="jumlah_1">0</span><input type="hidden" name="jumlah_hidden_1" id="jumlah_hidden_1" value="0"></td>
                    <td><button type="button">X</button></td>
                </tr>
            </table>
            <p><a href="#">+ Tambah baris</a></p>
            <table width="100%">
                <tr>
                    <td align="right">
                        <b>Subtotal: <span id="label_subtotal">0</span></b><br>
                        <b>PPN Masukan: <input type="text" name="ppn" id="input_ppn" value="0" style="width: 60px;" oninput="hitungTotalBeli()"> %</b><br>
                        <hr style="width: 200px;">
                        <b style="font-size: 16px;">Total: <span id="label_total">0</span></b>
                        <input type="hidden" name="total_hidden" id="input_total_hidden" value="0">
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/pembelian"><button type="button">Daftar</button></a>
            <button type="submit">Simpan transaksi</button>
        </form>
        <script>
        function pilihBarangBeli(row) {{
            var selectEl = document.getElementById('barang_' + row);
            var selectedOption = selectEl.options[selectEl.selectedIndex];
            var harga = selectedOption.getAttribute('data-harga') || '0';
            document.getElementById('harga_' + row).value = harga;
            document.getElementById('qty_' + row).value = '1';
            hitungTotalBeli();
        }}
        function hitungTotalBeli() {{
            var qty = parseFloat(document.getElementById('qty_1').value) || 0;
            var harga = parseFloat(document.getElementById('harga_1').value) || 0;
            var subtotal = qty * harga;
            var ppnPersen = parseFloat(document.getElementById('input_ppn').value) || 0;
            var nilaiPpn = subtotal * (ppnPersen / 100);
            var total = subtotal + nilaiPpn;

            document.getElementById('jumlah_1').innerText = subtotal.toLocaleString('id-ID');
            document.getElementById('jumlah_hidden_1').value = subtotal;
            document.getElementById('label_subtotal').innerText = subtotal.toLocaleString('id-ID');
            document.getElementById('label_total').innerText = total.toLocaleString('id-ID');
            document.getElementById('input_total_hidden').value = total.toLocaleString('id-ID');
        }}
        </script>
        '''

    elif menu_name == 'penerimaan-kas':
        tab = request.args.get('tab', 'pelunasan')
        today_str = datetime.now().strftime('%d/%m/%Y')
        options_pelanggan = "".join([f'<option value="{p["nama"]}">{p["kode"]} - {p["nama"]}</option>' for p in daftar_pelanggan])
        options_akun_kas = "".join([f'<option value="{a["kode"]} - {a["nama"]}">{a["kode"]} - {a["nama"]}</option>' for a in daftar_akun if "Kas" in a["nama"] or "Bank" in a["nama"]])
        options_akun_lain = "".join([f'<option value="{a["kode"]} - {a["nama"]}">{a["kode"]} - {a["nama"]}</option>' for a in daftar_akun])

        tabel_riwayat = '''
        <hr>
        <h3>Daftar Penerimaan Kas</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">
            <tr><th>TANGGAL</th><th>NO. BUKTI</th><th>KETERANGAN / DARI</th><th>AKUN KAS</th><th>TOTAL</th><th>AKSI</th></tr>
        '''
        if daftar_penerimaan_kas:
            for pk in daftar_penerimaan_kas:
                tabel_riwayat += f'''
                <tr>
                    <td>{pk['tanggal']}</td>
                    <td>{pk['no_bukti']}</td>
                    <td>{pk['keterangan']}</td>
                    <td>{pk['akun_kas']}</td>
                    <td align="right">{pk['total']}</td>
                    <td><a href="/hapus-penerimaan-kas?no_bukti={pk['no_bukti']}" onclick="return confirm(\'Hapus penerimaan ini?\');"><button type="button">Hapus</button></a></td>
                </tr>
                '''
        else:
            tabel_riwayat += '<tr><td colspan="6" align="center">Belum ada data pada periode ini.</td></tr>'
        tabel_riwayat += '</table>'

        if tab == 'lain':
            content_html = f'''
            <h2>Penerimaan Kas</h2>
            <p>Pelunasan piutang pelanggan (BKM) dan penerimaan kas lain-lain seperti pendapatan bunga atau setoran modal.</p>
            <p>
                <b><a href="/app/penerimaan-kas?tab=pelunasan" style="color: gray; text-decoration: none;">Pelunasan Piutang</a></b> &nbsp;&nbsp;|&nbsp;&nbsp;
                <b><a href="/app/penerimaan-kas?tab=lain" style="color: black; text-decoration: underline;">Penerimaan Lain</a></b>
            </p>
            <hr>
            <h3>Penerimaan kas lain baru</h3>
            <form method="POST" action="/tambah-penerimaan-lain-submit">
                <table width="100%">
                    <tr>
                        <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required></td>
                        <td>Masuk ke akun *<br>
                            <select name="akun_kas" style="width: 100%;">
                                {options_akun_kas}
                            </select>
                        </td>
                        <td>Diterima dari<br><input type="text" name="diterima_dari" placeholder="Nama pemberi"></td>
                        <td>No. bukti<br><input type="text" name="no_bukti" placeholder="BKM-otomatis"></td>
                    </tr>
                    <tr>
                        <td colspan="4">Memo<br><input type="text" name="memo" placeholder="Keterangan" style="width: 100%;"></td>
                    </tr>
                </table>
                <br>
                <table border="1" cellpadding="6" cellspacing="0" width="100%">
                    <tr>
                        <th>#</th>
                        <th>Akun (kode / nama)</th>
                        <th>Jumlah</th>
                        <th>Keterangan</th>
                        <th>Aksi</th>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>
                            <select name="akun_1" style="width: 100%;">
                                <option value="">-- Pilih Akun --</option>
                                {options_akun_lain}
                            </select>
                        </td>
                        <td><input type="text" name="jumlah_1" placeholder="0" style="width: 100px;"></td>
                        <td><input type="text" name="ket_1" placeholder="Keterangan baris" style="width: 100%;"></td>
                        <td><button type="button">X</button></td>
                    </tr>
                </table>
                <p><a href="#">+ Tambah baris</a></p>
                <hr>
                <button type="submit">Simpan</button>
            </form>
            {tabel_riwayat}
            '''
        else:
            content_html = f'''
            <h2>Penerimaan Kas</h2>
            <p>Pelunasan piutang pelanggan (BKM) dan penerimaan kas lain-lain seperti pendapatan bunga atau setoran modal.</p>
            <p>
                <b><a href="/app/penerimaan-kas?tab=pelunasan" style="color: black; text-decoration: underline;">Pelunasan Piutang</a></b> &nbsp;&nbsp;|&nbsp;&nbsp;
                <b><a href="/app/penerimaan-kas?tab=lain" style="color: gray; text-decoration: none;">Penerimaan Lain</a></b>
            </p>
            <hr>
            <h3>Pelunasan piutang baru</h3>
            <form method="POST" action="/tambah-pelunasan-submit">
                <table width="100%">
                    <tr>
                        <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required></td>
                        <td>Pelanggan (kode / nama) *<br>
                            <select name="pelanggan" style="width: 100%;" required>
                                <option value="">-- Pilih Pelanggan --</option>
                                {options_pelanggan}
                            </select>
                        </td>
                        <td>Setor ke akun *<br>
                            <select name="akun_kas" style="width: 100%;">
                                {options_akun_kas}
                            </select>
                        </td>
                        <td>No. bukti<br><input type="text" name="no_bukti" placeholder="BKM-otomatis"></td>
                    </tr>
                </table>
                <br>
                <fieldset>
                    <legend>Dialokasikan otomatis ke transaksi terlama</legend>
                    <p align="center" style="color: gray;">Pilih pelanggan untuk melihat sisa piutang.</p>
                </fieldset>
                <hr>
                <button type="submit">Simpan</button>
            </form>
            {tabel_riwayat}
            '''

    elif menu_name == 'pengeluaran-kas':
        tab = request.args.get('tab', 'pembayaran')
        today_str = datetime.now().strftime('%d/%m/%Y')
        options_pemasok = "".join([f'<option value="{s["nama"]}">{s["kode"]} - {s["nama"]}</option>' for s in daftar_pemasok])
        options_akun_kas = "".join([f'<option value="{a["kode"]} - {a["nama"]}">{a["kode"]} - {a["nama"]}</option>' for a in daftar_akun if "Kas" in a["nama"] or "Bank" in a["nama"]])
        options_akun_lain = "".join([f'<option value="{a["kode"]} - {a["nama"]}">{a["kode"]} - {a["nama"]}</option>' for a in daftar_akun])

        tabel_riwayat_keluar = '''
        <hr>
        <h3>Daftar Pengeluaran Kas</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">
            <tr><th>TANGGAL</th><th>NO. BUKTI</th><th>KETERANGAN / DIBAYAR KEPADA</th><th>AKUN KAS</th><th>TOTAL</th><th>AKSI</th></tr>
        '''
        if daftar_pengeluaran_kas:
            for pk in daftar_pengeluaran_kas:
                tabel_riwayat_keluar += f'''
                <tr>
                    <td>{pk['tanggal']}</td>
                    <td>{pk['no_bukti']}</td>
                    <td>{pk['keterangan']}</td>
                    <td>{pk['akun_kas']}</td>
                    <td align="right">{pk['total']}</td>
                    <td><a href="/hapus-pengeluaran-kas?no_bukti={pk['no_bukti']}" onclick="return confirm(\'Hapus pengeluaran ini?\');"><button type="button">Hapus</button></a></td>
                </tr>
                '''
        else:
            tabel_riwayat_keluar += '<tr><td colspan="6" align="center">Belum ada data pada periode ini.</td></tr>'
        tabel_riwayat_keluar += '</table>'

        if tab == 'lain':
            content_html = f'''
            <h2>Pengeluaran Kas</h2>
            <p>Pembayaran utang ke pemasok (BKK) dan pengeluaran kas lain-lain seperti beban, pembelian aset, atau prive/dividen.</p>
            <p>
                <b><a href="/app/pengeluaran-kas?tab=pembayaran" style="color: gray; text-decoration: none;">Pembayaran Utang</a></b> &nbsp;&nbsp;|&nbsp;&nbsp;
                <b><a href="/app/pengeluaran-kas?tab=lain" style="color: black; text-decoration: underline;">Pengeluaran Lain</a></b>
            </p>
            <hr>
            <h3>Pengeluaran kas lain baru</h3>
            <form method="POST" action="/tambah-pengeluaran-lain-submit">
                <table width="100%">
                    <tr>
                        <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required></td>
                        <td>Keluar dari akun *<br>
                            <select name="akun_kas" style="width: 100%;">
                                {options_akun_kas}
                            </select>
                        </td>
                        <td>Dibayar kepada<br><input type="text" name="dibayar_kepada" placeholder="Nama penerima"></td>
                        <td>No. bukti<br><input type="text" name="no_bukti" placeholder="BKK-otomatis"></td>
                    </tr>
                    <tr>
                        <td colspan="4">Memo<br><input type="text" name="memo" placeholder="Keterangan" style="width: 100%;"></td>
                    </tr>
                </table>
                <br>
                <table border="1" cellpadding="6" cellspacing="0" width="100%">
                    <tr>
                        <th>#</th>
                        <th>Akun (kode / nama)</th>
                        <th>Jumlah</th>
                        <th>Keterangan</th>
                        <th>Aksi</th>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>
                            <select name="akun_1" style="width: 100%;">
                                <option value="">-- Pilih Akun --</option>
                                {options_akun_lain}
                            </select>
                        </td>
                        <td><input type="text" name="jumlah_1" placeholder="0" style="width: 100px;"></td>
                        <td><input type="text" name="ket_1" placeholder="Keterangan baris" style="width: 100%;"></td>
                        <td><button type="button">X</button></td>
                    </tr>
                </table>
                <p><a href="#">+ Tambah baris</a></p>
                <p><small>Akun kontrol (Piutang, Utang, Persediaan) tidak dapat dipakai di sini — gunakan menu penjualan, pembelian, atau pelunasan. Jurnal: Dr akun-akun lawan / Cr Kas.</small></p>
                <hr>
                <button type="submit">Simpan</button>
            </form>
            {tabel_riwayat_keluar}
            '''
        else:
            content_html = f'''
            <h2>Pengeluaran Kas</h2>
            <p>Pembayaran utang ke pemasok (BKK) dan pengeluaran kas lain-lain seperti beban, pembelian aset, atau prive/dividen.</p>
            <p>
                <b><a href="/app/pengeluaran-kas?tab=pembayaran" style="color: black; text-decoration: underline;">Pembayaran Utang</a></b> &nbsp;&nbsp;|&nbsp;&nbsp;
                <b><a href="/app/pengeluaran-kas?tab=lain" style="color: gray; text-decoration: none;">Pengeluaran Lain</a></b>
            </p>
            <hr>
            <h3>Pembayaran utang baru</h3>
            <form method="POST" action="/tambah-pembayaran-utang-submit">
                <table width="100%">
                    <tr>
                        <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required></td>
                        <td>Pemasok (kode / nama) *<br>
                            <select name="pemasok" style="width: 100%;" required>
                                <option value="">-- Pilih Pemasok --</option>
                                {options_pemasok}
                            </select>
                        </td>
                        <td>Bayar dari akun *<br>
                            <select name="akun_kas" style="width: 100%;">
                                {options_akun_kas}
                            </select>
                        </td>
                        <td>No. bukti<br><input type="text" name="no_bukti" placeholder="BKK-otomatis"></td>
                    </tr>
                </table>
                <br>
                <fieldset>
                    <legend>Dialokasikan otomatis ke transaksi terlama</legend>
                    <p align="center" style="color: gray;">Pilih pemasok untuk melihat sisa utang.</p>
                </fieldset>
                <hr>
                <button type="submit">Simpan</button>
            </form>
            {tabel_riwayat_keluar}
            '''

    elif menu_name == 'jurnal-umum':
        tables_html = "<h2>Jurnal Umum</h2>"
        tables_html += '<p>Untuk transaksi di luar menu lain: jurnal umum (dividen, retur), jurnal penyesuaian (penyusutan, akrual), dan jurnal penutup.</p>'
        tables_html += '<p><a href="/app/jurnal-umum-baru"><button type="button">+ Jurnal umum baru</button></a></p>'
        tables_html += '<table border="1" cellpadding="6" cellspacing="0" style="width: 100%;">'
        tables_html += '<tr><th>TANGGAL</th><th>NO. BUKTI</th><th>AKUN & KETERANGAN</th><th>KODE</th><th>DEBIT</th><th>KREDIT</th><th>AKSI</th></tr>'
        
        if daftar_jurnal_umum:
            for trx in daftar_jurnal_umum:
                tables_html += f'''
                <tr>
                    <td>{trx['tanggal']}</td>
                    <td>{trx['no_bukti']}</td>
                    <td colspan="4">{trx['memo']}</td>
                    <td><a href="/hapus-jurnal?no_bukti={trx['no_bukti']}" onclick="return confirm(\'Hapus jurnal ini?\');"><button type="button">Hapus</button></a></td>
                </tr>
                '''
        else:
            tables_html += '<tr><td colspan="7" align="center">Belum ada jurnal pada periode ini.</td></tr>'
        tables_html += '</table>'
        content_html = tables_html

    elif menu_name == 'jurnal-umum-baru':
        today_str = datetime.now().strftime('%d/%m/%Y')
        next_bukti = f"JU-{str(len(daftar_jurnal_umum)+1).zfill(3)}"
        options_akun = "".join([f'<option value="{a["kode"]} - {a["nama"]}">{a["kode"]} - {a["nama"]}</option>' for a in daftar_akun])

        content_html = f'''
        <h2>Jurnal Umum Baru</h2>
        <p>Satu baris hanya boleh berisi debit ATAU kredit. Bisa tempel (Ctrl+V) dari Excel: Kode akun | Debit | Kredit | Keterangan.</p>
        <form method="POST" action="/tambah-jurnal-submit">
            <table width="100%">
                <tr>
                    <td>Tanggal *<br><input type="text" name="tanggal" value="{today_str}" required></td>
                    <td>No. bukti<br><input type="text" name="no_bukti" value="{next_bukti}"></td>
                    <td>Memo / keterangan<br><input type="text" name="memo" placeholder="mis. Penyusutan peralatan Januari" style="width: 100%;"></td>
                </tr>
                <tr>
                    <td colspan="3">Jenis jurnal<br>
                        <select name="jenis_jurnal" style="width: 30%;">
                            <option value="Jurnal Umum">Jurnal Umum</option>
                            <option value="Jurnal Penyesuaian">Jurnal Penyesuaian</option>
                            <option value="Jurnal Penutup">Jurnal Penutup</option>
                        </select>
                        <br><small>Transaksi biasa (mis. dividen, retur, koreksi).</small>
                    </td>
                </tr>
            </table>
            <br>
            <table border="1" cellpadding="6" cellspacing="0" width="100%">
                <tr>
                    <th>#</th>
                    <th>Akun (kode / nama)</th>
                    <th>Debit</th>
                    <th>Kredit</th>
                    <th>Keterangan</th>
                    <th>Aksi</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>
                        <select name="akun_1" style="width: 100%;">
                            <option value="">-- Pilih Akun --</option>
                            {options_akun}
                        </select>
                    </td>
                    <td><input type="text" name="debit_1" id="debit_1" placeholder="0" oninput="hitungJurnal()"></td>
                    <td><input type="text" name="kredit_1" id="kredit_1" placeholder="0" oninput="hitungJurnal()"></td>
                    <td><input type="text" name="ket_1" placeholder="Keterangan baris" style="width: 100%;"></td>
                    <td><button type="button">X</button></td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>
                        <select name="akun_2" style="width: 100%;">
                            <option value="">-- Pilih Akun --</option>
                            {options_akun}
                        </select>
                    </td>
                    <td><input type="text" name="debit_2" id="debit_2" placeholder="0" oninput="hitungJurnal()"></td>
                    <td><input type="text" name="kredit_2" id="kredit_2" placeholder="0" oninput="hitungJurnal()"></td>
                    <td><input type="text" name="ket_2" placeholder="Keterangan baris" style="width: 100%;"></td>
                    <td><button type="button">X</button></td>
                </tr>
            </table>
            <p><a href="#">+ Tambah baris</a></p>
            <table width="100%">
                <tr>
                    <td><span id="status_seimbang" style="background: #ffe6e6; color: #cc0000; padding: 3px 8px; border-radius: 4px;">✕ Selisih</span></td>
                    <td align="right">
                        <b>Total &nbsp;&nbsp;&nbsp;&nbsp; Debit: <span id="total_debit">0</span> &nbsp;&nbsp;&nbsp;&nbsp; Kredit: <span id="total_kredit">0</span></b>
                    </td>
                </tr>
            </table>
            <hr>
            <a href="/app/jurnal-umum"><button type="button">Daftar</button></a>
            <button type="submit" id="btn_simpan" disabled>Simpan</button>
        </form>
        <script>
        function hitungJurnal() {{
            var d1 = parseFloat(document.getElementById('debit_1').value) || 0;
            var k1 = parseFloat(document.getElementById('kredit_1').value) || 0;
            var d2 = parseFloat(document.getElementById('debit_2').value) || 0;
            var k2 = parseFloat(document.getElementById('kredit_2').value) || 0;

            var totalD = d1 + d2;
            var totalK = k1 + k2;

            document.getElementById('total_debit').innerText = totalD.toLocaleString('id-ID');
            document.getElementById('total_kredit').innerText = totalK.toLocaleString('id-ID');

            var statusEl = document.getElementById('status_seimbang');
            var btnSimpan = document.getElementById('btn_simpan');

            if (totalD > 0 && totalD === totalK) {{
                statusEl.innerHTML = '✓ Seimbang';
                statusEl.style.background = '#e6ffed';
                statusEl.style.color = '#006600';
                btnSimpan.disabled = false;
            }} else {{
                statusEl.innerHTML = '✕ Selisih';
                statusEl.style.background = '#ffe6e6';
                statusEl.style.color = '#cc0000';
                btnSimpan.disabled = true;
            }}
        }}
        </script>
        '''

    else:
        formatted_title = menu_name.replace('-', ' ').title()
        content_html = f'<h2>{formatted_title}</h2><p>Halaman ini sedang dalam tahap pengembangan (tempat kosong).</p>'

    return render_template_string('''
    <table>
        <tr>
            <td valign="top" width="220" style="border-right: 1px solid #000; padding-right: 15px;">
                <p><b>''' + (profil_perusahaan['nama'] if profil_perusahaan['nama'] else 'PT Dagang') + '''</b></p>
                <p><a href="/logout">[ Keluar ]</a></p>
                <hr>
                <b>BERANDA</b>
                <ul>
                    <li><a href="/app/dashboard">Dashboard</a></li>
                </ul>
                <b>SETUP</b>
                <ul>
                    <li><a href="/app/data-perusahaan">Data Perusahaan</a></li>
                    <li><a href="/app/daftar-akun">Daftar Akun</a></li>
                    <li><a href="/app/saldo-awal">Saldo Awal</a></li>
                </ul>
                <b>KARTU</b>
                <ul>
                    <li><a href="/app/pelanggan">Pelanggan</a></li>
                    <li><a href="/app/pemasok">Pemasok</a></li>
                    <li><a href="/app/barang">Barang</a></li>
                </ul>
                <b>TRANSAKSI</b>
                <ul>
                    <li><a href="/app/penjualan">Penjualan</a></li>
                    <li><a href="/app/pembelian">Pembelian</a></li>
                    <li><a href="/app/penerimaan-kas">Penerimaan Kas</a></li>
                    <li><a href="/app/pengeluaran-kas">Pengeluaran Kas</a></li>
                    <li><a href="/app/jurnal-umum">Jurnal Umum</a></li>
                </ul>
            </td>
            <td valign="top" style="padding-left: 20px;">
                ''' + content_html + '''
            </td>
        </tr>
    </table>
    ''')

@app.route('/tambah-pelanggan-submit', methods=['POST'])
def tambah_pelanggan_submit():
    kode = request.form.get('kode')
    nama = request.form.get('nama')
    telepon = request.form.get('telepon')
    syarat_bayar = request.form.get('syarat_bayar')
    potongan = request.form.get('potongan', '0')
    hari_diskon = request.form.get('hari_diskon', '0')
    jatuh_tempo = request.form.get('jatuh_tempo', '30')
    
    if syarat_bayar == "Tunai":
        termin_str = "Tunai"
    elif potongan and hari_diskon:
        termin_str = f"{potongan}/{hari_diskon}, n/{jatuh_tempo}"
    else:
        termin_str = f"n/{jatuh_tempo}"

    saldo_awal = request.form.get('saldo_awal')
    if not saldo_awal or saldo_awal.strip() == "" or saldo_awal == "0":
        saldo_awal_str = "-"
        val_sa = 0
    else:
        try:
            val_sa = float(saldo_awal.replace('.', '').replace(',', '.'))
            saldo_awal_str = f"{val_sa:,.0f}".replace(',', '.')
        except:
            val_sa = 0
            saldo_awal_str = saldo_awal

    daftar_pelanggan.append({
        "kode": kode,
        "nama": nama,
        "telepon": telepon if telepon else "-",
        "syarat_bayar": termin_str,
        "saldo_awal": saldo_awal_str
    })

    if val_sa > 0:
        no_faktur_sa = f"SA-{kode}"
        exists = any(trx['no_faktur'] == no_faktur_sa for trx in daftar_penjualan)
        if not exists:
            daftar_penjualan.append({
                "no_faktur": no_faktur_sa,
                "tanggal": profil_perusahaan['periode'],
                "pelanggan": nama,
                "pembayaran": "Kredit (dengan termin)",
                "total": saldo_awal_str,
                "status": "Belum Lunas",
                "jatuh_tempo": termin_str,
                "sisa": saldo_awal_str
            })

    return redirect(url_for('menu_handler', menu_name="pelanggan"))

@app.route('/tambah-pemasok-submit', methods=['POST'])
def tambah_pemasok_submit():
    kode = request.form.get('kode')
    nama = request.form.get('nama')
    telepon = request.form.get('telepon')
    syarat_bayar = request.form.get('syarat_bayar')
    potongan = request.form.get('potongan', '0')
    hari_diskon = request.form.get('hari_diskon', '0')
    jatuh_tempo = request.form.get('jatuh_tempo', '30')
    
    if syarat_bayar == "Tunai":
        termin_str = "Tunai"
    elif potongan and hari_diskon:
        termin_str = f"{potongan}/{hari_diskon}, n/{jatuh_tempo}"
    else:
        termin_str = f"n/{jatuh_tempo}"

    saldo_awal = request.form.get('saldo_awal')
    if not saldo_awal or saldo_awal.strip() == "" or saldo_awal == "0":
        saldo_awal_str = "-"
        val_sa = 0
    else:
        try:
            val_sa = float(saldo_awal.replace('.', '').replace(',', '.'))
            saldo_awal_str = f"{val_sa:,.0f}".replace(',', '.')
        except:
            val_sa = 0
            saldo_awal_str = saldo_awal

    daftar_pemasok.append({
        "kode": kode,
        "nama": nama,
        "telepon": telepon if telepon else "-",
        "syarat_bayar": termin_str,
        "saldo_awal": saldo_awal_str
    })

    if val_sa > 0:
        no_faktur_sa = f"SA-{kode}"
        exists = any(trx['no_faktur'] == no_faktur_sa for trx in daftar_pembelian)
        if not exists:
            daftar_pembelian.append({
                "no_faktur": no_faktur_sa,
                "tanggal": profil_perusahaan['periode'],
                "pemasok": nama,
                "pembayaran": "Kredit (dengan termin)",
                "total": saldo_awal_str,
                "status": "Belum Lunas",
                "jatuh_tempo": termin_str,
                "sisa": saldo_awal_str
            })

    return redirect(url_for('menu_handler', menu_name="pemasok"))

@app.route('/tambah-barang-submit', methods=['POST'])
def tambah_barang_submit():
    kode = request.form.get('kode')
    nama = request.form.get('nama')
    satuan = request.form.get('satuan', 'pcs')
    harga_jual = request.form.get('harga_jual', '0')
    qty = request.form.get('qty', '0')
    harga_pokok = request.form.get('harga_pokok', '0')
    nilai = request.form.get('nilai', '0')

    try:
        val_jual = float(harga_jual.replace('.', '').replace(',', '.'))
        jual_str = f"{val_jual:,.0f}".replace(',', '.')
    except:
        jual_str = harga_jual if harga_jual else "-"

    try:
        val_hpp = float(harga_pokok.replace('.', '').replace(',', '.'))
        hpp_str = f"{val_hpp:,.0f}".replace(',', '.')
    except:
        hpp_str = harga_pokok if harga_pokok else "0"

    try:
        val_nilai = float(nilai.replace('.', '').replace(',', '.'))
        nilai_str = f"{val_nilai:,.0f}".replace(',', '.')
    except:
        nilai_str = "0"

    daftar_barang.append({
        "kode": kode,
        "nama": nama,
        "satuan": satuan if satuan else "pcs",
        "harga_jual": jual_str,
        "qty": qty if qty else "0",
        "harga_pokok": hpp_str,
        "nilai": nilai_str
    })
    return redirect(url_for('menu_handler', menu_name="barang"))

@app.route('/tambah-penjualan-submit', methods=['POST'])
def tambah_penjualan_submit():
    tanggal = request.form.get('tanggal')
    pelanggan = request.form.get('pelanggan')
    no_faktur = request.form.get('no_faktur')
    pembayaran = request.form.get('pembayaran')
    total = request.form.get('total_hidden', '0')

    daftar_penjualan.append({
        "no_faktur": no_faktur if no_faktur else f"FJ-{str(len(daftar_penjualan)+1).zfill(3)}",
        "tanggal": tanggal,
        "pelanggan": pelanggan,
        "pembayaran": pembayaran,
        "total": total,
        "status": "Belum Lunas" if pembayaran == "Kredit (dengan termin)" else "Lunas",
        "jatuh_tempo": "30 hari" if pembayaran == "Kredit (dengan termin)" else "-",
        "sisa": total if pembayaran == "Kredit (dengan termin)" else "-"
    })
    return redirect(url_for('menu_handler', menu_name="penjualan"))

@app.route('/tambah-pembelian-submit', methods=['POST'])
def tambah_pembelian_submit():
    tanggal = request.form.get('tanggal')
    pemasok = request.form.get('pemasok')
    no_faktur = request.form.get('no_faktur')
    pembayaran = request.form.get('pembayaran')
    total = request.form.get('total_hidden', '0')

    daftar_pembelian.append({
        "no_faktur": no_faktur if no_faktur else f"FB-{str(len(daftar_pembelian)+1).zfill(3)}",
        "tanggal": tanggal,
        "pemasok": pemasok,
        "pembayaran": pembayaran,
        "total": total,
        "status": "Belum Lunas" if pembayaran == "Kredit (dengan termin)" else "Lunas",
        "jatuh_tempo": "30 hari" if pembayaran == "Kredit (dengan termin)" else "-",
        "sisa": total if pembayaran == "Kredit (dengan termin)" else "-"
    })
    return redirect(url_for('menu_handler', menu_name="pembelian"))

@app.route('/tambah-pelunasan-submit', methods=['POST'])
def tambah_pelunasan_submit():
    tanggal = request.form.get('tanggal')
    pelanggan = request.form.get('pelanggan')
    akun_kas = request.form.get('akun_kas')
    no_bukti = request.form.get('no_bukti')
    
    daftar_penerimaan_kas.append({
        "tanggal": tanggal,
        "no_bukti": no_bukti if no_bukti else f"BKM-{str(len(daftar_penerimaan_kas)+1).zfill(3)}",
        "keterangan": f"Pelunasan piutang - {pelanggan}",
        "akun_kas": akun_kas.split(" - ")[1] if " - " in akun_kas else akun_kas,
        "total": "0"
    })
    return redirect(url_for('menu_handler', menu_name="penerimaan-kas"))

@app.route('/tambah-penerimaan-lain-submit', methods=['POST'])
def tambah_penerimaan_lain_submit():
    tanggal = request.form.get('tanggal')
    akun_kas = request.form.get('akun_kas')
    diterima_dari = request.form.get('diterima_dari')
    no_bukti = request.form.get('no_bukti')
    jumlah = request.form.get('jumlah_1', '0')
    
    daftar_penerimaan_kas.append({
        "tanggal": tanggal,
        "no_bukti": no_bukti if no_bukti else f"BKM-{str(len(daftar_penerimaan_kas)+1).zfill(3)}",
        "keterangan": diterima_dari if diterima_dari else "Penerimaan Lain",
        "akun_kas": akun_kas.split(" - ")[1] if " - " in akun_kas else akun_kas,
        "total": jumlah if jumlah else "0"
    })
    return redirect(url_for('menu_handler', menu_name="penerimaan-kas"))

@app.route('/tambah-pembayaran-utang-submit', methods=['POST'])
def tambah_pembayaran_utang_submit():
    tanggal = request.form.get('tanggal')
    pemasok = request.form.get('pemasok')
    akun_kas = request.form.get('akun_kas')
    no_bukti = request.form.get('no_bukti')
    
    daftar_pengeluaran_kas.append({
        "tanggal": tanggal,
        "no_bukti": no_bukti if no_bukti else f"BKK-{str(len(daftar_pengeluaran_kas)+1).zfill(3)}",
        "keterangan": f"Pembayaran utang - {pemasok}",
        "akun_kas": akun_kas.split(" - ")[1] if " - " in akun_kas else akun_kas,
        "total": "0"
    })
    return redirect(url_for('menu_handler', menu_name="pengeluaran-kas"))

@app.route('/tambah-pengeluaran-lain-submit', methods=['POST'])
def tambah_pengeluaran_lain_submit():
    tanggal = request.form.get('tanggal')
    akun_kas = request.form.get('akun_kas')
    dibayar_kepada = request.form.get('dibayar_kepada')
    no_bukti = request.form.get('no_bukti')
    jumlah = request.form.get('jumlah_1', '0')
    
    daftar_pengeluaran_kas.append({
        "tanggal": tanggal,
        "no_bukti": no_bukti if no_bukti else f"BKK-{str(len(daftar_pengeluaran_kas)+1).zfill(3)}",
        "keterangan": dibayar_kepada if dibayar_kepada else "Pengeluaran Lain",
        "akun_kas": akun_kas.split(" - ")[1] if " - " in akun_kas else akun_kas,
        "total": jumlah if jumlah else "0"
    })
    return redirect(url_for('menu_handler', menu_name="pengeluaran-kas"))

@app.route('/tambah-jurnal-submit', methods=['POST'])
def tambah_jurnal_submit():
    tanggal = request.form.get('tanggal')
    no_bukti = request.form.get('no_bukti')
    memo = request.form.get('memo')

    daftar_jurnal_umum.append({
        "tanggal": tanggal,
        "no_bukti": no_bukti if no_bukti else f"JU-{str(len(daftar_jurnal_umum)+1).zfill(3)}",
        "memo": memo if memo else "Jurnal Umum"
    })
    return redirect(url_for('menu_handler', menu_name="jurnal-umum"))

@app.route('/ubah-pelanggan-submit', methods=['POST'])
def ubah_pelanggan_submit():
    kode_lama = request.form.get('kode_lama')
    kode_baru = request.form.get('kode')
    nama_baru = request.form.get('nama')
    telepon_baru = request.form.get('telepon')
    syarat_baru = request.form.get('syarat_bayar')
    saldo_baru = request.form.get('saldo_awal')
    
    for p in daftar_pelanggan:
        if p['kode'] == kode_lama:
            p['kode'] = kode_baru
            p['nama'] = nama_baru
            p['telepon'] = telepon_baru
            p['syarat_bayar'] = syarat_baru
            p['saldo_awal'] = saldo_baru
            break
            
    return redirect(url_for('menu_handler', menu_name="pelanggan"))

@app.route('/ubah-pemasok-submit', methods=['POST'])
def ubah_pemasok_submit():
    kode_lama = request.form.get('kode_lama')
    kode_baru = request.form.get('kode')
    nama_baru = request.form.get('nama')
    telepon_baru = request.form.get('telepon')
    syarat_baru = request.form.get('syarat_bayar')
    saldo_baru = request.form.get('saldo_awal')
    
    for s in daftar_pemasok:
        if s['kode'] == kode_lama:
            s['kode'] = kode_baru
            s['nama'] = nama_baru
            s['telepon'] = telepon_baru
            s['syarat_bayar'] = syarat_baru
            s['saldo_awal'] = saldo_baru
            break
            
    return redirect(url_for('menu_handler', menu_name="pemasok"))

@app.route('/ubah-barang-submit', methods=['POST'])
def ubah_barang_submit():
    kode_lama = request.form.get('kode_lama')
    kode_baru = request.form.get('kode')
    nama_baru = request.form.get('nama')
    satuan_baru = request.form.get('satuan')
    jual_baru = request.form.get('harga_jual')
    qty_baru = request.form.get('qty')
    hpp_baru = request.form.get('harga_pokok')
    nilai_baru = request.form.get('nilai')
    
    for b in daftar_barang:
        if b['kode'] == kode_lama:
            b['kode'] = kode_baru
            b['nama'] = nama_baru
            b['satuan'] = satuan_baru
            b['harga_jual'] = jual_baru
            b['qty'] = qty_baru
            b['harga_pokok'] = hpp_baru
            b['nilai'] = nilai_baru
            break
            
    return redirect(url_for('menu_handler', menu_name="barang"))

@app.route('/hapus-pelanggan')
def hapus_pelanggan():
    kode = request.args.get('kode')
    global daftar_pelanggan
    daftar_pelanggan = [p for p in daftar_pelanggan if p['kode'] != kode]
    return redirect(url_for('menu_handler', menu_name="pelanggan"))

@app.route('/hapus-pemasok')
def hapus_pemasok():
    kode = request.args.get('kode')
    global daftar_pemasok
    daftar_pemasok = [s for s in daftar_pemasok if s['kode'] != kode]
    return redirect(url_for('menu_handler', menu_name="pemasok"))

@app.route('/hapus-barang')
def hapus_barang():
    kode = request.args.get('kode')
    global daftar_barang
    daftar_barang = [b for b in daftar_barang if b['kode'] != kode]
    return redirect(url_for('menu_handler', menu_name="barang"))

@app.route('/hapus-penjualan')
def hapus_penjualan():
    no_faktur = request.args.get('no_faktur')
    global daftar_penjualan
    daftar_penjualan = [trx for trx in daftar_penjualan if trx['no_faktur'] != no_faktur]
    return redirect(url_for('menu_handler', menu_name="penjualan"))

@app.route('/hapus-pembelian')
def hapus_pembelian():
    no_faktur = request.args.get('no_faktur')
    global daftar_pembelian
    daftar_pembelian = [trx for trx in daftar_pembelian if trx['no_faktur'] != no_faktur]
    return redirect(url_for('menu_handler', menu_name="pembelian"))

@app.route('/hapus-penerimaan-kas')
def hapus_penerimaan_kas():
    no_bukti = request.args.get('no_bukti')
    global daftar_penerimaan_kas
    daftar_penerimaan_kas = [trx for trx in daftar_penerimaan_kas if trx['no_bukti'] != no_bukti]
    return redirect(url_for('menu_handler', menu_name="penerimaan-kas"))

@app.route('/hapus-pengeluaran-kas')
def hapus_pengeluaran_kas():
    no_bukti = request.args.get('no_bukti')
    global daftar_pengeluaran_kas
    daftar_pengeluaran_kas = [trx for trx in daftar_pengeluaran_kas if trx['no_bukti'] != no_bukti]
    return redirect(url_for('menu_handler', menu_name="pengeluaran-kas"))

@app.route('/hapus-jurnal')
def hapus_jurnal():
    no_bukti = request.args.get('no_bukti')
    global daftar_jurnal_umum
    daftar_jurnal_umum = [trx for trx in daftar_jurnal_umum if trx['no_bukti'] != no_bukti]
    return redirect(url_for('menu_handler', menu_name="jurnal-umum"))

@app.route('/simpan-saldo-awal', methods=['POST'])
def simpan_saldo_awal():
    global daftar_akun
    
    total_piutang = sum([float(str(p['saldo_awal']).replace('.', '').replace(',', '.')) for p in daftar_pelanggan if p['saldo_awal'] != '-'])
    total_utang = sum([float(str(s['saldo_awal']).replace('.', '').replace(',', '.')) for s in daftar_pemasok if s['saldo_awal'] != '-'])
    total_persediaan_kartu = sum([float(str(b['nilai']).replace('.', '').replace(',', '.')) for b in daftar_barang if b['nilai'] != '-'])

    total_persediaan_otomatis = total_persediaan_kartu + total_utang - total_piutang
    if total_persediaan_otomatis < 0:
        total_persediaan_otomatis = 0

    total_d = total_piutang + total_persediaan_otomatis
    total_k = total_utang
    
    for akun in daftar_akun:
        if 'debit' not in akun: akun['debit'] = ''
        if 'kredit' not in akun: akun['kredit'] = ''

        if akun['kode'] == '1-1300':
            akun['debit'] = f"{total_piutang:,.0f}".replace(',', '.') if total_piutang > 0 else ""
            akun['kredit'] = ""
        elif akun['kode'] == '1-1400':
            akun['debit'] = f"{total_persediaan_otomatis:,.0f}".replace(',', '.') if total_persediaan_otomatis > 0 else ""
            akun['kredit'] = ""
        elif akun['kode'] == '2-1100':
            akun['kredit'] = f"{total_utang:,.0f}".replace(',', '.') if total_utang > 0 else ""
            akun['debit'] = ""
        elif akun['kode'] != '3-9999':
            d_val = request.form.get(f"debit_{akun['kode']}", "")
            k_val = request.form.get(f"kredit_{akun['kode']}", "")
            
            akun['debit'] = d_val if d_val else ""
            akun['kredit'] = k_val if k_val else ""
            
            try:
                val_d = float(str(akun['debit']).replace('.', '').replace(',', '.'))
            except:
                val_d = 0
            try:
                val_k = float(str(akun['kredit']).replace('.', '').replace(',', '.'))
            except:
                val_k = 0
                
            total_d += val_d
            total_k += val_k
            
            if val_d > 0:
                akun['saldo'] = f"{val_d:,.0f}".replace(',', '.')
            elif val_k > 0:
                akun['saldo'] = f"{val_k:,.0f}".replace(',', '.')
            else:
                akun['saldo'] = "-"

    for akun in daftar_akun:
        if akun['kode'] == '1-1300':
            akun['saldo'] = akun['debit'] if akun['debit'] else "-"
        elif akun['kode'] == '1-1400':
            akun['saldo'] = akun['debit'] if akun['debit'] else "-"
        elif akun['kode'] == '2-1100':
            akun['saldo'] = akun['kredit'] if akun['kredit'] else "-"
                
    selisih = total_d - total_k
    for akun in daftar_akun:
        if akun['kode'] == '3-9999':
            if selisih > 0:
                akun['kredit'] = f"{selisih:,.0f}".replace(',', '.')
                akun['debit'] = ""
                akun['saldo'] = f"{selisih:,.0f}".replace(',', '.')
            elif selisih < 0:
                akun['debit'] = f"{abs(selisih):,.0f}".replace(',', '.')
                akun['kredit'] = ""
                akun['saldo'] = f"{abs(selisih):,.0f}".replace(',', '.')
            else:
                akun['debit'] = ""
                akun['kredit'] = ""
                akun['saldo'] = "-"
            break
            
    return redirect(url_for('menu_handler', menu_name="saldo-awal"))

@app.route('/tambah-akun-submit', methods=['POST'])
def tambah_akun_submit():
    kode = request.form.get('kode')
    nama = request.form.get('nama')
    tipe = request.form.get('tipe')
    saldo = request.form.get('saldo')
    if not saldo or saldo.strip() == "":
        saldo = "-"
        
    kategori = "Beban"
    dk = "D"
    if kode.startswith("1"):
        kategori = "Aset"
    elif kode.startswith("2"):
        kategori = "Liabilitas"
        dk = "K"
    elif kode.startswith("3"):
        kategori = "Ekuitas"
        dk = "K" if "Modal" in tipe or "Ditahan" in tipe else "D"
    elif kode.startswith("4"):
        kategori = "Pendapatan"
        dk = "K"
    elif kode.startswith("5"):
        kategori = "Harga Pokok Penjualan"
        dk = "K" if "Potongan Pembelian" in nama else "D"
    elif kode.startswith("7"):
        kategori = "Pendapatan Lain-lain"
        dk = "K"
    elif kode.startswith("8") or kode.startswith("9"):
        kategori = "Beban Lain-lain" if kode.startswith("8") else "Beban"
        dk = "D"
        
    daftar_akun.append({
        "kategori": kategori,
        "kode": kode,
        "nama": nama,
        "induk": tipe,
        "dk": dk,
        "sistem": False,
        "debit": "",
        "kredit": "",
        "saldo": saldo
    })
    return redirect(url_for('menu_handler', menu_name="daftar-akun"))

@app.route('/ubah-akun-submit', methods=['POST'])
def ubah_akun_submit():
    kode_lama = request.form.get('kode_lama')
    kode_baru = request.form.get('kode')
    nama_baru = request.form.get('nama')
    tipe_baru = request.form.get('tipe')
    saldo_baru = request.form.get('saldo')
    if not saldo_baru or saldo_baru.strip() == "":
        saldo_baru = "-"
    
    for akun in daftar_akun:
        if akun['kode'] == kode_lama:
            akun['kode'] = kode_baru
            akun['nama'] = nama_baru
            if not akun['sistem']:
                akun['induk'] = tipe_baru
            akun['saldo'] = saldo_baru
            break
            
    return redirect(url_for('menu_handler', menu_name="daftar-akun"))

@app.route('/hapus-akun')
def hapus_akun():
    kode = request.args.get('kode')
    global daftar_akun
    daftar_akun = [a for a in daftar_akun if not (a['kode'] == kode and a['sistem'])]
    return redirect(url_for('menu_handler', menu_name="daftar-akun"))

@app.route('/update-perusahaan', methods=['POST'])
def update_perusahaan():
    global profil_perusahaan
    profil_perusahaan['nama'] = request.form.get('nama')
    profil_perusahaan['alamat'] = request.form.get('alamat')
    profil_perusahaan['telepon'] = request.form.get('telepon')
    profil_perusahaan['periode'] = request.form.get('periode')
    return redirect(url_for('menu_handler', menu_name="data-perusahaan"))

if __name__ == '__main__':
    app.run(debug=True)
