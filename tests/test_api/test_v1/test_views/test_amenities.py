#!/usr/bin/python3
"""
Contains TestAmenitiesApiDocs and TestAmenitiesApi classes
"""

import unittest
import requests
from api.v1.views import amenities

class TestAmenitiesApiDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""

    def test_pep8_conformance_amenities(self):
        """Test that api/v1/views/amenities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenities(self):
        """Test that tests/test_api/test_v1/test_views/test_amenities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_api/test_v1/test_views/test_amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenities_module_docstring(self):
        """Test for the amenities.py module docstring"""
        self.assertIsNot(amenities.__doc__, None,
                         "ameniies.py needs a docstring")
        self.assertTrue(len(amenities.__doc__) >= 1,
                        "amenities.py needs a docstring")

    def test_amenities_func_docstrings(self):
        """Test for the presence of docstrings in Amenities methods"""
        for func in self.amenities_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestAmeniteisApi(unittest.TestCase):
    """Tests to check the Amenities api module"""
    api_url = "http://127.0.0.1:5000/api/v1/views/amenities"

    def test
