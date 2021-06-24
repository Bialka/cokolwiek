import json
from os.path import dirname, isfile, isdir, join, realpath
import shutil
import subprocess
import unittest

import ogarniacz_mp3

_current_dir = realpath(dirname(__file__))
_test_data_dir = join(_current_dir, "TestData")
_tmp_test_data_dir = join(_current_dir, "TmpTestData")
downloaded_dir = join(_tmp_test_data_dir, "Pobrane")
processing_dir = join(_tmp_test_data_dir, "Do Obróbki")


class TestProcessingFiles(unittest.TestCase):

    def setUp(self) -> None:
        # create temporary data folder
        shutil.copytree(_test_data_dir, _tmp_test_data_dir, symlinks=True, ignore_dangling_symlinks=True)

    def tearDown(self) -> None:
        # delete temporary data folder
        shutil.rmtree(_tmp_test_data_dir, ignore_errors=True)

    @staticmethod
    def get_file_info(file_path):
        proc = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path],
                              stdout=subprocess.PIPE)

        return json.loads(proc.stdout.decode("utf-8"))['format']

    def test_unzipping(self):
        # run unzipping
        ogarniacz_mp3.downloaded_to_processing(downloaded_dir, processing_dir)
        # check for results - unpacked files
        flOw_dir = join(processing_dir, "flOw", "flOw")
        self.assertTrue(isdir(flOw_dir))
        self.assertTrue(isfile(join(flOw_dir, "01. Birth.mp3")))
        self.assertTrue(isfile(join(flOw_dir, "10. Gratitude.mp3")))
        self.assertTrue(isfile(join(flOw_dir, "Folder.jpg")))
        # check if zip file got deleted
        self.assertFalse(isfile(join(downloaded_dir, "flOw.zip")))

    def test_deleting_duplicates(self):  # TODO
        # run removing duplicates
        pass

    def test_converting_to_mp3(self):
        # run mp3 conversion
        ogarniacz_mp3.convert_to_mp3(processing_dir)
        file_path = join(processing_dir, "1917FYC/1917 (FYC)/02. Trench to Yorks")
        # make sure the original file was deleted
        self.assertFalse(isfile(file_path + ".flac"))
        # make sure mp3 file exists
        self.assertTrue(isfile(file_path + ".mp3"))
        # make sure it is a real mp3 file
        file_info = self.get_file_info(file_path + ".mp3")
        self.assertEqual(file_info["format_name"], "mp3")
        self.assertEqual(file_info["format_long_name"], "MP2/3 (MPEG audio layer 2/3)")
        # make sure file was converted to proper bitrate
        self.assertIn("bit_rate", file_info)
        self.assertLess(int(file_info["bit_rate"]), 130000)
        # make sure tags were copied during conversion
        self.assertIn("tags", file_info)
        self.assertEqual(file_info["tags"]["title"], "Trench to Yorks")
        self.assertEqual(file_info["tags"]["artist"], "Thomas Newman")
        self.assertEqual(file_info["tags"]["album"], "1917 (FYC)")
        self.assertEqual(file_info["tags"]["track"], "02/17")
        self.assertEqual(file_info["tags"]["album_artist"], "Thomas Newman")
