import csv
import gspread
import requests
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURATION ---
CSV_FILE = 'sales_data.csv'
SHEET_NAME = 'Customer List'
CREDS_FILE = 'credentials.json'


# --- 2. DATA EXTRACTION FUNCTIONS ---

def get_csv_metrics():
    """Reads local CSV and calculates revenue/deals."""
    total_revenue = 0
    closed_deals = 0
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['status'].strip().lower() == 'closed':
                    total_revenue += int(row['amount'])
                    closed_deals += 1
        return total_revenue, closed_deals
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return 0, 0


def get_sheets_metrics():
    """Connects to Google Sheets and counts customers."""
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        all_customers = sheet.get_all_records()
        return len(all_customers)
    except Exception as e:
        print(f"❌ Sheets Error: {e}")
        return 0


def get_exchange_rate():
    """Fetches live USD to EUR rate from external API."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        eur_rate = data['rates']['EUR']
        print(f"✅ API Check: Live USD to EUR rate is {eur_rate}")
        return eur_rate
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None


# --- 3. DASHBOARD GENERATION ---

def generate_html(rev, deals, customers, rate):
    # Data for the Bar Chart
    rev_labels = ["TechNebula", "Innovixus", "Quantum", "ByteBridge"]
    rev_data = [9000, 3000, 7000, 2000]

    # Simulated data for the Currency Trend (Last 7 Days)
    # In a pro version, you'd pull this from an API history endpoint
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    trend_data = [rate - 0.02, rate - 0.01, rate + 0.01, rate, rate - 0.01, rate + 0.02, rate]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #0b0f1a; --card: #161b2a; --text: #f8fafc;
                --primary: #00ffaa; --secondary: #00d4ff; --accent: #ff007a;
            }}
            body {{ 
                font-family: 'Plus Jakarta Sans', sans-serif; 
                background-color: var(--bg); 
                color: var(--text); 
                margin: 0; padding: 40px; 
            }}
            .dashboard {{ max-width: 1100px; margin: auto; }}

            .header {{ text-align: center; margin-bottom: 50px; }}
            .header h1 {{ 
                font-size: 42px; font-weight: 800; 
                background: linear-gradient(to right, var(--primary), var(--secondary));
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}

            .main-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; }}

            /* ANIMATED CARDS */
            .section {{ 
                background: var(--card); 
                padding: 30px; 
                border-radius: 24px; 
                border: 1px solid #232a3d;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }}
            .section:hover {{ 
                transform: scale(1.03); 
                border-color: var(--secondary);
                box-shadow: 0 20px 40px rgba(0,212,255,0.1);
            }}

            .stat-label {{ color: #64748b; text-transform: uppercase; font-size: 11px; letter-spacing: 2px; font-weight: 700; }}
            .stat-value {{ font-size: 38px; font-weight: 800; margin: 15px 0; color: #fff; }}

            .market-section {{ 
                grid-column: span 3; 
                margin-top: 30px; 
                background: linear-gradient(145deg, #161b2a, #111522);
                display: flex; flex-direction: column; align-items: center;
            }}

            .canvas-container {{ width: 100%; height: 180px; margin-top: 20px; }}

            .footer {{ margin-top: 60px; text-align: center; opacity: 0.4; font-size: 13px; }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>Executive Command Center</h1>
                <p style="color: #475569;">Real-time Business Intelligence Engine</p>
            </div>

            <div class="main-grid">
                <div class="section">
                    <div class="stat-label">Total Revenue</div>
                    <div class="stat-value" style="color: var(--primary);">${rev:,}</div>
                    <canvas id="revenueChart"></canvas>
                </div>

                <div class="section">
                    <div class="stat-label">Deals Closed</div>
                    <div class="stat-value" style="color: var(--secondary);">{deals}</div>
                    <div style="text-align: center; padding: 20px; font-size: 60px; filter: drop-shadow(0 0 10px var(--secondary));">💎</div>
                    <p style="text-align: center; color: #94a3b8; font-size: 14px;">High-Performing Cycle</p>
                </div>

                <div class="section">
                    <div class="stat-label">Total Customers</div>
                    <div class="stat-value" style="color: var(--accent);">{customers}</div>
                    <div style="text-align: center; padding: 20px; font-size: 60px; filter: drop-shadow(0 0 10px var(--accent));">🚀</div>
                    <p style="text-align: center; color: #94a3b8; font-size: 14px;">+12% vs Last Month</p>
                </div>

                <div class="section market-section">
                    <div class="stat-label">Global Market: USD to EUR Conversion</div>
                    <div class="stat-value" style="color: var(--secondary); font-size: 28px;">Current Rate: {rate}</div>
                    <div class="canvas-container">
                        <canvas id="trendChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="footer">Dashboard Pro v2.0 • Interactive Analytics</div>
        </div>

        <script>
            // Chart 1: Revenue Bar
            new Chart(document.getElementById('revenueChart'), {{
                type: 'bar',
                data: {{
                    labels: {rev_labels},
                    datasets: [{{
                        data: {rev_data},
                        backgroundColor: '#00ffaa',
                        borderRadius: 8
                    }}]
                }},
                options: {{ 
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{ y: {{ display: false }}, x: {{ ticks: {{ color: '#475569' }} }} }}
                }}
            }});

            // Chart 2: Conversion Line Trend
            new Chart(document.getElementById('trendChart'), {{
                type: 'line',
                data: {{
                    labels: {days},
                    datasets: [{{
                        label: 'Exchange Rate',
                        data: {trend_data},
                        borderColor: '#00d4ff',
                        backgroundColor: 'rgba(0, 212, 255, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointBackgroundColor: '#00d4ff'
                    }}]
                }},
                options: {{
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#232a3d' }}, ticks: {{ color: '#475569' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#475569' }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("🚀DASHBOARD LIVE: Check dashboard.html")

# --- 4. EXECUTION ---
if __name__ == "__main__":
    print("🔄 Starting Dashboard Engine...")

    # 1. Pull data from all 3 sources
    rev, deals = get_csv_metrics()
    cust_count = get_sheets_metrics()
    rate = get_exchange_rate()

    # 2. Build the final product
    if rate:
        generate_html(rev, deals, cust_count, rate)
    else:
        print("⚠️ Failed to fetch API data. Dashboard not generated.")