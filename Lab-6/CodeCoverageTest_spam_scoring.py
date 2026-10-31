import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# ---- Starter tests ----
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

# ---- Added for LINE coverage (every statement executed at least once) ----
def test_spam_word_adds_two():
    assert score_message("FREE prize", False, 0) == 4

def test_shouting_word_adds_one():
    assert score_message("HELLO", False, 0) == 1

def test_many_links_adds_four():
    assert score_message("hi", False, 5) == 4

def test_few_links_adds_one():
    assert score_message("hi", False, 2) == 1

def test_known_sender_reduces_score():
    assert score_message("free cash winner urgent", True, 0) == 5

def test_known_sender_score_never_negative():
    assert score_message("hello", True, 0) == 0

def test_classify_spam():
    assert classify(10) == "spam"

def test_classify_suspicious():
    assert classify(5) == "suspicious"

def test_filter_inbox_counts():
    msgs = [("free cash winner prize", False, 5),   # spam
            ("free prize", False, 0),               # suspicious
            ("hello", False, 0)]                    # clean
    assert filter_inbox(msgs) == {"spam": 1, "suspicious": 1, "clean": 1}

def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"

def test_inbox_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"

def test_inbox_status_noisy():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 7}) == "noisy"

def test_inbox_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 9}) == "healthy"
