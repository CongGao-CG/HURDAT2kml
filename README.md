# HURDAT2 to KML

This repository uses the latest HURDAT2 datasets that include the 2025
hurricane season. NOAA's National Hurricane Center updated both datasets on
February 27, 2026.

- Atlantic, 1851–2025:
  [hurdat2-1851-2025-02272026.txt](https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-02272026.txt)
- Northeast and North Central Pacific, 1949–2025:
  [hurdat2-nepac-1949-2025-02272026.txt](https://www.nhc.noaa.gov/data/hurdat/hurdat2-nepac-1949-2025-02272026.txt)

## Convert the datasets

Split both datasets into one text file per tropical cyclone:

```bash
./split.sh hurdat2-1851-2025-02272026.txt
./split.sh hurdat2-nepac-1949-2025-02272026.txt
```

Convert all split files in `single_TC/` to KML:

```bash
./txt2kml.sh
```
