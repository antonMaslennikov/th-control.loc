function get_data() {
    fetch_data('/looker-studio/summary_page_data').then(data => {
        const tbody = document.querySelector("table#summary_table tbody");
        tbody.innerHTML = "";

        data.forEach((item) => {
            const row = document.createElement("tr");

            for (const [key, value] of Object.entries(item)) {
                const td = document.createElement("td");
                td.textContent = value;

//                console.log(item, value, key);

                if (key == 'rest_domains') {
                    if (value <= item.pbn_sites && value > 0) {
                        td.classList.add('red-td')
                    } else if (value <= 0) {
                        td.classList.add('green-td')
                    }
                }

                if (key == 'rest_links') {
                    if (value <= item.links && value > 0) {
                        td.classList.add('red-td')
                    } else if (value <= 0) {
                        td.classList.add('green-td')
                    }
                }

                row.appendChild(td);
            }

            tbody.appendChild(row);
        });
    });
}

$(document).ready(function () {

    get_data();

});