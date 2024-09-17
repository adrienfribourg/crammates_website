document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript Loaded");

    // Add study session functionality
    const form = document.getElementById('session-form');
    const confirmation = document.getElementById('confirmation');

    if (form && confirmation) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            // Get form values
            const topic = document.getElementById('topic').value;
            const date = document.getElementById('date').value;
            const time = document.getElementById('time').value;
            const location = document.getElementById('location').value;

            // Basic validation
            if (topic && date && time && location) {
                // Send data to the server using fetch
                fetch('/add_session', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'topic': topic,
                        'date': date,
                        'time': time,
                        'location': location
                    })
                })
                .then(response => {
                    if (response.ok) {
                        form.reset();
                        confirmation.style.display = 'block';
                        setTimeout(() => {
                            confirmation.style.display = 'none';
                        }, 3000);
                        fetchSessions(); // Refresh session list after adding
                    } else {
                        alert('An error occurred while adding the session.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the session.');
                });
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // Function to fetch and display study sessions
    function fetchSessions() {
        fetch('/get_sessions')
            .then(response => response.json())
            .then(sessions => {
                const sessionList = document.getElementById('session-list');
                sessionList.innerHTML = ''; // Clear the list before appending

                if (sessions.length > 0) {
                    sessions.forEach(session => {
                        const listItem = document.createElement('li');
                        listItem.textContent = `${session.topic} on ${session.date} at ${session.time}, Location: ${session.location}`;

                        // Add delete button for each session
                        const deleteButton = document.createElement('button');
                        deleteButton.textContent = 'Delete';
                        deleteButton.classList.add('btn', 'btn-danger');
                        deleteButton.setAttribute('data-id', session.id);  // Add session id to the button
                        deleteButton.addEventListener('click', function() {
                            console.log('Delete button clicked for session ID:', session.id); // Add this line
                            if (confirm('Are you sure you want to delete this session?')) {
                                deleteSession(session.id);
                            }
                        });

                        listItem.appendChild(deleteButton);
                        sessionList.appendChild(listItem);
                    });
                } else {
                    sessionList.textContent = 'No study sessions found.';
                }
            })
            .catch(error => {
                console.error('Error fetching sessions:', error);
            });
    }

    // Function to delete a session
    function deleteSession(sessionId) {
        console.log('Deleting session with ID:', sessionId);  // Add this line
        fetch(`/delete_session/${sessionId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log('Response from delete:', response); // Add this line
            if (response.ok) {
                alert('Session deleted successfully');
                fetchSessions(); // Refresh session list after deletion
            } else {
                alert('Failed to delete session.');
            }
        })
        .catch(error => {
            console.error('Error deleting session:', error);
            alert('An error occurred while trying to delete the session.');
        });
    }

    // Fetch and display sessions when the page loads
    if (document.getElementById('session-list')) {
        fetchSessions();
    }
});
