from modules.disk_usage import check_disk_usage
from modules.process_monitor import check_zombie_processes
from modules.alerting import send_teams_alert
from modules.system_detection import detect_application
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def main():
    threshold = 85
    scan_path = '/var/log'
    app_type = detect_application()

    if app_type == "Oracle DB":
        send_teams_alert("Oracle DB tespit edildi. Özel temizlik başlatılıyor...")
        check_disk_usage(threshold, "/u01/app/oracle/diag")

    check_disk_usage(threshold, scan_path)
    check_zombie_processes()

if __name__ == "__main__":
    main()
