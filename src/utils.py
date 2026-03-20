import os
import shutil


def copy_folder(source, destination):
    shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    contents = os.listdir(source)
    for content in contents:
        path = os.path.join(source, content)
        path_to = os.path.join(destination, content)
        if os.path.isfile(path):
            shutil.copy(path, path_to)
        else:
            copy_folder(path, path_to)
