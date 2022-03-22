import socket
import paramiko
from scp import SCPClient
import unittest

# 检查IP的有效性
def check_valid_ipaddr(ipaddr):
    try:
        socket.inet_aton(ipaddr)
        return True
    except socket.error:
        return False


class SSH:
    def login(self, host, username, password, port):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=host, username=username, password=password, port=port)
        self.ssh = ssh

    def exec(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        for echo in stdout.readlines():
            print(echo)
        for echo in stderr.readlines():
            print(echo)

    def scp(self, remote, local):
        scp = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)
        scp.get(remote, local)


class TestNetFunctions(unittest.TestCase):
    def test_check_valid_ipaddr(self):
        self.assertEqual(True, check_valid_ipaddr('192.168.2.43'))
        self.assertEqual(False, check_valid_ipaddr('192.168.2.266'))

    def test_ssh_connect(self):
        ssh = SSH()
        ssh.login('192.168.2.43', 'wchen', '12345', 22)
        ssh.exec('ls -al workspace')
        ssh.scp('workspace/test.c', './test.c')