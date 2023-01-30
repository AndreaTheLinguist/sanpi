# coding=utf-8

def print_iter(iter_obj):
    print(' ▸ '+'\n ▸ '.join(iter_obj))


def dur_round(time_dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "m"

        if time_dur >= 60:
            time_dur = time_dur / 60
            unit = "h"

    if time_dur < 10:
        dur_str = f"{round(time_dur, 2):.2f}{unit}"
    else:
        dur_str = f"{round(time_dur, 1):.1f}{unit}"

    return dur_str
