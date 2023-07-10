const MAIN_CHART_URL = '/sites/looker/api/chart-data';
const  FILTERS_URL = '/sites/looker/api/filters';
const DOMAIN_PBN_AND_PUBLICATIONS_URL = '/sites/looker/api/table/domain-pbn-and-publications';
const LINKS_TO_MONEY_SITES_URL = '/sites/looker/api/table/links-to-money-sites';
const LINKS_ANCHOR_COUNTER_URL = '/sites/looker/api/table/anchors';
const SUMMARY_URL='/sites/looker/api/summary';


const DEFAULT_PAGE_NUM=1;
const DEFAULT_PER_PAGE_COUNT=10;


$(document).ready(function() {

    function getRusDate(dt){
      return new Date(dt).toLocaleString('ru-RU', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        timeZone: 'Europe/Moscow', // Set the desired time zone
                        hour12: false, // Use 24-hour format
                    });
    }

	$('select').select2({
		theme: 'bootstrap',
		placeholder: 'Select an option',
		width: '100%',
	}).on('select2:open', function () {
  $('.select2-dropdown').addClass('custom-dropdown');
});


	function fillSummary() {
		var url=`${SUMMARY_URL}?`;
		url+=add_client_id_in_query();
	    url+=add_money_sites_in_query();
		fetchData(url).then(data => {
		$("#count_new_domains>strong").text(data.count_new_domains.count);
		$("#count_publications>strong").text(data.count_publications.count);
		$("#count_new_publications>strong").text(data.count_new_publications.count);
		});
	}

	function fillTableLinksToMoneySites(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
		var url=`${LINKS_TO_MONEY_SITES_URL}?page=${pageNumber}&per_page=${perPage}&`;
		url+=add_client_id_in_query();
	    url+=add_money_sites_in_query();
		fetchData(url).then(data => {

			const tbody = document.querySelector("table#table_links_to_money_sites tbody");
			tbody.innerHTML = "";
			createPagination('pagination_links_to_money_sites', data);
			if(data['links']!=undefined){
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

	function fillTableAnchorCounter(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
		var url=`${LINKS_ANCHOR_COUNTER_URL}?page=${pageNumber}&per_page=${perPage}&`;
		url+=add_client_id_in_query();
	    url+=add_money_sites_in_query();
	    fetchData(url).then(data => {
			const tbody = document.querySelector("table#table_anchor_counter tbody");
			tbody.innerHTML = "";
			createPagination('pagination_anchor_counter', data);
			if(data['links']!=undefined){
			    var counter=0;
                data['links'].forEach((item) => {
                    const row = document.createElement("tr");
                    Object.values(item).forEach((value) => {
                        const td = document.createElement("td");
                        td.textContent = value;
                        row.appendChild(td);

                        if(typeof value === 'number' && !isNaN(value)){
                        counter+=value;
                        }
                    });
                    tbody.appendChild(row);
                });
                var row = document.createElement("tr");
                var td = document.createElement("th");
                td.textContent = "Общий итог";
                td.colSpan="2";
                row.appendChild(td);
                var td = document.createElement("th");
                td.textContent = counter;
                row.appendChild(td);
                tbody.appendChild(row);
			}
		});
	}

	function fillTablePbnAndPublications(pageNumber = DEFAULT_PAGE_NUM, perPage = DEFAULT_PER_PAGE_COUNT) {
	    var url=`${DOMAIN_PBN_AND_PUBLICATIONS_URL}?page=${pageNumber}&per_page=${perPage}&`;
	    url+=add_client_id_in_query();
	    url+=add_money_sites_in_query();
		fetchData(url).then(data => {
			const tbody = document.querySelector("table#table_domain_and_pbn tbody");
			tbody.innerHTML = "";
			createPagination('pagination_domain_and_pbn', data);
			data['links'].forEach((item) => {
			        const row = document.createElement("tr");
                    item['last_post'] = getRusDate(item['last_post']);
                    item['date_create'] = getRusDate(item['date_create']);
                    Object.values(item).forEach((value) => {
                        const td = document.createElement("td");
                        td.textContent = value;
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
		});
	}
	function fetchFilters() {
	var url =FILTERS_URL;
	if(getCurrentClientId()){
		 url+="?client_id="+getCurrentClientId();
	}
		fetchData(url).then(data => {
		    if(data!=undefined && data['money_sites']){
		    	var options = '';
				for (var item of data['money_sites']) {
					var current_client = getCurrentClientId();
					var option = '<option value=":val" :params>:name</option>';
					if (current_client != null) {
						if (item.client.id == current_client) {
							options += option.replace(':val', item.id).replace(':name', item.name).replace(':params', 'selected="selected"');
						}
					} else {
						options += option.replace(':val', item.id).replace(':name', item.name);
					}

				}
				var money_sites = document.querySelector("select#money_sites");
				money_sites.innerHTML = options;
		    }
		    if(data!=undefined && data['client_list'])

				var options = '<option value="all">All</option>';
				for (var item of data['client_list']) {
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

	function fetchChart() {
        var url=`${MAIN_CHART_URL}?up&`;
        url+=add_client_id_in_query();
	 	fetchData(url).then(data => {
		   const datasets = {};
          // Group data by label
          data.forEach(item => {
            const label = item.label;
            if (!datasets[label]) {
              datasets[label] = {
                label: label,
                data: [],
                borderColor: getRandomColor(),
                backgroundColor: 'rgba(0, 0, 0, 0)',
              };
            }
            item['x'] = getRusDate(item['x']);
            console.log(item);
            datasets[label].data.push({
              x: item.x,
              y: item.y
            });
          });
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
									display: true,
									text: 'Publication Date'
								}
							},
							y: {
								title: {
									display: true,
									text: 'Publication Count'
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
	fetchFilters();
	fetchChart();
	fillTablePbnAndPublications();
	fillTableLinksToMoneySites();
	fillTableAnchorCounter();
	fillSummary();
	// Get the select element by its ID
	var select_clients = $("select#clients");
	select_clients.change(function() {
        	fetchFilters();
        	fillSummary();
				fetchChart(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
            	fillTablePbnAndPublications(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	            fillTableLinksToMoneySites(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	            fillTableAnchorCounter(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	});
	var select_money_sites = $("select#money_sites");
	select_money_sites.change(function() {
			fetchMoneySites(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
				fetchChart(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
            	fillTablePbnAndPublications(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	            fillTableLinksToMoneySites(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	            fillTableAnchorCounter(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);


	});
	var start_date =$('#start-date');
	var end_date =$('#end-date');
	 start_date.change(function() {
		fetchChart(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	 });
	 end_date.change(function() {
				fetchChart(DEFAULT_PAGE_NUM,DEFAULT_PER_PAGE_COUNT);
	   });



	document.querySelector("#pagination_links_to_money_sites").addEventListener("click", function(event) {
		event.preventDefault();
		if (event.target.tagName === "A") {
			const pageNumber = parseInt(event.target.dataset.page);
			fillTableLinksToMoneySites(pageNumber);
		}
	});

	document.querySelector("#pagination_domain_and_pbn").addEventListener("click", function(event) {
		event.preventDefault();
		if (event.target.tagName === "A") {
			const pageNumber = parseInt(event.target.dataset.page);
			fillTablePbnAndPublications(pageNumber);
		}
	});

	document.querySelector("#pagination_anchor_counter").addEventListener("click", function(event) {
		event.preventDefault();
	    document.querySelector('#pagination_anchor_counter a').style.color="";
		if (event.target.tagName === "A") {
			const pageNumber = parseInt(event.target.dataset.page);
			fillTableAnchorCounter(pageNumber);
		}
	});





});





////////////////////////////

function fetchData(url) {
	const cachedData = localStorage.getItem(url);
	if (false) {
		// Data found in cache, return it
		return Promise.resolve(JSON.parse(cachedData));
	}
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

// Prepare data for chart
function prepareData(data) {
	var output = {};
	for (var el of data) {
		if (output[el.label] == undefined) {
			output[el.label] = {
				data: [el.y],
				labels: [el.x]
			};
			output[el.label]['label'] = el.label;
		} else {
			output[el.label]['data'].push(el.y);
			output[el.label]['labels'].push(el.x);
		}

	}
	return output;
}

// Helper function to generate random colors for chart lines
function getRandomColor() {
	const letters = '0123456789ABCDEF';
	let color = '#';
	for (let i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

function has_value_changed(key, newValue) {
	var storedValue = localStorage.getItem(key);
	if (storedValue !== newValue) {
		localStorage.setItem(key, newValue);
		return true;
	}
	return false;
}

function getData(key) {
	if (localStorage.hasOwnProperty("current_client")) {
		return localStorage.getItem(key);
	}
	return null;
}


function saveLargeDataToLocalStorage(keyPrefix, data) {
	const CHUNK_SIZE = 1024 * 1024; // 1 MB per chunk
	const totalChunks = Math.ceil(data.length / CHUNK_SIZE);

	for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
		const startIndex = chunkIndex * CHUNK_SIZE;
		const endIndex = startIndex + CHUNK_SIZE;
		const chunkData = data.slice(startIndex, endIndex);

		const chunkKey = `${keyPrefix}_${chunkIndex}`;
		localStorage.setItem(chunkKey, JSON.stringify(chunkData));
	}

	// Store metadata about the large data
	const metadataKey = `${keyPrefix}_metadata`;
	const metadata = {
		totalChunks: totalChunks,
		originalSize: data.length
	};
	localStorage.setItem(metadataKey, JSON.stringify(metadata));
}

function retrieveLargeDataFromLocalStorage(keyPrefix) {
	const metadataKey = `${keyPrefix}_metadata`;
	const metadata = JSON.parse(localStorage.getItem(metadataKey));

	if (!metadata) {
		// Metadata not found, data not stored
		return null;
	}

	const totalChunks = metadata.totalChunks;
	const originalSize = metadata.originalSize;
	let data = '';

	for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
		const chunkKey = `${keyPrefix}_${chunkIndex}`;
		const chunkData = JSON.parse(localStorage.getItem(chunkKey));

		if (!chunkData) {
			// Missing chunk, data not complete
			return null;
		}

		data += chunkData;
	}

	// Data retrieved successfully
	return data.slice(0, originalSize);
}

function getCurrentClientId() {
   var client_id= parseInt($("#clients").val());
    return isNaN(client_id) ? null : client_id>0 ?client_id : null;
}

// Function to create pagination links
function createPagination(el, data) {
	const pagination = document.querySelector(`#${el} ul`);
	pagination.innerHTML = ""; // Clear existing links
	console.log('create_pagination');
	if(!(data!=undefined && data.total_pages!=undefined&&data.total_pages>1)){
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

function add_money_sites_in_query(){
	   var money_sites_query="money_sites=";
	   var money_sites = $('#money_sites').select2('data').map( (item)=> {return item.id});
	   if(money_sites.length>0){
	        return money_sites_query+=money_sites.join(',')+'&';
	   }
	   return '';
}

function add_client_id_in_query(){
		var client_id=getCurrentClientId();
	    if(client_id&&client_id!='all'){
	       return `client_id=${client_id}&`;
	    }
	    return '';
}

