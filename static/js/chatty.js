"use strict";
$(document).ready(function(){
    // Load the chat messages
    loadChat();
    loadUserList();
    // Start polling
    setInterval(loadChat,1000)
    setInterval(loadUserList,1010)

    // Define the success functions aka callbacks
    function loadMessages(results) {
        // Define a return string
        var history = '';
        // Get our results payload
        var messages = results.messages;
        // Get the offset
        var utcDiff = moment().utcOffset() / 60;
        // This works but is deprecated
        // var utcOffset_real = moment().zone() / 60;

        for (var i = 0; i < messages.length; i++) {
            // 2016-06-03T00:35:15.484657-07:00
            // YYYY-MM-DDTHH:mm:ss.SSSSSSZ

            var dt_stamp = moment(messages[i].created_at, 'YYYY-MM-DDTHH:mm:ss.SSSSSSZ').add(utcDiff,'hours').fromNow();

            history += "<tr><td class='tdMessageDate'><span class='hidden-xs messageDate'>" + dt_stamp + "</span></td><td class='tdMessageAuthor'><span class='messageAuthor'> " + messages[i].user_name + "</span></td><td class='tdMessageData'><span class='messageData'>" + messages[i].data + "</span></td></tr>";
        };

        // Pollute the global namespace like American Electric Power pollutes the air
        window.last_updated = messages[messages.length - 1].created_at
        // Replace the return string
        $('#messageHistory').html(history);

        // console.log("Finished replaceStatus");
    }

    // =====================================================================

    // Define the event handler to handle the AJAX GET users request
    function loadChat(evt) {
        // AJAX call
        $.getJSON("/api/rooms/1/messages",loadMessages);
    }

    function loadUsers(results) {
        // Define a return string
        // console.log("Starting loadUsers")
        var user_elements = '';
        var users = results.users;

        for (var i = 0; i < users.length; i++) { 
            user_elements += "<span class='list-group-item userName'>" + users[i].name + "</span>";

        };

        // Replace the return string
        $('#userList').html(user_elements);

    }

    // Define the event handler to handle the AJAX GET request
    function loadUserList(evt) {
        console.log("Starting loadUserList")
        // AJAX call
        $.getJSON("/api/rooms/1/users",loadUsers);
        console.log("Finished loadUserList")
    }

    // =====================================================================

    // Define the event handler to handle the AJAX POST message request
    function updateChat(evt) {
        var messageInput = {
            "data": $("#message_typing_box").val(),
            "user_id": 2 /*,
            "last_updated": 10*/
        };

        // clear the text area
        $('#message_typing_box').val('');
        // use the same callback function as the GET
        $.post('/api/rooms/1/messages', messageInput, loadMessages);
        document.getElementById("message_typing_box").focus();
        // console.log("Finished sending AJAX for user_id " + messageInput.user_id + ": " + messageInput.data);
    }

    // Add the event handler to the click event for the button
    $('#message_typing_submit').click(updateChat);


});

