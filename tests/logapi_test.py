import json
import os
import unittest

from django.test import TestCase

class LogApiTestCase(TestCase):

  def test_log_api_endpoint(self):
    response = self.client.get('/api/log/', {'filename': 'test.log'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    # file has 10 lines total
    self.assertEqual(response_dict['lines'], 10)
    self.assertEqual(len(response_dict['logs']), 10)
    self.assertEqual(response_dict['logs'][0], 'Test line 10')
    self.assertEqual(response_dict['logs'][9], 'Test line 1')

  def test_log_api_n_lines_param(self):
    response = self.client.get('/api/log/', {'filename': 'test.log', 'n': 5})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 5)
    self.assertEqual(len(response_dict['logs']), 5)
    self.assertEqual(response_dict['logs'][0], 'Test line 10')
    self.assertEqual(response_dict['logs'][4], 'Test line 6')

  def test_log_api_single_char(self):
    response = self.client.get('/api/log/', {'filename': 'single_char.log'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 1)
    self.assertEqual(response_dict['logs'][0], '')

  def test_log_api_empty_file(self):
    response = self.client.get('/api/log/', {'filename': 'empty.log'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 0)
    self.assertEqual(len(response_dict['logs']), 0)

  def test_log_api_single_line(self):
    response = self.client.get('/api/log/', {'filename': 'single_line.log'})
    self.assertEqual(response.status_code, 200)
    response_dict = json.loads(response.content)
    self.assertEqual(response_dict['lines'], 1)
    self.assertEqual(response_dict['logs'][0], 'single line test')    

    

    