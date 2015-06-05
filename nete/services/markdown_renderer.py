from PyQt5.QtCore import QObject, pyqtSlot
import markdown


class MarkdownRenderer(QObject):
    def __init__(self):
        super(MarkdownRenderer, self).__init__()

    @pyqtSlot('QString', result='QString')
    def renderToHtml(self, markdown_text):
        return markdown.markdown(markdown_text)
