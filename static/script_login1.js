document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();
        validateLoginForm();
    });

    function validateLoginForm() {
        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");
        const usernameError = document.getElementById("usernameError");
        const passwordError = document.getElementById("passwordError");

        // Reset errors
        usernameError.textContent = "";
        passwordError.textContent = "";

        let isValid = true;

        // Username validation
        if (usernameInput.value.trim() === "") {
            usernameError.textContent = "Username is required";
            isValid = false;
        }

        // Password validation
        if (passwordInput.value.trim() === "") {
            passwordError.textContent = "Password is required";
            isValid = false;
        }

        // If form is valid, submit it
        if (isValid) {
            sendLoginDataToServer();
        }
    }

    function sendLoginDataToServer() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Login successful!');
                sessionStorage.setItem('username', username);
                window.location.href = '/user/'+username;
            } else {
                alert('Invalid credentials!');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
