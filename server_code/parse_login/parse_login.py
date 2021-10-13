import re

'''
This function takes a regex string and a string to parse, 
as well as a string to look for. Returns true if it found the string, 
false if not.
'''
def parse_login(regex_str, string_to_parse, string_to_look_for):
    if '@' not in string_to_parse:
        return False
    
    result = re.search(regex_str, string_to_parse)
    return result is not None and string_to_look_for == result.group(3)