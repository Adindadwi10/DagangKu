from flask import Flask, jsonify, request

app = Flask(__name__)

# Database sementara untuk menyimpan akun pendaftaran
database_pengguna = []

# 1. Halaman utama (langsung menampilkan form tanpa file HTML terpisah)
@app.route('/')
def beranda():
    return """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>DagangKu - Akuntansi</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px; display: flex; justify-content: center;">
        <div style="background: white; width: 100%; max-width: 400px; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            
            <!-- FORM MASUK -->
            <div id="sectionMasuk">
                <h2>Masuk</h2>
                <form id="formMasuk">
                    <div style="margin-bottom: 15px;">
                        <label>Email *</label><br>
                        <input type="email" id="masukEmail" required style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label>Password *</label><br>
                        <input type="password" id="masukPassword" required style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 10px; cursor: pointer;">Masuk</button>
                </form>
                <p style="margin-top: 15px;">Belum punya akun? <span id="linkDaftar" style="color: blue; cursor: pointer; text-decoration: underline;">Daftar di sini</span></p>
            </div>

            <!-- FORM DAFTAR -->
            <div id="sectionDaftar" style="display: none;">
                <h2>Daftar Akun Baru</h2>
                <form id="formDaftar">
                    <div style="margin-bottom: 12px;">
                        <label>Nama lengkap *</label><br>
                        <input type="text" id="namaLengkap" required style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label>Email *</label><br>
                        <input type="email" id="daftarEmail" required style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label>Password *</label><br>
                        <input type="password" id="daftarPassword" required style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label>Nama perusahaan *</label><br>
                        <input type="text" id="namaPerusahaan" required value="PT Dagang" style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label>Tanggal saldo awal *</label><br>
                        <input type="date" id="tanggalSaldo" required value="2026-01-01" style="width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 10px; cursor: pointer;">Daftar & buat perusahaan</button>
                </form>
                <p style="margin-top: 15px;">Sudah punya akun? <span id="linkMasuk" style="color: blue; cursor: pointer; text-decoration: underline;">Masuk</span></p>
            </div>

            <p id="statusPesan" style="font-weight: bold; margin-top: 15px; text-align: center;"></p>
        </div>

        <script>
            const sMasuk = document.getElementById('sectionMasuk');
            const sDaftar = document.getElementById('sectionDaftar');
            const status = document.getElementById('statusPesan');

            document.getElementById('linkDaftar').onclick = () => {
                sMasuk.style.display = 'none';
                sDaftar.style.display = 'block';
                status.innerText = '';
            };

            document.getElementById('linkMasuk').onclick = () => {
                sDaftar.style.display = 'none';
                sMasuk.style.display = 'block';
                status.innerText = '';
            };

            // Kirim data pendaftaran
            document.getElementById('formDaftar').onsubmit = (e) => {
                e.preventDefault();
                const dataBaru = {
                    namaLengkap: document.getElementById('namaLengkap').value,
                    email: document.getElementById('daftarEmail').value,
                    password: document.getElementById('daftarPassword').value,
                    namaPerusahaan: document.getElementById('namaPerusahaan').value,
                    tanggalSaldo: document.getElementById('tanggalSaldo').value
                };

                fetch('/api/daftar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dataBaru)
                })
                .then(res => res.json())
                .then(resData => {
                    status.innerText = resData.pesan;
                    status.style.color = "green";
                    if(resData.sukses) {
                        setTimeout(() => {
                            sDaftar.style.display = 'none';
                            sMasuk.style.display = 'block';
                            status.innerText = '';
                        }, 2000);
                    }
                });
            };

            // Kirim data login
            document.getElementById('formMasuk').onsubmit = (e) => {
                e.preventDefault();
                const dataLogin = {
                    email: document.getElementById('masukEmail').value,
                    password: document.getElementById('masukPassword').value
                };

                fetch('/api/masuk', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dataLogin)
                })
                .then(res => res.json())
                .then(resData => {
                    status.innerText = resData.pesan;
                    status.style.color = resData.sukses ? "green" : "red";
                });
            };
        </script>
    </body>
    </html>
    """

# 2. Endpoint API Pendaftaran
@app.route('/api/daftar', methods=['POST'])
def daftar():
    data = request.json
    database_pengguna.append(data)
    return jsonify({
        "sukses": True,
        "pesan": f"Berhasil mendaftarkan perusahaan {data.get('namaPerusahaan')}! Silakan Masuk."
    })

# 3. Endpoint API Masuk (Login)
@app.route('/api/masuk', methods=['POST'])
def masuk():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = next((u for u in database_pengguna if u['email'] == email and u['password'] == password), None)
    
    if user:
        return jsonify({
            "sukses": True,
            "pesan": f"Berhasil masuk ke perusahaan: {user['namaPerusahaan']}!"
        })
    else:
        return jsonify({
            "sukses": False,
            "pesan": "Email atau password salah, atau akun belum terdaftar."
        })

if __name__ == '__main__':
    app.run(debug=True)