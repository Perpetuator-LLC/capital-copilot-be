# """
# Copyright (c) 2024 eContriver LLC
#
# This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
# See the LICENSE file in the root of this project for the full license text.
# """
#
# import logging
# import os
# from django.test import TestCase
# from pathlib import Path
# from unittest.mock import patch
# from .logging_service import LoggingService
#
# class LoggingServiceTests(TestCase):
#
#     def setUp(self):
#         # Create a temporary directory for log files during the tests
#         self.temp_log_dir = Path(os.path.join(os.path.dirname(__file__), 'test_logs'))
#         self.temp_log_dir.mkdir(exist_ok=True)
#
#     def tearDown(self):
#         # Cleanup the temporary directory after tests
#         for file in self.temp_log_dir.iterdir():
#             file.unlink()
#         self.temp_log_dir.rmdir()
#
#     def test_logging_configuration(self):
#         with patch('copilot.logging_service.HandlersManager') as mock_handler_manager:
#             LoggingService.configure_logging(output_dir=str(self.temp_log_dir))
#
#             # Verify that HandlersManager was called with expected arguments
#             mock_handler_manager.assert_called_once()
#             args, kwargs = mock_handler_manager.call_args
#             self.assertIn("file", args[0])  # Checking if 'file' is in the channels list
#             self.assertIn("stdout", args[0])  # Checking if 'stdout' is in the channels list
#
#             # Additional checks can be made here depending on the implementation of HandlersManager
#
#     def test_file_logging(self):
#         with self.assertLogs(level='DEBUG') as log:
#             LoggingService.configure_logging(output_dir=str(self.temp_log_dir))
#             logging.debug('Test debug log')
#
#             # Verify that a log file was created
#             log_files = list(self.temp_log_dir.glob('*.log'))
#             self.assertTrue(len(log_files) > 0, "Log file was not created")
#
#             # Verify that the log message is in the file
#             with open(log_files[0], 'r') as log_file:
#                 file_content = log_file.read()
#                 self.assertIn('Test debug log', file_content)
#
#     # def test_stdout_logging(self):
#     #     with self.assertLogs(level='DEBUG') as log:
#     #         LoggingService.configure_logging({'stdout': logging.DEBUG})
#     #         logging.debug('Test debug log')
#     #
#     #         # Verify that the log message was captured
#     #         self.assertIn('Test debug log', log.output[0])
#
#     def test_stdout_logging(self):
#         with self.assertLogs(level='DEBUG') as log:
#             LoggingService.configure_logging({'stdout': logging.DEBUG})
#             logging.debug('Test debug log')
#
#             # Check if StreamHandler is attached and set to DEBUG
#             root_logger = logging.getLogger()
#             stream_handlers = [handler for handler in root_logger.handlers if isinstance(handler,
#             logging.StreamHandler)]
#             self.assertTrue(any(handler.level == logging.DEBUG for handler in stream_handlers), "No StreamHandler at
#             DEBUG level.")
#
#             # Verify that the log message was captured
#             self.assertTrue(any('Test debug log' in record for record in log.records), "Log message 'Test debug log'
#             not found in captured records.")
#
