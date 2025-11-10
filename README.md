# Lunar Year Calculator

Calculates the position of a year in the [sexagenary cycle](https://en.wikipedia.org/wiki/Sexagenary_cycle) and displays the lunar year name in Chinese, Japanese, Korean, Vietnamese, and English.

## Features

- Convert Gregorian years to lunar year names
- Support for 5 languages: Chinese, Korean, Japanese, Vietnamese, and English
- Full 60-year sexagenary cycle coverage
- Type hints and modern Python 3 code
- Comprehensive error handling and input validation
- Command-line interface with help documentation

## Installation

No external dependencies required. Just clone and run:

```bash
git clone https://github.com/jjunho/lunar_year.git
cd lunar_year
```

## Usage

### Command Line

```bash
python lunar.py <year> <language>
```

**Arguments:**

- `year`: Gregorian year (4-9999)
- `language`: One of `chi`, `kor`, `jap`, `viet`, `eng`

**Examples:**

```bash
# Get Chinese name for 2025
python lunar.py 2025 chi
# Output: yǐ-sì  乙巳

# Get English name for 2024
python lunar.py 2024 eng
# Output: Yang Wood Dragon  甲辰

# Get Korean name for 2020
python lunar.py 2020 kor
# Output: gyeongja 경자  庚子

# Show help
python lunar.py --help

# Show version
python lunar.py --version
```

### As a Python Module

```python
from lunar import LunarYear

# Create lunar year object
lunar = LunarYear(2025)

# Get name in different languages
chinese = lunar.lang('chi')    # ['yǐ-sì', '乙巳']
korean = lunar.lang('kor')     # ['eulsa 을사', '乙巳']
japanese = lunar.lang('jap')   # ['itsushi/kinoto-mi', '乙巳']
vietnamese = lunar.lang('viet') # ['Ất Tỵ', '乙巳']
english = lunar.lang('eng')    # ['Yin Wood Snake', '乙巳']

# Access cycle information
print(lunar.gregorian_year)    # 2025
print(lunar.year_in_cycle)     # '42'
```

## Language Codes

| Code | Language   | Example Output         |
|------|------------|------------------------|
| chi  | Chinese    | jiǎ-chén 甲辰          |
| kor  | Korean     | gapjin 갑진 甲辰       |
| jap  | Japanese   | kōshin/kinoe-tatsu 甲辰|
| viet | Vietnamese | Giáp Thìn 甲辰         |
| eng  | English    | Yang Wood Dragon 甲辰  |

## The Sexagenary Cycle

The sexagenary cycle (干支) is a 60-year calendrical cycle used historically in China and other East Asian countries. Each year is named by combining:

- One of 10 Celestial Stems (天干)
- One of 12 Earthly Branches (地支)

The cycle has been used for over 3,000 years for dating purposes and is still widely recognized in East Asian cultures.

## Valid Year Range

- **Minimum:** Year 4 AD (start of first documented cycle)
- **Maximum:** Year 9999 (practical upper limit)

## Error Handling

The program validates inputs and provides clear error messages:

```bash
# Invalid year
python lunar.py 10000 eng
# Error: Year must be between 4 and 9999, got 10000

# Invalid language
python lunar.py 2025 spanish
# Error: argument language: invalid choice: 'spanish' (choose from 'chi', 'eng', 'jap', 'kor', 'viet')

# Missing arguments
python lunar.py 2025
# Error: the following arguments are required: language
```

## Testing

Run the comprehensive test suite:

```bash
python -m pytest test_lunar.py -v
```

Test coverage includes:

- Input validation (years, languages)
- Cycle calculation accuracy
- All language outputs
- Edge cases (cycle boundaries)
- CLI functionality
- Table integrity

## Development

The code follows modern Python best practices:

- Python 3.6+ with type hints
- Comprehensive docstrings
- Input validation and error handling
- argparse for robust CLI
- Full unit test coverage

## License

This project is open source and available for use and modification.

## References

- [Sexagenary Cycle - Wikipedia](https://en.wikipedia.org/wiki/Sexagenary_cycle)
- Data sourced from Wikipedia's sexagenary cycle tables
