"""Tools to make things more human readable."""

def human_bytes(num, suffix='B', use_binary_prefix=True):
    """Provide a human readable representation of a specified number of bytes.

    Convert a number of bytes into a higher order representation such as megabytes
    or gigabytes to make more human readable. Similar to specifying `-h` in many command
    line tools.

    Args:
        num (int): The number of bytes you wish to represent.
        suffix (str, optional): The suffix for the representation. Defaults to 'B'
        use_binary_prefix (bool, optional): Use binary prefix, Defaults to True, if False use decimal prefix.
                                            https://en.wikipedia.org/wiki/Binary_prefix

    Returns:
        str: The human representation of the bytes provided.

    Examples:
        >>> print(human_bytes(1024))
        1.0KiB

    """
    if use_binary_prefix:
        multiplyer = 1024.0
        units = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']
    else:
        multiplyer = 1000.0
        units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

    for unit in units:
        if abs(num) < multiplyer:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= multiplyer
    return "%.1f%s%s" % (num*multiplyer, units[-1], suffix)
