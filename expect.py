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