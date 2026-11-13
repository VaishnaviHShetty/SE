import re

_LINK_RE = re.compile(r'https?://\S+', re.IGNORECASE)


def sender_domain(email):
    """Return the lower-cased domain of an email address, or '' if invalid."""
    if not isinstance(email, str):
        return ""
    email = email.strip()
    local, sep, domain = email.rpartition('@')
    if not sep or not local or not domain:
        return ""
    return domain.strip().lower()


def first_link(text):
    """Return the first http(s) link found in text, or '' if there is none."""
    if not isinstance(text, str):
        return ""
    match = _LINK_RE.search(text)
    return match.group(0) if match else ""


def shout_ratio(text):
    """Return the fraction (0.0-1.0) of letters that are uppercase.
    Returns 0.0 for non-strings or text with no letters."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = [c for c in letters if c.isupper()]
    return len(upper) / len(letters)


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result if result else "(invalid email address)")

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result if result else "(no link found)")

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()
