const alertButton = document.getElementById("alert-button");
const alertResult = document.getElementById("alert-result");

if (alertButton) {
    alertButton.addEventListener("click", () => {
        alert("This is a Selenium practice alert.");
        alertResult.textContent = "The alert was displayed.";
    });
}

const delayedButton = document.getElementById("delayed-button");
const delayedMessage = document.getElementById("delayed-message");

if (delayedButton) {
    delayedButton.addEventListener("click", () => {
        delayedMessage.textContent = "Loading...";

        setTimeout(() => {
            delayedMessage.textContent =
                "The delayed message has loaded.";
        }, 3000);
    });
}