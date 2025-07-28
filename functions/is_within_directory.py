import os

def is_within_directory(base_dir, user_path):
    base_dir = os.path.abspath(base_dir)
    target_path = os.path.abspath(os.path.join(base_dir, user_path))
    return os.path.commonpath([base_dir]) == os.path.commonpath([base_dir, target_path])