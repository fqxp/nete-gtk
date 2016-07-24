from nete.gtkgui.note_list_view import NoteListModel
from nose2.tools import such
import mock


with such.A('NoteListModel') as it:

    with it.having('set_data'):

        @it.should('fill the model from given notes')
        def test():
            model = NoteListModel()

            model.set_data({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'TITLE 2'},
                'ID 3': {'title': 'TITLE 3'},
            })

            model_data = list(map(list, model))
            it.assertIn(['ID 1', 'TITLE 1'], model_data)
            it.assertIn(['ID 2', 'TITLE 2'], model_data)
            it.assertIn(['ID 3', 'TITLE 3'], model_data)

    with it.having('update'):

        @it.has_test_setup
        def test_setup():
            it.model = NoteListModel()
            it.model.set_data({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'TITLE 2'},
                'ID 3': {'title': 'TITLE 3'},
            })

        @it.has_test_teardown
        def test_teardown():
            it.model = None

        @it.should('update model where title is changed')
        def test():
            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'NEW TITLE'},
                'ID 3': {'title': 'TITLE 3'},
            })

            model_data = list(map(list, it.model))
            it.assertEqual(len(model_data), 3)
            it.assertIn(['ID 2', 'NEW TITLE'], model_data)

        @it.should('emit row-changed signal once for a change')
        def test():
            handler = mock.Mock()
            it.model.connect('row-changed', handler)

            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'NEW TITLE'},
                'ID 3': {'title': 'TITLE 3'},
            })

            it.assertEqual(handler.call_count, 1)

        @it.should('adds new rows')
        def test():
            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'TITLE 2'},
                'ID 3': {'title': 'TITLE 3'},
                'ID 4': {'title': 'TITLE 4'},
            })

            model_data = list(map(list, it.model))
            it.assertEqual(len(model_data), 4)
            it.assertIn(['ID 4', 'TITLE 4'], model_data)

        @it.should('emit row-inserted signal once for an added row')
        def test():
            handler = mock.Mock()
            it.model.connect('row-inserted', handler)

            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 2': {'title': 'TITLE 2'},
                'ID 3': {'title': 'TITLE 3'},
                'ID 4': {'title': 'TITLE 4'},
            })

            it.assertEqual(handler.call_count, 1)

        @it.should('removes deleted rows')
        def test():
            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 3': {'title': 'TITLE 3'},
            })

            model_data = list(map(list, it.model))
            it.assertEqual(len(model_data), 2)
            it.assertNotIn(['ID 2', 'TITLE 2'], model_data)

        @it.should('emit row-deleted signal once for a deleted row')
        def test():
            handler = mock.Mock()
            it.model.connect('row-deleted', handler)

            it.model.update({
                'ID 1': {'title': 'TITLE 1'},
                'ID 3': {'title': 'TITLE 3'},
            })

            it.assertEqual(handler.call_count, 1)

    it.createTests(globals())
