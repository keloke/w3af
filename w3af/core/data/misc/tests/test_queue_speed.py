"""
test_queue_speed.py

Copyright 2013 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import unittest
import time
import Queue

from w3af.core.data.misc.queue_speed import QueueSpeed


class TestQueueSpeed(unittest.TestCase):
    
    def test_simple(self):
        q = QueueSpeed()
        
        self.assertEqual(None, q.get_input_rpm())
        self.assertEqual(None, q.get_output_rpm())
        
        for i in xrange(4):
            q.put(i)
            # 20 RPM
            time.sleep(3)
        
        self.assertEqual(q.qsize(), 4)
        
        self.assertGreater(q.get_input_rpm(), 19)
        self.assertLess(q.get_input_rpm(), 20)

        for i in xrange(4):
            q.get()
            # 60 RPM
            time.sleep(1)
                        
        self.assertGreater(q.get_output_rpm(), 59)
        self.assertLess(q.get_output_rpm(), 60)
        self.assertEqual(q.qsize(), 0)

    def test_no_data(self):
        q = QueueSpeed()
        
        for _ in xrange(10):
            self.assertEqual(None, q.get_input_rpm())
            self.assertEqual(None, q.get_output_rpm())
    
    def test_many_items(self):
        q = QueueSpeed()

        self.assertEqual(len(q._input_data), 0)
        
        for _ in xrange(q.MAX_SIZE * 2):
            q.put(None)
        
        self.assertEqual(len(q._input_data), q.MAX_SIZE - 1)
        self.assertEqual(len(q._output_data), 0)
        
        for _ in xrange(q.MAX_SIZE * 2):
            q.get()

        self.assertEqual(len(q._output_data), q.MAX_SIZE - 1)
    
    def test_exceptions(self):
        q = QueueSpeed(4)
        
        self.assertEqual(None, q.get_input_rpm())
        self.assertEqual(None, q.get_output_rpm())
        
        for i in xrange(4):
            q.put(i)
            # 20 RPM
            time.sleep(3)
        
        for _ in xrange(10):
            self.assertRaises(Queue.Full, q.put_nowait, None)
        
        self.assertEqual(q.qsize(), 4)
        
        self.assertGreater(q.get_input_rpm(), 19)
        self.assertLess(q.get_input_rpm(), 20)

        for i in xrange(4):
            q.get()
            # 60 RPM
            time.sleep(1)

        for _ in xrange(10):
            self.assertRaises(Queue.Empty, q.get_nowait)
        
        self.assertGreater(q.get_output_rpm(), 59)
        self.assertLess(q.get_output_rpm(), 60)
        self.assertEqual(q.qsize(), 0)
    
    def test_wrapper(self):
        q = QueueSpeed(4)
        self.assertEqual(q.qsize(), 0)
        
        q.put(None)
        
        self.assertEqual(q.qsize(), 1)
        
        q.get()
        
        self.assertEqual(q.qsize(), 0)
