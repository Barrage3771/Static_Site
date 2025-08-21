import unittest
from extract_markdown import extract_title

class TestExtraction(unittest.TestCase):
    
    
    def test_regular_title(self):
        md = """

# this is my title line!

and these are my other lines.

"""

        document = extract_title(md)
        
        self.assertEqual("this is my title line!", document)
        
    
    def test_no_title(self):
        
        md="""

There is no title in here

at all nothing.

"""
        self.assertRaises(Exception, extract_title, md)
        
        
        """
        
        can also be written as
        with self.assertRaises(Exception):
            extract_title(md)
        
        """
        
    
    def test_edge_case(self):
        
        md = """

The title isnt here

nor is it here

# but its here

        
"""

        document = extract_title(md)
        self.assertEqual("but its here", document)