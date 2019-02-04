from pyrsistent import freeze


def add_new(notes, note):
    return freeze(ordered(notes.append(note)))


def without(notes, title):
    return freeze(
        ordered(
            [note for note in notes if note['title'] != title]
        ))


def first_note_title(notes):
    return notes[0]['title'] if len(notes) > 0 else None


def last_note_title(notes):
    return notes[-1]['title'] if len(notes) > 0 else None


def contains(notes, note_title):
    return any(note['title'] == note_title for note in notes)


def next_note_title(notes, current_note_title):
    for i, note in enumerate(notes):
        if note['title'] == current_note_title:
            return notes[i+1]['title'] if i+1 < len(notes) else None
    return None


def previous_note_title(notes, current_note_title):
    for i, note in enumerate(notes):
        if note['title'] == current_note_title:
            return notes[i-1]['title'] if i > 0 else None
    return None


def change_title(notes, old_title, new_title):
    return freeze(
        note.set('title', new_title) if note['title'] == old_title
        else note
        for note in notes)


def ordered(notes):
    return freeze(
        sorted(
            notes,
            key=lambda note: note['title'].lower()))


def is_visible(note_title, filter_term):
    return not filter_term or filter_term.lower() in note_title.lower()
