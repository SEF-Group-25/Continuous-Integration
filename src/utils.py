import subprocess

def run_command(command, run_dir=""):
    result = subprocess.run(command, cwd=run_dir, shell=True, capture_output=True, text=True)

    # print(f"Output:\n{result.stdout}")
    # print(f"Error:\n{result.stderr}")

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=command,
            output=result.stdout,
            stderr=result.stderr
        )

    return result