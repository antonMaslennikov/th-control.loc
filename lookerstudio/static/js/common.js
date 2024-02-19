function get_random_color() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function get_rus_date_format(dt) {
    return new Date(dt).toLocaleString('ru-RU', {
        year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Europe/Moscow', // Set the desired time zone
        hour12: false, // Use 24-hour format
    });
}

function fetch_data(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const serializedData = JSON.stringify(data);
            localStorage.setItem(url, serializedData);
            return data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function prepare_url(main_url) {
    var length = main_url.length;
    if (main_url.includes('?')) {
        if (main_url[length - 1] !== '&') {
            main_url += '&';
        }
    } else {
        main_url += '?';
    }
    return main_url;
}


function createPagination(el, data) {
    const pagination = document.querySelector(`#${el}`);
    pagination.innerHTML = ""; // Clear existing links
    if (!(data != undefined && data.total_pages != undefined && data.total_pages > 1)) {
        return;
    }

    let startPage = Math.max(1, data.page_number - 2);
    if (isNaN(startPage)) {
        startPage = 1;
    }

    let endPage = Math.min(startPage + 4, data.total_pages);
    if (startPage > 1) {
        const firstLink = document.createElement("li");
        firstLink.classList.add('page-item');
        if (1 === data.page_number) {
            firstLink.classList.add('active');
        }
        firstLink.innerHTML = `<a href="#" data-page="1" class="page-link">1</a>`;
        pagination.appendChild(firstLink);

        if (startPage > 2) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.classList.add('page-item');
            ellipsisLink.innerHTML = `<span class="page-link">...</span>`;
            pagination.appendChild(ellipsisLink);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageLink = document.createElement("li");
        pageLink.classList.add('page-item');
        if (i == data.page_number) {
            pageLink.classList.add('active');
        }
        pageLink.innerHTML = `<a href="#" data-page="${i}" class="page-link">${i}</a>`;
        pagination.appendChild(pageLink);
    }

    if (endPage < data.total_pages) {
        if (endPage < data.total_pages - 1) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.classList.add('page-item');
            ellipsisLink.innerHTML = `<span class="page-link">...</span>`;
            pagination.appendChild(ellipsisLink);
        }

        const lastLink = document.createElement("li");
        lastLink.innerHTML = `<a href="#" data-page="${data.total_pages}" class="page-link">${data.total_pages}</a>`;
        pagination.appendChild(lastLink);
    }
}