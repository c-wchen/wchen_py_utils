import socket
import paramiko
from scp import SCPClient


# 检查IP的有效性
def check_valid_ipaddr(ipaddr):
    try:
        socket.inet_aton(ipaddr)
        return True
    except socket.error:
        return False


# 远程登陆
def ssh_login(username, password, port, host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=host, username=username, password=password, port=port)
    return ssh


# 远程执行命令
def ssh_exec(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for echo in stdout.readlines():
        print(echo)
    for echo in stderr.readlines():
        print(echo)


# scp下载文件
def download(ssh, remote, local):
    scp = SCPClient(ssh.get_transport(), socket_timeout=15.0)
    scp.get(remote, local)

