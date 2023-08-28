import re

def remove_special_chars(s):
    return re.sub(r'[^\w\s]', '', s)