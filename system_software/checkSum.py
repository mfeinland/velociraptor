import regex as re

# Source: https://doschman.blogspot.com/2013/01/calculating-nmea-sentence-checksums.html

def checkSumCalc(msg):
    # from Quectel: the checkum is the 8-bit exclusive OR of all the characters between but not
    # including the $ and the * and including commas

    # need to calculate checksum for: PAIR062,int,int
    # This is a string, will need to convert it to hex for 
    # proper comparsion below
    cksum = msg[len(msg) - 2:]
    
    msgData = re.sub("(\n|\r\n)","", msg[msg.find("$")+1:msg.find("*")])
    # Initialize first XOR value
    csum = 0 
    # For each char in chksumdata, XOR against the previous XOR'd char.
        # The final XOR of the last char will be our checksum to verify against
        # the checksum we sliced off the NMEA sentence
    for c in msgData:
    # XOR'ing value of csum against the next char in line
    # and storing the new XOR value in csum
        csum ^= ord(c)
    answer = hex(csum)
    return answer

msg = "$PAIR062,0,6*"
print(checkSumCalc(msg))