#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:09:28 2019

@author: Alex
"""

import os
from distutils import dir_util

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
modified_time_1 = os.path.getmtime(path_1)
modified_time_2 = os.path.getmtime(path_2)

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
	dir_util.copy_tree(src_path, dest_path)
