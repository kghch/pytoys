

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

$(document).ready(function() {


});
