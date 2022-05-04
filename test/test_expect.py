from net import SSH
import unittest


class TestExpectFunctions(unittest.TestCase):
    def setUp(self):
        self.user = ('192.168.2.45', 'wchen', '12345', 22)
        ssh = SSH()
        ssh.login(*self.user)
        self.ssh = ssh

    def test_multi_cmd(self):
        expect_cmd = r'''
            expect << EOF
            set timeout 10
            spawn ~/workspace/cmd
            expect "diagnose*"
            send "hello world\n"
            expect "diagnose*"
            send "q\n"
            expect eof
            EOF
        '''
        expect_cmd = '\n'.join([item.strip() for item in expect_cmd.split('\n')])
        print(expect_cmd)
        self.ssh.exec(expect_cmd)

    def test_expect_cmd(self):
        cmd = WExpect('~/workspace/cmd')
        cmd.expect('diagnose*', 'hello world')
        cmd.expect('diagnose*', 'q')
        print(cmd.get_output())
        self.ssh.exec(cmd.get_output())

    def test_pexpect_cmd(self):
        """
        : ssh.prompt(): 等待命令返回
        from pexpect import pxssh
        ssh = pxssh.pxssh()
        ssh.login(server='192.168.2.45', username='wchen', password='12345')
        ssh.expect('diagnose> ')
        ssh.sendline('hello world')
        ssh.expect('diagnose> ')
        ssh.sendline('q')
        print(ssh.before)
        ssh.logout()
        """
        pass