from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

#dev_token = "S=s1:U=932b6:E=1603e3aa498:C=158e6897570:P=1cd:A=en-devtoken:V=2:H=feef61a985db7ba0ae3d47477daf7940"

class Note(object):
    def __init__(self):
        self.dev_token = "S=s1:U=932b6:E=1603e3aa498:C=158e6897570:P=1cd:A=en-devtoken:V=2:H=feef61a985db7ba0ae3d47477daf7940"
        self.client = EvernoteClient(token=self.dev_token)
        self.noteStore = self.client.get_note_store()

    def createEvernote(self, notebook_guid, title, html):
        note = Types.Note()
        #note.notebookGUID = 'd7900482-362b-4424-a698-99c1833fb81c'
        note.notebookGuid = notebook_guid
        note.title = title
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += "<en-note>"
        note.content += html
        note.content += "</en-note>"
        note = self.noteStore.createNote(note)
        return note

    def updateNote(self, note_guid, title, html):
        note = self.noteStore.getNote(note_guid, False, False, False, False)
        note.title = title
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += "<en-note>"
        note.content += html
        note.content += "</en-note>"
        note = self.noteStore.updateNote(note)
        return note


def test():
    html = """This is evening.
    """

    guid = "d7900482-362b-4424-a698-99c1833fb81c"
    note = Note().createEvernote(guid, "evening test", html)
    print note.guid
    html_new = """
    <blockquote style="border-left:4px solid #DDD;padding:0 15px;color:#777">
    <p>This is a quote.</p>
    </blockquote>
    """
    Note().updateNote(note.guid, 'Evening Update test', html_new)

test()