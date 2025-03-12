import os

def read_env(env_name):
    value = os.environ.get(env_name)
    if value:
        return value
    else:
        print(f"Environment variable '{env_name}' not set or invalid.")
        exit()

def read_secret(env_file_path):
    secret_file = os.environ.get(env_file_path)
    if not secret_file:
        print(f"Environment variable '{env_file_path}' not set or invalid.")
        exit()
    if not os.path.exists(secret_file):
        print(f"Secret file '{secret_file}' doesn't exist.")
        exit()    
    with open(secret_file, 'r') as f:
        secret_content = f.read().strip()
    return secret_content