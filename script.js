const form = document.querySelector('form');
const websiteInput = document.querySelector('#website');
const resultDiv = document.querySelector('#result');
const cookieTable = document.querySelector('#cookieTable tbody');

form.addEventListener('submit', async (event) => {
	event.preventDefault();
	
	const website = websiteInput.value;
	const response = await fetch(`http://127.0.0.1:5000/cookies?website=${website}`);
	
	if (response.ok) {
		const data = await response.json();
		console.log(data);
		const scanInfoTable = document.querySelector('#scanInfoTable tbody');
		scanInfoTable.innerHTML = '';
		if (data.scan_info_list.length > 0) {
			const scanInfo = data.scan_info_list[0];
			const row = scanInfoTable.insertRow();
			const dateCell = row.insertCell();
			const timeCell = row.insertCell();
			const locationCell = row.insertCell();
			const pagesCell = row.insertCell();
			const encryptedCell = row.insertCell();
			dateCell.textContent = scanInfo.date;
			timeCell.textContent = scanInfo.time;
			locationCell.textContent = scanInfo.location;
			pagesCell.textContent = scanInfo.pages;
			encryptedCell.textContent = scanInfo.is_encrypted ? 'Yes' : 'No';
  }
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
			const firstRow = document.querySelector('#cookieTable tbody tr:first-child');
            firstRow.addEventListener('click', () => {
                const otherRows = document.querySelectorAll('#cookieTable tbody tr:not(:first-child)');
                otherRows.forEach(row => {
                    row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
				});
            });
		}else {
			resultDiv.textContent = 'No cookies found for this website';
		 }
	} else {
		resultDiv.textContent = 'Error';
	}
});







