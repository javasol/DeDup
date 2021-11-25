import filecmp
import os
import magic
from DupFile import DupFile


class FileService:

    @staticmethod
    def get_list_of_potential_duplicate_files(root="."):
        potential_dup_files = []
        for path, subdirs, files in os.walk(root):
            for name in files:
                full_file_name = os.path.join(path, name)
                potential_dup_files.append(
                    DupFile(full_file_name, os.path.getsize(full_file_name)))
        return potential_dup_files

    @staticmethod
    def get_dict_of_all_files_by_size(potential_dup_files={}):
        all_files = {}
        for dup_file in potential_dup_files:
            all_files.setdefault(dup_file.size, []).append(dup_file)
        return all_files

    @staticmethod
    def get_file_type(file):
        return magic.from_file(file)

    @staticmethod
    def are_files_equal(file1, file2):
        if FileService.get_file_type(file1.name) != FileService.get_file_type(file2.name):
            return False
        return filecmp.cmp(file1.name, file2.name)

    @staticmethod
    def get_duplicates_in_list(list_of_files):
        duplicates = []
        for index, item in enumerate(list_of_files):
            for item2 in list_of_files[index:]:
                if FileService.are_files_equal(item, item2):
                    duplicates.append(item)
                    break
        return duplicates

    @staticmethod
    def delete_file(file):
        os.remove(file)
