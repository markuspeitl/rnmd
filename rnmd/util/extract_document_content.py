import os
from rnmd.util.web_tool import is_url, get_url_contents_utf8, page_exists
from rnmd.util.file_tool import get_file_contents, is_file_exists

def extract_document_content(source_location):

    if(not document_exists(source_location)):
        return None

    if(is_url(source_location)):
        return get_url_contents_utf8(source_location)
    else:
        return get_file_contents(source_location)

def document_exists(source_location):
    return is_url(source_location) and page_exists(source_location) or is_file_exists(source_location)

def get_abs_document_location(source_location):
    if(is_url(source_location)):
        return source_location
    elif(is_file_exists):
        return os.path.abspath(source_location)
    return None

def get_rel_document_location(source_location,reference_location):
    if(is_url(source_location)):
        return source_location
    elif(is_file_exists):
        return os.path.relpath(source_location, os.path.dirname(reference_location))
    return None

def get_rel_shell_path(source_location, reference_location):
    if(is_url(source_location)):
        return source_location
    elif(is_file_exists):
        rel_source_location = os.path.relpath(source_location, os.path.dirname(reference_location))
        #Has to be added in bash so that the path is resolved from the proxies location (and not the caller directory)
        return os.path.join("`dirname $0`", rel_source_location)
    return None