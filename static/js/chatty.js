"use strict";
$(document).ready(function(){
    // Load the chat messages
    loadChat();
    loadUserList();
    // Start polling
    setInterval(loadChat,1000)
    // setInterval(loadUsers,1010)

    // Eventually, we want to use moments.js for the timestamp

    // Define the success functions aka callbacks
    function loadMessages(results) {
        // Define a return string
        var history = '';
        var messages = results.messages;
        for (var i = 0; i < messages.length; i++) { 
            history += messages[i].created_at + " &nbsp;&nbsp;<span class='messageAuthor'> " + messages[i].user_name + "</span>: <span class='messageData'>" + messages[i].data + "</span><br>";
        };

        // Pollute the global namespace like American Electric Power pollutes the air
        window.last_updated = messages[messages.length - 1].created_at
        //console.log("last_updated for ", messages[messages.length - 1], " is ", window.last_updated)
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
        console.log("Starting loadUsers")
        var user_elements = '';
        var users = results.users;

        for (var i = 0; i < users.length; i++) { 
            user_elements += "<a href='#' class='list-group-item'><span class='userName'>" + users[i].name + "</span></a>";
            console.log("User ", users[i].name)
        };

        console.log(users.length + ' users found.')
        // Replace the return string
        $('#userList').html(user_elements);

        console.log("Finished loadUsers");
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
        // console.log("Finished sending AJAX for user_id " + messageInput.user_id + ": " + messageInput.data);
    }

    // Add the event handler to the click event for the button
    $('#message_typing_submit').click(updateChat);


});

