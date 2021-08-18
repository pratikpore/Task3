from run import execute
import unittest
import cli
from run import execute
import threading
import time

class Fio(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        execute("sudo umount /")
        execute("sudo lvremove -ff {}".format(cli.vg_name))
        execute("sudo vgremove {}".format(cli.vg_name))
        execute("sudo pvremove {}".format(cli.disk_name))
        print("Done")

        
#     def test_pvcreate(self):
#         execute("sudo pvcreate {}".format(cli.disk_name))
#         for i in cli.d:
#             self.assertRegex(execute("sudo pvdisplay").stdout, i)

#         execute("sudo vgcreate {} {}".format(cli.vg_name,cli.disk_name))
#         self.assertRegex(execute("sudo vgdisplay").stdout, cli.vg_name)

    
#         execute("sudo lvcreate -n {} --size {}G {}".format(cli.lv_name,cli.lv_size,cli.vg_name))
#         self.assertRegex(execute("sudo lvdisplay").stdout, cli.lv_name)

#         print("\n PV  LV  VG has been created")


    def test_fscreate(self):
        execute("sudo pvcreate {}".format(cli.disk_name))
        for i in cli.d:
            self.assertRegex(execute("sudo pvdisplay").stdout, i)
            
        execute("sudo vgcreate {} {}".format(cli.vg_name,cli.disk_name))
        self.assertRegex(execute("sudo vgdisplay").stdout, cli.vg_name)
        
        execute("sudo lvcreate -n {} --size {}G {}".format(cli.lv_name,cli.lv_size,cli.vg_name))
        self.assertRegex(execute("sudo lvdisplay").stdout, cli.lv_name)

        print("\n PV  LV  VG has been created, \n Creating file system")
        
        
        self.file_dest = "/"
        self.lvpath = ("/dev/{}/{}".format(cli.vg_name,cli.lv_name))
        execute("sudo mkfs.{} {}".format(cli.fs,self.lvpath))
        execute("mkdir {}".format(self.file_dest))
        execute("mount {} {}".format(self.lvpath,self.file_dest))
        self.assertRegex(execute("df -h").stdout, self.file_dest)
        

        
        a = execute("sudo fio --filename={} --size=500GB --direct=1 --rw=randrw --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1".format(self.lvpath))
        self.assertRegex(a.stdout, "Run status")
        print("File has been created, mounted & IO has been verified")
       
        #Note-
        #this for xfs file
        #data for ext4 file


    def T2(self):    
        time.sleep(2)
        execute("pvmove {}".format(cli.rmd))
        execute("vgreduce {} {}" .format(cli.vg_name,cli.rmd))
        self.output = execute("pvdisplay -C -o pv_name,vg_name -S vg_name={}".format(cli.vg_name))
        self.assertNotIn(cli.rmd,self.output)
        print("VG Reduced")


    def test_thread(self):
        t1=threading.Thread(target=self.test_fscreate)
        t2=threading.Thread(target=self.T2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
