import os
import logging
import traceback

from django.http import JsonResponse

from .constants import LOGS_DIRECTORY
from .util import is_not_start_byte

ALLOWED_EXTENSIONS = ('.txt', '.log')
MAX_LINES = 50000
DEFAULT_LINES = 100

def get_log_filenames(request):
  files = os.listdir(LOGS_DIRECTORY)
  filtered_files = [file for file in files if file.endswith(ALLOWED_EXTENSIONS)]
  return JsonResponse({'files': filtered_files})

def get_log(request):
  filename = request.GET.get('filename')
  if not filename:
    return JsonResponse({'error': 'Must provide filename parameter'}, status=404)

  if not filename.endswith(ALLOWED_EXTENSIONS):
    return JsonResponse({'error': 'Param filename must have one of the extensions %s' % str(ALLOWED_EXTENSIONS)}, status=422)

  keyword = request.GET.get('keyword', '')
  case_sensitive = request.GET.get('c', '')
  if not case_sensitive:
    keyword = keyword.lower()

  str_n_lines = request.GET.get('n', str(DEFAULT_LINES))
  if not str_n_lines.isdigit():
    return JsonResponse({'error': 'Param n must be digit'}, status=422)
  n_lines = min(int(str_n_lines), MAX_LINES)

  # Only use base file name to prevent accessing relative path / other folders
  file_path = os.path.join(LOGS_DIRECTORY, os.path.basename(filename))
  logging.info("Reading file %s, keyword: %s, lines: %s", file_path, keyword, n_lines)

  try:
    with open(file_path, 'rb') as file:
      line_count = 0
      curr_line = ''
      lines_buffer = []

      file.seek(0, os.SEEK_END)
      curr_pos = file.tell()
      final_char = False

      # the file is empty, just return empty json response here by setting n_lines to -1
      if curr_pos == 0:
        n_lines = -1
      else:  
        # Move file cursor to 1 char before end of file, so we can read last char
        file.seek(-1, os.SEEK_CUR)

      while line_count < n_lines:
        byte_length = 1
        curr_bytes = file.read(1)

        # From https://en.wikipedia.org/wiki/UTF-8#Encoding
        # We assume this text file is encoded in UTF-8
        # UTF-8 chars can be up to 4 bytes, if the current byte is not a start byte
        # we need to iterate back 1 char further and potentially read multiple bytes
        # for a single character
        first_byte = int.from_bytes(curr_bytes, byteorder='big')

        while is_not_start_byte(first_byte) and byte_length < 4:
          byte_length = byte_length + 1
          file.seek(-byte_length, os.SEEK_CUR)
          curr_bytes = file.read(byte_length)
          first_byte = curr_bytes[0]

        # We assume this is UTF-8, to handle other encodings we could
        # read the first line of the file and guess (can't be certain) the encoding based off of presence of 
        # byte order marks and other languages, something like the implementation here
        # https://github.com/gignupg/Detect-File-Encoding-And-Language/blob/c21e9907436b62deab21e7803ae55d34b5a82dbc/src/index-node.js#L45
        curr_char = curr_bytes.decode('utf-8')

        if curr_char != '\n':
          curr_line = curr_char + curr_line

        curr_pos = file.tell()
        if curr_pos <= byte_length:
          # we've hit the final character, need to append the line
          final_char = True

        end_of_line = curr_char == '\n' or final_char 
        if end_of_line:
          if not case_sensitive:
            keyword_match_line = curr_line.lower()
          else:
            keyword_match_line = curr_line
          # if no keyword, the keyword match always returns true
          if curr_line and keyword in keyword_match_line:
            lines_buffer.append(curr_line)
            line_count = line_count + 1
          curr_line = ''

        if final_char:
          break  

        # move cursor back to 1 byte before the character we just read
        file.seek(-(byte_length + 1), os.SEEK_CUR)

      response_data = {
        'lines': line_count,
        'logs': lines_buffer
      }
      return JsonResponse(response_data)
  except FileNotFoundError:
      logging.error('Could not find file %s', filename)
      return JsonResponse({'error': 'File not found'}, status=404)
  except Exception as e:
      traceback.print_exc()
      logging.error("Unexpected error occured", e)
      return JsonResponse({'error': str(e)}, status=500)
