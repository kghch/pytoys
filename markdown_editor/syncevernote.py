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
    noteStore = createNotestore(dev_token)
    note = noteStore.createNote(note)


def updateNote(note_guid, title, html):
    pass


html = """
<h2>First doc</h2>
<p>At WK's home. Drinking some yogurt is comfortable.</p>
<div style=" font-size: inherit; background-color: transparent; padding: 2px; white-space: pre-wrap; display: block; background: #f5f5f5; border-radius:4px; color: #333; border: 1px solid #ccc"><pre><span></span><span style=" color: #000000; font-weight: bold ">def</span> <span style=" color: #990000; font-weight: bold ">func</span><span>():</span>
      <span style=" color: #000000; font-weight: bold ">pass</span>

<span>func</span><span>()</span>
<span style=" color: #000000; font-weight: bold ">print</span> <span style=" color: #d01040 ">"do nothing"</span>
</pre></div>


<blockquote style="border-left:4px solid #DDD;padding:0 15px;color:#777">
<p>This is a quote.</p>
</blockquote>
<table style="border-collapse:collapse;border:1px solid grey;">
<thead>
<tr>
<th style="border:1px solid grey;" align="left">Item</th>
<th style="border:1px solid grey;" align="right">Value</th>
<th style="border:1px solid grey;" align="center">Qty</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border:1px solid grey;" align="left">Computer</td>
<td style="border:1px solid grey;" align="right">1600 USD</td>
<td style="border:1px solid grey;" align="center">5</td>
</tr>
</tbody>
</table>
<p>waa</p>
"""

guid = "d7900482-362b-4424-a698-99c1833fb81c"
createEvernote(guid, "fistEvernote", html)