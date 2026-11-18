import json
import os
import sys

REPORT_PATH = "castleberry_ledger_report.json"
TARGET_FREQ = 528.0
EXPECTED_TENSOR_SUM = 0.2937
FREQ_TOLERANCE = 0.1
ALERT_TRIGGERED = False

def analyze_drift_with_alerts():
    global ALERT_TRIGGERED
    if not os.path.exists(REPORT_PATH):
        print(f"[-] Report {REPORT_PATH} not found. Run export_ledger_json.py first.")
        return

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_records = 0
    anomalies = 0
    critical_alerts = 0

    print("========================================")
    print("[*] CML MESH LEDGER DRIFT & ANOMALY AUDIT")
    print("========================================")

    for table, rows in data.items():
        print(f"\n--- Scanning Table: {table} ({len(rows)} records) ---")
        
        for i, row in enumerate(rows):
            total_records += 1
            timestamp = row.get("timestamp", row.get("time", "N/A"))
            freq = row.get("frequency", row.get("freq", TARGET_FREQ))
            tensor_sum = row.get("tensor_sum", row.get("checksum", EXPECTED_TENSOR_SUM))
            status = str(row.get("status", row.get("audit_result", "OK")))

            # Calculate frequency drift
            try:
                freq_val = float(freq)
                freq_drift = abs(freq_val - TARGET_FREQ)
            except (ValueError, TypeError):
                freq_val = 0.0
                freq_drift = 999.0

            # Calculate tensor sum deviation
            try:
                tensor_val = float(tensor_sum)
                tensor_deviation = abs(tensor_val - EXPECTED_TENSOR_SUM)
            except (ValueError, TypeError):
                tensor_deviation = 0.0

            # Evaluate anomaly flags
            status_lower = status.lower()
            is_offline = "offline" in status_lower or "timeout" in status_lower
            is_freq_drift = freq_drift > FREQ_TOLERANCE
            is_tensor_drift = tensor_deviation > 0.001

            if is_offline or is_freq_drift or is_tensor_drift:
                anomalies += 1
                if is_offline or is_tensor_drift:
                    critical_alerts += 1
                    ALERT_TRIGGERED = True
                    print(f"[!] CRITICAL ALERT [Row {i}] Time: {timestamp}")
                    print(f"    -> Reason: {'Ollama Node Offline/Timeout' if is_offline else 'Tensor Checksum Deviation'}")
                    print(f"    -> Details: Freq={freq}Hz, Tensor Sum={tensor_sum}, Status={status}")
                else:
                    print(f"[!] WARNING [Row {i}] Time: {timestamp} | Freq Drift: {freq_drift:.4f}Hz | Status: {status}")
            else:
                print(f"[+] COHERENT [Row {i}] Time: {timestamp} | Freq: {freq}Hz | Checksum: {tensor_sum}")

    print(f"\n========================================")
    print(f"[*] Total Records Audited: {total_records}")
    print(f"[*] Total Anomalies Flagged: {anomalies}")
    print(f"[*] Critical Threshold Alerts: {critical_alerts}")
    print(f"========================================")

    if ALERT_TRIGGERED:
        print("[!] ALERT STATUS: Mesh stability warning issued. Review local Ollama daemon or packet integrity.")
        sys.exit(1)
    else:
        print("[+] MESH STATUS: 100% Coherent. All telemetry within nominal parameters.")
        sys.exit(0)

if __name__ == "__main__":
    analyze_drift_with_alerts()
