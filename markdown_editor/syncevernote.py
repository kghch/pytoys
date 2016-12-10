from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

dev_token = "S=s1:U=932b6:E=1603e3aa498:C=158e6897570:P=1cd:A=en-devtoken:V=2:H=feef61a985db7ba0ae3d47477daf7940"


def createNotestore(dev_token):
    client = EvernoteClient(token=dev_token)
    noteStore = client.get_note_store()
    return noteStore

#notebooks = noteStore.listNotebooks()
#guid = notebooks[1].guid
#print guid

def createEvernote(notebook_guid, title, html):
    note = Types.Note()
    #note.notebookGUID = 'd7900482-362b-4424-a698-99c1833fb81c'
    note.notebookGuid = notebook_guid
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += "<en-note>"
    note.content += html
    note.content += "</en-note>"
    noteStore = createNotestore()
    note = noteStore.createNote(note)