import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# ---- Starter tests ----
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

# ---- score_message: word loop branches ----
def test_empty_text_loop_never_runs():
    # for-loop exits immediately (zero-iteration branch)
    assert score_message("", False, 0) == 0

def test_spam_word_adds_two():
    assert score_message("free", False, 0) == 2

def test_spam_word_case_and_punctuation_ignored():
    assert score_message("WINNER!!!", False, 0) == 2
    assert score_message("Cash,", False, 0) == 2

def test_shouting_word_adds_one():            # elif True
    assert score_message("HELLO", False, 0) == 1

def test_lowercase_word_adds_nothing():       # elif False (not upper)
    assert score_message("hello", False, 0) == 0

def test_short_uppercase_word_adds_nothing(): # elif False (upper but len <= 3)
    assert score_message("ABC", False, 0) == 0

def test_uppercase_boundary_length_four():    # len == 4 -> counts
    assert score_message("ABCD", False, 0) == 1

# ---- score_message: link branches ----
def test_no_links():                          # both link conditions False
    assert score_message("hi", False, 0) == 0

def test_one_link_boundary():                 # elif True (>0)
    assert score_message("hi", False, 1) == 1

def test_three_links_boundary():              # >3 False, >0 True
    assert score_message("hi", False, 3) == 1

def test_four_links_boundary():               # >3 True
    assert score_message("hi", False, 4) == 4

# ---- score_message: known sender branches ----
def test_unknown_sender_no_discount():        # if sender_known False
    assert score_message("free", False, 0) == 2

def test_known_sender_discount_stays_positive():  # known True, score >= 0 (inner False)
    assert score_message("free cash winner urgent", True, 0) == 5

def test_known_sender_one_link_clamped():
    assert score_message("hi", True, 3) == 0      # 1 - 3 = -2 -> clamped

def test_known_sender_clamped_to_zero():      # known True, score < 0 (inner True)
    assert score_message("hello", True, 0) == 0

def test_known_sender_score_exactly_three_gives_zero_no_clamp():
    assert score_message("free", True, 1) == 0    # 2+1-3 = 0, not < 0

# ---- classify: all three outcomes + boundaries ----
@pytest.mark.parametrize("score,expected", [
    (0, "clean"), (3, "clean"),
    (4, "suspicious"), (7, "suspicious"),
    (8, "spam"), (100, "spam"),
])
def test_classify_boundaries(score, expected):
    assert classify(score) == expected

# ---- filter_inbox ----
def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}

def test_filter_inbox_mixed():
    msgs = [("free cash winner prize", False, 5),
            ("free prize", False, 0),
            ("hello", False, 0),
            ("free cash winner prize", True, 0)]   # known sender -> 5 -> suspicious
    assert filter_inbox(msgs) == {"spam": 1, "suspicious": 2, "clean": 1}

# ---- inbox_status: all branches + boundaries ----
def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"

def test_inbox_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"

def test_inbox_status_exactly_half_is_noisy():   # ratio 0.5 -> not > 0.5
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"

def test_inbox_status_noisy():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 7}) == "noisy"

def test_inbox_status_exactly_point_two_is_healthy():  # ratio 0.2 -> not > 0.2
    assert inbox_status({"spam": 2, "suspicious": 0, "clean": 8}) == "healthy"

def test_inbox_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 9}) == "healthy"
