import subprocess
import json
import os
from datetime import datetime, timezone

def run_command(cmd, description):
    print(f"[*] {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] Error during {description}:")
        print(result.stderr)
        return False
    print(f"[+] Success: {description}")
    if result.stdout.strip():
        print(result.stdout.strip())
    return True

def main():
    print("=== CASTLEBERRY BLOOM MASTER AUTOMATION PIPELINE ==\n")
    
    # Step 1: Run tensor synthesis and master runner telemetry
    if not run_command("python3 castleberry_master_runner.py", "Executing tensor sync and UDP broadcast"):
        return

    # Step 2: Generate a unique timestamped JSON audit report
    print("[*] Compiling latest audit report...")
    utc_now = datetime.now(timezone.utc)
    timestamp_str = utc_now.strftime("%Y%m%d_%H%M%S")
    report_filename = f"castleberry_ledger_report_{timestamp_str}.json"
    
    report_data = {
        "timestamp": utc_now.isoformat(),
        "status": "NOMINAL",
        "frequency": 528.0,
        "phi_constant": 1.618033988749895,
        "tensor_dimensions": 2048,
        "ecosystem": "Castleberry Bloom Swarm"
    }
    
    with open(report_filename, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"[+] Created audit report: {report_filename}")

    # Step 3: Trigger OpenTimestamps (ots) anchoring on the unique report
    if run_command(f"ots stamp {report_filename}", "Anchoring audit report with OpenTimestamps"):
        print(f"\n[+] Pipeline completed successfully! {report_filename}.ots anchored in decentralized time.")
    else:
        print("\n[!] Pipeline completed with warnings during OTS stamping.")

if __name__ == "__main__":
    main()
