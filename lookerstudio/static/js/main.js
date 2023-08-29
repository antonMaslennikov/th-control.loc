const FILTER_GET_CLIENT_LIST_URL = '/looker-studio/get-client-list';
const FILTER_GET_MONEY_SITES_LIST_URL = '/looker-studio/get-money-sites-list';
const MAIN_CHART_URL = '/looker-studio/chart-data';
const FILTERS_CLIENTS_URL = '/sites/looker/api/filter/client-list';
const FILTERS_MONEY_SITES_URL = '/sites/looker/api/filter/money-sites-list';
const DOMAIN_PBN_AND_PUBLICATIONS_URL = '/sites/looker/api/table/domain-pbn-and-publications';
const LINKS_TO_MONEY_SITES_URL = '/sites/looker/api/table/links-to-money-sites';
const LINKS_ANCHOR_COUNTER_URL = '/sites/looker/api/table/anchors';
const SUMMARY_URL = '/looker-studio/summary';
const DEFAULT_PAGE_NUM = 1;
const DEFAULT_PER_PAGE_COUNT = 10;

function get_summary_list() {
    var url = add_clients_in_query(SUMMARY_URL);
    url = add_money_sites_in_query(url);
    url = add_date_in_query(url);
    fetch_data(url).then(data => {
        $("#count_new_domains>strong").text(data.new_domains.new_domains);
        $("#count_publications>strong").text(data.publications.new_publications);
        $("#count_new_publications>strong").text(data.pbn_domains.count);
    });
}

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

function add_clients_in_query(main_url) {
    main_url = prepare_url(main_url);

    var clients_query = '';
    var clients = [];

    $('#filter-client-list input[type="checkbox"]:checked').each((i, item) => {
        clients.push($(item).val());
    });

    if (clients.length > 0) {
        clients_query = "clients=" + clients.join(',');
    }

    return main_url + clients_query;
}

function add_money_sites_in_query(main_url) {
    main_url = prepare_url(main_url);

    var money_sites_query = '';
    var money_sites = [];

    var money_sites_query = "money_sites=";

    $('#filter-money-sites-list input[type="checkbox"]:checked').each((i, item) => {
        money_sites.push($(item).val());
    });

    if (money_sites.length > 0) {
        money_sites_query = "money_sites=" + money_sites.join(',');
    }

    return main_url + money_sites_query;
}

function add_date_in_query(main_url) {
    main_url = prepare_url(main_url);
    var query = '';
    var start_date = $('#datepicker').data('range-from');
    var end_date = $('#datepicker').data('range-to');
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
        if (1 === data.page_number) {
            firstLink.classList.add('active');
        }
        firstLink.innerHTML = `<a href="#" data-page="1">1</a>`;
        pagination.appendChild(firstLink);

        if (startPage > 2) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.innerHTML = `<span>...</span>`;
            pagination.appendChild(ellipsisLink);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageLink = document.createElement("li");
        if (i == data.page_number) {
            pageLink.classList.add('active');
        }
        pageLink.innerHTML = `<a href="#" data-page="${i}">${i}</a>`;
        pagination.appendChild(pageLink);
    }

    if (endPage < data.total_pages) {
        if (endPage < data.total_pages - 1) {
            const ellipsisLink = document.createElement("li");
            ellipsisLink.innerHTML = `<span>...</span>`;
            pagination.appendChild(ellipsisLink);
        }

        const lastLink = document.createElement("li");
        lastLink.innerHTML = `<a href="#" data-page="${data.total_pages}">${data.total_pages}</a>`;
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


// Separate object for dropdown functionality
class Dropdown {
    constructor(containerID, optionsURL) {
        this.containerID = containerID;
        this.optionsURL = optionsURL;
    }

    fetchOptions() {

        this.optionsURL = add_clients_in_query(this.optionsURL);

        fetch(this.optionsURL)
            .then((response) => response.json())
            .then((data) => {
                const optionsHTML = data.map((client) => `
              <li>
                <span>
                  <label>
                    <input type="checkbox" class="filter-checkbox" value="${client.item}" />
                    <span>${client.item}</span>
                  </label>
                </span>
              </li>
            `).join('');

                $(`#${this.containerID} li:gt(0)`).remove();
                $(`#${this.containerID}`).append(optionsHTML);

                this.initDropdown();

            })
            .catch((error) => console.error('Error fetching options:', error));
    }

    initDropdown() {

        var container_id = '#' + this.containerID;

        $(`.dropdown-trigger[data-target="${this.containerID}"]`).dropdown({
            closeOnClick: false,
            coverTrigger: false,
            constrainWidth: false,
            alignment: 'left',
        });

        $(`${container_id} .search-box`).on('keyup', function () {
            const searchText = $(this).val().toLowerCase();
            const $options = $(`${container_id} li span:not(.search-wrap)`);
            $options.each(function () {
                const $option = $(this);
                const optionText = $option.text().toLowerCase();
                const isVisible = optionText.includes(searchText);
                $option.closest('li').toggle(isVisible);
            });
        });

        $(container_id + ' input[type="checkbox"]').on('change', function () {
            const selectedOptions = $(`${container_id} input[type="checkbox"]:checked`)
                .map(function () {
                    return $(this).val();
                })
                .get();

            $(container_id).parent().find('.selected-options').html(
                '<p>Selected options: ' + selectedOptions.join(', ') + '</p>'
            );

            if (container_id == '#filter-client-list') {
                var dropdown = new Dropdown('filter-money-sites-list', FILTER_GET_MONEY_SITES_LIST_URL);
                dropdown.fetchOptions();
            }

            get_summary_list();
            get_data_for_chart();
            get_data_for_anchors_table();
            get_data_for_table_pbn_and_publications();
            get_date_for_links_to_money_sites_table();
        });
    }

    getSelectedOptions() {
        const selectedOptions = $(`.${this.containerID} input[type="checkbox"]:checked`)
            .map(function () {
                return $(this).val();
            })
            .get();

        return selectedOptions;
    }
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


function get_data_for_chart() {
    var url = add_clients_in_query(MAIN_CHART_URL);
    url = add_money_sites_in_query(url);
    fetch_data(url).then(data => {
        const datasets = {};
        // Group data by label
        data.forEach(item => {
            const label = item.pbn_owner;
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

function get_data_for_table_pbn_and_publications(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
    var url = `${DOMAIN_PBN_AND_PUBLICATIONS_URL}?page=${pageNumber}&per_page=${perPage}&`;
    url = add_clients_in_query(url);
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

function get_date_for_links_to_money_sites_table(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
    var url = `${LINKS_TO_MONEY_SITES_URL}?page=${pageNumber}&per_page=${perPage}&`;
    url = add_clients_in_query(url);
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
    url = add_clients_in_query(url);
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


$(document).ready(function () {
    // Initialize the dropdown
    var dropdown = new Dropdown('filter-client-list', FILTER_GET_CLIENT_LIST_URL);
    dropdown.fetchOptions();
//    console.log(dropdown.getSelectedOptions());

    var dropdown2 = new Dropdown('filter-money-sites-list', FILTER_GET_MONEY_SITES_LIST_URL);
    dropdown2.fetchOptions();
//    console.log(dropdown2.getSelectedOptions());

    duDatepicker('#datepicker', {
        format: 'mmmm d, yyyy',
        outFormat: 'yyyy-mm-dd',
        range: true,
        clearBtn: true,
        cancelBtn: true,
        events: {
            dateChanged: function (data) {
                get_data_for_chart();
                get_summary_list();
                get_data_for_anchors_table();
                get_data_for_table_pbn_and_publications();
                get_date_for_links_to_money_sites_table();
            },
            onRangeFormat: function (from, to) {

                var fromFormat = 'mmmm d, yyyy', toFormat = 'mmmm d, yyyy';

                if (from.getMonth() === to.getMonth() && from.getFullYear() === to.getFullYear()) {
                    fromFormat = 'mmmm d'
                    toFormat = 'd, yyyy'
                } else if (from.getFullYear() === to.getFullYear()) {
                    fromFormat = 'mmmm d'
                    toFormat = 'mmmm d, yyyy'
                }

                return from.getTime() === to.getTime() ?
                    this.formatDate(from, 'mmmm d, yyyy') :
                    [this.formatDate(from, fromFormat), this.formatDate(to, toFormat)].join('-');
            }
        }
    });


    get_data_for_chart();
    get_summary_list();
    get_data_for_anchors_table();
    get_data_for_table_pbn_and_publications();
    get_date_for_links_to_money_sites_table();


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