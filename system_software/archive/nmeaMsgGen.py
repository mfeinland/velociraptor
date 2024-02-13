import numpy as np

def generateMsg(type, freq):
    # takes in NMEA message type (options 1-8) and number of messages per N fixes (options 1-20)
    # returns complete NMEA message with checksum
    sentence = "PAIR062," + str(type) + "," + str(freq)
    csum = 0
    for char in sentence:
        csum ^= ord(char)
    checksum_hex = hex(csum)[2:].upper()
    checksum = checksum_hex.zfill(2)

    # generate message for receiver
    return f"${sentence}*{checksum}"

# Example usage:
# msgNum = 5
# msgFreq = 6
# nmeaMsg = generateMsg(msgNum, msgFreq)
# print("Complete NMEA sentence:", nmeaMsg)

# check all possibilities (checked everything through 4,4 plus some random ones and it was all correct)
freqs = np.linspace(0,8,9).astype(int)
print(freqs)
msgs = np.linspace(1,20,20).astype(int)
print(msgs)
for m in msgs:
    for f in freqs:
       print(generateMsg(msgs[m-1],freqs[f]))
