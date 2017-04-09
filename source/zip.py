import zipfile, os
import command_plugin.constants

def zip_pvn():
    if not os.path.isdir(os.path.join(os.environ.get('PVN_HOME'), 'plugins')):
        os.makedirs(os.path.join(os.environ.get('PVN_HOME'), 'plugins'))
    zf = zipfile.ZipFile(os.path.join(os.environ.get('PVN_HOME'), 'plugins', 'command-plugin_' + command_plugin.constants.VERSION + '.zip'), mode='w')
    
    zf.write('__init__.py')
    
    zf.write('command_plugin/__init__.py')
    zf.write('command_plugin/constants.py')
    zf.write('command_plugin/parser.py')
    zf.write('command_plugin/command.py')
    
if __name__ == '__main__':
    zip_pvn()
