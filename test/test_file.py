import unittest
import shutil
from file import replace_content, iter_dir


class TestFileFunctions(unittest.TestCase):
    def test_replace_content(self):
        replace_content('./test.c', '#include', '@INCLUDE')

    def test_iter_dir(self):
        iter_dir(r'D:\Workspace\C\gcc', print)

    def test_compressed_format(self):
        print(shutil.get_archive_formats())
