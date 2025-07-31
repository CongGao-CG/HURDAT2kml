import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def main():
    # 1) build global 0.25° grid
    lons = np.arange(-179.875, 180.0, 0.25)
    lats = np.arange(-89.875,  90.0, 0.25)
    Lon, Lat = np.meshgrid(lons, lats)
    pts = np.column_stack((Lon.ravel(), Lat.ravel()))
    
    # 2) your desired location
    desired_lon, desired_lat = -55, 13
    
    # 3) snap to nearest grid point
    d2_snap = (pts[:,0] - desired_lon)**2 + (pts[:,1] - desired_lat)**2
    idx_snap = np.argmin(d2_snap)
    lon0, lat0 = pts[idx_snap]
    
    # 4) compute squared‐degree distance from the chosen grid‐point
    d2 = (pts[:,0] - lon0)**2 + (pts[:,1] - lat0)**2
    
    # 5) select all points within the 101st-smallest distance (including ties)
    k = 101
    sorted_idx = np.argsort(d2)
    cutoff = d2[sorted_idx[k-1]]
    mask_inside = d2 <= cutoff
    inside_pts = pts[mask_inside]
    
    # 6) find the very next cutoff and points just outside
    unique_d2 = np.unique(d2)
    ci = np.where(unique_d2 == cutoff)[0][0]
    if ci < len(unique_d2) - 1:
        next_cutoff = unique_d2[ci + 1]
        mask_outside = (d2 > cutoff) & (d2 <= next_cutoff)
        outside_pts = pts[mask_outside]
    else:
        outside_pts = np.empty((0,2))
    
    # 7) plotting
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1,1,1, projection=proj)
    
    # ocean white, land grey
    ax.add_feature(cfeature.OCEAN.with_scale('50m'), facecolor='white')
    ax.add_feature(cfeature.LAND.with_scale('50m'),  facecolor='lightgrey')
    ax.coastlines('50m')
    
    # zoom ±5° around the chosen point
    margin = 5
    ax.set_extent([lon0-margin, lon0+margin, lat0-margin, lat0+margin],
                  crs=proj)
    
    # plot inside neighbors (black), outside ring (grey), chosen point (red)
    ax.scatter(inside_pts[:,0], inside_pts[:,1],
               s=20, color='black', transform=proj)
    ax.scatter(outside_pts[:,0], outside_pts[:,1],
               s=20, color='grey', transform=proj)
    ax.scatter(lon0, lat0,
               s=60, color='red', transform=proj)
    
    # draw cutoff circle
    radius = np.sqrt(cutoff)
    theta = np.linspace(0, 2*np.pi, 360)
    circle_lon = lon0 + radius * np.cos(theta)
    circle_lat = lat0 + radius * np.sin(theta)
    ax.plot(circle_lon, circle_lat,
            transform=proj, linestyle='--', linewidth=1, color='black')
    
    # axis labels
    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    
    # title with .001 precision
    ax.set_title(f"Chosen grid: ({lon0:.3f}°, {lat0:.3f}°)  •  Inside: {len(inside_pts)}  Outside: {len(outside_pts)}")
    
    # save outputs
    for ext in ('png','pdf'):
        fig.savefig(f"example.{ext}", dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    main()