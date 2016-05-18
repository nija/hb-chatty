"use strict";

// Define the success function
function replaceStatus(results) {
    var messages = results.messages;
    var history = ''
    console.log(messages);
    for (var i = 0; i < messages.length; i++) { 
        history += messages[i].created_at + " &nbsp;&nbsp; " + messages[i].user_name + ": " + messages[i].data + "<br>";
    };
    $('#messageHistory').html(history);
    console.log("Finished replaceStatus");
}

// Define the event handler
function updateChat(evt) {
	var messageInput = {
		"data": $("#message_typing_box").val(),
		"user_id": 2
	};

    $('#message_typing_box').val('');
    $.post('/api/rooms/1/messages', messageInput, replaceStatus);
    // console.log("Finished sending AJAX for user_id " + messageInput.user_id + ": " + messageInput.data);
}

// Add the event handler to the click event for the button
$('#message_typing_submit').click(updateChat);