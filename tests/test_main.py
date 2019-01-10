"""test_main.py
|This file is a part of the testing scripts for GASTOp
|Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
|Licensed under GNU GPLv3.
|This module implements testing for the main script

"""
#!/usr/bin/env python3

import unittest
import gastop.__main__


class TestCLParse(unittest.TestCase):
    """Tests CLI argparse"""

    def test_parser(self):
        """Passes in a basic list of args and makes sure parser does its thing"""

        clargs = '-t 2 -p 1000 -g 100 folder/test_file_path.txt'
        clargs = clargs.split()
        args = gastop.__main__.parse_args(clargs)
        self.assertEqual(args.num_threads, 2)
        self.assertEqual(args.pop_size, 1000)
        self.assertEqual(args.num_gens, 100)
        self.assertEqual(args.config_path, 'folder/test_file_path.txt')


class TestMain(unittest.TestCase):
    """Tests for main function.
    They don't assert anything, just make sure the code runs without
    errors in different situations.
    """

    def test_main(self):
        """Runs main twice with different args"""

        clargs1 = '-t 2 -p 50 -g 10 gastop-config/struct_making_test_init.txt'.split()
        gastop.__main__.main(clargs1)
        clargs2 = '-q gastop-config/main_test.txt'.split()
        gastop.__main__.main(clargs2)

    def test_big_pop(self):
        """Tests in parallel with a large population"""

        clargs3 = '-t 2 -p 11000 -g 1 gastop-config/struct_making_test_init.txt'.split()
        gastop.__main__.main(clargs3)

    def test_single_threaded_display(self):
        """Tests single threaded with graphical display"""

        clargs4 = '-o output.json -d -t 1 -p 50 -g 10 gastop-config/struct_making_test_init.txt'.split()
        gastop.__main__.main(clargs4)


if __name__ == '__main__':
    unittest.main()
