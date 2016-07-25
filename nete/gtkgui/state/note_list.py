from pyrsistent import freeze


def add_new(notes, note_id, title):
    return freeze(
        ordered(
            notes.append(
                build_entry({'id': note_id, 'title': title}))))


def first_note_id(notes):
    return notes[0]['id'] if len(notes) > 0 else None


def next_note_id(notes, current_note_id):
    for i, note in enumerate(notes):
        if note['id'] == current_note_id:
            return notes[i+1]['id'] if i+1 < len(notes) else current_note_id
    return current_note_id


def previous_note_id(notes, current_note_id):
    for i, note in enumerate(notes):
        if note['id'] == current_note_id:
            return notes[i-1]['id'] if i > 0 else current_note_id
    return current_note_id


def build_entry(note):
    return freeze({
        'id': note['id'],
        'title': note['title'],
    })


def change_title(notes, note_id, title):
    return freeze({
        'id': note['id'],
        'title': note['title'] if note['id'] != note_id else title}
        for note in notes)


def ordered(notes):
    return freeze(
        sorted(
            notes,
            key=lambda note: note['title'].lower()))
