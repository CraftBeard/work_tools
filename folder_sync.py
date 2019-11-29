#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:09:28 2019

@author: Alex
"""

import os
from distutils import dir_util
from datetime import datetime
import glob

# directory paths
path_1 = r""
path_2 = r""

# confirmation
print("Do you want to synchronize")
print("Path 1: " + path_1)
print("Path 2: " + path_2)
confirmation = input("(Y/N): ")

if confirmation != "Y":
	print("Quiting...")
	quit()

print("Synchronizing...")

# compare modified datetimes of folders
modified_1 = glob.glob(path_1 + r"\**", recursive=True)
list_1_file = max(modified_1, key=os.path.getmtime)
modified_2 = glob.glob(path_2 + r"\**", recursive=True)
list_2_file = max(modified_2, key=os.path.getmtime)

modified_time_1 = os.path.getmtime(list_1_file)
print("Path 1: " + list_1_file)
print("Path 1 Modified Time: " + datetime.fromtimestamp(modified_time_1).strftime("%Y.%m.%d %H:%M:%S"))

modified_time_2 = os.path.getmtime(list_2_file)
print("Path 2: " + list_2_file)
print("Path 2 Modified Time: " + datetime.fromtimestamp(modified_time_2).strftime("%Y.%m.%d %H:%M:%S"))

list_1 = os.listdir(path_1)
list_2 = os.listdir(path_2)

src_path = ""
dest_path = ""

if len(list_1) and len(list_1):
	if modified_time_1 < modified_time_2:
		src_path, dest_path = path_2, path_1
	elif modified_time_2 < modified_time_1:
		src_path, dest_path = path_1, path_2
elif len(list_1):
	src_path, dest_path = path_1, path_2
elif len(list_2):
	src_path, dest_path = path_2, path_1

# overwrite old folder with new one
if src_path != "":
	print("Copying...")
	print("From : " + src_path)
	print("To : " + dest_path)
	dir_util.copy_tree(src_path, dest_path)
