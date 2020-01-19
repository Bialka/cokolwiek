import unittest

import os

import shutil

class TestStringMethods(unittest.TestCase):
    file_name = "cokolwiek.txt"
    to_do_path = "do_zrobienia"
    destination_path = "zrobione"
    backup_path = "backup"
    def setUp(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        shutil.rmtree(self.destination_path, ignore_errors=True)
        os.mkdir(self.destination_path)
        shutil.rmtree(self.to_do_path, ignore_errors=True)
        shutil.copytree(self.backup_path, self.to_do_path)


    def test_upper(self):
        pass


if __name__=="__main__":
    unittest.main()