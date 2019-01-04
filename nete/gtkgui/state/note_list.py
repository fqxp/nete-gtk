from pyrsistent import freeze
from .initial import Note


def add_new(notes, note):
    return freeze(
        ordered(
            notes.append(note)))


def without(notes, note_id):
    return freeze(
        ordered(
            [note for note in notes if note['id'] != note_id]
        ))


def first_note_id(notes):
    return notes[0]['id'] if len(notes) > 0 else None


def last_note_id(notes):
    return notes[-1]['id'] if len(notes) > 0 else None


def contains(notes, note_id):
    return any(note['id'] == note_id for note in notes)


def next_note_id(notes, current_note_id):
    for i, note in enumerate(notes):
        if note['id'] == current_note_id:
            return notes[i+1]['id'] if i+1 < len(notes) else None
    return None


def previous_note_id(notes, current_note_id):
    for i, note in enumerate(notes):
        if note['id'] == current_note_id:
            return notes[i-1]['id'] if i > 0 else None
    return None


def build_entry(note):
    return Note.create({
        'id': note['id'],
        'title': note['title'],
    })


def change_title(notes, note_id, title):
    return freeze(
        Note.create({
            'id': note['id'],
            'title': note['title'] if note['id'] != note_id else title})
        for note in notes)


def ordered(notes):
    return freeze(
        sorted(
            notes,
            key=lambda note: note['title'].lower()))
