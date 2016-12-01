

function updatePreview() {
  update_text = $('#raw').val();
  $.ajax({
    type: 'POST',
    url: '/preview',
    data: update_text,
    contentType: 'text/plain',
    success: function(data) {
      $('#mirror').html(data);
    }
  });
}

function createDoc() {
  $.ajax({
    type: 'GET',
    url: '/create',
    success: function(data) {
      $('#raw').val('');
      $('#mirror').html('');
      $('#doc_id').html(data['fid']);
      document.title = data['title'];
    }
  });
}

function preview() {
  fid = $('#doc_id').html();
  window.location.replace('/showpreview/' + fid)
}

function render_data(data) {
  html = '<table id="pagination_table"class="table"><thead style="color:red;"><tr><td>Title</td><td>Created Time</td></tr></thead><tbody>'
  for(var i=0; i<data.length; i++) {
    html += '<tr><td>';
    html += '<a href="/show/'
    html += data[i]['fid']
    html += '">'
    html += data[i]['title'];
    html += '</a></td><td>';
    html += data[i]['created'];
    html += '</td></tr>';
  }
  html += '</tbody></table>';
  return html
}

$(document).ready(function() {
  $(document).on('keydown', function(e){
      if(e.ctrlKey && e.which === 83){ // Check for the Ctrl key being pressed, and if the key = [S] (83)
          raw = $('#raw').val();
          html = $('#mirror').html();
          fid = $('#doc_id').html();
          title = raw.substring(0, 6);
          $.ajax({
            type: 'POST',
            url: '/save',
            data: JSON.stringify({fid: fid, title: title, raw: raw, html: html}),
            contentType: 'json',
            success: function(data) {
                document.title = title;
                $('#doc_id').html(data);
            }
          });
          e.preventDefault();

      }
  });

  $('#doc_modal').on('click', function() {
    $.ajax({
      type: 'GET',
      url: '/mydocs',
      success: function(data) {
        $('#modal_body').html(render_data(data['docs']));
        $('#pagination_table').DataTable();
      }
    });
  });

});
