from hypothesis import given, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio


@given(st.text() | st.none())
def test_sender_domain_no_crash(s):
    try:
        sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {e!r}"


@given(st.text() | st.none())
def test_first_link_no_crash(s):
    try:
        first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {e!r}"


@given(st.text() | st.none())
def test_shout_ratio_no_crash(s):
    try:
        shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {e!r}"


# ---- Extra properties: check correctness, not just "no crash" ----

@given(st.text() | st.none())
def test_sender_domain_output_is_clean(s):
    d = sender_domain(s)
    assert isinstance(d, str)
    assert d == d.lower()
    assert '@' not in d


@given(st.text() | st.none())
def test_first_link_starts_with_http_or_empty(s):
    link = first_link(s)
    assert isinstance(link, str)
    assert link == "" or link.lower().startswith(("http://", "https://"))
    assert not any(ch.isspace() for ch in link)


@given(st.text() | st.none())
def test_shout_ratio_in_range(s):
    r = shout_ratio(s)
    assert 0.0 <= r <= 1.0


def test_known_examples():
    assert sender_domain("offers@Deals.com") == "deals.com"
    assert first_link("Win at http://spam.com/x today") == "http://spam.com/x"
    assert shout_ratio("FREE prize NOW") == 7 / 12
