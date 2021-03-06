import os, subprocess, time
import pyven.constants

from pyven.plugins.plugin_api.process import Process

from pyven.logging.logger import Logger

class Command(Process):

    def __init__(self, cwd, name, command, directory):
        super(Command, self).__init__(cwd, name)
        self.duration = 0
        self.type = 'command'
        self.command = command
        self.directory = directory
        if self.directory != '.':
            self.cwd = os.path.join(self.cwd, self.directory)
    
    @Process.error_checks
    def process(self, verbose=False, warning_as_error=False):
        Logger.get().info('Command : ' + self.type + ':' + self.name)
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        Logger.get().info('Entering directory : ' + self.directory)
        self.duration, out, err, returncode = self._call_command(self._format_call())
        Logger.get().info('Leaving directory : ' + self.directory)
        
        if verbose:
            for line in out:
                Logger.get().info('[' + self.type + ']' + line)
            for line in err:
                Logger.get().info('[' + self.type + ']' + line)
        
        if returncode != 0:
            self.status = pyven.constants.STATUS[1]
            self.errors.extend([out + err])
            Logger.get().error('Command failed : ' + self.type + ':' + self.name)
        else:
            self.status = pyven.constants.STATUS[0]
        return returncode == 0
    
    @Process.error_checks
    def clean(self, verbose=False, warning_as_error=False):
        self.status = pyven.constants.STATUS[0]
        return True
        
    def report_summary(self):
        return self.report_title()
    
    def report_title(self):
        return self.name
        
    def report_properties(self):
        properties = []
        properties.append(('Command', self.command))
        properties.append(('Workspace', self.directory))
        properties.append(('Duration', str(self.duration) + ' seconds'))
        return properties
        
    def _call_command(self, command):
        tic = time.time()
        out = ''
        err = ''
        try:
            try:
                sp = subprocess.Popen(command,\
                                      stdin=subprocess.PIPE,\
                                      stdout=subprocess.PIPE,\
                                      stderr=subprocess.PIPE,\
                                      universal_newlines=True,\
                                      cwd=self.cwd,\
                                      shell=pyven.constants.PLATFORM == pyven.constants.PLATFORMS[1])
                out, err = sp.communicate(input='\n')
                out = out.splitlines()
                err = err.splitlines()
                returncode = sp.returncode
            except UnicodeDecodeError as e:
                sp = subprocess.Popen(command,\
                                      stdin=subprocess.PIPE,\
                                      stdout=subprocess.PIPE,\
                                      stderr=subprocess.PIPE,\
                                      cwd=self.cwd,\
                                      shell=pyven.constants.PLATFORM == pyven.constants.PLATFORMS[1])
                out, err = sp.communicate()
                out = out.decode("cp1252").split('\n')
                err = err.decode("cp1252").split('\n')
                returncode = sp.returncode
        except FileNotFoundError as e:
            returncode = 1
            self.errors.append(['Unknown command'])
        toc = time.time()
        return round(toc - tic, 3), out, err, returncode
        
    def _format_call(self):
        call = self.command.split(' ')
        Logger.get().info(self.command)
        return call
        