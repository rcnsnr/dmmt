import subprocess

def check_zombie_processes():
    result = subprocess.run(['ps', '-eo', 'pid,ppid,stat,cmd'], capture_output=True, text=True)
    zombies = [line for line in result.stdout.splitlines() if 'Z' in line.split()[2]]
    return zombies
