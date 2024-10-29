document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("problemForm");
    const confirmationMessage = document.getElementById("confirmationMessage");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission to show the message

        // Show confirmation message
        confirmationMessage.classList.remove("hidden");

        // Clear the form fields
        form.reset();
    });
});