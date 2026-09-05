import json
import sys
import os
import glob

def convert_poweramp_to_apo(json_file_path, output_txt_path=None):
    if output_txt_path is None:
        base = os.path.splitext(json_file_path)[0]
        output_txt_path = base + ".txt"

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Poweramp exports presets as an array wrapping a single object
    if isinstance(data, list):
        data = data[0]

    apo_lines = []
    
    bands = data.get("bands", [])
    max_boost = max((b.get("gain", 0.0) for b in bands), default=0.0)
    preamp = -max(0.0, max_boost)
    apo_lines.append(f"Preamp: {preamp:.1f} dB")

    # Numeric type codes from Poweramp wrapped-preset export:
    #   0 = LSC, 1 = HSC, 2 = PK, everything else → PK
    filter_type_map = {
        0: "LSC",
        1: "HSC",
        2: "PK",
        3: "PK",
        4: "PK",
        5: "PK"
    }

    for idx, band in enumerate(bands, 1):
        f_type = filter_type_map.get(band.get("type", 0), "PK")
        freq = band.get("frequency", 1000)
        gain = band.get("gain", 0.0)
        q = band.get("q", 0.0)
        if q <= 0.0:
            q = 1.41

        # < 100 Hz → 1 decimal, >= 100 Hz → integer
        if freq < 100:
            freq_s = f"{freq:.1f}"
        else:
            freq_s = str(int(freq))

        # Gain 1 decimal, Q 3 decimals
        apo_lines.append(f"Filter {idx}: ON {f_type} Fc {freq_s} Hz Gain {gain:.1f} dB Q {q:.3f}")

    with open(output_txt_path, 'w') as f:
        f.write("\n".join(apo_lines))
        
    print(f"Converted: {json_file_path} -> {output_txt_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single file mode
        json_path = sys.argv[1]
        out_path = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            convert_poweramp_to_apo(json_path, out_path)
        except FileNotFoundError:
            print(f"Error: file not found — {json_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON — {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"Error: missing expected field — {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Batch mode: convert all .json files in current folder
        src_dir = os.getcwd()
        out_dir = os.path.join(src_dir, "APO")
        os.makedirs(out_dir, exist_ok=True)

        json_files = sorted(glob.glob(os.path.join(src_dir, "*.json")))
        if not json_files:
            print("No .json files found in current folder.")
            sys.exit(1)

        for json_path in json_files:
            name = os.path.splitext(os.path.basename(json_path))[0]
            out_path = os.path.join(out_dir, name + ".txt")
            try:
                convert_poweramp_to_apo(json_path, out_path)
            except Exception as e:
                print(f"Error: {json_path} — {e}")

        print(f"\nDone. {len(json_files)} file(s) converted to {out_dir}")