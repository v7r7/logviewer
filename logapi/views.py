import os
import logging
import traceback

from django.http import JsonResponse

from .constants import LOGS_DIRECTORY

def get_log(request):
    filename = request.GET.get('filename', 'default.log')
    keyword = request.GET.get('keyword', '')
    last_n_lines = int(request.GET.get('n', 100))
    file_path = os.path.join(LOGS_DIRECTORY, filename)
    logging.info("Reading file %s, keyword: %s, lines: %s", file_path, keyword, last_n_lines)

    try:
        with open(file_path, 'rb') as file:
          line_count = 0
          curr_line = ''
          lines_buffer = []
          
          file.seek(0, os.SEEK_END)
          curr_pos = file.tell()

          # the file is empty, just return empty json response here by setting last_n_lines to -1
          if curr_pos == 0:
            last_n_lines = -1
          else:  
            final_char = curr_pos == 1
            # Move file cursor to 1 char before end of file, so we can read last char
            file.seek(-1, os.SEEK_CUR)

          while line_count < last_n_lines:
            curr_char = file.read(1)
            # TODO Support encodings with more than 1 byte per char, ie UTF-16 or japanese
            curr_char = curr_char.decode('utf-8')

            # if hit newline, determine whether it passes keyword filter before appending to return
            if curr_char == '\n' or final_char:
              if not keyword or keyword in curr_line:
                lines_buffer.append(curr_line)
                line_count = line_count + 1
              curr_line = ''
              if final_char:
                break
            else:
              curr_line = curr_char + curr_line

            curr_pos = file.tell()
            if curr_pos == 1:
              # we've hit the final character, on next iteration, ignore the char read, and
              # append the line to our buffer to return the final output
              final_char = True
            else:
              # move back max of 2 char since on above file.read(1) we iterate 1 forwards
              # so every iteration of while loop our cursor -2+1
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
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)