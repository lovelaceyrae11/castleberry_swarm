import sqlite3
import numpy as np

def analyze_swarm_ledger():
    db_name = "castleberry_swarm.db"
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT cycle, frequency, taurus_coord, timestamp FROM telemetry_log ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("[!] No telemetry records found in the database.")
            return

        cycles = []
        frequencies = []
        taurus_coords = []
        
        for row in rows:
            cycle, freq_str, taurus_str, ts = row
            try:
                f_val = float(freq_str.replace("Hz", "").strip())
                t_val = float(taurus_str.replace("deg", "").strip())
                frequencies.append(f_val)
                taurus_coords.append(t_val)
                cycles.append(str(cycle).strip() if cycle else str(len(cycles)+1))
            except ValueError:
                continue
                
        if not frequencies:
            print("[!] Unable to parse numeric values from telemetry log.")
            return

        freq_arr = np.array(frequencies)
        taurus_arr = np.array(taurus_coords)
        
        mean_freq = np.mean(freq_arr)
        std_freq = np.std(freq_arr)
        min_freq = np.min(freq_arr)
        max_freq = np.max(freq_arr)
        drift_delta = max_freq - min_freq
        mean_taurus = np.mean(taurus_arr)
        
        print("\n" + "=" * 65)
        print("=== CASTLEBERRY SWARM HARMONIC DRIFT REPORT & ASCII CHART ===")
        print("=" * 65)
        print(f"Total Cycles Analyzed : {len(frequencies)}")
        print(f"Frequency Mean       : {mean_freq:.4f} Hz")
        print(f"Frequency Std Dev    : {std_freq:.4f} Hz")
        print(f"Frequency Drift Span : {drift_delta:.4f} Hz  [{min_freq}Hz - {max_freq}Hz]")
        print(f"Taurus Axis Mean     : {mean_taurus:.4f} deg")
        print(f"Baseline Delta (528Hz): {mean_freq - 528.0:+.4f} Hz offset")
        print("-" * 65)
        print("FREQ PROGRESSION CHART (Cycle vs Frequency Hz):")
        
        chart_min = min_freq - 0.02
        chart_max = max_freq + 0.02
        span = chart_max - chart_min if chart_max != chart_min else 1.0
        bar_width = 25
        
        for c, f in zip(cycles, frequencies):
            normalized = (f - chart_min) / span
            filled_len = int(round(normalized * bar_width))
            bar = "█" * filled_len + "░" * (bar_width - filled_len)
            print(f" Cycle {c.zfill(2) if len(c) < 2 else c:>2} | {f:.2f}Hz |{bar}|")
            
        print("=" * 65)
        
    except Exception as e:
        print(f"[!] Error analyzing ledger: {e}")

if __name__ == "__main__":
    analyze_swarm_ledger()
