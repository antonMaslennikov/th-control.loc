const FILTER_GET_CLIENT_LIST_URL = '/looker-studio/get-client-list';
const FILTER_GET_MONEY_SITES_LIST_URL = '/looker-studio/get-money-sites-list';
const MAIN_CHART_URL = '/looker-studio/chart-data';
const REDIRECT_CHART_URL = '/looker-studio/chart-redirects-data';
const FILTERS_CLIENTS_URL = '/sites/looker/api/filter/client-list';
const FILTERS_MONEY_SITES_URL = '/sites/looker/api/filter/money-sites-list';
const DOMAIN_PBN_AND_PUBLICATIONS_URL = '/looker-studio/domain-and-publications';
const LINKS_TO_MONEY_SITES_URL = '/looker-studio/link-to-money-sites';
const LINKS_ANCHOR_COUNTER_URL = '/looker-studio/anchor-links';
const SUMMARY_URL = '/looker-studio/get-summary';
const PUBLICATIONS_URL = '/looker-studio/publications';
const DEFAULT_PAGE_NUM = 1;
const DEFAULT_PER_PAGE_COUNT = 10;

function get_summary_list() {
    var url = add_clients_in_query(SUMMARY_URL);
    url = add_money_sites_in_query(url);
    url = add_date_in_query(url);
    fetch_data(url).then(data => {

        $("#deadline .valueLabel").text(data.deadline_data[0].deadline ?? 'Нет данных');
        $("#days_left .valueLabel").text(data.deadline_data[0].diff ?? 'Нет данных');

        if (data.pbn_domains.max_site_url != null) {
            $("#count_domains .card-subtitle strong").text(data.pbn_domains.max_site_url + ' (' + data.pbn_domains.progress_bar + '%)');

            $("#count_domains .progress-bar").removeClass('hide');
            $("#count_domains .progress-bar").css('width', Math.min(data.pbn_domains.progress_bar, 100) + '%');
            $("#count_domains .svg-text").text(data.pbn_domains.sum_pbn_sites);
//            $("#count_domains .progress-bar .svg-percent").attr('width', Math.min(data.pbn_domains.progress_bar, 100) + '%');
//            $("#count_domains .progress-bar .svg-text").text(data.pbn_domains.sum_pbn_sites);
        } else {
            $("#count_domains .progress-bar").addClass('hide');
            $("#count_domains .card-subtitle strong").text('Нет данных');
        }

        $("#count_new_domains>strong").text(data.new_domains.new_domains);

        $("#count_publications>strong").text(data.publications.count);
        $("#count_new_publications>strong").text(data.new_publications.count);

        $("#count_money_links>strong").text(data.new_domains.money_links ?? 0);

        if (data.money_sites.summ_url_to_acceptor != null) {
            $("#count_money_links .card-subtitle strong").text(data.money_sites.summ_url_to_acceptor + ' (' + data.money_sites.progress + '%)');
            $("#count_money_links .progress-bar").css('width', Math.min(data.money_sites.progress, 100) + '%');
            $("#count_money_links .svg-text").text(data.money_sites.summ_links);
//            $("#count_money_links .progress-bar .svg-percent").attr('width', Math.min(data.money_sites.progress, 100) + '%');
//            $("#count_money_links .progress-bar .svg-text").text(data.money_sites.summ_links);
        } else {
            $("#count_money_links .progress-bar").addClass('hide');
            $("#count_money_links .card-subtitle strong").text('Нет данных');
        }
    });
}

function add_clients_in_query(main_url) {
    main_url = prepare_url(main_url);

    var clients_query = '';
    var clients = $('#filter-client-list').val();

    if (clients.length > 0) {
        clients_query = "clients=" + clients.join(',');
    }

    return main_url + clients_query;
}

function add_money_sites_in_query(main_url) {
    main_url = prepare_url(main_url);

    var money_sites_query = '';
    var money_sites = $('#filter-money-sites-list').val();

    var money_sites_query = "money_sites=";

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

function add_date_deadline_in_query(main_url) {
    main_url = prepare_url(main_url);
    var query = '';
    var start_date = $('#datepicker_deadline').data('range-from');
    var end_date = $('#datepicker_deadline').data('range-to');
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

function add_days_left_in_query(main_url) {
    main_url = prepare_url(main_url);
    var query = '';
    var days_left = $('#days_left').val();
    if (days_left) {
        query += 'days_left=' + days_left;
    }
    return main_url + query;
}


// Separate object for dropdown functionality
class Dropdown {
    constructor(containerID, optionsURL) {
        this.containerID = containerID;
        this.optionsURL = optionsURL;
    }

    fetchOptions() {

        let self = this;

        this.optionsURL = add_clients_in_query(this.optionsURL);

        fetch(this.optionsURL)
            .then((response) => response.json())
            .then((data) => {
                $(`#${this.containerID} option`).remove();

                data.forEach(function(client) {
                    let option = document.createElement('option');
                    option.setAttribute('value', client.item);
                    option.innerHTML = client.item;
                    $(`#${self.containerID}`).append(option);
                });

                this.initDropdown();

            })
            .catch((error) => console.error('Error fetching options:', error));
    }

    initDropdown() {

        var container_id = '#' + this.containerID;

        $(container_id).select2({
          theme: 'bootstrap4'
        }).on(
            'change', function(e) {
                var data = $(container_id).val();

                get_summary_list();
                get_data_for_chart();
                get_data_for_redirects_chart();
                get_data_for_anchors_table();
                get_data_for_table_pbn_and_publications();
                get_data_for_table_publications();
                get_date_for_links_to_money_sites_table();
            }
        );


//        $(`.dropdown-trigger[data-target="${this.containerID}"]`).dropdown({
//            closeOnClick: false,
//            coverTrigger: false,
//            constrainWidth: false,
//            alignment: 'left',
//        });

//        $(`${container_id} .search-box`).on('keyup', function () {
//            const searchText = $(this).val().toLowerCase();
//            const $options = $(`${container_id} li span:not(.search-wrap)`);
//            $options.each(function () {
//                const $option = $(this);
//                const optionText = $option.text().toLowerCase();
//                const isVisible = optionText.includes(searchText);
//                $option.closest('li').toggle(isVisible);
//            });
//        });

//        $(container_id + ' input[type="checkbox"]').on('change', function () {
//            const selectedOptions = $(`${container_id} input[type="checkbox"]:checked`)
//                .map(function () {
//                    return $(this).val();
//                })
//                .get();
//
//            $(container_id).parent().find('.selected-options').html(
//                '<p>Selected options: ' + selectedOptions.join(', ') + '</p>'
//            );
//
//            if (container_id == '#filter-client-list') {
//                var dropdown = new Dropdown('filter-money-sites-list', FILTER_GET_MONEY_SITES_LIST_URL);
//                dropdown.fetchOptions();
//            }
//
//            get_summary_list();
//            get_data_for_chart();
//            get_data_for_anchors_table();
//            get_data_for_table_pbn_and_publications();
//            get_data_for_table_publications();
//            get_date_for_links_to_money_sites_table();
//        });
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


function get_data_for_chart() {
    var url = add_clients_in_query(MAIN_CHART_URL);
    url = add_money_sites_in_query(url);
    fetch_data(url).then(data => {
        const datasets_tmp = {};

        // Group data by label
        data.forEach(item => {
            const label = item.pbn_owner;
            if (!datasets_tmp[label]) {
                datasets_tmp[label] = {
                    label: label, data: [], borderColor: get_random_color(), backgroundColor: 'rgba(0, 0, 0, 0)',
                };
            }
            item['x'] = get_rus_date_format(item['x']);
            datasets_tmp[label].data.push({
                x: item.x, y: item.y
            });
        });

        const datasets = {};

        for (var key in datasets_tmp) {
            if (datasets_tmp[key].data.length > 1) {
                datasets[key] = datasets_tmp[key];
            }
        }

        const chartData = {
            labels: Array.from(new Set(data.map(item => item.x))),
            datasets: Object.values(datasets),
        };

        const ctx = document.getElementById('publicationChart').getContext('2d');
        const existingChart = Chart.getChart(ctx);

        if (existingChart) {
            existingChart.destroy();
        }

        var chart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'Publications by Client'
                },
                scales: {
                    x: {
                        title: {
                            display: true
//                            ,
//                            text: 'Publication Date'
                        }
                    }, y: {
                        title: {
                            display: true
//                            ,
//                            text: 'Publication Count'
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

function get_data_for_redirects_chart() {

    var url = add_clients_in_query(REDIRECT_CHART_URL);
        url = add_money_sites_in_query(url);

    fetch_data(url).then(data => {

        const ctx1 = document.getElementById('redirectsChart').getContext('2d');
        const existingChart1 = Chart.getChart(ctx1);

        if (existingChart1) {
            existingChart1.destroy();
        }
        let labels = [],
            values = []

        data.forEach((item) => {
            if (item[0] == '0') {
                labels.push('ОК');
                values.push(item[1]);
            } else if (item[0] == 1) {
                labels.push('Редирект');
                values.push(item[1]);
            } else {
                labels.push('Ответ не получен');
                values.push(item[1]);
            }
        });

        var chart = new Chart(ctx1,
        {
          type: 'doughnut',
          data: {
          labels: labels,
          datasets: [
            {
              label: 'redirects',
              data: values,
            }
          ]
        },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Редирект'
              }
            }
          },
        })
        ;
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
            item['site_create'] = get_rus_date_format(item['site_create']);
            item['count_article'] = item['last_update'] ? item['count_article'] : 0;
            item['last_update'] = item['last_update'] ? get_rus_date_format(item['last_update']) : 'Нет данных';
            item['date_diff'] = item['date_diff'] ? item['date_diff'] : 'Нет данных';
            Object.values(item).forEach((value) => {
                const td = document.createElement("td");
                td.textContent = value;
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
    });
}

function get_data_for_table_publications(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
    var url = `${PUBLICATIONS_URL}?page=${pageNumber}&per_page=${perPage}&`;
    url = add_clients_in_query(url);
    url = add_date_in_query(url);
    fetch_data(url).then(data => {
        const tbody = document.querySelector("table#table_publications tbody");
        tbody.innerHTML = "";
        createPagination('pagination_publications', data);
        data['links'].forEach((item) => {
            const row = document.createElement("tr");
            Object.values(item).forEach((value) => {
                const td = document.createElement("td");
                if (/^(ftp|http|https):\/\/[^ "]+$/.test(value)) {
                    td.appendChild(createA(value));
                } else {
                    td.textContent = value;
                }
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

                    if (/^(ftp|http|https):\/\/[^ "]+$/.test(value)) {
                        td.appendChild(createA(value));
                    } else {
                        td.textContent = value;
                    }

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

    if (localStorage.getItem('anchors--show-more')) {
        url += '&query_type=2';
    }

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

            document.querySelector("table#table_anchor_counter_footer .total").textContent = counter;
        }
    });
}

function createA(url) {
    let a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('target', '_blank');
    a.innerHTML = url;

    return a;
}


$(document).ready(function () {
    // Initialize the dropdown
    var dropdown = new Dropdown('filter-client-list', FILTER_GET_CLIENT_LIST_URL);
    dropdown.fetchOptions();
//    console.log(dropdown.getSelectedOptions());

    var dropdown2 = new Dropdown('filter-money-sites-list', FILTER_GET_MONEY_SITES_LIST_URL);
    dropdown2.fetchOptions();
//    console.log(dropdown2.getSelectedOptions());

    /*
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
    */

    $('#datepicker').daterangepicker({
        autoApply: true
    })
    .on('apply.daterangepicker', function(ev, picker) {

        this.setAttribute('data-range-from', picker.startDate.format('YYYY-MM-DD'));
        this.setAttribute('data-range-to', picker.endDate.format('YYYY-MM-DD'));

        get_data_for_chart();
        get_data_for_redirects_chart();
        get_summary_list();
        get_data_for_anchors_table();
        get_data_for_table_pbn_and_publications();
        get_date_for_links_to_money_sites_table();
    });

    if (document.querySelector(".anchors--show-more")) {
        if (localStorage.getItem('anchors--show-more')) {
            document.querySelector(".anchors--show-more").innerHTML = '-';
            document.getElementById('table_anchor_counter_header').querySelector('th.table_anchor-domain_name').classList.remove('hidden');
        } else {
            document.querySelector(".anchors--show-more").innerHTML = '+';
            document.getElementById('table_anchor_counter_header').querySelector('th.table_anchor-domain_name').classList.add('hidden');
        }
    }


    get_data_for_chart();
    get_data_for_redirects_chart();
    get_summary_list();
    get_data_for_anchors_table();
    get_data_for_table_pbn_and_publications();
    get_data_for_table_publications();
    get_date_for_links_to_money_sites_table();


    // Пагинации
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

    document.querySelector("#pagination_publications").addEventListener("click", function (event) {
        event.preventDefault();
        if (event.target.tagName === "A") {
            const pageNumber = parseInt(event.target.dataset.page);
            get_data_for_table_publications(pageNumber);
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
    // \ Пагинации


    document.querySelector(".anchors--show-more").addEventListener("click", function (event) {
        if (localStorage.getItem('anchors--show-more')) {
            localStorage.removeItem('anchors--show-more');
            event.currentTarget.innerHTML = '+';
            document.getElementById('table_anchor_counter_header').querySelector('th.table_anchor-domain_name').classList.add('hidden');
        } else {
            localStorage.setItem('anchors--show-more', true);
            event.currentTarget.innerHTML = '-';
            document.getElementById('table_anchor_counter_header').querySelector('th.table_anchor-domain_name').classList.remove('hidden');
        }
        get_data_for_anchors_table();
    });
});