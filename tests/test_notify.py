from src.notify import *

#def test_read_tokens():
 #   tokens = read_tokens()
  #  assert len(tokens) == 2

def test_valid_commit_status():
    result = set_commit_status("ac707d7ae01c1dfb631380e68b5d730a5990f7fc", "success", "PyTest")
    assert result == 201


def test_invalid_commit_status():
    result = set_commit_status("INVALID:)", "success", "PyTest")
    assert result != 201


def test_valid_discord(capsys):
    discord_notify("ac707d7ae01c1dfb631380e68b5d730a5990f7fc", "Valid Test")
    captured = capsys.readouterr()
    assert captured.out == "Message sent successfully!\n"


def test_invalid_discord(capsys):
    discord_notify("ac707d7ae01c1dfb631380e68b5d730a5990f7fc", "Invalid", "invalid_webhook")
    captured = capsys.readouterr()
    assert captured.out != "Message sent successfully!\n"
