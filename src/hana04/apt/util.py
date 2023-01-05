def capitalize_first_letter(s: str):
    if s[0].islower():
        return s[0].capitalize() + s[1:]
    else:
        return s