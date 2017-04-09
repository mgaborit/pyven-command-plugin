from pyven.exceptions.parser_exception import ParserException
from pyven.plugins.plugin_api.parser import Parser

from command_plugin.command import Command

class CommandParser(Parser):
    COUNT = 0
    SINGLETON = None
    
    def __init__(self, cwd):
        CommandParser.COUNT += 1
        super(CommandParser, self).__init__(cwd)
    
    def parse(self, node):
        objects = []
        members = self.parse_process(node)
        errors = []
        directory_node = node.find('directory')
        directory = '.'
        if directory_node is not None:
            directory = directory_node.text
        command_node = node.find('command')
        if command_node is None:
            errors.append('Missing command')
        else:
            command = command_node.text
        if len(errors) > 0:
            e = ParserException('')
            e.args = tuple(errors)
            raise e
        objects.append(Command(self.cwd, members[0], command, directory))
        return objects
        
def get(cwd):
    if CommandParser.COUNT <= 0 or CommandParser.SINGLETON is None:
        CommandParser.SINGLETON = CommandParser(cwd)
    CommandParser.SINGLETON.cwd = cwd
    return CommandParser.SINGLETON