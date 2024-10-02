


function copyUsername1() {
// Get the value from the input field
var form = document.getElementById('createUserform')
var inputValue = form.querySelector('#username').value;

// Set the value
document.getElementById('pasteUser1').innerText = "Create user " + inputValue + " ?";  

}

function copyUsername2() {
// Get the value from the input field
var form = document.getElementById('deleteUserform')
var inputValue = form.querySelector('#username').value;

// Set the value
document.getElementById('pasteUser2').innerText = "Delete user " + inputValue + " ?";  

}

// return img result
function showResultModal(message) {
    var resultModal = document.getElementById('resultModal');
    var resultText = document.getElementById('resultText');
    resultText.innerText = message;
    resultModal.style.display = 'block';
    setTimeout(function() {
        resultModal.style.display = 'none';
    }, 3000);
}

// add user
function confirmAddUser () {
    var form = document.getElementById('createUserform');
    var username = form.querySelector('#username').value;
    var password = form.querySelector('#password').value;

    $.ajax({
        type: 'POST',
        url: '/create_user',
        data: { username: username, password: password },
        success: function(data) {
            if (data.success) {
                showResultModal('User created successfully!');
            } else {
                showResultModal('Error: ' + data.message);
            }
        },
        error: function() {
            showResultModal('An error occurred while creating the user.');
        }
    });
}

// delete user
function confirmDeleteUser () {
    var form = document.getElementById('deleteUserform');
    var username = form.querySelector('#username').value;

    $.ajax({
        type: 'POST',
        url: '/delete_user',
        data: { username: username },
        success: function(data) {
            if (data.success) {
                showResultModal('User deleted successfully!');
            } else {
                showResultModal('Error: ' + data.message);
            }
        },
        error: function() {
            showResultModal('An error occurred while deleting the user.');
        }
    });
}

