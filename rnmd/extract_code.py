import urllib.request

delimiterToken="```"

def get_file_contents(path):
    with open(path, "r") as documentation_file:
        documentation_contents = documentation_file.read()
    return documentation_contents

def get_url_contents(url):
    return urllib.request.urlopen(url).read()

def extract_code_from_doc(sourceUri):
    
    documentation_contents = None

    if("http" in sourceUri):
        documentation_contents = get_url_contents(sourceUri)
    else:
        documentation_contents = get_file_contents(sourceUri)

    if(documentation_contents is None):
        raise Exception("Could not read documentation file from: " + sourceUri)
        
    lines = documentation_contents.split('\n')

    code_block_lines = []

    startindex = -1
    endindex = -1
    for index in range(0, len(lines)):
        line = lines[index]
        
        if(line.startswith(delimiterToken)):
            if(startindex == -1):
                startindex = index
            else:
                endindex = index

        if(startindex != -1 and endindex != -1):
            code_block_lines.append(lines[startindex+1:endindex])
            startindex = -1
            endindex = -1

    if(startindex > -1 or endindex > -1):
        raise Exception("Invalid Markdown document, code block not closed")

    #print(code_block_lines)

    code_blocks = [('\n').join(array) for array in code_block_lines]

    code = ('\n\n').join(code_blocks)
    
    return code

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Extrace all code from markdown file"
    )
    parser.add_argument('source', help="Source of the documentation file, can be a path or an url")
    arguments = parser.parse_args()
    source = arguments.source

    code = extract_code_from_doc(source)
    print(code)
