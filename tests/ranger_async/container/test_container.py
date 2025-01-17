from __future__ import absolute_import, division, print_function

from ranger_async.container import history

HISTORY_TEST_ENTRIES = [str(k) for k in range(20)]
OTHER_TEST_ENTRIES = [str(k) for k in range(40, 45)]


def testhistorybasic():
    # A history is a buffer of limited size that stores the last `maxlen`
    # item added to it. It has a `current` index that serves as a cursor.

    # A history has a limited size, check that only `maxlen` items are stored
    hist = history.History(maxlen=10)
    for entry in HISTORY_TEST_ENTRIES:
        hist.add(entry)

    # 10 items are stored
    assert len(hist) == 10
    assert hist.current() == "19"
    assert hist.top() == "19"
    assert hist.bottom() == "10"

    # going back in time affects only changes current item
    hist.back()
    assert len(hist) == 10
    assert hist.current() == "18"
    assert hist.top() == "19"
    assert hist.bottom() == "10"

    # __iter__ is actually an interator and we can iterate through the list
    iterator = iter(hist)
    assert iter(iterator) == iterator
    assert list(iterator) == HISTORY_TEST_ENTRIES[10:]

    # search allows to go back in time as long as a pattern matches and we don't
    # go over a step limit
    assert hist.search("45", -9) == "18"
    assert hist.search("1", -5) == "13"

    # fast forward selects the last item
    hist.fast_forward()
    assert hist.current() == "19"

    # back followed by forward is a noop
    hist.back()
    hist.forward()
    assert hist.current() == "19"

    # move can be expressed as multiple calls to back and forward
    hist.move(-3)
    hist.forward()
    hist.forward()
    hist.forward()
    assert hist.current() == "19"

    # back, forward, move play well with boundaries
    for _ in range(30):
        hist.back()

    for _ in range(30):
        hist.forward()

    for _ in range(30):
        hist.move(-2)

    for _ in range(30):
        hist.move(2)
    assert hist.current() == "19"

    # we can create an history from another history
    hist = history.History(maxlen=10)
    for entry in HISTORY_TEST_ENTRIES:
        hist.add(entry)
    # XXX maxlen should not be used to refer to something that isn't a length
    otherh = history.History(maxlen=hist)
    assert list(hist) == list(otherh)

    # Rebase replaces the past of the history with that of another
    otherh = history.History(maxlen=hist)
    old_current_item = hist.current()
    for entry in OTHER_TEST_ENTRIES:
        otherh.add(entry)
    assert list(otherh)[-3:] == ["42", "43", "44"]
    hist.rebase(otherh)
    assert hist.current() == old_current_item
    assert list(hist)[-3:] == ["43", "44", old_current_item]

    # modify, modifies the top of the stack
    hist.modify("23")
    assert hist.current() == "23"


def testhistoryunique():
    # Check that unique history refuses to store duplicated entries
    hist = history.History(maxlen=10, unique=True)
    for entry in HISTORY_TEST_ENTRIES:
        hist.add(entry)
    assert hist.current() == "19"
    hist.add("17")
    assert list(hist).count("17") == 1
    assert hist.current() == "17"
