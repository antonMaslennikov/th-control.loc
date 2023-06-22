// Fetch the data using AJAX
fetch('/sites/looker/api/get-publications-chart')
  .then(response => response.json())
  .then(data => {
    // Process the data and create the chart

    // Example data (replace with your actual data)
    const publicationsData = data;

    // Process the data to create labels and datasets for the chart
    const labels = publicationsData.labels;
    const datasets = publicationsData.datasets.map(dataset => ({
      label: dataset.client_name,
      data: dataset.publication_count,
      borderColor: getRandomColor(),
      fill: false
    }));

    // Create the chart
    const ctx = document.getElementById('publicationChart').getContext('2d');
    new Chart(ctx, {
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

// Helper function to generate random colors for chart lines
function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
