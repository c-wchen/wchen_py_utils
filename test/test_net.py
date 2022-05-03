import unittest
from net import SSH, check_ip_valid


class TestNetFunctions(unittest.TestCase):
    def setUp(self):
        self.user = ('192.168.2.45', 'wchen', '12345', 22)
        ssh = SSH()
        ssh.login(*self.user)
        self.ssh = ssh

    def test_check_valid_ipaddr(self):
        self.assertEqual(True, check_ip_valid('192.168.2.43'))
        self.assertEqual(False, check_ip_valid('192.168.2.266'))

    def test_download(self):
        self.ssh.download('workspace/test.c', './test.c')

    def test_upload(self):
        self.ssh.upload('./demo/cmd.c', '~/workspace/')

    def test_ssh_cmd(self):
        self.ssh.exec('ls -al', 'who')

    def test_active_terminal(self):
        self.ssh.active_terminal()
        self.ssh.exec('~/workspace/cmd', 'hello world', 'q')
