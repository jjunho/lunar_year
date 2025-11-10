#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for lunar.py module
"""

import unittest
import sys
from io import StringIO
from lunar import LunarYear, main


class TestLunarYear(unittest.TestCase):
    """Test cases for the LunarYear class"""
    
    def test_init_valid_year(self):
        """Test initialization with valid years"""
        lunar = LunarYear(2024)
        self.assertEqual(lunar.gregorian_year, 2024)
        self.assertEqual(lunar.year_in_cycle, 41)
        
    def test_init_string_year(self):
        """Test initialization with string year (should convert)"""
        lunar = LunarYear("2024")
        self.assertEqual(lunar.gregorian_year, 2024)
        
    def test_init_year_too_low(self):
        """Test initialization with year below minimum"""
        with self.assertRaises(ValueError) as context:
            LunarYear(3)
        self.assertIn("must be between", str(context.exception))
        
    def test_init_year_too_high(self):
        """Test initialization with year above maximum"""
        with self.assertRaises(ValueError) as context:
            LunarYear(10000)
        self.assertIn("must be between", str(context.exception))
        
    def test_init_invalid_type(self):
        """Test initialization with invalid type"""
        with self.assertRaises(TypeError) as context:
            LunarYear("not_a_year")
        self.assertIn("must be an integer", str(context.exception))
        
    def test_cycle_calculation_first_year(self):
        """Test cycle calculation for first year (year 4)"""
        lunar = LunarYear(4)
        self.assertEqual(lunar.year_in_cycle, 1)
        
    def test_cycle_calculation_full_cycle(self):
        """Test that year 64 maps to position 1 (new cycle)"""
        lunar = LunarYear(64)
        self.assertEqual(lunar.year_in_cycle, 1)
        
    def test_cycle_calculation_end_of_cycle(self):
        """Test that year 63 maps to position 60 (end of cycle)"""
        lunar = LunarYear(63)
        self.assertEqual(lunar.year_in_cycle, 60)
        
    def test_lang_chinese(self):
        """Test getting Chinese name"""
        lunar = LunarYear(2024)
        result = lunar.lang('chi')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'jiǎ-chén')
        self.assertEqual(result[1], '甲辰')
        
    def test_lang_korean(self):
        """Test getting Korean name"""
        lunar = LunarYear(2024)
        result = lunar.lang('kor')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'gapjin 갑진')
        self.assertEqual(result[1], '甲辰')
        
    def test_lang_japanese(self):
        """Test getting Japanese name"""
        lunar = LunarYear(2024)
        result = lunar.lang('jap')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'kōshin/kinoe-tatsu')
        self.assertEqual(result[1], '甲辰')
        
    def test_lang_vietnamese(self):
        """Test getting Vietnamese name"""
        lunar = LunarYear(2024)
        result = lunar.lang('viet')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'Giáp Thìn')
        self.assertEqual(result[1], '甲辰')
        
    def test_lang_english(self):
        """Test getting English name"""
        lunar = LunarYear(2024)
        result = lunar.lang('eng')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'Yang Wood Dragon')
        self.assertEqual(result[1], '甲辰')
        
    def test_lang_invalid_language(self):
        """Test with invalid language code"""
        lunar = LunarYear(2024)
        with self.assertRaises(ValueError) as context:
            lunar.lang('invalid')
        self.assertIn("not supported", str(context.exception))
        
    def test_supported_languages(self):
        """Test that all supported languages are accessible"""
        lunar = LunarYear(2024)
        for lang in LunarYear.SUPPORTED_LANGUAGES:
            result = lunar.lang(lang)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 2)
            
    def test_various_years(self):
        """Test various years to ensure correct cycle calculation"""
        test_cases = [
            (1984, 1),   # Year from table
            (1985, 2),
            (2020, 37),
            (2025, 42),
            (2043, 60),  # Last year in cycle
            (2044, 1),   # Start of new cycle
        ]
        
        for year, expected_position in test_cases:
            with self.subTest(year=year):
                lunar = LunarYear(year)
                self.assertEqual(lunar.year_in_cycle, expected_position)
                
    def test_year_2025_english(self):
        """Test current year (2025) returns correct English name"""
        lunar = LunarYear(2025)
        result = lunar.lang('eng')
        self.assertEqual(result[0], 'Yin Wood Snake')
        self.assertEqual(result[1], '乙巳')


class TestMainFunction(unittest.TestCase):
    """Test cases for the main() function"""
    
    def test_main_with_valid_args(self):
        """Test main function with valid arguments"""
        sys.argv = ['lunar.py', '2024', 'eng']
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn('Yang Wood Dragon', output)
            self.assertIn('甲辰', output)
        finally:
            sys.stdout = sys.__stdout__
            
    def test_main_with_help(self):
        """Test main function with --help flag"""
        sys.argv = ['lunar.py', '--help']
        
        with self.assertRaises(SystemExit) as context:
            main()
        # argparse exits with 0 for --help
        self.assertEqual(context.exception.code, 0)
        
    def test_main_with_invalid_year(self):
        """Test main function with invalid year"""
        sys.argv = ['lunar.py', '10000', 'eng']
        
        # Capture stderr
        captured_error = StringIO()
        sys.stderr = captured_error
        
        try:
            with self.assertRaises(SystemExit) as context:
                main()
            self.assertEqual(context.exception.code, 1)
            error_output = captured_error.getvalue()
            self.assertIn('Error:', error_output)
        finally:
            sys.stderr = sys.__stderr__


class TestTableIntegrity(unittest.TestCase):
    """Test cases to verify the sexagenary cycle table integrity"""
    
    def test_table_has_60_entries(self):
        """Test that the table has exactly 60 entries"""
        lunar = LunarYear(2024)
        table = lunar._TABLE
        self.assertEqual(len(table), 60)
        
    def test_table_sequential_keys(self):
        """Test that table keys are sequential from 1 to 60"""
        lunar = LunarYear(2024)
        table = lunar._TABLE
        expected_keys = {i for i in range(1, 61)}
        actual_keys = set(table.keys())
        self.assertEqual(actual_keys, expected_keys)
        
    def test_all_entries_have_required_languages(self):
        """Test that all table entries have all required language fields"""
        lunar = LunarYear(2024)
        table = lunar._TABLE
        required_langs = LunarYear.SUPPORTED_LANGUAGES
        
        for position, data in table.items():
            with self.subTest(position=position):
                for lang in required_langs:
                    self.assertIn(lang, data)
                    self.assertIsInstance(data[lang], list)
                    self.assertEqual(len(data[lang]), 2)
    
    def test_table_loaded_once(self):
        """Test that table is loaded once and shared across instances"""
        lunar1 = LunarYear(2024)
        lunar2 = LunarYear(2025)
        # Should be the same object in memory
        self.assertIs(lunar1._TABLE, lunar2._TABLE)


if __name__ == '__main__':
    unittest.main()
