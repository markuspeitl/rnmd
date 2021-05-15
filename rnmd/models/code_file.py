from rnmd.models.code_block import CodeBlock
from rnmd.models.code_parser import get_enclosed_indices

class CodeFile():
    
    def __init__(self):
        self.code_blocks = []
        self.language = None
        self.run_bin = None
        self.import_paths = []

    def get_import_paths(self):
        return self.import_paths

    def is_valid_markdown(self):
        return True

    def detect_language(self):
        language = None
        for code_block in self.code_blocks:
            if(language is None):
                language = code_block.language
            if(not language is code_block.language):
                raise("Error multiple languages in one file currently not supported")
        
        self.language = language

    def parse_import_paths(self, code_block):
        if(code_block.has_imports()):
            print("Not impl " + str(code_block.import_paths))

    def parse_all_imports(self):
        for code_block in self.code_blocks:
            self.parse_import_paths(code_block)

    def parse_all_code_blocks(self, markdown_text):
        lines = markdown_text.split('\n')

        enclosed_ranges = get_enclosed_indices("```", markdown_text)

        for serange in enclosed_ranges:
            new_code_block = CodeBlock()
            new_code_block.parse(lines[serange[0]:serange[1]])
            self.code_blocks.append(new_code_block)

    def parse(self, markdown_text):

        if(markdown_text is None or len(markdown_text) < 1):
            raise Exception("Can not parse empty code block")

        if(not self.is_valid_markdown):
            raise Exception("Can not parse invalid markdown text")

        self.parse_all_code_blocks()
        self.detect_language()
        self.parse_all_imports()

    def get_code(self):

        text_blocks = []
        for code_block in self.code_blocks:
            text_blocks.append(code_block.parse())

        return ("\n\n").join(text_blocks)

    def get_blocks_by_index(self, block_indices):

        text_blocks = []
        for block_index in block_indices:
            if(len(self.code_blocks) < block_index or block_index < 0):
                raise Exception("Invalid block index for block range 0-" + len(self.code_blocks) + " passed was " + block_index)
            text_blocks.append(self.code_block[block_index].parse())

        return ("\n\n").join(text_blocks)