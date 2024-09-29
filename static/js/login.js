function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}




document.getElementById('show-login').addEventListener('click', () => {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
});

document.getElementById('show-register').addEventListener('click', () => {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
});

document.getElementById('login-btn').addEventListener('click', async () => {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const usernameError = document.getElementById('login-username-error');
    const passwordError = document.getElementById('login-password-error');
    const loginError = document.getElementById('login-error');

    usernameError.textContent = '';
    passwordError.textContent = '';
    loginError.textContent = '';

    let isValid = true;

    if (password.length < 8 || password.length > 16) {
        passwordError.textContent = 'Пароль має бути від 8 до 16 символів.';
        isValid = false;
    }

    if (!isValid) return;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const result = await response.json();

        if (response.ok) {
            setCookie('user', username, 7);
            window.location.href = '/';
        } else {
            loginError.textContent = result.error || 'Невдала спроба входу.';
        }
    } catch (error) {
        loginError.textContent = 'Сталася помилка при вході.';
    }
});

document.getElementById('register-btn').addEventListener('click', async () => {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const accessRights = document.getElementById('register-access-rights').value;

    const usernameError = document.getElementById('register-username-error');
    const passwordError = document.getElementById('register-password-error');
    const accessRightsError = document.getElementById('register-access-rights-error');
    const registerError = document.getElementById('register-error');

    usernameError.textContent = '';
    passwordError.textContent = '';
    accessRightsError.textContent = '';
    registerError.textContent = '';

    let isValid = true;

    if (password.length < 8 || password.length > 16) {
        passwordError.textContent = 'Пароль має бути від 8 до 16 символів.';
        isValid = false;
    }

    if (!isValid) return;

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password,
                access_rights: accessRights
            })
        });

        const result = await response.json();

        if (response.ok) {
            setCookie('user', username, 7);
            window.location.href = '/';
        } else {
            registerError.textContent = result.error || 'Невдала спроба реєстрації.';
        }
    } catch (error) {
        registerError.textContent = 'Сталася помилка при реєстрації.';
    }
});

document.getElementById('forgot-password-btn').addEventListener('click', async () => {
    const username = document.getElementById('login-username').value;

    if (!username) {
        document.getElementById('login-username-error').textContent = 'Введіть логін для відновлення паролю';
        return;
    }

    document.getElementById('login-username-error').textContent = '';

    try {
        const response = await fetch('/api/login/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('forgot-password-response').textContent = 'Ваш пароль: ' + data.password;
        } else {
            document.getElementById('forgot-password-response').textContent = 'Помилка: ' + data.error;
        }
    } catch (error) {
        console.error('Помилка:', error);
        document.getElementById('forgot-password-response').textContent = 'Помилка при відновленні паролю';
    }
});