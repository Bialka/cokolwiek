import unittest

import os

import shutil

class TestStringMethods(unittest.TestCase):
    file_name1 = "cokolwiek.txt"
    file_name2 = "dane_plikow.txt"
    to_do_path = "do_zrobienia"
    destination_path = "zrobione"
    backup_path = "backup"
    def setUp(self):
        if os.path.exists(self.file_name1):
            os.remove(self.file_name1)
        if os.path.exists(self.file_name2):
            os.remove(self.file_name2)
        shutil.rmtree(self.destination_path, ignore_errors=True)
        os.mkdir(self.destination_path)
        shutil.rmtree(self.to_do_path, ignore_errors=True)
        shutil.copytree(self.backup_path, self.to_do_path)


    def test_upper(self):
        pass


if __name__=="__main__":
    unittest.main()