
def is_not_start_byte(byte_int):
  # Check if the byte does not start with '10' (binary 10)
  return (byte_int & 0xC0) == 0x80
