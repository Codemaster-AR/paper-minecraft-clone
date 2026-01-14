import re
import struct

def get_base85_decode_value(char_code):
    if char_code == 0x28:  # (
        char_code = 0x3c  # <
    if char_code == 0x29:  # )
        char_code = 0x3e  # >
    return char_code - 0x2a # *

def base85_decode(encoded_str):
    decoded_bytes = bytearray()
    
    # Process in chunks of 5
    for i in range(0, len(encoded_str), 5):
        chunk = encoded_str[i:i+5]
        if len(chunk) < 5:
            # As per the original JS, it seems to expect full 5-char chunks.
            # We'll ignore incomplete chunks at the end if any.
            continue

        value = 0
        value += get_base85_decode_value(ord(chunk[0]))
        value += get_base85_decode_value(ord(chunk[1])) * 85
        value += get_base85_decode_value(ord(chunk[2])) * 85**2
        value += get_base85_decode_value(ord(chunk[3])) * 85**3
        value += get_base85_decode_value(ord(chunk[4])) * 85**4

        # Pack the 32-bit integer as 4 bytes, little-endian
        decoded_bytes.extend(struct.pack('<I', value))
        
    return decoded_bytes

# Read the HTML file
with open('Paper Minecraft v11.7 (Minecraft 2D).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all data chunks and concatenate them
data_chunks = re.findall(r'<script data="([^"]+)">', html_content)
encoded_data = "".join(data_chunks)

# Decode the data
# The original JS allocates a buffer of 3509300 and processes up to 3509299 bytes.
# Let's decode and then truncate to the correct size if needed.
decoded_data = base85_decode(encoded_data)

# The project size is mentioned in the JS as 3509299. Let's verify our output size
# and trim if necessary.
final_data = decoded_data[:3509299]

# Write the result to an .sb3 file
with open('Paper-Minecraft.sb3', 'wb') as f:
    f.write(final_data)

print("Successfully extracted Paper-Minecraft.sb3")
