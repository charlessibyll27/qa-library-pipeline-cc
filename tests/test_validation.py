from data_processing.validation import validate_isbn

def test_valid_isbn():
    result = validate_isbn('9780306406157')
    assert result

def test_invalid_isbn():
    result = validate_isbn('not-an-isbn')
    assert not result

def test_wrong_length():
    result = validate_isbn('123456789')
    assert not result

def test_invalid_check_digit():
    # valid isbn: 9780306406157
    result = validate_isbn('9780306406158')
    assert not result