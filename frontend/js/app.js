let records = [];

const totalRecords = document.getElementById("totalRecords");
const validNumbers = document.getElementById("validNumbers");
const duplicates = document.getElementById("duplicates");
const auditStatus = document.getElementById("auditStatus");
const recordsBody = document.getElementById("records");
const search = document.getElementById("search");


async function loadData() {
    try {
        const response = await fetch("data.json");

        if (!response.ok) {
            throw new Error("Unable to load data.json");
        }

        const data = await response.json();

        records = data.records || [];

        totalRecords.textContent = data.total_records ?? records.length;
        validNumbers.textContent = data.valid_numbers ?? 0;
        duplicates.textContent = data.duplicates ?? 0;
        auditStatus.textContent = data.audit_status ?? "UNKNOWN";

        render(records);

    } catch (error) {
        console.error(error);

        auditStatus.textContent = "ERROR";
        recordsBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Unable to load frontend data.
                </td>
            </tr>
        `;
    }
}


function render(data) {

    recordsBody.innerHTML = "";

    for (const record of data) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${escapeHtml(record.id)}</td>
            <td>${escapeHtml(record.phone)}</td>
            <td>${escapeHtml(record.country)}</td>
            <td>${escapeHtml(record.source)}</td>
            <td>
                <a href="${safeMockUrl(record.facebook)}"
                   target="_blank"
                   rel="noopener noreferrer">
                    Mock Profile
                </a>
            </td>
            <td>
                <a href="${safeMockUrl(record.instagram)}"
                   target="_blank"
                   rel="noopener noreferrer">
                    Mock Profile
                </a>
            </td>
        `;

        recordsBody.appendChild(row);
    }
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function safeMockUrl(url) {

    if (
        typeof url === "string" &&
        url.startsWith("https://example.com/")
    ) {
        return url;
    }

    return "#";
}


search.addEventListener("input", () => {

    const query = search.value.toLowerCase().trim();

    const filtered = records.filter(record =>
        record.phone.toLowerCase().includes(query) ||
        record.country.toLowerCase().includes(query) ||
        record.source.toLowerCase().includes(query) ||
        record.id.toLowerCase().includes(query)
    );

    render(filtered);
});


loadData();
