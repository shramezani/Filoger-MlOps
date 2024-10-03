// Password Strength Meter
const passwordInput = document.querySelector('#password');
const strengthBar = document.querySelector('#passwordStrengthBar');
const strengthText = document.querySelector('#passwordStrengthText');

passwordInput.addEventListener('input', function () {
    const val = passwordInput.value;
    let strength = 0;

    if (val.length >= 8) strength += 1; // Minimum length check
    if (/[A-Z]/.test(val)) strength += 1; // At least one uppercase letter
    if (/[a-z]/.test(val)) strength += 1; // At least one lowercase letter
    if (/[0-9]/.test(val)) strength += 1; // At least one digit
    if (/[^A-Za-z0-9]/.test(val)) strength += 1; // At least one special character

    let strengthPercentage = 0;
    let strengthClass = '';
    let strengthLabel = '';

    switch (strength) {
        case 0:
        case 1:
            strengthPercentage = 20;
            strengthClass = 'bg-danger';
            strengthLabel = 'Very Weak';
            break;
        case 2:
            strengthPercentage = 40;
            strengthClass = 'bg-warning';
            strengthLabel = 'Weak';
            break;
        case 3:
            strengthPercentage = 60;
            strengthClass = 'bg-info';
            strengthLabel = 'Moderate';
            break;
        case 4:
            strengthPercentage = 80;
            strengthClass = 'bg-primary';
            strengthLabel = 'Strong';
            break;
        case 5:
            strengthPercentage = 100;
            strengthClass = 'bg-success';
            strengthLabel = 'Very Strong';
            break;
    }

    strengthBar.style.width = strengthPercentage + '%';
    strengthBar.className = 'progress-bar ' + strengthClass;
    strengthBar.setAttribute('aria-valuenow', strengthPercentage);
    strengthText.textContent = strengthLabel;
});

// Form Validation
(function () {
    'use strict'

    const form = document.getElementById('registrationForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const confirmPasswordHelp = document.getElementById('confirmPasswordHelp');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');

    // Toggle Password Visibility
    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
    });

    toggleConfirmPassword.addEventListener('click', function () {
        const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPassword.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
    });

    // Validate Password Match
    function validatePasswordMatch() {
        if (password.value !== confirmPassword.value) {
            confirmPassword.classList.add('is-invalid');
            confirmPasswordHelp.textContent = 'Passwords do not match.';
            return false;
        } else {
            confirmPassword.classList.remove('is-invalid');
            confirmPasswordHelp.textContent = '';
            return true;
        }
    }

    confirmPassword.addEventListener('input', validatePasswordMatch);

    form.addEventListener('submit', function (event) {
        const isPasswordValid = validatePasswordMatch();

        if (!form.checkValidity() || !isPasswordValid) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
        }
    }, false);
})();

// Send Email Verification Code
document.getElementById('sendEmailCode').addEventListener('click', function() {
    const email = document.getElementById('email').value;

    // Ensure the email field is not empty
    if (!email) {
        alert('Please enter your email first.');
        return;
    }

    fetch('/send_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'email': email
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Verification code sent to your email.');
        } else {
            alert(data.message); // Show error if failed to send code
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while sending the verification code. Please try again.');
    });
});

// Resend Verification Code
document.getElementById('resendCode').addEventListener('click', function() {
    const email = document.getElementById('email').value;

    if (!email) {
        alert('Please enter your email first.');
        return;
    }

    fetch('/send_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'email': email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Verification code has been resent.');
        } else {
            alert(data.message); // Show error if failed to resend
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while resending the verification code. Please try again.');
    });
});
