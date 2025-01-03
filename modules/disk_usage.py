import psutil
import os
from modules.alerting import send_teams_alert, send_email_alert
from modules.elk_logger import send_log_to_elk

def check_disk_usage(threshold, path='/'):
    """
    Belirtilen path üzerinde disk kullanımını kontrol eder.
    Eşik aşılırsa uyarı gönderir ve ELK'ya loglar.
    """
    usage = psutil.disk_usage(path)
    percent_used = usage.percent

    log_data = {
        "path": path,
        "disk_usage_percent": percent_used
    }

    if percent_used >= threshold:
        message = f"⚠️ UYARI! {path} üzerindeki disk kullanımı %{percent_used} seviyesinde!"
        send_teams_alert(message)
        send_email_alert("Disk Kullanım Uyarısı", message)
        log_data["status"] = "ALERT"
    else:
        log_data["status"] = "OK"
    
    # Logları ELK'ya gönder
    send_log_to_elk(log_data)
