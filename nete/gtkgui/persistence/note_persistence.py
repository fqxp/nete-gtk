from nete.services.storage_factory import create_storage
from nete.gtkgui.state.actions import saved_note

__all__ = ('on_note_changed',)


def on_note_changed(current_note, dispatch):
    if not current_note['needs_save']:
        return

    storage = create_storage(current_note['storage_uri'])
    storage.save(build_note(current_note))
    dispatch(saved_note())


def build_note(current_note):
    return {
        'id': current_note['id'],
        'title': current_note['title'],
        'text': current_note['text'],
    }
