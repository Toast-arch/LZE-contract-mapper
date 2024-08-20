import logging
import os
import readline
from .completer import Completer
import sys


DDB_HELP = f"""LZECM - Level Zero: Extraction Contract Mapper - Version 0.0.1
  help				display this help message
  clear				clear the terminal
  exit				exit the LZECM
"""

class LZECM:
    def __init__(self):
        self.command_dict = {
            "clear":		    		self.clear_cmd,
            "exit":			    		self.exit_cmd,
            "help":			    		self.help_cmd
        }
        
    def run(self):
        while self.cli_loop():
            continue
        
        return 0
    
    def cli_loop(self):
        comp = Completer(list(self.command_dict.keys()))

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(comp.complete)
        
        histfile = os.path.expanduser('~/.lze_cm_console_history')

        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)
        
        try:
            cli_input = input('ECM> ')
        except KeyboardInterrupt:
            sys.exit()

        if readline:
            readline.set_history_length(1000)
            readline.write_history_file(histfile)
        
        logging.info(cli_input)
        
        if not cli_input.isspace() and cli_input != "":
            return self.apply_cmd(cli_input)
        else:
            return 1
    
    def apply_cmd(self, cli_input):
        arg_list = arg_split(cli_input)
        
        cmd = arg_list[0]
        cli_input_args = arg_list[1:]
        
        if cmd in self.command_dict:
            return self.command_dict[cmd](cli_input_args) # return 1 to continue # return 0 to exit
        else:
            print(f"Command not found: {cmd}")
            return 2
        
    def help_cmd(self, cli_input_args):
        if len(cli_input_args) == 0:
            print(DDB_HELP)
        else:
            for cmd in cli_input_args:
                self.apply_cmd(cmd + " -h")
        
        return 1

    def exit_cmd(self, cli_input_args):
        return 0

    # CLEAR CMD - Clear terminal
    def clear_cmd(self, cli_input_args):
        os.system('cls' if os.name == 'nt' else 'clear')

        return 1