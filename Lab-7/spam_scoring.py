"""Extract sender, link, and capitalization signals from untrusted message data."""

import re
from urllib.parse import urlsplit

HTTP_URL = re.compile(r"""\bhttps?://[^\s<>"']+""", re.IGNORECASE)


def _is_domain(name):
    return bool(name) and all(
        label
        and label[0].isalnum()
        and label[-1].isalnum()
        and all(character.isalnum() or character == "-" for character in label)
        for label in name.split(".")
    )


def sender_domain(email):
    """Return the normalized domain of a simple sender address, or None."""
    if not isinstance(email, str):
        return None
    local, separator, domain = email.strip().partition("@")
    if not separator or not local or any(char.isspace() for char in local):
        return None
    return domain.lower() if _is_domain(domain) else None


def first_link(text):
    """Return the first syntactically valid HTTP(S) link, or None."""
    if not isinstance(text, str):
        return None
    for match in HTTP_URL.finditer(text):
        candidate = match.group().rstrip(".,!?;")
        for opening, closing in (("(", ")"), ("[", "]"), ("{", "}")):
            while candidate.endswith(closing) and candidate.count(closing) > candidate.count(opening):
                candidate = candidate[:-1]
        try:
            url = urlsplit(candidate)
            port = url.port
        except ValueError:
            continue
        host = url.hostname
        if host and (":" in host or _is_domain(host.rstrip("."))) and (port is None or port > 0):
            return candidate
    return None


def shout_ratio(text):
    """Return uppercase letters divided by all letters, or 0.0 without letters."""
    if not isinstance(text, str):
        return 0.0
    letters = [character for character in text if character.isalpha()]
    return sum(character.isupper() for character in letters) / len(letters) if letters else 0.0


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    print("Sender Domain:", sender_domain(user_input))

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    print("First Link:", first_link(user_input))

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    print("Uppercase Ratio:", shout_ratio(user_input))


if __name__ == "__main__":
    main()
