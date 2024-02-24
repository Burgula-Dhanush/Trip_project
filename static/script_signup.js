document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", function(event) {
        event.preventDefault();
        validateForm();
    });

    function validateForm() {
        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");
        const dobInput = document.getElementById("dob");
        const usernameError = document.getElementById("usernameError");
        const passwordError = document.getElementById("passwordError");
        const dobError = document.getElementById("dobError");

        // Reset errors
        usernameError.textContent = "";
        passwordError.textContent = "";
        dobError.textContent = "";

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

        // Date of Birth validation
        if (dobInput.value === "") {
            dobError.textContent = "Date of Birth is required";
            isValid = false;
        }

        // If form is valid, submit it
        if (isValid) {
            console.log("Yooooo did it");
            sendDataToServer();
        }
    }

    function sendDataToServer() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const dob = document.getElementById("dob").value;
        console.log("HIIII");
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, dob }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Sign Up successful!');
                window.location.href = '/';
            } else {
                alert('Error!');
            }
            })
        .catch(error => console.error('Error:', error));
    }
});
