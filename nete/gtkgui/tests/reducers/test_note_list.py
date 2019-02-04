from nose2.tools import such
from nete.gtkgui.reducers.note_list import reduce
from nete.gtkgui.state.models import NoteList, NoteListItem, Note
from nete.gtkgui.actions.action_types import ActionType


with such.A('reduce') as it:
    @it.has_setup
    def setup():
        it.state = NoteList(
            filter_term='',
            notes=[
                NoteListItem(title='FOO', visible=True),
                NoteListItem(title='BAR', visible=True),
            ])

    @it.should('add an empty note on CREATED_NOTE action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CREATED_NOTE,
            'note': Note(title='NEW NOTE'),
        })

        titles = sorted(note['title'] for note in result['notes'])
        it.assertEqual(titles, ['BAR', 'FOO', 'NEW NOTE'])

    @it.should('set visibility according to current filter for CREATED_NOTE action')
    def test():
        state = it.state.set('filter_term', 'FO')
        result = reduce(state, {
            'type': ActionType.CREATED_NOTE,
            'note': Note(title='NEW NOTE'),
        })

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        it.assertNotIn('NEW NOTE', titles)

    @it.should('delete note on DELETE_NOTE action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.DELETE_NOTE,
            'title': 'FOO'
        })

        it.assertEqual(len(result['notes']), 1)
        it.assertEqual(result['notes'][0]['title'], 'BAR')

    @it.should('change the note title on CHANGE_NOTE_TITLE action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CHANGE_NOTE_TITLE,
            'old_title': 'FOO',
            'new_title': 'NEW TITLE',
        })

        titles = sorted(note['title'] for note in result['notes'])
        it.assertEqual(titles, ['BAR', 'NEW TITLE'])

    @it.should('set the filter term on CHANGE_FILTER_TERM action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        it.assertEqual(result['filter_term'], 'FO')

    @it.should('filter notes on CHANGE_FILTER_TERM action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        it.assertEqual(titles, ['FOO'])

    @it.should('set the note list on LOADED_NOTES action')
    def test():
        result = reduce(it.state, {
            'type': ActionType.LOADED_NOTES,
            'notes': [
                NoteListItem(title='NEW NOTE 1', visible=True),
                NoteListItem(title='NEW NOTE 2', visible=True),
            ]})

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        it.assertEqual(titles, ['NEW NOTE 1', 'NEW NOTE 2'])

    it.createTests(globals())
