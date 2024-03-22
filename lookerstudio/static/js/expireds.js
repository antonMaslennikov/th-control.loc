function get_data() {
    fetch_data('/looker-studio/expireds_page_data').then(data => {
        const tbody = document.querySelector("table#data_table tbody");
        tbody.innerHTML = "";

        data.forEach((item) => {
            const row = document.createElement("tr");

            for (const [key, value] of Object.entries(item)) {
                const td = document.createElement("td");
                td.textContent = value;


                row.appendChild(td);
            }

            tbody.appendChild(row);
        });
    });
}

$(document).ready(function () {

    get_data();

});