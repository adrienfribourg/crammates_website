document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript Loaded");

    // Add any JavaScript functionality here if needed

    // Example: Display a confirmation message when a study session is created
    const form = document.getElementById('session-form');
    const confirmation = document.getElementById('confirmation');

    if (form && confirmation) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            // Get form values (Example IDs, modify as needed)
            const topic = document.getElementById('topic').value;
            const date = document.getElementById('date').value;
            const time = document.getElementById('time').value;
            const location = document.getElementById('location').value;

            // Basic validation (could be expanded)
            if (topic && date && time && location) {
                // Here, you would typically send the data to a server
                // For demonstration, we'll just show a confirmation message

                form.reset();
                confirmation.style.display = 'block';
                setTimeout(() => {
                    confirmation.style.display = 'none';
                }, 3000);
            } else {
                alert('Please fill in all fields.');
            }
        });
    }
});