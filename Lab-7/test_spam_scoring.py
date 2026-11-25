"""Fuzz the three message helpers with generated text and structured inputs."""

import string

from hypothesis import example, given, settings, strategies as st

from spam_scoring import first_link, sender_domain, shout_ratio

possible_inputs = st.one_of(st.text(max_size=150), st.none(), st.integers(), st.binary())
labels = st.text(string.ascii_letters + string.digits, min_size=1, max_size=15)
words = st.text(string.ascii_letters, min_size=1, max_size=12)


@settings(max_examples=250, derandomize=True)
@given(possible_inputs)
@example("")
@example("alice@@example.com")
@example("alice@")
def test_sender_domain_handles_arbitrary_input(value):
    domain = sender_domain(value)
    if domain is not None:
        assert isinstance(value, str)
        assert value.count("@") == 1
        assert domain and domain == domain.lower()
    if not isinstance(value, str) or value.count("@") != 1:
        assert domain is None


@given(words, labels, labels)
def test_sender_domain_normalizes_valid_addresses(name, host, suffix):
    domain = f"{host}.{suffix}"
    assert sender_domain(f"{name}@{domain}") == domain.lower()


@settings(max_examples=250, derandomize=True)
@given(possible_inputs)
@example("")
@example("ordinary text")
@example("nohttp://site.example")
def test_first_link_handles_arbitrary_input(value):
    link = first_link(value)
    if link is not None:
        assert isinstance(value, str)
        assert link in value
        assert link.lower().startswith(("http://", "https://"))
    if not isinstance(value, str) or "http" not in value.lower():
        assert link is None


@given(labels, words, st.sampled_from([" ", "\t", "\n"]), st.sampled_from(["http", "https"]))
def test_first_link_extracts_first_http_url(host, path, whitespace, scheme):
    url = f"{scheme}://{host}.example/{path}"
    assert first_link(f"Read{whitespace}({url}).{whitespace}https://second.example") == url


@settings(max_examples=250, derandomize=True)
@given(possible_inputs)
@example("")
@example("123 !")
def test_shout_ratio_matches_letter_counts(value):
    ratio = shout_ratio(value)
    assert 0.0 <= ratio <= 1.0
    letters = [character for character in value if character.isalpha()] if isinstance(value, str) else []
    expected = sum(letter.isupper() for letter in letters) / len(letters) if letters else 0.0
    assert ratio == expected


@given(st.text(max_size=100), st.text(string.digits + string.punctuation, max_size=40))
def test_punctuation_and_digits_do_not_change_ratio(text, noise):
    assert shout_ratio(f"{noise}{text}{noise}") == shout_ratio(text)
