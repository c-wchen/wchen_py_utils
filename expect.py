import unittest
from net import SSH
# from pexpect.pxssh import pxssh


class WExpect:
    def __init__(self, spawn, timeout=10):
        self.cmd_list = []
        self.cmd_list.append('expect <<EOF')
        self.cmd_list.append('set timeout %d' % timeout)
        self.cmd_list.append('spawn %s' % spawn)

    def expect(self, pattern, send, end='\\n'):
        expect_expr = '\n'.join(['expect "%s"' % pattern, 'send "%s"' % (send + end)])
        self.cmd_list.append(expect_expr)

    def get_output(self):
        output = [*self.cmd_list, 'expect eof', 'EOF']
        return '\n'.join(output)


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
        pass
        # ssh = pxssh()
        # ssh.login(server='192.168.2.45', username='wchen', password='12345')