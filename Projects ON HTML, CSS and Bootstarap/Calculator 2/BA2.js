let balance = 0; // Initial balance

function deposit() {
    let amount = parseFloat(document.getElementById("amount").value);
    
    if (isNaN(amount) || amount <= 0) {
        document.getElementById("message").innerText = "Please enter a valid amount!";
        return;
    }

    balance += amount;
    updateBalance();
    document.getElementById("message").innerText = `Deposited $${amount}.`;
}

function withdraw() {
    let amount = parseFloat(document.getElementById("amount").value);

    if (isNaN(amount) || amount <= 0) {
        document.getElementById("message").innerText = "Please enter a valid amount!";
        return;
    }

    if (amount > balance) {
        document.getElementById("message").innerText = "Insufficient balance.";
        return;
    }

    balance -= amount;
    updateBalance();
    document.getElementById("message").innerText = `Withdrew $${amount}.`;
}

function updateBalance() {
    document.getElementById("balance").innerText = balance;
}
