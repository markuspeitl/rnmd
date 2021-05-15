def get_enclosed_indices(token, text):
    lines = text.split('\n')

    enclosed_ranges = []

    startindex = -1
    endindex = -1
    for index in range(0, len(lines)):
        line = lines[index]
        
        if(line.startswith(token)):
            if(startindex == -1):
                startindex = index
            else:
                endindex = index

        if(startindex != -1 and endindex != -1):
            enclosed_ranges.append((startindex, endindex + 1))

            startindex = -1
            endindex = -1

    if(startindex > -1 or endindex > -1):
        raise Exception("Invalid Markdown document, code block not closed")

    return enclosed_ranges