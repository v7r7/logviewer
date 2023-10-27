import json
import os
import unittest

from django.test import TestCase

class LogApiTestCase(TestCase):

  def test_log_api(self):
    response = self.client.get('/api/log/', {'filename': 'test.txt'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    # file has 10 lines total
    self.assertEqual(response_dict['lines'], 10)
    self.assertEqual(len(response_dict['logs']), 10)
    self.assertEqual(response_dict['logs'][0], 'Test line 10')
    self.assertEqual(response_dict['logs'][9], 'Test line 1')

  def test_log_api_n_lines_param(self):
    response = self.client.get('/api/log/', {'filename': 'test.txt', 'n': 5})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 5)
    self.assertEqual(len(response_dict['logs']), 5)
    self.assertEqual(response_dict['logs'][0], 'Test line 10')
    self.assertEqual(response_dict['logs'][4], 'Test line 6')

  def test_log_api_single_char(self):
    response = self.client.get('/api/log/', {'filename': 'single_char.txt'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 1)
    self.assertEqual(response_dict['logs'][0], '')

  def test_log_api_empty_file(self):
    response = self.client.get('/api/log/', {'filename': 'empty.txt'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 0)
    self.assertEqual(len(response_dict['logs']), 0)

  def test_log_api_single_line(self):
    response = self.client.get('/api/log/', {'filename': 'single_line.txt'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 1)
    self.assertEqual(response_dict['logs'][0], 'single line test')    

  def test_files_api(self):
    response = self.client.get('/api/logs/')
    response_dict = json.loads(response.content)
    self.assertEqual(set(response_dict['files']), set(['empty.txt', 'test.txt', 'single_line.txt', 'single_char.txt']))
