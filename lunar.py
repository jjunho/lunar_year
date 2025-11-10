#!/usr/bin/env python3
# encoding: utf-8
"""
module lunar.py

Calculates the lunar year from a Gregorian year and
displays the year's name in Chinese, Korean, Japanese,
Vietnamese and English.

Usage:

python lunar.py [gregorian year] [language]

[gregorian year] in numbers
[language] as chi, kor, jap, viet, eng
"""

from typing import Dict, List
import argparse
import sys


class LunarYear:
    """
    Builds a Lunar Year table with the years' names in
    Chinese, Korean, Japanese, Vietnamese and English.
    """
    
    # Supported languages for lunar year display
    SUPPORTED_LANGUAGES = {'chi', 'kor', 'jap', 'viet', 'eng'}
    
    # Valid year range for the sexagenary cycle calculation
    MIN_YEAR = 4  # First year in the cycle
    MAX_YEAR = 9999  # Practical upper limit
    
    # Class-level table loaded once
    _TABLE = None
    
    def __init__(self, gregorian_year: int) -> None:
        """
        Instantiate the class with a Gregorian year.
        
        Args:
            gregorian_year: A Gregorian calendar year (integer)
            
        Raises:
            ValueError: If year is outside valid range
            TypeError: If year is not an integer
        """
        # Normalize to int
        try:
            gregorian_year = int(gregorian_year)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Year must be an integer, got {type(gregorian_year).__name__}") from e
        
        # Validate range
        if not self.MIN_YEAR <= gregorian_year <= self.MAX_YEAR:
            raise ValueError(
                f"Year must be between {self.MIN_YEAR} and {self.MAX_YEAR}, got {gregorian_year}"
            )
        
        self.gregorian_year = gregorian_year
        
        # Calculate position in 60-year cycle (1-60)
        # Formula from Wikipedia (http://en.wikipedia.org/wiki/Sexagenary_cycle)
        self.year_in_cycle = ((gregorian_year - 4) % 60) + 1
        
        # Load table once at class level
        if LunarYear._TABLE is None:
            LunarYear._TABLE = self._get_year()

    def lang(self, lang: str) -> List[str]:
        """
        Choose the language to display:
        chi:  Chinese
        kor:  Korean
        jap:  Japanese
        viet: Vietnamese
        eng:  English
        
        Args:
            lang: Language code (chi, kor, jap, viet, or eng)
            
        Returns:
            List containing [language_name, hanja_characters]
            
        Raises:
            ValueError: If language is not supported
        """
        if lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Language '{lang}' not supported. Choose from: {', '.join(sorted(self.SUPPORTED_LANGUAGES))}"
            )
        
        return self._TABLE[self.year_in_cycle][lang]

    @staticmethod
    def _get_year() -> Dict[int, Dict[str, List[str]]]:
        """
        Parse the sexagenary cycle table and return a dictionary.
        
        Returns:
            Dictionary mapping cycle position to language-specific year names
        """
        # from wikipedia (http://en.wikipedia.org/wiki/Sexagenary_cycle)
        table = u"""\
        1	甲子	jiǎ-zǐ	gapja 갑자	kōshi(kasshi)/kinoe-ne	Giáp Tý	Yang Wood Rat	4	57	1984
        2	乙丑	yǐ-chǒu	eulchuk 을축	itchū/kinoto-ushi	Ất Sửu	Yin Wood Ox	5	56	1985
        3	丙寅	bǐng-yín	byeongin 병인	heiin/hinoe-tora	Bính Dần	Yang Fire Tiger	6	55	1986
        4	丁卯	dīng-mǎo	jeongmyo 정묘	teibō/hinoto-u	Đinh Mão	Yin Fire Rabbit	7	54	1987
        5	戊辰	wù-chén	mujin 무진	boshin/tsuchinoe-tatsu	Mậu Thìn	Yang Earth Dragon	8	53	1988
        6	己巳	jǐ-sì	gisa 기사	kishi/tsuchinoto-mi	Kỷ Tỵ	Yin Earth Snake	9	52	1989
        7	庚午	gēng-wǔ	gyeongo 경오	kōgo/kanoe-uma	Canh Ngọ	Yang Metal Horse	10	51	1990
        8	辛未	xīn-wèi	shinmi 신미	shinbi/kanoto-hitsuji	Tân Mùi	Yin Metal Goat	11	50	1991
        9	壬申	rén-shēn	imshin 임신	jinshin/mizunoe-saru	Nhâm Thân	Yang Water Monkey	12	49	1992
        10	癸酉	guǐ-yǒu	gyeyu 계유	kiyū/mizunoto-tori	Quý Dậu	Yin Water Rooster	13	48	1993
        11	甲戌	jiǎ-xū	gapsul 갑술	kōjutsu/kinoe-inu	Giáp Tuất	Yang Wood Dog	14	47	1994
        12	乙亥	yǐ-hài	eulhae 을해	itsugai/kinoto-i	Ât Hợi	Yin Wood Pig	15	46	1995
        13	丙子	bǐng-zǐ	byeongja 병자	heishi/hinoe-ne	Bính Tý	Yang Fire Rat	16	45	1996
        14	丁丑	dīng-chǒu	jeongchuk 정축	teichū/hinoto-ushi	Đinh Sửu	Yin Fire Ox	17	44	1997
        15	戊寅	wù-yín	muin 무인	boin/tsuchinoe-tora	Mậu Dần	Yang Earth Tiger	18	43	1998
        16	己卯	jǐ-mǎo	gimyo 기묘	kibō/tsuchinoto-u	Kỷ Mão	Yin Earth Rabbit	19	42	1999
        17	庚辰	gēng-chén	gyeongjin 경진	kōshin/kanoe-tatsu	Canh Thìn	Yang Metal Dragon	20	41	2000
        18	辛巳	xīn-sì	shinsa 신사	shinshi/kanoto-mi	Tân Tỵ	Yin Metal Snake	21	40	2001
        19	壬午	rén-wǔ	imo 임오	jingo/mizunoe-uma	Nhâm Ngọ	Yang Water Horse	22	39	2002
        20	癸未	guǐ-wèi	gyemi 계미	kibi/mizunoto-hitsuji	Quý Mùi	Yin Water Goat	23	38	2003
        21	甲申	jiǎ-shēn	gapshin 갑신	kōshin/kinoe-saru	Giáp Thân	Yang Wood Monkey	24	37	2004
        22	乙酉	yǐ-yǒu	eulyu 을유	itsuyū/kinoto-tori	Ất Dậu	Yin Wood Rooster	25	36	2005
        23	丙戌	bǐng-xū	byeongsul 병술	heijutsu/hinoe-inu	Bính Tuất	Yang Fire Dog	26	35	2006
        24	丁亥	dīng-hài	jeonghae 정해	teigai/hinoto-i	Đinh Hợi	Yin Fire Pig	27	34	2007
        25	戊子	wù-zǐ	muja 무자	boshi/tsuchinoe-ne	Mậu Tý	Yang Earth Rat	28	33	2008
        26	己丑	jǐ-chǒu	gichuk 기축	kichū/tsuchinoto-ushi	Kỷ Sửu	Yin Earth Ox	29	32	2009
        27	庚寅	gēng-yín	gyeongin 경인	kōin/kanoe-tora	Canh Dần	Yang Metal Tiger	30	31	2010
        28	辛卯	xīn-mǎo	shinmyo 신묘	shinbō/kanoto-u	Tân Mão	Yin Metal Rabbit	31	30	2011
        29	壬辰	rén-chén	imjin 임진	jinshin/mizunoe-tatsu	Nhâm Thìn	Yang Water Dragon	32	29	2012
        30	癸巳	guǐ-sì	gyesa 계사	kishi/mizunoto-mi	Quý Tỵ	Yin Water Snake	33	28	2013
        31	甲午	jiǎ-wǔ	gapo 갑오	kōgo/kinoe-uma	Giáo Ngọ	Yang Wood Horse	34	27	2014
        32	乙未	yǐ-wèi	eulmi 을미	itsubi/kinoto-hitsuji	Ất Mùi	Yin Wood Goat	35	26	2015
        33	丙申	bǐng-shēn	byeongshin 병신	heishin/hinoe-saru	Bính Thân	Yang Fire Monkey	36	25	2016
        34	丁酉	dīng-yǒu	jeongyu 정유	teiyū/hinoto-tori	Đinh Dậu	Yin Fire Rooster	37	24	2017
        35	戊戌	wù-xū	musul 무술	bojutsu/tsuchinoe-inu	Mậu Tuất	Yang Earth Dog	38	23	2018
        36	己亥	jǐ-hài	gihae 기해	kigai/tsuchinoto-i	Kỷ Hợi	Yin Earth Pig	39	22	2019
        37	庚子	gēng-zǐ	gyeongja 경자	kōshi/kanoe-ne	Canh Tý	Yang Metal Rat	40	21	2020
        38	辛丑	xīn-chǒu	shinchuk 신축	shinchū/kanoto-ushi	Tân Sửu	Yin Metal Ox	41	20	2021
        39	壬寅	rén-yín	imin 임인	jin'in/mizunoe-tora	Nhâm Dần	Yang Water Tiger	42	19	2022
        40	癸卯	guǐ-mǎo	gyemyo 계묘	kibō/mizunoto-u	Quý Mão	Yin Water Rabbit	43	18	2023
        41	甲辰	jiǎ-chén	gapjin 갑진	kōshin/kinoe-tatsu	Giáp Thìn	Yang Wood Dragon	44	17	2024
        42	乙巳	yǐ-sì	eulsa 을사	itsushi/kinoto-mi	Ất Tỵ	Yin Wood Snake	45	16	2025
        43	丙午	bǐng-wǔ	byeongo 병오	heigo/hinoe-uma	Bính Ngọ	Yang Fire Horse	46	15	2026
        44	丁未	dīng-wèi	jeongmi 정미	teibi/hinoto-hitsuji	Đinh Mùi	Yin Fire Goat	47	14	2027
        45	戊申	wù-shēn	mushin 무신	boshin/tsuchinoe-saru	Mậu Thân	Yang Earth Monkey	48	13	2028
        46	己酉	jǐ-yǒu	giyu 기유	kiyū/tsuchinoto-tori	Kỷ Dậu	Yin Earth Rooster	49	12	2029
        47	庚戌	gēng-xū	gyeongsul 경술	kōjutsu/kanoe-inu	Canh Tuất	Yang Metal Dog	50	11	2030
        48	辛亥	xīn-hài	shinhae 신해	shingai/kanoto-i	Tân Hợi	Yin Metal Pig	51	10	2031
        49	壬子	rén-zǐ	imja 임자	jinshi/mizunoe-ne	Nhâm Tý	Yang Water Rat	52	9	2032
        50	癸丑	guǐ-chǒu	gyechuk 계축	kichū/mizunoto-ushi	Quý Sửu	Yin Water Ox	53	8	2033
        51	甲寅	jiǎ-yín	gapin 갑인	kōin/kinoe-tora	Giáp Dần	Yang Wood Tiger	54	7	2034
        52	乙卯	yǐ-mǎo	eulmyo 을묘	itsubō/kinoto-u	Ất Mão	Yin Wood Rabbit	55	6	2035
        53	丙辰	bǐng-chén	byeongjin 병진	heishin/hinoe-tatsu	Bính Thìn	Yang Fire Dragon	56	5	2036
        54	丁巳	dīng-sì	jeongsa 정사	teishi/hinoto-mi	Đinh Tỵ	Yin Fire Snake	57	4	2037
        55	戊午	wù-wǔ	muo 무오	bogo/tsuchinoe-uma	Mậu Ngọ	Yang Earth Horse	58	3	2038
        56	己未	jǐ-wèi	gimi 기미	kibi/tsuchinoto-hitsuji	Kỷ Mùi	Yin Earth Goat	59	2	2039
        57	庚申	gēng-shēn	gyeongshin 경신	kōshin/kanoe-saru	Canh Thân	Yang Metal Monkey	60	1	2040
        58	辛酉	xīn-yǒu	shinyu 신유	shin'yū/kanoto-tori	Tân Dậu	Yin Metal Rooster	1	60	2041
        59	壬戌	rén-xū	imsul 임술	jinjutsu/mizunoe-inu	Nhâm Tuất	Yang Water Dog	2	59	2042
        60	癸亥	guǐ-hài	gyehae 계해	kigai/mizunoto-i	Quý Hợi	Yin Water Pig	3	58	2043
        """.strip()

        lunar_table = {}
        for line in table.split('\n'):
            try:
                parts = line.strip().split('\t')
                year_order = int(parts[0])
                hanja = parts[1]
                
                # Build entry with shared hanja (DRY principle)
                lunar_table[year_order] = {
                    'chi': [parts[2], hanja],
                    'kor': [parts[3], hanja],
                    'jap': [parts[4], hanja],
                    'viet': [parts[5], hanja],
                    'eng': [parts[6], hanja]
                }
            except (ValueError, IndexError):
                pass

        return lunar_table


def main() -> None:
    """
    Main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description='Calculate lunar year from Gregorian year and display in various languages.',
        epilog='Example: %(prog)s 2024 chi'
    )
    
    parser.add_argument(
        'year',
        type=int,
        help=f'Gregorian year ({LunarYear.MIN_YEAR}-{LunarYear.MAX_YEAR})'
    )
    
    parser.add_argument(
        'language',
        choices=sorted(LunarYear.SUPPORTED_LANGUAGES),
        help='Language for output (chi=Chinese, kor=Korean, jap=Japanese, viet=Vietnamese, eng=English)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0'
    )
    
    try:
        args = parser.parse_args()
        lunar_year = LunarYear(args.year)
        result = lunar_year.lang(args.language)
        print('\t'.join(result))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
