# Function to read in file lines to variable
def read_file(filename):

    file = open(filename, 'r')
    lines = file.readlines()
    i = 0
    for line in lines:
        lines[i] = line.strip("\n")
        i = i+1
    file.close()
    return lines

# Function to write to file
def write_file(content,filename):
    f = open(filename, "r+")
    for item in content:
        f.write(str(item) + "\n")
    f.close()
    return