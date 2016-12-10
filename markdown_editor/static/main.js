
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

$(document).ready(function() {
  $(document).on('keydown', function(e){
      if(e.ctrlKey && e.which === 83){ // Check for the Ctrl key being pressed, and if the key = [S] (83)
          raw = $('#raw').val();
          html = $('#mirror').html();
          fid = $('#doc_id').html();
          $.ajax({
            type: 'POST',
            url: '/save',
            data: JSON.stringify({fid: fid, raw: raw, html: html}),
            contentType: 'json',
            success: function(data) {
                document.title = data['title'];
                $('#doc_id').html(data['fid']);
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
        $('#modal_body').html(data);
        $('#pagination_table').DataTable();
      }
    });
  });

});
