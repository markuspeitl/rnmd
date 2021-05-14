from rnmd.util.web_tool import is_url, get_url_contents_utf8, page_exists
from rnmd.util.file_tool import get_file_contents, file_exists

def extract_document_content(source_location):

    if(not document_exists(source_location)):
        return None

    if(is_url(source_location)):
        return get_url_contents_utf8(source_location)
    else:
        return get_file_contents(source_location)

def document_exists(source_location):
    return is_url(source_location) and page_exists(source_location) or file_exists(source_location)
