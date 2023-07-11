const MAIN_CHART_URL = '/sites/looker/api/chart-data';
const FILTERS_CLIENTS_URL = '/sites/looker/api/filter/client-list';
const FILTERS_MONEY_SITES_URL = '/sites/looker/api/filter/money-sites-list';
const DOMAIN_PBN_AND_PUBLICATIONS_URL = '/sites/looker/api/table/domain-pbn-and-publications';
const LINKS_TO_MONEY_SITES_URL = '/sites/looker/api/table/links-to-money-sites';
const LINKS_ANCHOR_COUNTER_URL = '/sites/looker/api/table/anchors';
const SUMMARY_URL = '/sites/looker/api/summary';
const DEFAULT_PAGE_NUM = 1;
const DEFAULT_PER_PAGE_COUNT = 10;


$(document).ready(function () {

    function get_rus_date_format(dt) {
        return new Date(dt).toLocaleString('ru-RU', {
            year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Europe/Moscow', // Set the desired time zone
            hour12: false, // Use 24-hour format
        });
    }

    $('select').select2({
        theme: 'bootstrap', placeholder: 'Select an option', width: '100%',
    }).on('select2:open', function () {
        $('.select2-dropdown').addClass('custom-dropdown');
    });


    function get_summary_list() {
        var url = add_client_id_in_query(SUMMARY_URL);
        url = add_money_sites_in_query(url);
        url = add_date_in_query(url);
        fetch_data(url).then(data => {
            $("#count_new_domains>strong").text(data.count_new_domains.count);
            $("#count_publications>strong").text(data.count_publications.count);
            $("#count_new_publications>strong").text(data.count_new_publications.count);
        });
    }

    function get_date_for_links_to_money_sites_table(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
        var url = `${LINKS_TO_MONEY_SITES_URL}?page=${pageNumber}&per_page=${perPage}&`;
        url = add_client_id_in_query(url);
        url = add_money_sites_in_query(url);
        url = add_date_in_query(url);
        fetch_data(url).then(data => {

            const tbody = document.querySelector("table#table_links_to_money_sites tbody");
            tbody.innerHTML = "";
            createPagination('pagination_links_to_money_sites', data);
            if (data['links'] != undefined) {
                data['links'].forEach((item) => {
                    const row = document.createElement("tr");
                    Object.values(item).forEach((value) => {

                        const td = document.createElement("td");
                        td.textContent = value;
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
            }
        });
    }

    function get_data_for_anchors_table(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
        var url = `${LINKS_ANCHOR_COUNTER_URL}?page=${pageNumber}&per_page=${perPage}&`;
        url = add_client_id_in_query(url);
        url = add_money_sites_in_query(url);
        url = add_date_in_query(url);

        fetch_data(url).then(data => {
            const tbody = document.querySelector("table#table_anchor_counter tbody");
            tbody.innerHTML = "";
            createPagination('pagination_anchor_counter', data);
            if (data['links'] != undefined) {
                var counter = 0;
                data['links'].forEach((item) => {
                    const row = document.createElement("tr");
                    Object.values(item).forEach((value) => {
                        const td = document.createElement("td");
                        td.textContent = value;
                        row.appendChild(td);

                        if (typeof value === 'number' && !isNaN(value)) {
                            counter += value;
                        }
                    });
                    tbody.appendChild(row);
                });
                var row = document.createElement("tr");
                var td = document.createElement("th");
                td.textContent = "Общий итог";
                td.colSpan = "2";
                row.appendChild(td);
                var td = document.createElement("th");
                td.textContent = counter;
                row.appendChild(td);
                tbody.appendChild(row);
            }
        });
    }

    function get_data_for_table_pbn_and_publications(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
        var url = `${DOMAIN_PBN_AND_PUBLICATIONS_URL}?page=${pageNumber}&per_page=${perPage}&`;
        url = add_client_id_in_query(url);
        url = add_money_sites_in_query(url);
        url = add_date_in_query(url);
        fetch_data(url).then(data => {
            const tbody = document.querySelector("table#table_domain_and_pbn tbody");
            tbody.innerHTML = "";
            createPagination('pagination_domain_and_pbn', data);
            data['links'].forEach((item) => {
                const row = document.createElement("tr");
                item['last_post'] = get_rus_date_format(item['last_post']);
                item['date_create'] = get_rus_date_format(item['date_create']);
                Object.values(item).forEach((value) => {
                    const td = document.createElement("td");
                    td.textContent = value;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });
        });
    }

    function get_data_for_filter_by_client() {
        var url = FILTERS_CLIENTS_URL;
        fetch_data(url).then(data => {
            var options = '<option value="all">All</option>';
            for (var item of data) {
                var option = '<option value=":val">:name</option>';
                options += option.replace(':val', item.id).replace(':name', item.name);
            }
            var clients = document.querySelector("select#clients");
            clients.innerHTML = options;
        })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }


    function get_data_for_filter_by_money_sites() {
        var url = add_client_id_in_query(FILTERS_MONEY_SITES_URL);
        fetch_data(url).then(data => {
            var options = '';
            for (var item of data) {
                var current_client = get_client_id();
                var option = '<option value=":val" :params>:name</option>';
                options += option.replace(':val', item.id).replace(':name', item.name);
            }
            var money_sites = document.querySelector("select#money_sites");
            money_sites.innerHTML = options;
        }).catch(error => {
            console.error('Error fetching data:', error);
        });
    }

    function get_data_for_chart() {
        var url = add_client_id_in_query(MAIN_CHART_URL);
        url = add_money_sites_in_query(url);
        fetch_data(url).then(data => {
            const datasets = {};
            // Group data by label
            data.forEach(item => {
                const label = item.label;
                if (!datasets[label]) {
                    datasets[label] = {
                        label: label, data: [], borderColor: get_random_color(), backgroundColor: 'rgba(0, 0, 0, 0)',
                    };
                }
                item['x'] = get_rus_date_format(item['x']);
                datasets[label].data.push({
                    x: item.x, y: item.y
                });
            });
            const chartData = {
                labels: Array.from(new Set(data.map(item => item.x))), datasets: Object.values(datasets),
            };
            const ctx = document.getElementById('publicationChart').getContext('2d');
            const existingChart = Chart.getChart(ctx);
            if (existingChart) {
                existingChart.destroy();
            }
            var chart = new Chart(ctx, {
                type: 'line', data: chartData, options: {
                    responsive: true, title: {
                        display: true, text: 'Publications by Client'
                    }, scales: {
                        x: {
                            title: {
                                display: true, text: 'Publication Date'
                            }
                        }, y: {
                            title: {
                                display: true, text: 'Publication Count'
                            }
                        }
                    }
                }
            });
        })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    get_data_for_filter_by_client();
    get_data_for_chart();
    get_data_for_table_pbn_and_publications();
    get_date_for_links_to_money_sites_table();
    get_data_for_anchors_table();
    get_summary_list();
    get_data_for_filter_by_money_sites();
    // Get the select element by its ID
    var select_clients = $("select#clients");
    select_clients.change(function () {
        get_data_for_filter_by_money_sites();
        get_summary_list();
        get_data_for_chart();
        get_data_for_table_pbn_and_publications();
        get_date_for_links_to_money_sites_table();
        get_data_for_anchors_table();
    });
    var select_money_sites = $("select#money_sites");
    select_money_sites.change(function () {
        get_data_for_chart();
        get_data_for_table_pbn_and_publications();
        get_date_for_links_to_money_sites_table();
        get_data_for_anchors_table();
        get_summary_list();

    });
    var start_date = $('#start-date');
    var end_date = $('#end-date');
    start_date.change(function () {

    });
    end_date.change(function () {

    });

    document.querySelector("#pagination_links_to_money_sites").addEventListener("click", function (event) {
        event.preventDefault();
        if (event.target.tagName === "A") {
            const pageNumber = parseInt(event.target.dataset.page);
            get_date_for_links_to_money_sites_table(pageNumber);
        }
    });

    document.querySelector("#pagination_domain_and_pbn").addEventListener("click", function (event) {
        event.preventDefault();
        if (event.target.tagName === "A") {
            const pageNumber = parseInt(event.target.dataset.page);
            get_data_for_table_pbn_and_publications(pageNumber);
        }
    });

    document.querySelector("#pagination_anchor_counter").addEventListener("click", function (event) {
        event.preventDefault();
        document.querySelector('#pagination_anchor_counter a').style.color = "";
        if (event.target.tagName === "A") {
            const pageNumber = parseInt(event.target.dataset.page);
            get_data_for_anchors_table(pageNumber);
        }
    });


});


////////////////////////////

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

// Helper function to generate random colors for chart lines
function get_random_color() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


function get_client_id() {
    var client_id = parseInt($("#clients").val());
    return isNaN(client_id) ? null : client_id > 0 ? client_id : null;
}

// Function to create pagination links
function createPagination(el, data) {
    const pagination = document.querySelector(`#${el} ul`);
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
        const activeClass = (1 === data.page_number) ? "active" : "";
        firstLink.innerHTML = `<a class="page-link ${activeClass}" href="#" data-page="1">1</a>`;
        pagination.appendChild(firstLink);

        if (startPage > 2) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.innerHTML = `<span class="page-link">...</span>`;
            pagination.appendChild(ellipsisLink);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageLink = document.createElement("li");
        const activeClass = (i === data.page_number) ? "active" : "";
        pageLink.innerHTML = `<a class="page-link ${activeClass}" href="#" data-page="${i}">${i}</a>`;
        pagination.appendChild(pageLink);
    }

    if (endPage < data.total_pages) {
        if (endPage < data.total_pages - 1) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.innerHTML = `<span class="page-link">...</span>`;
            pagination.appendChild(ellipsisLink);
        }

        const lastLink = document.createElement("li");
        lastLink.innerHTML = `<a class="page-link" href="#" data-page="${data.total_pages}">${data.total_pages}</a>`;
        pagination.appendChild(lastLink);
    }
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

function add_money_sites_in_query(main_url) {
    main_url = prepare_url(main_url);
    var money_sites_query = "money_sites=";
    var money_sites = $('#money_sites').select2('data').map((item) => {
        return item.id
    });
    if (money_sites.length > 0) {
        money_sites_query += money_sites.join(',');
    }
    return main_url + money_sites_query;
}

function add_client_id_in_query(main_url) {
    main_url = prepare_url(main_url);
    var client_id = get_client_id();
    if (client_id && client_id !== 'all') {
        return main_url + `client_id=${client_id}`;
    }
    return main_url;
}

function add_date_in_query(main_url) {
    main_url = prepare_url(main_url);
    var query = '';
    var start_date = $('#start-date').val();
    var end_date = $('#end-date').val();
    if (start_date) {
        query += 'start_date=' + start_date;
    }
    if (end_date) {
        if (query) {
            query += '&'
        }
        query += 'end_date=' + end_date;
    }
    return main_url + query;
}

