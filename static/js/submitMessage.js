"use strict";

// Define the success function
function replaceStatus(results) {
    var new_msg = results.user_id + ": " + results.data;
    console.log(new_msg);
    $('#messageHistory').html(results.data);
    console.log("Finished replaceStatus");
}

// Define the event handler
function updateChatRoom(evt) {
	var messageInput = {
		"data": $("#message_typing_box").val(),
		"user_id": 1
	};

    $.post('/api/rooms/1/messages', messageInput, replaceStatus);
    console.log("Finished sending AJAX for user_id " + messageInput.user_id + ": " + messageInput.data);
}

// Add the event handler to the click event for the button
$('#message_typing_submit').click(updateChatRoom);