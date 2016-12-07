
$(document).ready(function() {
  $("#shout").on('click', function() {
    var shout_node = $("#shout_text");
    var data = $(shout_node).val();
    $.ajax({
      url: '/new',
      method: 'POST',
      dataType: 'text',
      data: data,
      success: function(data) {
        $(shout_node).val("");
      }
    })

  });


  $("#shout_text").on('keypress', function(e) {
    if(e.keyCode == 13) {
      var shout_node = $("#shout_text");
      var data = $(shout_node).val();
      $.ajax({
        url: '/new',
        method: 'POST',
        dataType: 'text',
        data: data,
        success: function(data) {
          $(shout_node).val("");
        }
      });
    }
  });

  updater.poll();
});

var updater = {
  poll: function() {
    $.ajax({
      url: '/update',
      method: 'POST',
      dataType: 'text',
      data: 'aaa',
      success: function(data) {
        // add the message to chatbox.
        console.log(data);

        $("#chatbox").append(data);

        updater.poll();
      }
    });
  }

}
