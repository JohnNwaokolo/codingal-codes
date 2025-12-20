let balance = 0;

function deposit(){
    let amount = parseFloat(document.getElementById("amount").value);

    if (isNaN(amount) || amount<=0) {
        document.getElementById("alert").innerText = "Please enter a valid amount!";
        return;
    }

    balance += amount;
    updateBalance();
    document.getElementById("amount").value = "";
    document.getElementById("alert").innerText = `Deposited $${amount}.`;

    let now = new Date();
    let timeString = now.toLocaleTimeString();


    let history = document.getElementById("history");
    let li = document.createElement("li");
    li.style.color = "green"
    li.innerText = `Deposited $${amount}`;
    let prevText = li.innerText;
    let finalText = prevText + " ----- " + timeString;
    li.innerText = finalText;
    history.appendChild(li);

    

}

function withdraw() {
    let amount = parseFloat(document.getElementById("amount").value);

    if (isNaN(amount) || amount <= 0) {
        document.getElementById("alert").innerText = "Please enter a valid amount!";
        return;
    }

    if (amount > balance) {
        document.getElementById("alert").innerText = "Insufficient funds!";
        document.getElementById("amount").value = "";
        return;
    }

    balance -= amount;
    updateBalance();
    document.getElementById("amount").value = "";
    document.getElementById("alert").innerText = `Withdrew $${amount}.`;

    let now = new Date();
    let timeString= now.toLocaleTimeString()


    let history = document.getElementById("history");
    let li = document.createElement("li");
    li.style.color = "red"
    li.innerText = `Withdrew $${amount}`;
    let prevText= li.innerText
    let finalText = prevText + " ----- "+ timeString
    li.innerText = finalText
    history.appendChild(li);
}

function updateBalance() {
    document.getElementById("balance").innerText = balance;
}

document.getElementById("depositBtn").addEventListener("click", deposit);
document.getElementById("withdrawBtn").addEventListener("click", withdraw);
