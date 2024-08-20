import re
import readline

RE_SPACE = re.compile(r'.*\s+$', re.M)

dataflow_names = [
    "ACC_004"
]

class Completer(object):
    def __init__(self, commands):
        self.commands = commands

        self.active_command = None
    
    def _complete_dataflow_name(self, dataflow_name=None):
        results = [c + ' ' for c in dataflow_names if c.startswith(dataflow_name)] + [None] 
        
        return results
    
    def complete_options(self, args):        
        return self._complete_dataflow_name(args[-1])


    def complete(self, text, state):
        tmp_buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in self.commands][state]
        # account for last argument ending in a space
        if RE_SPACE.match(tmp_buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in self.commands or cmd[0] == '!':
            impl = getattr(self, 'complete_options')
            args = line[1:]
            
            self.active_command = line[0]
            
            for word in line:
                if word.endswith("_pyfmt.json") and not self.fmt_file_selected:
                    self.fmt_file_selected = True
                    self._load_fmt_fields(word)
                    break
                else:
                    self.fmt_file_selected = False
                    self.selected_fmt_fields = []
                    
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in self.commands if c.startswith(cmd)] + [None]
        return results[state]