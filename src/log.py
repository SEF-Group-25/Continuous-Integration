from datetime import datetime

logs = []

def log_command_result(command, result):
    """Log the result of the executed command, stored in a list
    
        Args:
            command (str): The executed command
            result (CompletedProcess[str]): Return value of subprocess.run
    """

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "return_code": result.returncode,
        "stdout": result.stdout.strip().split("\n") if result.stdout else [],
        "stderr": result.stderr.strip().split("\n") if result.stderr else []
    }

    logs.append(log_entry)

def get_logs():
    """Get the list of logs
    """
    return logs