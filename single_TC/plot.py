import os
import sys
import argparse

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def parse_hurdat2_track(fname):
    lats, lons = [], []
    with open(fname) as f:
        f.readline()  # skip header
        for line in f:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 6:
                continue
            lat_s, lon_s = parts[4], parts[5]
            lat = float(lat_s[:-1]) * (1 if lat_s[-1] == 'N' else -1)
            lon = float(lon_s[:-1]) * (1 if lon_s[-1] == 'E' else -1)
            lats.append(lat)
            lons.append(lon)
    return lats, lons

def main():
    p = argparse.ArgumentParser(description="Plot HURDAT2 track")
    p.add_argument("track_file", help="path to .txt track file")
    args = p.parse_args()

    fname = args.track_file
    base, _ = os.path.splitext(os.path.basename(fname))
    lats, lons = parse_hurdat2_track(fname)
    if not lats:
        print(f"No track points found in {fname}", file=sys.stderr)
        sys.exit(1)

    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    # ocean light blue, land gray
    ax.add_feature(cfeature.OCEAN.with_scale('50m'), facecolor='lightblue')
    ax.add_feature(cfeature.LAND.with_scale('50m'),  facecolor='gray')
    ax.coastlines('50m')

    # decimal-degree gridlines
    gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LongitudeFormatter(
        number_format='.1f', degree_symbol='°', dateline_direction_label=False
    )
    gl.yformatter = LatitudeFormatter(number_format='.1f', degree_symbol='°')

    # extent with 2° margin
    m = 2
    ax.set_extent(
        [min(lons)-m, max(lons)+m, min(lats)-m, max(lats)+m],
        crs=proj
    )

    # track in black, no legend
    ax.plot(
        lons, lats,
        marker='o', linestyle='-', color='black',
        transform=proj
    )

    ax.set_title(base)

    # save files
    for ext in ('png', 'pdf'):
        plt.savefig(f"{base}.{ext}", dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    main()