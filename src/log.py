from datetime import datetime

logs = []

def log_command_result(command, result):
    """log the result from the executed command"""

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "return_code": result.returncode,
        "stdout": result.stdout.strip().split("\n") if result.stdout else [],
        "stderr": result.stderr.strip().split("\n") if result.stderr else []
    }

    logs.append(log_entry)

def get_logs():
    return logs