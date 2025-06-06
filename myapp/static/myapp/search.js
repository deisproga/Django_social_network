const searchInput = document.getElementById('search');
const resultsDiv = document.getElementById('results');
const body = document.body; // для проверки темы

searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();
    if (query.length < 2) {
        resultsDiv.innerHTML = '';
        return;
    }

    fetch(`/search_ajax/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            resultsDiv.innerHTML = '';
            if (data.results.length === 0) {
                resultsDiv.textContent = 'Ничего не найдено 😕';
                return;
            }
            data.results.forEach(item => {
                const div = document.createElement('div');
                div.style.padding = '5px 0';

                // Добавим стиль для тёмной темы
                if (body.classList.contains('dark-theme')) {
                    div.style.color = '#ddd';
                } else {
                    div.style.color = '#222';
                }

                div.innerHTML = `<a href="${item.url}" target="_blank" style="text-decoration:none; color: inherit;">${item.title}</a>`;
                resultsDiv.appendChild(div);
            });
        })
        .catch(() => {
            resultsDiv.textContent = 'Ошибка при поиске!';
        });
});


