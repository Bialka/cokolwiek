import json
from os.path import dirname, getctime, isfile, isdir, join, realpath
import shutil
import subprocess
import unittest

import ogarniacz_mp3

_current_dir = realpath(dirname(__file__))
_test_data_dir = join(_current_dir, "TestData")
_tmp_test_data_dir = join(_current_dir, "TmpTestData")
downloaded_dir = join(_tmp_test_data_dir, "Pobrane")
processing_dir = join(_tmp_test_data_dir, "Do Obróbki")


class BaseProcessingFilesTestCase(unittest.TestCase):

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

        info = json.loads(proc.stdout.decode("utf-8"))['format']
        # add file creation timestamp to info
        info["ctime"] = getctime(file_path)
        return info


class TestProcessingFiles(BaseProcessingFilesTestCase):

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

    def test_deleting_duplicates(self):
        # run removing duplicates
        ogarniacz_mp3.remove_duplicates(processing_dir)
        # make sure original flac was deleted and mp3 was kept
        httyd_file = join(processing_dir, "How to Train Your Dragon - The Hidden World",
                          "01. Raiders Return to Busy, Busy Berk")
        self.assertFalse(isfile(httyd_file + ".flac"))
        self.assertTrue(isfile(httyd_file + ".mp3"))
        # make sure flac files that were no duplicates are still in place
        _1917_dir = join(processing_dir, "1917FYC", "1917 (FYC)")
        self.assertTrue(isfile(join(_1917_dir, "01. Meadow , First Trench.flac")))
        self.assertTrue(isfile(join(_1917_dir, "02. Trench to Yorks.flac")))

    def test_converting_to_mp3(self):
        # run mp3 conversion
        _1917_dir = join(processing_dir, "1917FYC", "1917 (FYC)")
        ogarniacz_mp3.convert_to_mp3(_1917_dir)
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

    def test_bitrate_adjustment(self):
        top_bitrate = 142000
        # get file paths
        sorry_path = join(processing_dir, "Big Mess", "CD1", "1. Sorry.mp3")
        happy_path = join(processing_dir, "Big Mess", "CD2", "1. Happy.mp3")
        fisherman_path = join(processing_dir, "26-06-19", "Dolce Fine Giornata", "1. Fishermen.mp3")
        # get files infos
        sorry_info_1 = self.get_file_info(sorry_path)
        happy_info_1 = self.get_file_info(happy_path)
        fisherman_info_1 = self.get_file_info(fisherman_path)

        ogarniacz_mp3.adjust_bitrates(processing_dir)

        # get data after changes and do the assertions
        sorry_info_2 = self.get_file_info(sorry_path)
        self.assertTrue(int(sorry_info_1["bit_rate"]) > int(sorry_info_2["bit_rate"]))
        self.assertTrue(top_bitrate > int(sorry_info_2["bit_rate"]))
        self.assertTrue(sorry_info_1["ctime"] < sorry_info_2["ctime"])

        happy_info_2 = self.get_file_info(happy_path)
        self.assertTrue(int(happy_info_1["bit_rate"]) > int(happy_info_2["bit_rate"]))
        self.assertTrue(top_bitrate > int(happy_info_2["bit_rate"]))
        self.assertTrue(happy_info_1["ctime"] < happy_info_2["ctime"])

        # ensure fisherman wasn't touched
        fisherman_info_2 = self.get_file_info(fisherman_path)
        self.assertEqual(fisherman_info_1["bit_rate"], fisherman_info_2["bit_rate"])
        self.assertEqual(fisherman_info_1["ctime"], fisherman_info_2["ctime"])


class TestWritingMp3Tags(BaseProcessingFilesTestCase):

    def test_writing_id3_tags(self):
        file_path = join(_test_data_dir, "Do Obróbki", "How to Train Your Dragon - The Hidden World",
                         "01. Raiders Return to Busy, Busy Berk.mp3")
        # make adjustments
        from getting_file_info import set_file_info
        changes = {
            "album_artist": "John Powell",
            "album": "How to Train Your Dragon: The Hidden World"
        }
        set_file_info(file_path, changes)
        # verify file after changes
        file_info = self.get_file_info(file_path)
        tags = file_info["tags"]
        # things that changed
        self.assertEqual(tags["album"], "How to Train Your Dragon: The Hidden World")
        self.assertEqual(tags["album_artist"], "John Powell")
        # things that should stay the same
        self.assertEqual(tags["track"], "01")
        self.assertEqual(tags["title"], "Raiders Return to Busy, Busy Berk")
        self.assertEqual(tags["artist"], "John Powell")
        self.assertEqual(tags["date"], "2019")
