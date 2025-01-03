import os
import psutil
import subprocess
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse
from datetime import datetime

# Microsoft Teams Webhook URL'si (Kendi URL'inizi ekleyin)
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/YOUR-WEBHOOK-URL"

# SMTP Sunucu Yapılandırması (E-posta göndermek için gerekli)
SMTP_SERVER = "smtp.example.com"        # SMTP sunucusunun adresi
SMTP_PORT = 587                         # SMTP sunucu portu (TLS için genellikle 587 kullanılır)
EMAIL_ADDRESS = "your-email@example.com"  # E-posta adresiniz
EMAIL_PASSWORD = "your-email-password"    # E-posta şifreniz


def check_disk_usage(threshold, path='/'):
    """ Disk kullanımını kontrol eder ve eşik aşılırsa uyarı gönderir """
    usage = psutil.disk_usage(path)
    percent_used = usage.percent

    if percent_used >= threshold:
        message = f"⚠️ UYARI! {path} üzerindeki disk kullanımı %{percent_used} seviyesinde!"
        send_teams_alert(message)  # Microsoft Teams'e uyarı gönder
        send_email_alert("Disk Kullanım Uyarısı", message)  # E-posta gönder

    print(f"Disk kullanımı: {percent_used}%")


def find_large_files(path, size):
    """ Belirtilen boyutun üzerindeki büyük dosyaları bulur ve uyarı gönderir """
    cmd = f"find {path} -type f -size +{size}M"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        for file in result.stdout.splitlines():
            print(f"Büyük dosya tespit edildi: {file}")
            send_teams_alert(f"Büyük dosya tespit edildi: {file}")
            send_email_alert("Büyük Dosya Uyarısı", f"Büyük dosya tespit edildi: {file}")


def cleanup_logs(path, retention_days):
    """ Eski log dosyalarını temizler ve uyarı gönderir """
    cmd = f"find {path} -type f -name '*.log' -mtime +{retention_days}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        for file in result.stdout.splitlines():
            os.remove(file)  # Log dosyasını sil
            print(f"Silinen eski log: {file}")
            send_teams_alert(f"Silinen eski log: {file}")
            send_email_alert("Log Temizleme Bildirimi", f"Silinen eski log: {file}")


def check_zombie_processes():
    """ Zombie process'leri kontrol eder ve tespit ederse uyarı gönderir """
    result = subprocess.run(['ps', '-eo', 'pid,ppid,stat,cmd'], capture_output=True, text=True)
    zombies = [line for line in result.stdout.splitlines() if 'Z' in line.split()[2]]

    if zombies:
        print(f"{len(zombies)} zombie process tespit edildi.")
        for z in zombies:
            print(z)
        send_teams_alert(f"⚠️ {len(zombies)} zombie process tespit edildi!")
        send_email_alert("Zombie Process Uyarısı", f"{len(zombies)} zombie process tespit edildi!")
    else:
        print("Zombie process bulunamadı.")


def kill_zombie_parent():
    """ Tespit edilen zombie process'lerin parent'larını sonlandırır """
    result = subprocess.run(['ps', '-eo', 'ppid,stat'], capture_output=True, text=True)
    zombie_parents = {line.split()[0] for line in result.stdout.splitlines() if 'Z' in line}

    for parent in zombie_parents:
        try:
            subprocess.run(['kill', '-9', parent])  # Zombie parent'ı sonlandır
            print(f"Parent process sonlandırıldı: {parent}")
            send_teams_alert(f"Zombie parent process {parent} sonlandırıldı.")
            send_email_alert("Zombie Parent Sonlandırıldı", f"Zombie parent process {parent} sonlandırıldı.")
        except Exception as e:
            send_teams_alert(f"Parent process {parent} sonlandırılamadı: {str(e)}")
            send_email_alert("Sonlandırma Başarısız", f"Parent process {parent} sonlandırılamadı: {str(e)}")


def send_teams_alert(message):
    """ Microsoft Teams'e uyarı gönderir """
    payload = {"text": message}
    requests.post(TEAMS_WEBHOOK_URL, json=payload)
    print(f"Teams uyarısı gönderildi: {message}")


def send_email_alert(subject, body):
    """ SMTP kullanarak e-posta gönderir """
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()

        print(f"E-posta uyarısı gönderildi: {subject}")
    except Exception as e:
        print(f"E-posta gönderimi başarısız: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Disk ve Process İzleme Aracı")
    parser.add_argument('--threshold', type=int, required=True, help='Disk kullanım eşiği (%)')
    parser.add_argument('--log_retention_days', type=int, required=True, help='Log dosyası saklama süresi (gün)')
    parser.add_argument('--scan_path', type=str, default='/', help='Taranacak dizin')
    parser.add_argument('--file_size', type=int, default=500, help='Büyük dosya tespiti için eşik (MB)')
    parser.add_argument('--check_zombies', type=bool, default=False, help='Zombie process kontrolü yap')

    args = parser.parse_args()

    check_disk_usage(args.threshold, args.scan_path)
    find_large_files(args.scan_path, args.file_size)
    cleanup_logs(args.scan_path, args.log_retention_days)

    if args.check_zombies:
        check_zombie_processes()
        kill_zombie_parent()
