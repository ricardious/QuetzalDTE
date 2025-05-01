import re


class Validator:
    def validate_nit(self, nit: str) -> bool:
        if not nit:
            return False
        cleaned = nit.replace("-", "").replace(" ", "").upper()
        if not (cleaned.isdigit() or (cleaned[:-1].isdigit() and cleaned[-1] == "K")):
            return False

        check = cleaned[-1]
        number = cleaned[:-1]
        if check == "K":
            check_val = 10
        else:
            check_val = int(check)

        total = 0
        for idx, digit_char in enumerate(reversed(number), start=2):
            total += int(digit_char) * idx
        remainder = total % 11
        computed = (11 - remainder) % 11

        return computed == check_val
