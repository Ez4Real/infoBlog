const showHideBtnPass = document.getElementById('pass');
const showHideBtnConfPass = document.getElementById('re-pass')
const passwordField = document.getElementById('password_field');
const passwordConfField = document.getElementById('password_conf_field');
const showHideIcon = document.querySelector('#show_hide_password i');
const showReHideIcon = document.querySelector('#show_hide_conf_password i');

showHideBtnPass.addEventListener('click', function () {
  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    showHideIcon.classList.remove('fa-eye');
    showHideIcon.classList.add('fa-eye-slash');
  } else {
    passwordField.type = 'password';
    showHideIcon.classList.remove('fa-eye-slash');
    showHideIcon.classList.add('fa-eye');
  }
});

showHideBtnConfPass.addEventListener('click', function () {
  if (passwordConfField.type === 'password') {
    passwordConfField.type = 'text';
    showReHideIcon.classList.remove('fa-eye');
    showReHideIcon.classList.add('fa-eye-slash');
  } else {
    passwordConfField.type = 'password';
    showReHideIcon.classList.remove('fa-eye-slash');
    showReHideIcon.classList.add('fa-eye');
  }
});