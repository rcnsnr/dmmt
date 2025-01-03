# Disk Monitoring and System Maintenance Tool

This project is a comprehensive **disk monitoring and system maintenance tool** designed to track disk utilization, identify large files, manage log rotation, and detect zombie processes. It integrates seamlessly with Jenkins pipelines for scheduled checks and generates alerts via Microsoft Teams. The tool is designed to work across various environments, including:

- **Oracle Enterprise Linux**  
- **Oracle DB, MongoDB, Cassandra, Redis, Kafka**  
- **OpenShift clusters**  
- **Jenkins, Bitbucket, Jira, Confluence servers**  
- **Application servers running Java and other test environments**  

---

## Project Structure

```
/.
│
├── disk_check.py          # Main Python script for disk and process monitoring
├── Jenkinsfile            # Jenkins pipeline for automation
└── requirements.txt       # Python dependencies

```

## Features

### 1. Disk Usage Monitoring

- **Threshold-based Monitoring:**  
  - Monitors disk usage and sends alerts if a specified threshold is exceeded.  
  - Supports multiple mount points and paths.  
- **Large File Detection:**  
  - Scans for files exceeding a specified size and archives or deletes them.  
- **Log Rotation and Archiving:**  
  - Automatically compresses or deletes log files older than a specified number of days.  

### 2. File Type-Specific Actions

- **Log Files (`.log`):** Compress, delete, or rotate based on retention days.  
- **Backup Files (`.bak, .tar, .gz`):** Archive or delete after a certain period.  
- **Temporary Files (`.tmp, .swp`):** Immediate cleanup of temporary files.  
- **Database Dumps (`.sql, .db`):** Archive or move older dumps.  
- **Media Files (`.mp4, .mkv`):** Move or archive large media files.  
- **ISO Images (`.iso, .img`):** Archive or delete after a period.  

### 3. LVM and Filesystem Management

- **Filesystem Detection and Management:**  
  - Supports ext3, ext4, XFS, ZFS, and Btrfs filesystems.  
  - Automatically detects filesystem types and performs appropriate actions.  
- **LVM Monitoring and Auto-Expansion:**  
  - Detects logical volume usage and triggers `lvextend` when thresholds are exceeded.  

### 4. Zombie Process Detection and Cleanup

- **Zombie Process Detection:**  
  - Scans for zombie processes (`ps aux | grep 'Z'`) and identifies their parent processes (PPID).  
- **Parent Process Cleanup:**  
  - Automatically terminates parent processes (`kill -9`) to eliminate zombie processes.  
- **Threshold-Based Alerts:**  
  - Sends Teams notifications when the number of zombie processes exceeds a defined threshold.  

### 5. Jenkins Integration

- **Pipeline Integration:**  
  - Designed to run as part of Jenkins pipelines.  
  - Supports parameterized builds for flexible disk checks and process monitoring.  

---

### 6. Application and Filesystem-Specific Actions

- **Oracle DB (on ext4 or XFS):**

  - Cleans up Oracle database logs and archive files automatically.  
  - Detects database dump files and moves them to archival storage.  

- **MongoDB, Cassandra, Redis:**

  - Scans `/var/lib` directories for large `.wt` or `.sst` files.  
  - Performs automatic compaction or backup on large files.  

- **LVM Management:**

  - Expands logical volumes (`lvextend`) when disk usage reaches a certain threshold.  
  - Automatically detects volume groups and resizes them as needed.  

- **ZFS and XFS Filesystems:**

  - Detects and triggers snapshot-based cleanup or archival processes.  
  - Runs `xfs_growfs` or `zfs list` commands to manage disk health.  

---

## Technology Stack

- **Language:** Python 3.9+  
- **Dependencies:**  
  - `psutil` – Disk and process monitoring  
  - `requests` – Microsoft Teams integration  
  - `subprocess` – Command execution for disk and process management  
- **Tools:**  
  - Jenkins (for scheduled execution)  
  - Microsoft Teams (for alerting)  

---

## Installation

### Requirements

- Python 3.9+  
- Jenkins (optional for CI/CD integration)  
- Microsoft Teams Webhook URL for notifications  

### Setup

1. Clone the repository

2. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up Microsoft Teams Webhook URL in ```disk_check.py```:

```python
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/YOUR-WEBHOOK-URL"
```

### Usage

#### Run Manually

```bash
python3 disk_check.py --threshold 85 --log_retention_days 30 --scan_path /var/log --check_zombies true
```

##### Run via Jenkins Pipeline

```groovy
pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
    }

    parameters {
        string(name: 'THRESHOLD', defaultValue: '85', description: 'Disk usage threshold')
        string(name: 'LOG_RETENTION_DAYS', defaultValue: '30', description: 'Log retention period (days)')
        string(name: 'SCAN_PATH', defaultValue: '/', description: 'Directory to scan')
        booleanParam(name: 'CHECK_ZOMBIES', defaultValue: true, description: 'Enable zombie process detection')
    }

    stages {
        stage('Disk and Process Monitoring') {
            steps {
                sh """
                source venv/bin/activate
                python disk_check.py --threshold ${THRESHOLD} --log_retention_days ${LOG_RETENTION_DAYS} --scan_path ${SCAN_PATH} --check_zombies ${CHECK_ZOMBIES}
                """
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
```

### Customization

- Modify the file paths and threshold values in disk_check.py to match your environment.

- Adjust the Jenkins pipeline to fit specific server types (DB servers, app servers, etc.).

- Add exclusion lists for directories or files that should not be scanned.

### Roadmap

- [ ] Add Slack Integration as an alternative to Microsoft Teams.

- [ ] Implement Dynamic Configuration using YAML or JSON for server-specific settings.

- [ ] Multi-threaded Disk Scans for faster large-directory analysis.

- [ ] Dockerization for containerized deployment.
