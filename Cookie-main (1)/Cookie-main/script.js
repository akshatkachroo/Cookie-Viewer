const form = document.querySelector('form');
const websiteInput = document.querySelector('#website');
const resultDiv = document.querySelector('#result');
const cookieTable = document.querySelector('#cookieTable tbody');

form.addEventListener('submit', async (event) => {
	event.preventDefault();
	
	const website = websiteInput.value;
	const response = await fetch(`http://127.0.0.1:5500/cookies?website=${website}`);
	
	if (response.ok) {
		const data = await response.json();
		console.log(data);
		if (data.cookies.length > 0) {
			// Clear any existing rows from the table
			cookieTable.innerHTML = '';

			// Add rows for each cookie
			data.cookies.forEach((cookie) => {
				const row = cookieTable.insertRow();
				const nameCell = row.insertCell();
				const valueCell = row.insertCell();
				const domainCell = row.insertCell();
				const pathCell = row.insertCell();
				const expiresCell = row.insertCell();
				const secureCell = row.insertCell();
				const httpOnlyCell = row.insertCell();
				nameCell.textContent = cookie.name;
				valueCell.textContent = cookie.value;
				domainCell.textContent = cookie.domain;
				pathCell.textContent = cookie.path;
				expiresCell.textContent = cookie.expires ? new Date(cookie.expires * 1000).toString() : '';
				secureCell.textContent = cookie.secure ? 'Yes' : 'No';
				httpOnlyCell.textContent = cookie.httponly ? 'Yes' : 'No'; // Note: the property name is "httponly" in the Python code, not "httpOnly"
			});

			// Add scan date, time and location to the table
			const scanRow = cookieTable.insertRow();
			const scanNameCell = scanRow.insertCell();
			const scanValueCell = scanRow.insertCell();
			const scanDomainCell = scanRow.insertCell();
			const scanPathCell = scanRow.insertCell();
			const scanExpiresCell = scanRow.insertCell();
			const scanSecureCell = scanRow.insertCell();
			const scanHttpOnlyCell = scanRow.insertCell();
			const date = new Date();
			scanNameCell.textContent = 'Scan Information';
			scanValueCell.textContent = '';
			scanDomainCell.textContent = '';
			scanPathCell.textContent = '';
			scanExpiresCell.textContent = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
			scanSecureCell.textContent = '';
			navigator.geolocation.getCurrentPosition(function(position) {
				scanHttpOnlyCell.textContent = position.coords.latitude + ', ' + position.coords.longitude;
			});

			// Display the GDPR compliance message
		 } else {
			resultDiv.textContent = 'No cookies found for this website';
		 }
	} else {
		resultDiv.textContent = 'Error retrieving cookies';
	}
});







