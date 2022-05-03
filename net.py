import socket
import paramiko
from scp import SCPClient
import time


# 检查IP的有效性
def check_ip_valid(ipaddr):
    try:
        socket.inet_aton(ipaddr)
        return True
    except socket.error:
        return False


class SSH:
    def __init__(self):
        self.ssh = None
        self.is_active_ssh = False
        self.shell = None

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
    def download(self, remote, local):
        scp = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)
        scp.get(remote, local, recursive=True)

    # 上传文件
    def upload(self, local, remote):
        scp = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)
        scp.put(local, remote, recursive=True)

