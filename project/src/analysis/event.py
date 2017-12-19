"""
Various tools used in the analysis.
"""

import csv


class Event(object):
    """
    Models an event entity.
    """

    def __init__(self, event_id, description, date_occured, keywords):
        self._event_id = event_id
        self._description = description
        self._date_occured = date_occured
        self._functor = self._parse_keywords(keywords)

    @staticmethod
    def _parse_keywords(keywords):
        # terms is a list of lists:
        # the first level list contains the OR terms
        # each second level list contains the AND terms
        terms = [x.split('&') for x in keywords.split('|')]
        # functor is the "check match" function:
        # given an tweet text, returns whether the tweet matches
        # the specified keyword scheme
        functor = lambda x: any([all([kw in x for kw in and_term])
                                 for and_term in terms])
        return functor

    @property
    def event_id(self):
        return self._event_id

    @property
    def description(self):
        return self._description

    @property
    def date_occured(self):
        return self._date_occured

    def matches(self, word_bag):
        return self._functor(word_bag)


class EventParser(object):
    """
    Parses an "event file", that is, a CSV file containing event definitions.

    The event definition shall have the following columns:
        - event_id: the unique event identifier
        - description: the event description
        - date: the date the event occurred
        - keywords: the keyword specification, as explained below

    The keyword specification shall be a disjunction of conjunctions of words
    that should appear to some text (tweet) in order for the tweet to match
    the given event.

    The disjunction character is | and the conjunction character is &.
    Example:
        hello&earth|hello&mars:
            matches some text containing the word "hello" and the word "earth"
            or containing the word "hello" and the word "mars".
        syria&chemical&attack|sarin:
            matches some text containing the word "syria" and the word
            "chemical" and the word "attack" or containing the word "sarin".
    """

    def __init__(self, events_fpath):
        self._event_list = []
        with open(events_fpath, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # skip csv header
            for row in reader:
                event_id, desc, dt, keywords = row
                self._event_list.append(Event(event_id, desc, dt, keywords))

    @property
    def event_list(self):
        return self._event_list
