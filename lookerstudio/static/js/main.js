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
    var url = add_client_id_in_query(SUMMARY_URL);
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

function add_money_sites_in_query(main_url) {
    main_url = prepare_url(main_url);
    var money_sites_query = "money_sites=";
    if (false) {
        money_sites_query += money_sites.join(',');
    }
    return main_url + money_sites_query;
}

function get_client_id() {
    var client_id = parseInt($("#clients").val());
    return isNaN(client_id) ? null : client_id > 0 ? client_id : null;
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
        this.initDropdown();
        fetch(this.optionsURL)
            .then((response) => response.json())
            .then((data) => {
                const optionsHTML = data.map((client) => `
              <li>
                <span>
                  <label>
                    <input type="checkbox" value="${client.item}" />
                    <span>${client.item}</span>
                  </label>
                </span>
              </li>
            `).join('');

                $(`#${this.containerID}`).append(optionsHTML);

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

        $(`#${this.containerID} input[type="checkbox"]`).on('change', function () {
            const selectedOptions = $(`${container_id} input[type="checkbox"]:checked`)
                .map(function () {
                    return $(this).val();
                })
                .get();

            $(`.selected-options`).html(
                '<p>Selected options: ' + selectedOptions.join(', ') + '</p>'
            );
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
    var url = add_client_id_in_query(MAIN_CHART_URL);
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


$(document).ready(function () {
    // Initialize the dropdown
    var dropdown = new Dropdown('filter-client-list', FILTER_GET_CLIENT_LIST_URL);
    dropdown.fetchOptions();
    console.log(dropdown.getSelectedOptions());

    var dropdown2 = new Dropdown('filter-money-sites-list', FILTER_GET_MONEY_SITES_LIST_URL);
    dropdown2.fetchOptions();
    console.log(dropdown2.getSelectedOptions());
    get_data_for_chart();
});