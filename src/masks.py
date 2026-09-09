def get_mask_card_number(card_string: str) -> str:
    if not isinstance(card_string, str):
        return card_string

    i = 0
    n = len(card_string)
    start = -1
    length = 0

    while i < n:
        if card_string[i].isdigit():
            if start == -1:
                start = i
            length += 1
        else:
            if start != -1:
                if 13 <= length <= 19:
                    break
                start = -1
                length = 0
        i += 1

    if start == -1 or not (13 <= length <= 19):
        return card_string

    digits = card_string[start: start + length]
    masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    return card_string[:start] + masked + card_string[start + length:]


def get_mask_account(account_string: str) -> str:
    if not isinstance(account_string, str):
        return account_string

    i = 0
    n = len(account_string)
    start = -1
    length = 0

    while i < n:
        if account_string[i].isdigit():
            if start == -1:
                start = i
            length += 1
        else:
            if start != -1:
                if length == 20:
                    break
                start = -1
                length = 0
        i += 1

    if start != -1 and length == 20:
        digits = account_string[start: start + 20]
        masked = f"**{digits[-4:]}"
        return account_string[:start] + masked + account_string[start + 20:]

    return account_string
