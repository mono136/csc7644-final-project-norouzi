def word_count(text):
    return len(text.split())

def has_numbers(text):
    return any(char.isdigit() for char in text)