function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    const chatContent = document.getElementById('chat-content');
    chatContent.innerHTML += `<p>User: ${userInput}</p>`;

    fetch('/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ queryResult: { queryText: userInput } })
    })
    .then(response => response.json())
    .then(data => {
        chatContent.innerHTML += `<p>Bot: ${data.fulfillmentText}</p>`;
        document.getElementById('user-input').value = '';
    })
    .catch(error => console.error('Error:', error));
}
