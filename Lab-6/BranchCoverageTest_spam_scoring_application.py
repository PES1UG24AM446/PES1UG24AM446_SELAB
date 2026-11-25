"""Exercise both sides of every decision and the score and ratio boundaries."""

import pytest

from spam_scoring import classify, filter_inbox, inbox_status, score_message


@pytest.mark.parametrize(
    ("text", "known", "links", "expected"),
    [
        ("", False, 0, 0),
        ("free! CASH, winner. urgent PRIZE", False, 0, 10),
        ("ABC ABCD lower", False, 0, 1),
        ("ordinary", False, 1, 1),
        ("ordinary", False, 3, 1),
        ("ordinary", False, 4, 4),
        ("ordinary", True, 0, 0),
        ("free", True, 1, 0),
        ("free prize", True, 1, 2),
    ],
)
def test_scoring_decisions(text, known, links, expected):
    assert score_message(text, known, links) == expected


@pytest.mark.parametrize(
    ("points", "label"),
    [(3, "clean"), (4, "suspicious"), (7, "suspicious"), (8, "spam")],
)
def test_classification_thresholds(points, label):
    assert classify(points) == label


def test_empty_inbox_has_zero_counts():
    assert filter_inbox([]) == {"clean": 0, "suspicious": 0, "spam": 0}


def test_mixed_inbox_counts_every_message_once():
    messages = [("hello", True, 0), ("free prize", False, 0), ("urgent cash", False, 4)]
    assert filter_inbox(messages) == {"clean": 1, "suspicious": 1, "spam": 1}


@pytest.mark.parametrize(
    ("spam", "other", "status"),
    [
        (0, 0, "empty"),
        (1, 5, "healthy"),
        (1, 4, "healthy"),
        (1, 3, "noisy"),
        (1, 1, "noisy"),
        (2, 1, "flooded"),
    ],
)
def test_inbox_ratio_boundaries(spam, other, status):
    assert inbox_status({"spam": spam, "suspicious": other, "clean": 0}) == status
