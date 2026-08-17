let records = [];

const totalRecords = document.getElementById("totalRecords");
const validNumbers = document.getElementById("validNumbers");
const duplicates = document.getElementById("duplicates");
const auditStatus = document.getElementById("auditStatus");

const search = document.getElementById("search");
const profileGrid = document.getElementById("profileGrid");

const listView = document.getElementById("listView");
const profileView = document.getElementById("profileView");
const profileDetails = document.getElementById("profileDetails");
const backButton = document.getElementById("backButton");


async function loadData() {

    try {

        const response = await fetch("data.json");

        if (!response.ok) {
            throw new Error("data.json could not be loaded");
        }

        const data = await response.json();

        records = data.records || [];

        totalRecords.textContent = data.total_records ?? records.length;
        validNumbers.textContent = data.valid_numbers ?? 0;
        duplicates.textContent = data.duplicates ?? 0;
        auditStatus.textContent = data.audit_status ?? "UNKNOWN";

        renderProfiles(records);

    } catch (error) {

        console.error(error);

        profileGrid.innerHTML = `
            <div class="profile-card">
                Unable to load profile data.
            </div>
        `;
    }
}


function renderProfiles(data) {

    profileGrid.innerHTML = "";

    if (data.length === 0) {

        profileGrid.innerHTML = `
            <div class="profile-card">
                No matching profiles found.
            </div>
        `;

        return;
    }

    for (const record of data) {

        const card = document.createElement("article");

        card.className = "profile-card";

        card.innerHTML = `
            <div class="avatar">
                ${escapeHtml(record.id)}
            </div>

            <h3>Test Profile ${escapeHtml(record.id)}</h3>

            <p><strong>Phone:</strong> ${escapeHtml(record.phone)}</p>

            <p><strong>Country:</strong> ${escapeHtml(record.country)}</p>

            <p><strong>Source:</strong> ${escapeHtml(record.source)}</p>

            <span class="profile-tag">
                SYNTHETIC / DEMO
            </span>
        `;

        card.addEventListener("click", () => {
            showProfile(record.id);
        });

        profileGrid.appendChild(card);
    }
}


function showProfile(id) {

    const profile = records.find(
        record => String(record.id) === String(id)
    );

    if (!profile) {
        return;
    }

    profileDetails.innerHTML = `
        <div class="detail-header">

            <div class="detail-avatar">
                ${escapeHtml(profile.id)}
            </div>

            <div>
                <h2>Test Profile ${escapeHtml(profile.id)}</h2>
                <p>Synthetic educational record</p>
            </div>

        </div>

        <div class="detail-grid">

            ${detail("Record ID", profile.id)}
            ${detail("Phone Number", profile.phone)}
            ${detail("Country", profile.country)}
            ${detail("Source Type", profile.source)}
            ${detail("Confidence", profile.confidence)}
            ${detail("Privacy Status", "SYNTHETIC / DEMO ONLY")}
            ${detail("Identity Status", "NOT IDENTIFIED")}
            ${detail("Real-person Lookup", "DISABLED")}

        </div>

        <div class="social-links">

            ${mockLink(
                "Mock Facebook Profile",
                profile.facebook
            )}

            ${mockLink(
                "Mock Instagram Profile",
                profile.instagram
            )}

        </div>
    `;

    listView.classList.add("hidden");
    profileView.classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function detail(label, value) {

    return `
        <div class="detail-item">
            <label>${escapeHtml(label)}</label>
            <strong>${escapeHtml(value)}</strong>
        </div>
    `;
}


function mockLink(label, url) {

    if (
        typeof url !== "string" ||
        !url.startsWith("https://example.com/")
    ) {
        return "";
    }

    return `
        <a
            href="${escapeAttribute(url)}"
            target="_blank"
            rel="noopener noreferrer"
        >
            ${escapeHtml(label)}
        </a>
    `;
}


function escapeHtml(value) {

    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function escapeAttribute(value) {
    return escapeHtml(value);
}


search.addEventListener("input", () => {

    const query = search.value.toLowerCase().trim();

    const filtered = records.filter(record =>

        String(record.id).toLowerCase().includes(query) ||
        String(record.phone).toLowerCase().includes(query) ||
        String(record.country).toLowerCase().includes(query) ||
        String(record.source).toLowerCase().includes(query)
    );

    renderProfiles(filtered);
});


backButton.addEventListener("click", () => {

    profileView.classList.add("hidden");
    listView.classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});


loadData();
