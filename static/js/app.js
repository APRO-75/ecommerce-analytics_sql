// E-commerce Analytics Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Set default dates
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('kpiDate').value = today;
    document.getElementById('rfmDate').value = today;

    // Bind event listeners
    bindEventListeners();
});

function bindEventListeners() {
    // KPI loading
    document.getElementById('loadKPI').addEventListener('click', loadKPI);
    
    // Analytics loading
    document.getElementById('loadRevenue').addEventListener('click', loadRevenue);
    document.getElementById('loadRepeat').addEventListener('click', loadRepeatRate);
    document.getElementById('loadCohort').addEventListener('click', loadCohortRetention);
    document.getElementById('loadRFM').addEventListener('click', loadRFM);
    document.getElementById('loadProducts').addEventListener('click', loadTopProducts);
    document.getElementById('loadInventory').addEventListener('click', loadLowStock);
    document.getElementById('loadFunnel').addEventListener('click', loadOrderFunnel);
    
    // CSV download
    document.getElementById('downloadRFM').addEventListener('click', downloadRFMAsCSV);
}

// Utility functions
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="text-center py-4">
            <div class="loading-spinner me-2"></div>
            Loading data...
        </div>
    `;
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        </div>
    `;
}

function showNoData(elementId, message = "No data available for the selected criteria.") {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="no-data">
            <i class="fas fa-chart-line"></i>
            <p>${message}</p>
        </div>
    `;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

// KPI Dashboard
async function loadKPI() {
    const date = document.getElementById('kpiDate').value;
    if (!date) {
        showError('kpiResults', 'Please select a date.');
        return;
    }

    showLoading('kpiResults');

    try {
        const response = await fetch(`/analytics/kpi?date=${date}`);
        const data = await response.json();

        if (response.ok) {
            renderKPI(data);
        } else {
            showError('kpiResults', data.error || 'Failed to load KPI data.');
        }
    } catch (error) {
        showError('kpiResults', 'Network error occurred.');
    }
}

function renderKPI(data) {
    const kpiHtml = `
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${formatNumber(data.orders)}</div>
                <div class="kpi-label">Orders</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${formatCurrency(data.revenue)}</div>
                <div class="kpi-label">Revenue</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${formatCurrency(data.aov)}</div>
                <div class="kpi-label">AOV</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${formatNumber(data.unique_customers)}</div>
                <div class="kpi-label">Customers</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${formatNumber(data.new_customers)}</div>
                <div class="kpi-label">New Customers</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${data.repeat_rate}%</div>
                <div class="kpi-label">Repeat Rate</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${data.top_category}</div>
                <div class="kpi-label">Top Category</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="kpi-card">
                <div class="kpi-value">${data.top_product}</div>
                <div class="kpi-label">Top Product</div>
            </div>
        </div>
    `;

    document.getElementById('kpiResults').innerHTML = kpiHtml;
}

// Revenue Analysis
async function loadRevenue() {
    const start = document.getElementById('revenueStart').value;
    const end = document.getElementById('revenueEnd').value;

    if (!start || !end) {
        showError('revenueResults', 'Please select start and end dates.');
        return;
    }

    showLoading('revenueResults');

    try {
        const response = await fetch(`/analytics/revenue-by-month-category?start=${start}&end=${end}`);
        const data = await response.json();

        if (response.ok) {
            renderRevenueTable(data);
        } else {
            showError('revenueResults', data.error || 'Failed to load revenue data.');
        }
    } catch (error) {
        showError('revenueResults', 'Network error occurred.');
    }
}

function renderRevenueTable(data) {
    if (!data || data.length === 0) {
        showNoData('revenueResults');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Category</th>
                        <th>Revenue</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.forEach(row => {
        const monthFormatted = new Date(row.month).toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
        tableHtml += `
            <tr>
                <td>${monthFormatted}</td>
                <td>${row.category_name}</td>
                <td>${formatCurrency(row.revenue)}</td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('revenueResults').innerHTML = tableHtml;
}

// Repeat Rate Analysis
async function loadRepeatRate() {
    const start = document.getElementById('repeatStart').value;
    const end = document.getElementById('repeatEnd').value;

    if (!start || !end) {
        showError('repeatResults', 'Please select start and end dates.');
        return;
    }

    showLoading('repeatResults');

    try {
        const response = await fetch(`/analytics/repeat-rate?start=${start}&end=${end}`);
        const data = await response.json();

        if (response.ok) {
            renderRepeatRateTable(data);
        } else {
            showError('repeatResults', data.error || 'Failed to load repeat rate data.');
        }
    } catch (error) {
        showError('repeatResults', 'Network error occurred.');
    }
}

function renderRepeatRateTable(data) {
    if (!data || data.length === 0) {
        showNoData('repeatResults');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Total Customers</th>
                        <th>Repeat Customers</th>
                        <th>Repeat Rate</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.forEach(row => {
        const monthFormatted = new Date(row.month).toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
        tableHtml += `
            <tr>
                <td>${monthFormatted}</td>
                <td>${formatNumber(row.total_customers)}</td>
                <td>${formatNumber(row.repeat_customers)}</td>
                <td>${row.repeat_rate}%</td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('repeatResults').innerHTML = tableHtml;
}

// Cohort Retention Analysis
async function loadCohortRetention() {
    const start = document.getElementById('cohortStart').value;
    const end = document.getElementById('cohortEnd').value;
    const horizon = document.getElementById('cohortHorizon').value;

    if (!start || !end) {
        showError('cohortResults', 'Please select start and end dates.');
        return;
    }

    showLoading('cohortResults');

    try {
        const response = await fetch(`/analytics/cohort-retention?start=${start}&end=${end}&horizon=${horizon}`);
        const data = await response.json();

        if (response.ok) {
            renderCohortTable(data);
        } else {
            showError('cohortResults', data.error || 'Failed to load cohort data.');
        }
    } catch (error) {
        showError('cohortResults', 'Network error occurred.');
    }
}

function renderCohortTable(data) {
    if (!data || data.length === 0) {
        showNoData('cohortResults');
        return;
    }

    // Transform data into pivot table format
    const cohorts = [...new Set(data.map(row => row.cohort_month))].sort();
    const maxMonths = Math.max(...data.map(row => row.months_since));

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-sm cohort-heatmap">
                <thead>
                    <tr>
                        <th>Cohort</th>
                        <th>Size</th>
    `;

    for (let i = 0; i <= maxMonths; i++) {
        tableHtml += `<th>M${i}</th>`;
    }

    tableHtml += `
                    </tr>
                </thead>
                <tbody>
    `;

    cohorts.forEach(cohort => {
        const cohortData = data.filter(row => row.cohort_month === cohort);
        const cohortSize = cohortData[0]?.cohort_size || 0;
        const cohortFormatted = new Date(cohort).toLocaleDateString('en-US', { year: 'numeric', month: 'short' });

        tableHtml += `
            <tr>
                <td><strong>${cohortFormatted}</strong></td>
                <td>${formatNumber(cohortSize)}</td>
        `;

        for (let i = 0; i <= maxMonths; i++) {
            const monthData = cohortData.find(row => row.months_since === i);
            if (monthData) {
                const rate = parseFloat(monthData.retention_rate);
                let cssClass = '';
                if (rate >= 50) cssClass = 'retention-high';
                else if (rate >= 20) cssClass = 'retention-medium';
                else cssClass = 'retention-low';

                tableHtml += `<td class="${cssClass}">${rate}%</td>`;
            } else {
                tableHtml += `<td>-</td>`;
            }
        }

        tableHtml += `</tr>`;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('cohortResults').innerHTML = tableHtml;
}

// RFM Analysis
let rfmData = [];

async function loadRFM() {
    const asOfDate = document.getElementById('rfmDate').value;

    if (!asOfDate) {
        showError('rfmResults', 'Please select an "as of" date.');
        return;
    }

    showLoading('rfmResults');

    try {
        const response = await fetch(`/analytics/rfm?as_of=${asOfDate}`);
        const data = await response.json();

        if (response.ok) {
            rfmData = data;
            renderRFMTable(data);
            document.getElementById('downloadRFM').disabled = false;
        } else {
            showError('rfmResults', data.error || 'Failed to load RFM data.');
        }
    } catch (error) {
        showError('rfmResults', 'Network error occurred.');
    }
}

function renderRFMTable(data) {
    if (!data || data.length === 0) {
        showNoData('rfmResults');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Customer ID</th>
                        <th>Recency (days)</th>
                        <th>Frequency</th>
                        <th>Monetary</th>
                        <th>R</th>
                        <th>F</th>
                        <th>M</th>
                        <th>RFM Total</th>
                        <th>Segment</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.slice(0, 100).forEach(row => { // Limit to first 100 for performance
        const segmentClass = getSegmentClass(row.segment);
        tableHtml += `
            <tr>
                <td>${row.customer_id}</td>
                <td>${row.recency_days}</td>
                <td>${row.frequency}</td>
                <td>${formatCurrency(row.monetary)}</td>
                <td>${row.r_score}</td>
                <td>${row.f_score}</td>
                <td>${row.m_score}</td>
                <td><strong>${row.rfm_total}</strong></td>
                <td><span class="${segmentClass}">${row.segment}</span></td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    if (data.length > 100) {
        tableHtml += `<p class="text-muted">Showing first 100 customers. Use download CSV for full data.</p>`;
    }

    document.getElementById('rfmResults').innerHTML = tableHtml;
}

function getSegmentClass(segment) {
    const segmentMap = {
        'Champions': 'segment-champions',
        'Loyal Customers': 'segment-loyal',
        'At Risk': 'segment-at-risk',
        'Cannot Lose Them': 'segment-at-risk',
        'Lost': 'segment-lost'
    };
    return segmentMap[segment] || 'segment-loyal';
}

function downloadRFMAsCSV() {
    if (!rfmData || rfmData.length === 0) {
        alert('No RFM data to download. Please run the analysis first.');
        return;
    }

    const csv = convertToCSV(rfmData);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rfm_analysis_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    if (!data || data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => 
            headers.map(header => {
                const value = row[header];
                return typeof value === 'string' ? `"${value}"` : value;
            }).join(',')
        )
    ].join('\n');

    return csvContent;
}

// Top Products Analysis
async function loadTopProducts() {
    const metric = document.getElementById('productsMetric').value;
    const n = document.getElementById('productsN').value;
    const start = document.getElementById('productsStart').value;
    const end = document.getElementById('productsEnd').value;

    if (!start || !end) {
        showError('productsResults', 'Please select start and end dates.');
        return;
    }

    showLoading('productsResults');

    try {
        const response = await fetch(`/analytics/top-products?metric=${metric}&n=${n}&start=${start}&end=${end}`);
        const data = await response.json();

        if (response.ok) {
            renderTopProductsTable(data);
        } else {
            showError('productsResults', data.error || 'Failed to load products data.');
        }
    } catch (error) {
        showError('productsResults', 'Network error occurred.');
    }
}

function renderTopProductsTable(data) {
    if (!data || data.length === 0) {
        showNoData('productsResults');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Category</th>
                        <th>Units Sold</th>
                        <th>Revenue</th>
                        <th>Margin</th>
                        <th>Margin %</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.forEach(row => {
        tableHtml += `
            <tr>
                <td>${row.product_id}</td>
                <td>${row.product_name}</td>
                <td>${row.category_name}</td>
                <td>${formatNumber(row.units_sold)}</td>
                <td>${formatCurrency(row.revenue)}</td>
                <td>${formatCurrency(row.margin)}</td>
                <td>${row.margin_percent}%</td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('productsResults').innerHTML = tableHtml;
}

// Low Stock Analysis
async function loadLowStock() {
    const n = document.getElementById('inventoryN').value;

    showLoading('inventoryResults');

    try {
        const response = await fetch(`/analytics/low-stock?n=${n}`);
        const data = await response.json();

        if (response.ok) {
            renderLowStockTable(data);
        } else {
            showError('inventoryResults', data.error || 'Failed to load inventory data.');
        }
    } catch (error) {
        showError('inventoryResults', 'Network error occurred.');
    }
}

function renderLowStockTable(data) {
    if (!data || data.length === 0) {
        showNoData('inventoryResults', 'No low stock items found. All products are well stocked!');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Category</th>
                        <th>On Hand</th>
                        <th>Reorder Point</th>
                        <th>Recommended Order</th>
                        <th>Urgency</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.forEach(row => {
        const urgencyClass = getUrgencyClass(row.urgency);
        tableHtml += `
            <tr>
                <td>${row.product_id}</td>
                <td>${row.product_name}</td>
                <td>${row.category_name}</td>
                <td>${formatNumber(row.on_hand_qty)}</td>
                <td>${formatNumber(row.reorder_point)}</td>
                <td>${formatNumber(row.recommended_order_qty)}</td>
                <td><span class="${urgencyClass}">${row.urgency}</span></td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('inventoryResults').innerHTML = tableHtml;
}

function getUrgencyClass(urgency) {
    const urgencyMap = {
        'Critical': 'urgency-critical',
        'Low': 'urgency-low',
        'Out of Stock': 'urgency-out'
    };
    return urgencyMap[urgency] || 'urgency-low';
}

// Order Funnel Analysis
async function loadOrderFunnel() {
    const start = document.getElementById('funnelStart').value;
    const end = document.getElementById('funnelEnd').value;

    if (!start || !end) {
        showError('funnelResults', 'Please select start and end dates.');
        return;
    }

    showLoading('funnelResults');

    try {
        const response = await fetch(`/analytics/order-funnel?start=${start}&end=${end}`);
        const data = await response.json();

        if (response.ok) {
            renderOrderFunnelTable(data);
        } else {
            showError('funnelResults', data.error || 'Failed to load funnel data.');
        }
    } catch (error) {
        showError('funnelResults', 'Network error occurred.');
    }
}

function renderOrderFunnelTable(data) {
    if (!data || data.length === 0) {
        showNoData('funnelResults');
        return;
    }

    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Orders</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.forEach(row => {
        tableHtml += `
            <tr>
                <td><strong>${row.status}</strong></td>
                <td>${formatNumber(row.orders)}</td>
                <td>${row.percentage}%</td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById('funnelResults').innerHTML = tableHtml;
}
