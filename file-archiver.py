import os
from pwd import getpwuid
from os import stat, listdir
from os.path import isfile, join
import json
from stat import *
import pwd
import grp
import ast

class arch_extr:

    def __init__(self):
        self.pre_archive = {}


    def user_interface():
        while True:
            mode = input("Extract/Archive: (E/A)\n", "To Exit, please type 'Exit':")
            if mode == "A":
                path_to_file = input("Enter the path to a file:\n")
                pre_archiver(self, path_to_file)
            elif mode == "E":
                path_to_file = input("Enter the path to a archive:\n")
                extract(path_to_file)
                break
            else:
                return post_archiver(self)


    def pre_archiver(self, path_to_file):

        content = open(path_to_file, "rb").read()

        body = content

        name, ext = os.path.splitext(path_to_file)
        perm = os.stat(path_to_file)[ST_MODE]
        stat_info = os.stat(path_to_file)
        uid = pwd.getpwuid(stat_info.st_uid)[0]
        gid = grp.getgrgid(stat_info.st_gid)[0]
        size = os.stat(path_to_file).st_size 
        time = os.path.getmtime(path_to_file)

        header = [
            name,
            ext,
            perm,
            uid,
            gid,
            size,
            time
        ]

        str_header = "{}".format(header)
        str_body = "{}".format(content)
        self.pre_archive[str_header] = str_body
    
    def get_filepaths(self, directory):
  
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath) 
        return file_paths
        
    
    def dict_to_binary(self):
        str = json.dumps(self.pre_archive)
        binary = ' '.join(format(ord(letter), 'b') for letter in str)
        return binary
    
    def binary_to_dict(self, the_binary):
        jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
        dict = json.loads(jsn)  
        return dict


    def dir_pre_archiver(self, path_to_folder):
        list_with_paths = self.get_filepaths(path_to_folder)
        for path in list_with_paths:
            self.pre_archiver(path)

    
    def post_archiver(self):
        my_arch = open("the_best_archive_ever.myarch", "wb+")
        my_arch.write(self.dict_to_binary())
        my_arch.close()

    def archive(self, path_to_item):
        if path_to_item.endswith("/"):
            self.dir_pre_archiver(path_to_item)
        else:
            self.pre_archiver(path_to_item)


    def extractor(self, path_to_archiver=None):
        if path_to_archiver is None:
            path_to_fol = os.path.dirname(os.path.abspath(__file__))
            path_to_archiver = path_to_fol + "/the_best_archive_ever.myarch"

    
        content_arch = open(path_to_archiver, "rb").read()
        fin_dict = self.binary_to_dict(content_arch)

        for header, body in fin_dict.iteritems():
            l = ast.literal_eval(header)
            path_to_fol = os.path.dirname(os.path.abspath(__file__))
            
            pre_path = l[0]
            post_path = l[0]
            rev_path = pre_path[::-1]
            res = ""
            for item in rev_path:
                str_item = str(item)
            
                if str_item == "/":
                    break
                res += str_item

            file_name = res[::-1]
            file_ext = l[1]

            dir_creation = pre_path[:(len(post_path)-len(file_name))]
            path_to_extraction = path_to_fol + dir_creation

            if not os.path.exists(path_to_extraction):
                os.makedirs(path_to_extraction)
            
            path_file_creation = path_to_extraction + file_name + file_ext

            create_file = open(path_file_creation, "w+")
            create_file.write(body)
            create_file.close()
            perm = int(l[2])
            uid = pwd.getpwnam(l[3])[2]
            gid = pwd.getpwnam(l[4])[3]
            os.chown(path_file_creation, uid, gid)
            os.chmod(path_file_creation, perm)


archiver = arch_extr()
archiver.archive("/home/osboxes/Desktop/Test_prog/")
archiver.post_archiver()
archiver.extractor()