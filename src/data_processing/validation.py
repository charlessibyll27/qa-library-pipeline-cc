"""
Data validation functions.
"""


# Example function to implement:
def validate_isbn(isbn):
    """Validate ISBN-13 format."""

    isbn = str(isbn).replace("-", "") #Removing hyphens

    # ISBN must be 13 digits
    if len(isbn) != 13:
        return False

    # Can only be digits
    if not isbn.isdigit():
        return False

    # Check digit from first 12 digits calc
    total = 0
    for i, digit in enumerate(isbn[:12]):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3
    
    check_digit = (10 - (total % 10)) % 10

    return check_digit == int(isbn[12])
