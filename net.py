import os
import socket
import paramiko
from scp import SCPClient
import unittest
import time


# 检查IP的有效性
def check_valid_ipaddr(ipaddr):
    try:
        socket.inet_aton(ipaddr)
        return True
    except socket.error:
        return False


class WExpect:
    def __init__(self, spawn, timeout=10):
        self.cmd_list = []
        self.cmd_list.append('expect <<EOF')
        self.cmd_list.append('set timeout %d' % timeout)
        self.cmd_list.append('spawn %s' % spawn)

    def expect(self, pattern, send_val, end='\\n'):
        # TODO: replace替换字符串存在问题?
        expect_expr = r'''
            expect "{pattern}"
            send "{send}"
        '''.replace(' ' * 12, '').format(pattern=pattern, send=send_val + end).strip()
        self.cmd_list.append(expect_expr)

    def get_output(self):
        output = [*self.cmd_list, 'expect eof', 'EOF']
        return '\n'.join(output)


class SSH:
    def __init__(self):
        self.ssh = None
        self.is_active_ssh = False

    def __active(self):
        return self.is_active_ssh

    # 登陆服务端
    def login(self, host, username, password, port):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=host, username=username, password=password, port=port)
        self.ssh = ssh

    def active_terminal(self):
        self.is_active_ssh = True
        self.shell = self.ssh.invoke_shell()

    # 执行远程命令
    def exec(self, *cmd):
        if not self.__active():
            stdin, stdout, stderr = self.ssh.exec_command('\n'.join(cmd))
            for echo in stdout.readlines():
                print(echo.strip())
            for echo in stderr.readlines():
                print(echo.strip())
        else:
            for sub_cmd in cmd:
                self.shell.send(sub_cmd + '\n')
                time.sleep(1)
            output = self.shell.recv(65535).decode().strip()
            print(output)
            self.ssh.close()

    # 复制远程文件到本地
    def scp(self, remote, local):
        scp = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)
        scp.get(remote, local)


class TestNetFunctions(unittest.TestCase):
    def setUp(self):
        self.user = ('192.168.2.45', 'wchen', '12345', 22)
        ssh = SSH()
        ssh.login(*self.user)
        self.ssh = ssh

    def test_check_valid_ipaddr(self):
        self.assertEqual(True, check_valid_ipaddr('192.168.2.43'))
        self.assertEqual(False, check_valid_ipaddr('192.168.2.266'))

    def test_ssh_connect(self):
        self.ssh.exec('ls -al workspace')
        self.ssh.scp('workspace/test.c', './test.c')

    def test_ssh_cmd(self):
        self.ssh.exec('ls -al', 'who')

    def test_active_terminal(self):
        self.ssh.active_terminal()
        self.ssh.exec('~/workspace/cmd', 'hello world', 'q')

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
        '''.replace(' ' * 12, '').strip()
        print(expect_cmd)
        self.ssh.exec(expect_cmd)

    def test_expect_cmd(self):
        cmd = WExpect('~/workspace/cmd')
        cmd.expect('diagnose*', 'hello world')
        cmd.expect('diagnose*', 'q')
        print(cmd.get_output())
        self.ssh.exec(cmd.get_output())
