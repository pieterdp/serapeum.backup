import subprocess
from backup.modules.ds.stack import Stack
from backup.modules.config import Config


class Run:

    def __init__(self):
        self.__cmd_output = ''
        self.c = Config(config_file='config/config.ini')

    @property
    def cmd_output(self):
        return self.__cmd_output

    @cmd_output.setter
    def cmd_output(self, command_output):
        if command_output is not None:
            self.__cmd_output += command_output.decode('utf-8')

    def run(self, command):
        proc_result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc_result.returncode != 0:
            self.cmd_output = proc_result.stderr
            raise Exception('Failed to execute {0}: the subprocess returned an error: {1}'
                            .format(command[0], proc_result.returncode))
        self.cmd_output = proc_result.stdout
        return self.cmd_output

    def zip_output(self, command, output_file):
        """
        Zip (using gzip) the output of command "command" to output_file
        :param command:
        :param output_file:
        :return:
        """
        op_fh = open(output_file, 'wb')
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        gzip = subprocess.Popen([self.c.config['SYSTEM']['gzip_path']], stdin=proc.stdout, stdout=op_fh)
        proc.stdout.close()
        op_fh.close()
        self.cmd_output = gzip.communicate()[0]
        return self.cmd_output

    def pipe(self, commands):
        pipes = Stack()
        cmd_output = []
        for command in commands:
            if pipes.peek() is not None:
                previous = pipes.pop()
                proc = subprocess.Popen(command, stdin=previous.stdout, stdout=subprocess.PIPE)
                previous.stdout.close()
                pipes.add(previous)
            else:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            if proc.returncode != 0:
                self.cmd_output = proc.stderr
                raise Exception('Failed to execute {0}: the subprocess returned an error: {1}'
                                .format(command[0], proc.returncode))
            pipes.add(proc)
            cmd_output.append(proc.communicate()[0])
            proc.wait()
        self.cmd_output = '|'.join(cmd_output)
        return self.cmd_output
