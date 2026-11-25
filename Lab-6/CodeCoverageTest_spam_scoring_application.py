"""Exercise each executable line of the assigned spam scorer."""

import pytest

from spam_scoring import classify, filter_inbox, inbox_status, score_message


def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_warnings_case_and_punctuation_contribute_to_score():
    assert score_message("FREE! winner, PRIZE. TODAY", False, 4) == 11


def test_known_sender_discount_is_clamped_at_zero():
    assert score_message("meeting tomorrow", True, 1) == 0


@pytest.mark.parametrize(("score", "label"), [(1, "clean"), (4, "suspicious"), (8, "spam")])
def test_classify(score, label):
    assert classify(score) == label


def test_filter_groups_all_three_message_labels():
    messages = [("hello", True, 0), ("free prize", False, 0), ("urgent cash winner free", False, 0)]
    assert filter_inbox(messages) == {"clean": 1, "suspicious": 1, "spam": 1}


@pytest.mark.parametrize(
    ("spam", "clean", "status"),
    [(0, 0, "empty"), (3, 2, "flooded"), (1, 2, "noisy"), (1, 6, "healthy")],
)
def test_inbox_status(spam, clean, status):
    assert inbox_status({"spam": spam, "suspicious": 0, "clean": clean}) == status
