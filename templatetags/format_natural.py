# -*- encoding: utf-8 -*-

from django import template
from django.template import defaultfilters
from datetime import datetime, date
import re

register = template.Library()


def format_natural(value, arg=None):
    try:
        value1 = datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    delta_date = value1.date() - date.today()
    delta = value1 - datetime.now()
    if not delta_date.days:
        if delta.total_seconds() < 0:
            return u'Actuellement'
        return u'Ce soir'
    elif delta_date.days == 1:
        return u'Demain'
    else:
        return u'%s' % defaultfilters.date(value1, 'l d M.').lower()


def timeslot(value):
    if isinstance(value, datetime):
        if value.hour <= 4:
            return "early"
        elif 5 <= value.hour <= 11:
            return "morning"
        elif 12 <= value.hour <= 17:
            return "afternoon"
        elif 18 <= value.hour <= 20:
            return "evening"
        else:
            return "prime"
    else:
        return "unknown (" + str(type(value)) + ")"

i18n_today = {
    'early': 'très tôt',
    'morning': 'ce matin',
    'afternoon': 'cet après-midi',
    'evening': 'en début de soirée',
    'prime': 'ce soir'
}

i18n_later = {
    'early': 'très tôt',
    'morning': 'matin',
    'afternoon': 'après-midi',
    'evening': 'en début de soirée',
    'prime': 'soir'
}


def day_and_timeslot(value):
    global i18n_today, i18n_later
    if isinstance(value, datetime):
        delta_date = value.date() - date.today()
        if not delta_date.days:
            return i18n_today[timeslot(value)].capitalize()
        else:
            dat_timeslot = i18n_later[timeslot(value)].decode('utf-8')
            if delta_date.days < 7:
                return defaultfilters.date(value, 'l').capitalize() + " " + dat_timeslot
            else:
                return defaultfilters.date(value, 'l d M.').capitalize() + " " + dat_timeslot
    else:
        return "unknown (" + str(type(value)) + ")"


def before_now(value):
    if isinstance(value, datetime):
        delta = value - datetime.now()
        if delta.total_seconds() < 0:
            return 1
    return 0


def leading_zeros(value, desired_digits):
    """
    Given an integer, returns a string representation, padded with [desired_digits] zeros.
    """
    num_zeros = int(desired_digits) - len(str(value))
    padded_value = []
    while num_zeros >= 1:
        padded_value.append("0")
        num_zeros -= 1
    padded_value.append(str(value))
    return "".join(padded_value)

register.filter('format_time', format_natural)
register.filter('timeslot', timeslot)
register.filter('day_and_timeslot', day_and_timeslot)
register.filter('before_now', before_now)
register.filter('zfill', leading_zeros)