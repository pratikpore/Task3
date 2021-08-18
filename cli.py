import argparse
import unittest
from unittest.suite import TestSuite
from run import execute
import subprocess


parser = argparse.ArgumentParser()

parser.add_argument("--fs", help = "filesystem to be mounted")
parser.add_argument("--disk",nargs='+', help = "Name of the disk")
parser.add_argument('--lv_name', help="name of the logical volume")
parser.add_argument('--lv_size', help="Determine lv_size of LV")
parser.add_argument('--vg_name', help="Enter name of volume group")
parser.add_argument("--rmd", help = "name of Drive to be removed")
args = parser.parse_args()


fs = args.fs
disk_name = args.disk
lv_name = args.lv_name
lv_size = args.lv_size
vg_name = args.vg_name
rmd = args.rmd

if __name__ == '__main__':
    import test3
    suite = TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromName("test.Fio"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
