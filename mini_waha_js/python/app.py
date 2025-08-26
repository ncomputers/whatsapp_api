import os
import shutil
import subprocess
import time
from pathlib import Path

import requests
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
NODE_DIR = ROOT / 'node'


def ensure_node():
  if not shutil.which('node') or not shutil.which('npm'):
    raise SystemExit('Node.js and npm are required')
  if not (NODE_DIR / 'node_modules').exists():
    subprocess.run(['npm', 'ci'], cwd=NODE_DIR, check=True)


def load_env():
  env_path = NODE_DIR / '.env'
  if not env_path.exists():
    env_path = NODE_DIR / '.env.example'
  return dotenv_values(env_path)


def wait_for_server(port):
  url = f'http://localhost:{port}/status'
  for _ in range(30):
    try:
      r = requests.get(url, timeout=1)
      if r.status_code == 200:
        return True
    except requests.RequestException:
      pass
    time.sleep(1)
  return False


def main():
  ensure_node()
  env = load_env()
  port = env.get('PORT', '8000')
  proc = subprocess.Popen(['npm', 'run', 'dev'], cwd=NODE_DIR)
  print(f'Starting server on http://localhost:{port}')
  try:
    if wait_for_server(port):
      print('Server is up. Ctrl+C to stop.')
    proc.wait()
  except KeyboardInterrupt:
    proc.terminate()
    proc.wait()


if __name__ == '__main__':
  main()
