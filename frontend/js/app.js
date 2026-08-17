let records = [];

const pages = {
    dashboard: document.getElementById("dashboardPage"),
    profiles: document.getElementById("profilesPage"),
    profile: document.getElementById("profilePage"),
    audit: document.getElementById("auditPage"),
    methodology: document.getElementById("methodologyPage")
};

const pageTitle = document.getElementById("pageTitle");
const profileGrid = document.getElementById("profileGrid");
const profileDetails = document.getElementById("profileDetails");
const search = document.getElementById("search");

async function loadData() {

    const response = await fetch("data.json");

    if (!response.ok) {
        throw new Error("Unable to load data.json");
    }

    const data = await response.json();

    records = data.records || [];

    document.getElementById("totalRecords").textContent =
        data.total_records ?? records.length;

    document.getElementById("validNumbers").textContent =
        data.valid_numbers ?? 0;

    document.getElementById("duplicates").textContent =
        data.duplicates ?? 0;

    document.getElementById("auditStatus").textContent =
        data.audit_status ?? "UNKNOWN";

    document.getElementById("auditLarge").textContent =
        data.audit_status ?? "UNKNOWN";

    renderProfiles(records);
}

function renderProfiles(list) {

    profileGrid.innerHTML = "";

    if (!list.length) {
        profileGrid.innerHTML = `
            <div class="profile-card">
                No profiles found.
            </div>
        `;
        return;
    }

    list.forEach(record => {

        const card = document.createElement("article");

        card.className = "profile-card";

        card.innerHTML = `
            <div class="avatar">${escapeHtml(record.id)}</div>

            <h3>Test Profile ${escapeHtml(record.id)}</h3>

            <p>Phone: ${escapeHtml(record.phone)}</p>
            <p>Country: ${escapeHtml(record.country)}</p>
            <p>Source: ${escapeHtml(record.source)}</p>

            <span class="tag">SYNTHETIC / DEMO</span>
        `;

        card.addEventListener("click", () => {
            openProfile(record.id);
        });

        profileGrid.appendChild(card);
    });
}

function openProfile(id) {

    const record = records.find(
        item => String(item.id) === String(id)
    );

    if (!record) return;

    profileDetails.innerHTML = `
        <div class="panel">

            <div class="detail-header">

                <div class="detail-avatar">
                    ${escapeHtml(record.id)}
                </div>

                <div>
                    <h2>Test Profile ${escapeHtml(record.id)}</h2>
                    <p>Synthetic educational record</p>
                </div>

            </div>

            <div class="detail-grid">

                ${detail("Record ID", record.id)}
                ${detail("Phone Number", record.phone)}
                ${detail("Country", record.country)}
                ${detail("Source Type", record.source)}
                ${detail("Confidence", record.confidence)}
                ${detail("Privacy Status", "SYNTHETIC / DEMO")}
                ${detail("Identity", "NOT IDENTIFIED")}
                ${detail("Real Lookup", "DISABLED")}

            </div>

            <div class="social-links">

                ${mockLink(
                    "Mock Facebook",
                    record.facebook
                )}

                ${mockLink(
                    "Mock Instagram",
                    record.instagram
                )}

            </div>

        </div>
    `;

    showPage("profile");
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
        <a href="${escapeHtml(url)}"
           target="_blank"
           rel="noopener noreferrer">
            ${escapeHtml(label)}
        </a>
    `;
}

function showPage(name) {

    Object.values(pages).forEach(page => {
        page.classList.add("hidden");
    });

    pages[name].classList.remove("hidden");

    const titles = {
        dashboard: "Dashboard",
        profiles: "Profiles",
        profile: "Profile Details",
        audit: "Safety Audit",
        methodology: "Methodology"
    };

    pageTitle.textContent = titles[name];

    document.querySelectorAll(".nav-btn").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.page === name
        );
    });

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

document.querySelectorAll(".nav-btn").forEach(button => {

    button.addEventListener("click", () => {

        const page = button.dataset.page;

        showPage(page);

    });

});

document.getElementById("backButton").addEventListener(
    "click",
    () => showPage("profiles")
);

search.addEventListener("input", () => {

    const query = search.value.toLowerCase().trim();

    const filtered = records.filter(record =>
        String(record.id).toLowerCase().includes(query) ||
        String(record.phone).toLowerCase().includes(query) ||
        String(record.country).toLowerCase().includes(query)
    );

    renderProfiles(filtered);
});

function escapeHtml(value) {

    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

loadData().catch(error => {

    console.error(error);

    profileGrid.innerHTML = `
        <div class="profile-card">
            Failed to load dataset.
        </div>
    `;
});
