document.getElementById("resetPasswordForm").addEventListener("submit", function(event) {
    // Prevent default form submission until we check the validation
    let securityAnswer = document.getElementById("securityAnswer").value.trim();
    let newPassword = document.getElementById("newPassword").value.trim();
    let confirmPassword = document.getElementById("confirmPassword").value.trim();

    // Basic Validation
    if (newPassword !== confirmPassword) {
        alert("Passwords do not match!");
        event.preventDefault();  // Prevent form submission if passwords don't match
        return false;
    }

    if (securityAnswer === "") {
        alert("Please answer the security question.");
        event.preventDefault();  // Prevent form submission if the email is empty
        return false;
    }

    // Validation passed, form will now submit
    return true;
});
