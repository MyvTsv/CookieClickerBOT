class CookieString:
    
    def format_number(cls, number: str) -> int:
        units = {
            "million": 10**6,
            "billion": 10**9,
            "trillion": 10**12,
            "quadrillion": 10**15,
            "quintillion": 10**18,
            "sextillion": 10**21,
            "septillion": 10**24,
        }
        number = number.strip().lower().replace(",", "")
        for unit, value in units.items():
            if unit in number:
                numeric_part = number.split()[0].replace(",", "")
                try:
                    number_value = float(numeric_part) * value
                    return int(number_value)
                except ValueError:
                    raise ValueError(f"Invalid number format: {numeric_part}")
        return number