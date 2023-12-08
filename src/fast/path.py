import os
import shutil
import sys

def clear_directory(path):
    """
    清空指定目录下的所有文件和子目录。
    """
    if not os.path.exists(path):
        sys.exit("要清空的目录不存在")

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
