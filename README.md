# My Poweramp Equalizer presets for headphones and speakers

Poweramp EQ presets for various devices. Use `convert.py` to convert them to
[Equalizer APO](https://sourceforge.net/projects/equalizerapo/) format for Windows.

## How to use the converter

### 1. Export a preset from Poweramp (Android)
- Open Poweramp → Equalizer → tap the preset name
- Tap **Export** → save the `.json` file
- Transfer the file to your PC

### 2. Run the converter

**Convert all presets at once** (recommended):
- Place the `.json` file(s) in the same folder as `convert.py`
- Open a terminal in that folder and run:

```
python convert.py
```

- The script creates an `APO` subfolder with all converted `.txt` files

**Convert a single file:**
```
python convert.py "My Preset.json"
```

**Convert to a custom path:**
```
python convert.py "My Preset.json" "output.txt"
```

### 3. Install in Equalizer APO
- Copy the `.txt` file(s) from the `APO` folder to `C:\Program Files\EqualizerAPO\config\`
- Open **Equalizer APO** and select the preset from the dropdown

### What the converter does
- Maps Poweramp's numeric filter types (0→LSC, 1→HSC, 2–5→PK)
- Sets preamp to prevent clipping (negative of the loudest band)
- Outputs numbered filters in Equalizer APO syntax

Conversion logic based on [Equalizer314](https://github.com/bearinmindcat/Equalizer314)
by [bearinmindcat](https://github.com/bearinmindcat) — the numeric type mapping
(0→LSC, 1→HSC, 2→PK) and APO output format are derived from that project.
