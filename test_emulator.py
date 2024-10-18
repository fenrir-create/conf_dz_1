from shellemulator import ShellEmulator
import unittest

class Test_shell(unittest.TestCase):
    def setUp(self):
        self.shell = ShellEmulator("testuser","v_file_s.tar")
    
    

    def test_whoami(self):
        self.assertEqual(self.shell.whoami(),"testuser")
        
    def test_ls(self):
        self.assertEqual(self.shell.ls()," f1 p1 p2 txttt.txt")
        
    def test_du(self):
        self.assertEqual(self.shell.du(),"Directory size: 364 bytes")
        
        
    def test_head(self):
        self.assertEqual(self.shell.head("f1"), "kbbvibvibvkvbaobvovbnnbollbvlsbvkbvkbfk\n")
        
    def test_cd(self):
        self.assertEqual(self.shell.cd("p1"),None)
        
    
        
    
    
if __name__ == '__main__':
    
    unittest.main()
