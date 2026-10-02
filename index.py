from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

user_session = {"logged_in": False, "username": "", "page": "login"}
profil_perusahaan = {
    "nama": "PT Dagang Simulasi",
    "alamat": "",
    "telepon": "",
    "periode": "01/01/2026"
}

@app.route('/')
def index():
    if not user_session["logged_in"]:
        page = request.args.get('page', 'login')
        
        if page == 'register':
            return render_template_string('''
            <h2>Daftar Akun Baru</h2>
            <form method="POST" action="/auth-submit">
                <input type="hidden" name="mode" value="register">
                <p>Nama lengkap:<br><input type="text" name="nama_lengkap" required></p>
                <p>Email:<br><input type="email" name="email" required></p>
                <p>Password:<br><input type="password" name="password" required></p>
                <p>Nama perusahaan:<br><input type="text" name="nama_perusahaan" value="PT Dagang Simulasi" required></p>
                <p>Tanggal saldo awal:<br><input type="text" name="tanggal" value="01/01/2026"></p>
                <button type="submit">Daftar & buat perusahaan</button>
            </form>
            <p>Sudah punya akun? <a href="/?page=login">Masuk</a></p>
            ''')
        else:
            return render_template_string('''
            <h2>Masuk</h2>
            <form method="POST" action="/auth-submit">
                <input type="hidden" name="mode" value="login">
                <p>Email:<br><input type="email" name="email" required></p>
                <p>Password:<br><input type="password" name="password" required></p>
                <button type="submit">Masuk</button>
            </form>
            <p>Belum punya akun? <a href="/?page=register">Daftar di sini</a></p>
            ''')
    else:
        return redirect(url_for('data_perusahaan'))

@app.route('/auth-submit', methods=['POST'])
def auth_submit():
    mode = request.form.get('mode')
    email = request.form.get('email')
    
    user_session["logged_in"] = True
    user_session["username"] = email
    
    if mode == 'register':
        nama_pt = request.form.get('nama_perusahaan')
        tanggal = request.form.get('tanggal')
        if nama_pt:
            profil_perusahaan["nama"] = nama_pt
        if tanggal:
            profil_perusahaan["periode"] = tanggal
            
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
    <h2>Data Perusahaan</h2>
    <hr>
    <ul>
        <li><b>Menu:</b> Data Perusahaan</li>
        <li><a href="/logout">Keluar</a></li>
    </ul>
    <hr>
    <form method="POST" action="/update-perusahaan">
        <p>Nama Perusahaan:<br><input type="text" name="nama" value="{{ profil.nama }}"></p>
        <p>Alamat:<br><input type="text" name="alamat" value="{{ profil.alamat }}"></p>
        <p>Nomor Telepon:<br><input type="text" name="telepon" value="{{ profil.telepon }}"></p>
        <p>Periode Akuntansi:<br><input type="text" name="periode" value="{{ profil.periode }}"></p>
        <button type="submit">Simpan Perubahan</button>
    </form>
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
