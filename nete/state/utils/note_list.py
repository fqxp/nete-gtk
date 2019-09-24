from pyrsistent import freeze


def add_new(notes, note):
    return freeze(ordered(notes.append(note)))


def without(notes, title):
    return freeze(
        ordered(
            [note for note in notes if note['title'] != title]
        ))


def ordered(notes):
    return freeze(
        sorted(
            notes,
            key=lambda note: note['title'].lower()))


def is_visible(note_title, filter_term):
    return not filter_term or filter_term.lower() in note_title.lower()
