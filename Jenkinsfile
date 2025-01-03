pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
    }

    parameters {
        string(name: 'THRESHOLD', defaultValue: '85', description: 'Disk kullanım eşiği (%)')
        string(name: 'LOG_RETENTION_DAYS', defaultValue: '30', description: 'Log saklama süresi (gün)')
        string(name: 'SCAN_PATH', defaultValue: '/', description: 'Taranacak dizin')
        string(name: 'FILE_SIZE', defaultValue: '500', description: 'Büyük dosya tespiti (MB)')
        booleanParam(name: 'CHECK_ZOMBIES', defaultValue: true, description: 'Zombie process kontrolü')
        string(name: 'EMAIL_ADDRESS', defaultValue: 'your-email@example.com', description: 'Bildirim için e-posta adresi')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Monitoring Script') {
            steps {
                sh """
                source venv/bin/activate
                python disk_check.py \
                    --threshold ${THRESHOLD} \
                    --log_retention_days ${LOG_RETENTION_DAYS} \
                    --scan_path ${SCAN_PATH} \
                    --file_size ${FILE_SIZE} \
                    --check_zombies ${CHECK_ZOMBIES} \
                    --email_address ${EMAIL_ADDRESS}
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
