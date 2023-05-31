log_file_path = "./smtp_debug.log"
# 1. Cetak pesan EHLO
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("send:") and "ehlo" in line:
            result = line.split("send:")[1].strip()
            print(result.encode().decode("utf-8"))
            break

# 2. Cetak pesan bahwa server mendukung TLS
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("reply:") and "250-STARTTLS" in line:
            result = line.split("reply:")[1].strip()
            print(result.encode().decode("utf-8").strip("b"))
            break

# 3. Cetak pesan bahwa server siap mengirim email
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("reply:") and "retcode (220)" in line:
            result = line.split("reply:")[1].strip()
            print(result.encode().decode("utf-8"))
            break

# 4. Cetak pesan yang menunjukkan username yang sudah di-hash
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("send:") and "AUTH LOGIN" in line:
            result = line.split("send:")[1].strip()
            print(result.encode().decode("utf-8"))
            break

# 5. Cetak pesan balasan server dari sebuah hello message dari client
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("reply:") and "Hello" in line:
            result = line.split("reply:")[1].strip()
            print(result.encode().decode("utf-8").strip("b"))
            break

# 6. Cetak pesan bahwa koneksi telah ditutup
with open(log_file_path, "r") as file:
    for line in file:
        if line.startswith("reply:") and "221" in line:
            result = line.split("reply:")[1].strip()
            print(result.encode().decode("utf-8").strip("b"))
            break

# 7. Tunjukkan email yang diterima di Gmail
import imaplib,os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(BASE_DIR, 'smtp.conf')) as config_file:
    config = dict(line.strip().split('=') for line in config_file)

FROMADDR = config['fromaddr']
PASS = config['pass']

TOADDR = config['toaddr']
TOADDRPASS = config['toaddrpass']

# Login ke akun Gmail
imap_server = 'imap.gmail.com'
imap_port = 993
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(TOADDR, TOADDRPASS)

# Cari email yang dikirim dari Outlook
mail.select('INBOX')
status, data = mail.search(None, 'FROM', FROMADDR)
email_ids = data[0].split()

if email_ids:
    # Ambil ID email terbaru
    latest_email_id = email_ids[-1]

    # Dapatkan isi email
    status, email_data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = email_data[0][1]

    # Decode isi email
    raw_email_string = raw_email.decode('utf-8')

    # Tampilkan isi email
    print(raw_email_string)
else:
    print("Tidak ada email dari Outlook yang ditemukan di Gmail.")

# Tutup koneksi ke akun Gmail
mail.logout()