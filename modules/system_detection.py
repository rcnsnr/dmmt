import subprocess
import os

def detect_filesystem(path='/'):
    result = subprocess.run(f"df -T {path} | awk 'NR==2 {{print $2}}'", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def detect_application():
    if os.path.exists("/u01/app/oracle"):
        return "Oracle DB"
    elif os.path.exists("/var/lib/mongo"):
        return "MongoDB"
    elif os.path.exists("/var/lib/cassandra"):
        return "Cassandra DB"
    elif os.path.exists("/var/lib/redis"):
        return "Redis"
    return "General"

def cleanup_mongo_logs():
    """
    MongoDB için büyük log dosyalarını temizler.
    """
    mongo_log_path = "/var/lib/mongo/"
    cmd = f"find {mongo_log_path} -type f -name '*.log' -mtime +30 -exec rm -f {{}} \\;"
    os.system(cmd)

def cleanup_redis_logs():
    """
    Redis için eski log dosyalarını temizler.
    """
    redis_log_path = "/var/log/redis/"
    cmd = f"find {redis_log_path} -type f -name '*.log' -mtime +30 -exec rm -f {{}} \\;"
    os.system(cmd)