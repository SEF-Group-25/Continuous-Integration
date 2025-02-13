import subprocess
from src.log import log_command_result

def run_command(command, run_dir=""):
    """
    Run the command under specific directory, the result of run will be store in the log.
    If the command fails, it will raise a subprocess.CalledProcessError
    """

    result = subprocess.run(command, cwd=run_dir, shell=True, capture_output=True, text=True)

    log_command_result(command, result)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=command,
        )