from rnmd.models.code_file import CodeFile
from rnmd.util.extract_document_content import extract_document_content, resolve_document_location

class CodeProjectParser():

    def __init__(self):
        self.code_files = []

    def parse_document(self, markdown_doc_location):
        document_contents = extract_document_content(markdown_doc_location)

        if(document_contents is None):
            raise Exception("Could not read documentation file from: " + markdown_doc_location)

        new_code_file = CodeFile()
        new_code_file.parse(document_contents)

        self.code_files.append(new_code_file)

        import_paths = new_code_file.get_import_paths()

        for import_path in import_paths:
            import_doc_location = resolve_document_location(markdown_doc_location, import_path)
            self.parse_document(import_doc_location)