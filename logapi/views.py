import os
import logging

from django.http import JsonResponse

from .constants import LOGS_DIRECTORY

ALLOWED_EXTENSIONS = ('.txt', '.log')

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
  str_n_lines = request.GET.get('n', '100')
  if not str_n_lines.isdigit():
    return JsonResponse({'error': 'Param n must be digit'}, status=422)
  last_n_lines = int(str_n_lines)

  file_path = os.path.join(LOGS_DIRECTORY, filename)
  logging.info("Reading file %s, keyword: %s, lines: %s", file_path, keyword, last_n_lines)

  try:
    with open(file_path, 'rb') as file:
      line_count = 0
      curr_line = ''
      lines_buffer = []

      file.seek(0, os.SEEK_END)
      curr_pos = file.tell()
      final_char = False

      # the file is empty, just return empty json response here by setting last_n_lines to -1
      if curr_pos == 0:
        last_n_lines = -1
      else:  
        # Move file cursor to 1 char before end of file, so we can read last char
        file.seek(-1, os.SEEK_CUR)

      while line_count < last_n_lines:
        curr_byte = file.read(1)
        # TODO Support encodings with more than 1 byte per char, ie non ascii, japanese
        curr_char = curr_byte.decode('utf-8')
        curr_pos = file.tell()

        if curr_char != '\n':
          curr_line = curr_char + curr_line

        if curr_pos == 1:
          # we've hit the final character, need to append the line
          final_char = True

        append_line = curr_char == '\n' or final_char 
        if append_line:
          if curr_line and (not keyword or keyword.lower() in curr_line.lower()):
            lines_buffer.append(curr_line)
            line_count = line_count + 1
          curr_line = ''

        if final_char:
          break  

        # move back max of 2 bytes since on above file.read(1) we iterate 1 forwards
        # so every iteration of while loop our cursor -2+1=-1 byte backwards
        file.seek(-2, os.SEEK_CUR)    

      response_data = {
        'lines': line_count,
        'logs': lines_buffer
      }
      return JsonResponse(response_data)
  except FileNotFoundError:
      return JsonResponse({'error': 'File not found'}, status=404)
  except Exception as e:
      logging.error('An unexpected error occured', e)
      return JsonResponse({'error': str(e)}, status=500)
