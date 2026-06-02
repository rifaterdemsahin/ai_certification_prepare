# ☁️ Cost Estimation: Story Saves & Azure Storage Integration

This formula document provides an expected cost analysis for operations on the Story Writer page based on observed logs. It outlines current operations, projects expected Azure service costs, and highlights opportunities to optimize.

---

## 📊 Operations Log Summary (18.5 Minutes)
Between **10:32:36** and **10:51:07** (1,111 seconds / ~18.5 minutes), the following API and storage transactions occurred:

| Operation Type | Count | Payload Info / Rate | Azure Storage Action |
| :--- | :---: | :--- | :--- |
| **Rapid Burst Saves** | 22 | 22 saves in 3 seconds (10:32:36 - 10:32:39) | `POST` / Write (Class A) |
| **Interval / Action Saves** | 23 | Scheduled ~45s interval auto-saves & manual saves | `POST` / Write (Class A) |
| **Image Clipboard Paste** | 1 | 884 KB PNG upload (10:43:05 - 10:43:16) | `POST` / Write (Class A) + Blob Storage |
| **Total Transactions** | **46** | **~2.5 operations per minute** | |

---

## 💰 Azure Cost Formula & Rates

Azure costs are calculated across two main services: **Azure Functions** (the backend API `claude-cert-api`) and **Azure Blob Storage** (`claudecertstore`).

### 1. Azure Functions (Consumption Plan)
* **Execution Rate**: $0.20 per million executions (first 1 million free/month).
* **Resource Duration Rate**: $0.000016 per Gigabyte-second (GB-s).
  * *Assumptions*: Function memory limit = **128 MB (0.125 GB)**. Average execution duration = **1.0 second**.
  * *Formula*: $`\text{Cost} = \text{Executions} \times (0.0000002 + (\text{GB} \times \text{Duration} \times 0.000016))`$
  * *Per Execution Cost*: $0.0000002 + (0.125 \times 1.0 \times 0.000016) = \$0.0000022$ per execution.

### 2. Azure Blob Storage (LRS - Hot Tier)
* **Class A Operations (Write/Create/List)**: $0.05 per 10,000 operations ($0.000005 per write).
* **Data Storage**: $0.018 per GB per month.
* **Data Transfer (Egress)**: $0.087 per GB (outbound to internet).

---

## 🧮 Expected Cost Calculations

### A. Observed Session Cost (18.5 minutes)
* **API Executions (46 requests)**:
  $$46 \times \$0.0000022 = \$0.0001012$$
* **Storage Write Operations (46 Class A)**:
  $$46 \times \$0.000005 = \$0.000230$$
* **Data Storage (0.88 MB Image + JSON payloads)**:
  $$\approx \text{Negligible} \ (< \$0.000001)$$
* **Total Session Cost**: **`$0.0003312`**

### B. Projected Costs (Active Developer Usage)
If a developer is actively writing stories (assuming 8 hours/day, 20 days/month):

| Period | Total Writes (avg. 2.5/min) | Azure Functions Cost | Azure Storage Write Cost | Total Monthly Cost |
| :--- | :---: | :---: | :---: | :---: |
| **Hour** | 150 | $0.00033 | $0.00075 | **$0.00108** |
| **Day (8h)** | 1,200 | $0.00264 | $0.00600 | **$0.00864** |
| **Month (20d)** | 24,000 | $0.05280 | $0.12000 | **$0.17280** |

*Note: Since these amounts fall well within the free tier thresholds (1 million executions/month and 400,000 GB-s/month for Functions), the actual billed cost for a single developer is **$0.00**.*

---

## ⚠️ The Burst Save Risk: System Vulnerabilities
During `10:32:36` to `10:32:39`, **22 writes occurred in 3 seconds**. If a bug or user action triggers an unthrottled loop (e.g. saving on every single keystroke instead of a debounced interval):
* **Keystroke Rate**: ~5 keystrokes per second = **18,000 saves/hour**.
* **Keystroke Hourly Cost**: **$0.1296** / hour (no free tier covers this long-term).
* **Network & DB Thrashing**: Leads to Azure Function concurrency limits and UI freezes.

---

## 🛠️ Optimization Recommendations
To ensure cost efficiency and prevent API abuse:
1. **Keystroke Debouncing**: Implement a 2 to 3-second debounce window on the frontend before triggering an autosave flag.
2. **State-Diff Checking**: Compare current story JSON hash with the last saved state; only push to Azure if actual changes exist.
3. **Adaptive Auto-Save**: If the user is actively typing, defer auto-save until 10 seconds of idle time or force save at a strict 60s hard ceiling.
