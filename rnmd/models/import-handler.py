import re
import rnmd.extract_code

#Todo improve detect and extract regex
python_regex_detect = re.compile('(import +.+)|(from +.+ +import +.+)')
python_regex_extract = re.compile('(?<=from).+(?=import)')
python_regex_extract = re.compile('(?<=import).+(?=as)')
detect_regexes = {
    'python': python_regex_detect,
    'py': python_regex_detect
    }

def detect_import(self, line, language):
    
    match_result = re.search(detect_regexes[language], line)

    if(match_result is not None):
        return True
    return False

def extract_import_path(self, line, language):
    if(not self.detect_import(line,language)):
        return None

    return "my/path/import"