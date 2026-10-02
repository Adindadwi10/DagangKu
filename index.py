from flask import Flask, request, render_template_string

app = Flask(__name__)

# Menyimpan data perusahaan sementara (bisa dikembangkan dengan database nantinya)
profil_perusahaan = {
    "nama": "DagangKu",
    "alamat": "Semarang, Jawa Tengah",
    "telepon": "081234567890",
    "periode": "2026"
}

@app.route('/')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulasi Akuntansi - DagangKu</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; display: flex; }
            .sidebar { width: 250px; background-color: #1e293b; color: white; height: 100vh; position: fixed; padding-top: 20px; }
            .sidebar h2 { font-size: 18px; padding: 0 20px; margin-bottom: 20px; color: #38bdf8; }
            .sidebar a { display: block; color: #cbd5e1; padding: 12px 20px; text-decoration: none; font-size: 14px; }
            .sidebar a:hover, .sidebar a.active { background-color: #db2777; color: white; }
            .content { margin-left: 250px; padding: 30px; width: calc(100% - 250px); }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #334155; }
            .form-group input { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 4px; box-sizing: border-box; }
            .btn { background-color: #db2777; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background-color: #be185d; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Simulasi Akuntansi</h2>
            <a href="/">Dashboard</a>
            <a href="/data-perusahaan" class="active">Data Perusahaan</a>
            <a href="#">Daftar Akun</a>
            <a href="#">Saldo Awal</a>
            <a href="#">Pelanggan</a>
            <a href="#">Pemasok</a>
            <a href="#">Barang</a>
        </div>
        <div class="content">
            <h1>Data Perusahaan</h1>
            <div class="card">
                <form method="POST" action="/update-perusahaan">
                    <div class="form-group">
                        <label>Nama Perusahaan:</label>
                        <input type="text" name="nama" value="{{ profil.nama }}">
                    </div>
                    <div class="form-group">
                        <label>Alamat:</label>
                        <input type="text" name="alamat" value="{{ profil.alamat }}">
                    </div>
                    <div class="form-group">
                        <label>Nomor Telepon:</label>
                        <input type="text" name="telepon" value="{{ profil.telepon }}">
                    </div>
                    <div class="form-group">
                        <label>Periode Akuntansi:</label>
                        <input type="text" name="periode" value="{{ profil.periode }}">
                    </div>
                    <button type="submit" class="btn">Simpan Perubahan</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    ''', profil=profil_perusahaan)

@app.route('/data-perusahaan')
def data_perusahaan():
    return dashboard()

@app.route('/update-perusahaan', methods=['POST'])
def update_perusahaan():
    global profil_perusahaan
    profil_perusahaan['nama'] = request.form.get('nama')
    profil_perusahaan['alamat'] = request.form.get('alamat')
    profil_perusahaan['telepon'] = request.form.get('telepon')
    profil_perusahaan['periode'] = request.form.get('periode')
    return dashboard()

if __name__ == '__main__':
    app.run(debug=True)
