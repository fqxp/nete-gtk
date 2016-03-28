from immutable import ImmutableList


def add_new(note_list, note_id, title):
    return ImmutableList(
        ordered(
            note_list.append(
                build_entry({'id': note_id, 'title': title}))))


def first_note_id(note_list):
    return note_list[0]['id'] if len(note_list) > 0 else None


def next_note_id(note_list, current_note_id):
    for i, note in enumerate(note_list):
        if note['id'] == current_note_id:
            return note_list[i+1]['id'] if i+1 < len(note_list) else current_note_id
    return current_note_id


def previous_note_id(note_list, current_note_id):
    for i, note in enumerate(note_list):
        if note['id'] == current_note_id:
            return note_list[i-1]['id'] if i > 0 else current_note_id
    return current_note_id


def build_entry(note):
    return {
        'id': note['id'],
        'title': note['title'],
    }


def change_title(note_list, note_id, title):
    return ImmutableList({
        'id': note['id'],
        'title': note['title'] if note['id'] != note_id else title}
        for note in note_list)


def ordered(note_list):
    return sorted(
        note_list,
        key=lambda note: note['title'].lower())
