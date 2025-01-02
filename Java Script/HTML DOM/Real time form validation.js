function validate(e) {
    e.preventdefault();

    const email = document.getElementById("email").innerHTML.value;
    const pass = document.getElementById("pass").innerHTML.value;
    const age = document.getElementById("age").innerHTML.value;
    const msgBox = document.getElementById("msgBox").innerHTML;

    let message = "";

    if (email === "") {
        message = "Enter an email";
        msgBox.style.color = "red";
    }
    else if (pass === "") {
        message = "Enter a password";
        msgBox.style.color = "blue";
    }
    else if (age === "") {
        message = "Enter your age";
        msgBox.style.color = "orange";
    }
    else {
        message = "Login successful";
        msgBox.style.color = "green";
    }
    msgBox.innerText = message;
    document.getElementById("loginForm").addEventListener("submit", validate);
}
