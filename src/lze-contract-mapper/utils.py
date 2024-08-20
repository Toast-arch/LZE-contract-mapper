# Custom split
def arg_split(input_str):
    arg_list = []

    arg = ""
    ignore_spaces = False

    for c in input_str:
        if c.isspace() and not ignore_spaces:
            arg_list.append(arg)
            arg = ""
        elif c == '\"':
            ignore_spaces = not ignore_spaces
        else:
            arg += c
        
    if arg:
        arg_list.append(arg)
    
    arg_list = list(filter(None, arg_list))

    return arg_list