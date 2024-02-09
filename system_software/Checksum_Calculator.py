# Luke ripped this straight from ChatGPt, but it works like a glove
# Thanks for the idea Becca

def calculate_checksum(sentence):
    """
    Calculates the checksum for an NMEA sentence.

    Args:
        sentence (str): NMEA sentence without the starting '$' and ending '*' characters.

    Returns:
        str: Calculated checksum (2 characters, hexadecimal).
    """
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    checksum_hex = hex(checksum)[2:].upper()
    return checksum_hex.zfill(2)

def generate_nmea_sentence(sentence):
    """
    Generates a complete NMEA sentence with the checksum.

    Args:
        sentence (str): NMEA sentence without the starting '$' and ending '*' characters.

    Returns:
        str: Complete NMEA sentence.
    """
    checksum = calculate_checksum(sentence)
    return f"${sentence}*{checksum}"

# Example usage:
nmea_sentence = "TypeHere"
complete_nmea_sentence = generate_nmea_sentence(nmea_sentence)
print("Complete NMEA sentence:", complete_nmea_sentence)
