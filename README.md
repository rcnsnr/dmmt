# Disk Monitoring and System Maintenance Tool

This project is a comprehensive **disk usage and process monitoring tool** designed to track disk utilization, identify large files, manage log rotation, and detect zombie processes. It integrates seamlessly with Jenkins pipelines for scheduled checks and generates alerts via Microsoft Teams. The tool is designed to work across various environments, including:

- **Oracle Enterprise Linux**  
- **Oracle DB, MongoDB, Cassandra, Redis, Kafka**  
- **OpenShift clusters**  
- **Jenkins, Bitbucket, Jira, Confluence servers**  
- **Application servers running Java and other test environments**  

---

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

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/disk-monitoring-tool.git
   cd disk-monitoring-tool
