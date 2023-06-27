const MAIN_CHART_URL = '/sites/looker/api/get-publications-chart';
const CLIENTS_URL = '/sites/looker/api/clients';
const MONEY_SITES_URL = '/sites/looker/api/money-sites';
const DOMAIN_PBN_AND_PUBLICATIONS_URL = '/sites/looker/api/domain-pbn-and-publications';
const LINKS_TO_MONEY_SITES_URL = '/sites/looker/api/links-to-money-sites';
const LINKS_ANCHOR_COUNTER_URL = '/sites/looker/api/anchor-counter';

$(document).ready(function() {

	$('select').select2({
		theme: 'bootstrap',
		placeholder: 'Select an option',
		width: '100%'
	});

	function fillTableLinksToMoneySites(pageNumber = 1, perPage = 20) {
		fetchData(`${LINKS_TO_MONEY_SITES_URL}?page=${pageNumber}&per_page=${perPage}`).then(data => {
			const tbody = document.querySelector("table#table_links_to_money_sites tbody");
			tbody.innerHTML = "";
			createPagination('pagination_links_to_money_sites', data);
			data['links'].forEach((item) => {
				const row = document.createElement("tr");
				Object.values(item).forEach((value) => {
					const td = document.createElement("td");
					td.textContent = value;
					row.appendChild(td);
				});
				tbody.appendChild(row);
			});


		});
	}

	function fillTableAnchorCounter(pageNumber = 1, perPage = 20) {
		fetchData(`${LINKS_ANCHOR_COUNTER_URL}?page=${pageNumber}&per_page=${perPage}`).then(data => {
			const tbody = document.querySelector("table#table_anchor_counter tbody");
			tbody.innerHTML = "";
			createPagination('pagination_anchor_counter', data);
			data['links'].forEach((item) => {
				const row = document.createElement("tr");
				Object.values(item).forEach((value) => {
					const td = document.createElement("td");
					td.textContent = value;
					row.appendChild(td);
				});
				tbody.appendChild(row);
			});


		});
	}

	function fillTablePbnAndPublications(pageNumber = 1, perPage = 5) {
		fetchData(`${DOMAIN_PBN_AND_PUBLICATIONS_URL}?page=${pageNumber}&per_page=${perPage}`).then(data => {
			const tbody = document.querySelector("table#table_domain_and_pbn tbody");
			tbody.innerHTML = "";
			createPagination('pagination_domain_and_pbn', data);
			data['links'].forEach((item) => {
				const row = document.createElement("tr");
				const options = {
					year: 'numeric',
					month: 'long',
					day: 'numeric',
					timeZone: 'Europe/Moscow', // Set the desired time zone
					hour12: false, // Use 24-hour format
				};
				item['date_create'] = new Date(item['date_create']).toLocaleString('ru-RU', options);
				item['last_post'] = new Date(item['last_post']).toLocaleString('ru-RU', options);
				Object.values(item).forEach((value) => {
					const td = document.createElement("td");
					td.textContent = value;
					row.appendChild(td);
				});
				tbody.appendChild(row);
			});
		});
	}






	function fetchClients() {
		fetchData(CLIENTS_URL).then(data => {
				var options = '';

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

	function fetchMoneySites() {
		fetchData(MONEY_SITES_URL).then(data => {
				var options = '';
				for (var item of data) {
					var current_client = getCurrentClientId();
					var option = '<option value=":val" :params>:name</option>';
					if (current_client != null) {
						if (item.client.id == current_client) {
							options += option.replace(':val', item.id).replace(':name', item.site_url).replace(':params', 'selected="selected"');
						}
					} else {
						options += option.replace(':val', item.id).replace(':name', item.site_url);
					}

				}
				var money_sites = document.querySelector("select#money_sites");
				money_sites.innerHTML = options;
			})
			.catch(error => {
				console.error('Error fetching data:', error);
			});
	}

	function fetchChart() {
		fetchData(MAIN_CHART_URL).then(data => {
				const publicationsData = prepareData(data);
				var datasets = [];
				var labels = [];
				var dateList = [];
				for (var key in publicationsData) {
					var el = publicationsData[key];
					if (getCurrentClientId() == null) {
						dateList.push(...el.labels);
						datasets.push({
							label: el.label,
							data: el.data,
							borderColor: getRandomColor(),
							fill: false
						});
						labels = el.labels;
					} else {
						if (getCurrentClientId() == el.client_id) {
							dateList.push(...el.labels);
							datasets.push({
								label: el.label,
								data: el.data,
								borderColor: getRandomColor(),
								fill: false
							});
							labels = el.labels;
						}
					}
				}
				dateList = dateList.sort();
				var minDate = new Date(dateList[0]);
				var minDateString = minDate.toISOString().split('T')[0];
				var maxDate = new Date(dateList[dateList.length - 1]);
				var maxDateString = maxDate.toISOString().split('T')[0];

				$('#start-date').attr('min', minDateString);
				$('#start-date').attr('max', maxDateString);
				$('#end-date').attr('min', minDateString);
				$('#end-date').attr('max', maxDateString);
				// Create the chart
				const ctx = document.getElementById('publicationChart').getContext('2d');
				const existingChart = Chart.getChart(ctx);
				if (existingChart) {
					existingChart.destroy();
				}
				var chart = new Chart(ctx, {
					type: 'line',
					data: {
						labels: labels,
						datasets: datasets
					},
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




	//////// fetch client list

	fetchClients();
	fetchMoneySites();
	fetchChart();
	fillTablePbnAndPublications();
	fillTableLinksToMoneySites();
	fillTableAnchorCounter();
	// Get the select element by its ID
	var select_clients = $("select#clients");
	select_clients.change(function() {

		if (has_value_changed('current_client', $(this).val())) {
			fetchMoneySites();
			fetchChart();
		}
	});

	var select_money_sites = $("select#money_sites");
	select_money_sites.change(function() {

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
		if (output[el.client_name] == undefined) {
			output[el.client_name] = {
				data: [el.publication_count],
				labels: [el.publication_date]
			};
			output[el.client_name]['label'] = el.client_name;
			output[el.client_name]['client_id'] = el.client_id;
		} else {
			output[el.client_name]['data'].push(el.publication_count);
			output[el.client_name]['labels'].push(el.publication_date);
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
	if (!localStorage.hasOwnProperty("current_client")) {
		return null;
	} else {
		var current_client = parseInt(localStorage.getItem("current_client"));
		return isNaN(current_client) ? null : current_client;
	}
	return null;
}

// Function to create pagination links
function createPagination(el, data) {
	const pagination = document.querySelector(`#${el} ul`);
	pagination.innerHTML = ""; // Clear existing links
	console.log('create_pagination');

	let startPage = Math.max(1, data.page_number - 2);
	if (isNaN(startPage)) {
		startPage = 1;
	}
	let endPage = Math.min(startPage + 4, data.total_pages);



	console.log(endPage);
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