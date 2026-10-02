from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Status login sederhana
user_session = {"logged_in": False, "username": ""}

# Menyimpan data perusahaan sementara
profil_perusahaan = {
    "nama": "",
    "alamat": "",
    "telepon": "",
    "periode": "2026"
}

@app.route('/')
def index():
    if not user_session["logged_in"]:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Masuk - DagangKu</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 350px; }
                .login-card h2 { text-align: center; color: #1e293b; margin-bottom: 20px; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #334155; font-size: 14px; }
                .form-group input { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 4px; box-sizing: border-box; }
                .btn { width: 100%; background-color: #db2777; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 15px; }
                .btn:hover { background-color: #be185d; }
            </style>
        </head>
        <body>
            <div class="login-card">
                <h2>Masuk ke DagangKu</h2>
                <form method="POST" action="/login">
                    <div class="form-group">
                        <label>Nama Perusahaan / Akun:</label>
                        <input type="text" name="username" placeholder="Contoh: PT DagangKu Jaya" required>
                    </div>
                    <button type="submit" class="btn">Masuk</button>
                </form>
            </div>
        </body>
        </html>
        ''')
    else:
        return redirect(url_for('data_perusahaan'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if username:
        user_session["logged_in"] = True
        user_session["username"] = username
        profil_perusahaan["nama"] = username
    return redirect(url_for('data_perusahaan'))

@app.route('/logout')
def logout():
    user_session["logged_in"] = False
    user_session["username"] = ""
    return redirect(url_for('index'))

@app.route('/data-perusahaan')
def data_perusahaan():
    if not user_session["logged_in"]:
        return redirect(url_for('index'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Perusahaan - DagangKu</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; display: flex; }
            .sidebar { width: 250px; background-color: #1e293b; color: white; height: 100vh; position: fixed; padding-top: 20px; }
            .sidebar h2 { font-size: 18px; padding: 0 20px; margin-bottom: 20px; color: #38bdf8; }
            .sidebar a { display: block; color: #cbd5e1; padding: 12px 20px; text-decoration: none; font-size: 14px; }
            .sidebar a:hover, .sidebar a.active { background-color: #db2777; color: white; }
            .logout-btn { position: absolute; bottom: 20px; left: 20px; width: calc(100% - 40px); background-color: #475569; color: white; padding: 10px; text-align: center; border-radius: 4px; text-decoration: none; font-size: 14px; }
            .logout-btn:hover { background-color: #64748b; }
            .content { margin-left: 250px; padding: 30px; width: calc(100% - 250px); box-sizing: border-box; }
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
            <a href="/data-perusahaan" class="active">Data Perusahaan</a>
            <a href="#">Daftar Akun</a>
            <a href="#">Saldo Awal</a>
            <a href="#">Pelanggan</a>
            <a href="#">Pemasok</a>
            <a href="#">Barang</a>
            <a href="/logout" class="logout-btn">Keluar</a>
        </div>
        <div class="content">
            <h1>Data Perusahaan</h1>
            <div class="card">
                <form method="POST" action="/update-perusahaan">
                    <div class="form-group">
                        <label>Nama Perusahaan:</label>
                        <input type="text" name="nama" value="{{ profil.nama }}" placeholder="Contoh: PT DagangKu Jaya">
                    </div>
                    <div class="form-group">
                        <label>Alamat:</label>
                        <input type="text" name="alamat" value="{{ profil.alamat }}" placeholder="Contoh: Jl. Sudirman No. 123, Semarang">
                    </div>
                    <div class="form-group">
                        <label>Nomor Telepon:</label>
                        <input type="text" name="telepon" value="{{ profil.telepon }}" placeholder="Contoh: 081234567890">
                    </div>
                    <div class="form-group">
                        <label>Periode Akuntansi:</label>
                        <input type="text" name="periode" value="{{ profil.periode }}" placeholder="Contoh: 2026">
                    </div>
                    <button type="submit" class="btn">Simpan Perubahan</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    ''', profil=profil_perusahaan)

@app.route('/update-perusahaan', methods=['POST'])
def update_perusahaan():
    global profil_perusahaan
    profil_perusahaan['nama'] = request.form.get('nama')
    profil_perusahaan['alamat'] = request.form.get('alamat')
    profil_perusahaan['telepon'] = request.form.get('telepon')
    profil_perusahaan['periode'] = request.form.get('periode')
    return redirect(url_for('data_perusahaan'))

if __name__ == '__main__':
    app.run(debug=True)
