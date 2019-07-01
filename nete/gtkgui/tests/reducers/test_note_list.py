from nose2.tools import such
from nete.gtkgui.reducers.note_list import reduce
from nete.gtkgui.state.models import NoteList, NoteListItem, Note
from nete.gtkgui.actions.action_types import ActionType


with such.A('reduce') as it:
    @it.has_test_setup
    def setup():
        it.state = NoteList(
            filter_term='',
            notes=[
                NoteListItem(title='FOO', visible=True),
                NoteListItem(title='BAR', visible=True),
            ],
            preselected_note_title=None,
        )
        it.note = Note(
            note_collection_id='NOTE COLLECTION ID',
            title='TITLE',
            text='TEXT',
            needs_save=False,
            cursor_position=0
        )

    with it.having('a CREATED_NOTE action'):
        @it.should('add an empty note')
        def test():
            result = reduce(it.state, {
                'type': ActionType.CREATED_NOTE,
                'note': it.note,
            })

            titles = sorted(note['title'] for note in result['notes'])
            it.assertEqual(titles, ['BAR', 'FOO', 'TITLE'])

        @it.should('set visibility according to current filter')
        def test():
            state = it.state.set('filter_term', 'FO')
            result = reduce(state, {
                'type': ActionType.CREATED_NOTE,
                'note': it.note,
            })

            titles = sorted(note['title']
                            for note in result['notes']
                            if note['visible'])
            it.assertNotIn('TITLE', titles)

    with it.having('a DELETE_NOTE action'):
        @it.should('delete a note')
        def test():
            result = reduce(it.state, {
                'type': ActionType.DELETE_NOTE,
                'note_title': 'FOO'
            })

            it.assertEqual(len(result['notes']), 1)
            it.assertEqual(result['notes'][0]['title'], 'BAR')

    with it.having('a FINISH_EDIT_NOTE_TITLE action'):
        @it.should('change the note title')
        def test():
            result = reduce(it.state, {
                'type': ActionType.FINISH_EDIT_NOTE_TITLE,
                'old_title': 'FOO',
                'new_title': 'NEW TITLE',
            })

            titles = sorted(note['title'] for note in result['notes'])
            it.assertEqual(titles, ['BAR', 'NEW TITLE'])

    with it.having('a CHANGE_FILTER_TERM action'):
        @it.should('set the filter term')
        def test():
            result = reduce(it.state, {
                'type': ActionType.CHANGE_FILTER_TERM,
                'filter_term': 'FO',
            })

            it.assertEqual(result['filter_term'], 'FO')

        @it.should('filter notes')
        def test():
            result = reduce(it.state, {
                'type': ActionType.CHANGE_FILTER_TERM,
                'filter_term': 'FO',
            })

            titles = sorted(note['title']
                            for note in result['notes']
                            if note['visible'])
            it.assertEqual(titles, ['FOO'])

        with it.having('no preselected note'):
            @it.has_test_setup
            def setup():
                it.state.set('preselected_note_title', None)

            @it.should('preselect the first visible note')
            def test():
                result = reduce(it.state, {
                    'type': ActionType.CHANGE_FILTER_TERM,
                    'filter_term': 'FO',
                })

                it.assertEqual(result['preselected_note_title'], 'FOO')

        with it.having('a preselected note'):
            @it.has_test_setup
            def setup():
                it.state.set('preselected_note_title', 'FOO')

            @it.should('leave the preselection as it is if filter matches')
            def test():
                result = reduce(it.state, {
                    'type': ActionType.CHANGE_FILTER_TERM,
                    'filter_term': 'FO',
                })

                it.assertEqual(result['preselected_note_title'], 'FOO')

            @it.should('preselect first visible note otherwise')
            def test():
                result = reduce(it.state, {
                    'type': ActionType.CHANGE_FILTER_TERM,
                    'filter_term': 'BA',
                })

                it.assertEqual(result['preselected_note_title'], 'BAR')

    with it.having('a LOADED_NOTES action'):
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
