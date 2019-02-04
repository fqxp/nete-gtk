from nose2.tools import such
from nete.gtkgui.reducers.current_note import reduce
from nete.gtkgui.state.models import Note
from nete.gtkgui.actions.action_types import ActionType


with such.A('reduce') as it:
    @it.has_setup
    def setup():
        it.state = Note(
            title='TITLE',
            text='TEXT',
            needs_save=False)

    @it.should('change the current note on SELECT_NOTE action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.SELECT_NOTE,
            'note': Note(
                title='OTHER TITLE',
                text='OTHER TEXT',
                needs_save=True)})

        it.assertEqual(result['title'], 'OTHER TITLE')
        it.assertEqual(result['text'], 'OTHER TEXT')
        it.assertEqual(result['needs_save'], True)

    @it.should('change the note text on CHANGE_NOTE_TEXT action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CHANGE_NOTE_TEXT,
            'text': 'NEW TEXT',
        })

        it.assertEqual(result['text'], 'NEW TEXT')

    @it.should('change the note title on CHANGE_NOTE_TITLE action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CHANGE_NOTE_TITLE,
            'title': 'NEW TITLE',
        })

        it.assertEqual(result['title'], 'NEW TITLE')

    @it.should('switch the »needs save« switch to False on NOTE_SAVED action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.NOTE_SAVED,
            'needs_save': True,
        })

        it.assertEqual(result['needs_save'], False)

    it.createTests(globals())
