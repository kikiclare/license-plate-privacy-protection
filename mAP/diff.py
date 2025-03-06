#coding=utf8

import os


def compare_folder(dir1, dir2):
    files1 = os.listdir(dir1)
    files2 = os.listdir(dir2)
    files1.sort()
    files2.sort()

    for f in files1:
        if f not in files2:
            # file_path = dir2 + f
            file_path = os.path.join(dir2, f)
            file = open(file_path, 'w')
            file.close()
            print("已创建文件：" + file_path)

    for f in files2:
        if f not in files1:
            file_path = os.path.join(dir1, f)
            file = open(file_path, 'w')
            file.close()
            print("已创建文件：" + file_path)


def diff(dir1, dir2):   
    compare_folder(dir1, dir2)
