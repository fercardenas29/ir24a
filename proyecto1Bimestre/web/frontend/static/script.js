document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var query = document.getElementById('query').value;
    var method = document.getElementById('method').value;
    var threshold = document.getElementById('threshold').value;

    fetch(`/search?q=${encodeURIComponent(query)}&method=${method}&threshold=${threshold}`)
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Error:', error));
});

function displayResults(results) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    // Mostrar resultados
    if (results.length > 0) {
        const resultsTitle = document.createElement('h3');
        resultsTitle.textContent = 'Resultados';
        resultsContainer.appendChild(resultsTitle);
        
        const resultsList = document.createElement('ul');
        results.forEach(result => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>Documento:</strong> ${result.filename}<br><strong>Contenido:</strong> ${result.content}`;
            resultsList.appendChild(listItem);
        });
        resultsContainer.appendChild(resultsList);
    } else {
        const noResults = document.createElement('p');
        noResults.textContent = 'No se encontraron resultados, aplica Berry Picking';
        resultsContainer.appendChild(noResults);
    }
}
