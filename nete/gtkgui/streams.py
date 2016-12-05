from flurx import debug_reducer
from functools import partial
from gi.repository import Gtk
from nete.services.note_storage import save_note
from nete.services.ui_state_storage import save_ui_state
from rx.subjects import BehaviorSubject, Subject
from rx.concurrency import GtkScheduler
from .reducers import reduce_action
from .state import selectors
from . import actions
import logging


logger = logging.getLogger(__name__)


state_mutating_actions = (
    actions.change_filter_term,
    actions.change_cursor_position,
    actions.change_note_text,
    actions.change_note_title,
    actions.create_note,
<<<<<<< HEAD
    actions.finish_edit_mode_text,
    actions.finish_edit_mode_title,
=======
    actions.finish_edit_note_text,
    actions.finish_edit_note_title,
>>>>>>> 72348d3... Refactor streams and state code
    actions.load_note,
    actions.load_notes,
    actions.load_ui_state,
    actions.loaded_note,
    actions.loaded_notes,
    actions.loaded_ui_state,
    actions.move_paned,
    actions.next_note,
    actions.prev_note,
    actions.select_first,
    actions.select_last,
    actions.set_filter_term_entry_focus,
<<<<<<< HEAD
    actions.toggle_edit_mode_text,
    actions.toggle_edit_mode_title,
=======
    actions.toggle_edit_note_text,
    actions.toggle_edit_note_title,
>>>>>>> 72348d3... Refactor streams and state code
)

scheduler = GtkScheduler()

note_ready_stream = BehaviorSubject(True)


def setup_streams(store, debug=False):
    reducer = reduce_action

    if debug:
        reducer = debug_reducer(print_traceback=False)(reducer)

    action_stream = Subject() \
        .merge(*state_mutating_actions) \
        .map(partial(resolve_action, store=store)) \
        .filter(lambda action: action is not None) \
        .map(lambda action: reducer(store.value, action))
    action_stream.subscribe(store)

    changed_notes_stream = store \
        .map(selectors.current_note) \
        .distinct_until_changed() \
        .debounce(1000, scheduler=scheduler) \
        .pausable_buffered(note_ready_stream)
    changed_notes_stream.subscribe(do_save_note)

    ui_state_stream = store \
        .map(selectors.ui_state) \
        .debounce(500, scheduler=scheduler) \
        .distinct_until_changed()
    ui_state_stream.subscribe(save_ui_state)

    actions.quit.subscribe(do_quit)


def do_save_note(note):
    note_ready_stream.on_next(False)
    future = save_note(note)
    future.add_done_callback(
        lambda f: note_ready_stream.on_next(True))


def do_quit(data):
    Gtk.main_quit()


def resolve_action(action, store):
    while callable(action):
        action = action(state=store.value)

    return action
