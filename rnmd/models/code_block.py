class CodeBlock():
    
    def __init__(self):
        self.language = None
        self.command_addon = None
        self.lines = []
        self.import_paths = []
        self.import_indices = []

    def detect_import(self, line, language):
        if("import" in  line):
            return True
        return False
    
    def extract_import_path(self, line, language):
        if(not self.detect_import(line,language)):
            return None

        return "my/path/import"

    def has_imports(self):
        if(len(self.import_paths) > 0):
            return True

        return False

    def parse(self, text_block_lines):

        if(text_block_lines is None or len(text_block_lines) < 3):
            raise Exception("Can not parse empty code block")

        if("```" not in text_block_lines[0] and "```" not in text_block_lines[len(text_block_lines)-1]):
            raise Exception("Can not parse block that is missing the enclosure with ```")
        
        self.language = text_block_lines[0].replace("```","")
        self.lines = text_block_lines[1:len(text_block_lines)-1]

        #Additional info in first comment
        self.command_addon = self.lines[0]

        #Detect imports that need to be resolved
        line_nr = 0
        for line in self.lines:
            extracted_import_path = self.extract_import_path(line, self.language)
            if(extracted_import_path is not None):
                self.import_paths.append(line)
                self.import_indices.append(line_nr)

            line_nr += 1

    def get_code(self):
        if(self.lines is None):
            raise Exception("Can not get code from empty block")

        return ("\n").join(self.lines)