import subprocess
from src.log import log_command_result

def run_command(command, run_dir=""):
    """Run the command under specific directory, the result of run will be logged. 
    Raise a subprocess.CalledProcessError if the command fails.

        Args:
            command (str): The command to be executed.
            run_dir (str): The directory location where the command is executed
    """

    result = subprocess.run(command, cwd=run_dir, shell=True, capture_output=True, text=True)

    log_command_result(command, result)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=command,
        )