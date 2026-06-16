import os
import glob
import xarray as xr
import rioxarray

# Settings

INPUT_FOLDER = "data"
OUTPUT_FOLDER = "output"

# Load all NETCDF files

files = glob.glob(os.path.join(INPUT_FOLDER, "*.nc"))

if len(files) == 0:
    raise Exception("No .nc files found in data folder.")

print(f"Found {len(files)} NetCDF files.")

# Combine all files into one dataset
ds = xr.open_mfdataset(files, combine="by_coords")

# Detect time variable

if "valid_time" in ds.coords:
    time_var = "valid_time"
elif "time" in ds.coords:
    time_var = "time"
else:
    raise Exception("Could not find time coordinate.")

# Create month + hour fields

ds = ds.assign_coords(
    month=ds[time_var].dt.month,
    hour=ds[time_var].dt.hour
)

# Define seasons

season_months = {
    "spring": [3, 4, 5],
    "summer": [6, 7, 8],
    "autumn": [9, 10, 11],
    "winter": [12, 1, 2]
}

# Process each season

for season, months in season_months.items():

    print(f"\nProcessing {season}...")

    # Select all timestamps belonging to season
    season_ds = ds.where(
        ds["month"].isin(months),
        drop=True
    )

    # Average by hour across ALL years/files
    hourly_mean = season_ds.groupby("hour").mean(
        dim=time_var
    )

    # GIS setup
    hourly_mean = hourly_mean.rename({
        "latitude": "lat",
        "longitude": "lon"
    })

    hourly_mean = hourly_mean.rio.set_spatial_dims(
        x_dim="lon",
        y_dim="lat"
    )

    hourly_mean = hourly_mean.rio.write_crs("EPSG:4326")

    # Create folders
    u_folder = os.path.join(
        OUTPUT_FOLDER,
        season,
        "u"
    )

    v_folder = os.path.join(
        OUTPUT_FOLDER,
        season,
        "v"
    )

    os.makedirs(u_folder, exist_ok=True)
    os.makedirs(v_folder, exist_ok=True)

    # Export hourly rasters
    for h in range(24):

        subset = hourly_mean.sel(hour=h)

        subset["u10"].rio.to_raster(
            os.path.join(
                u_folder,
                f"{season}_u_{h:02d}.tif"
            )
        )

        subset["v10"].rio.to_raster(
            os.path.join(
                v_folder,
                f"{season}_v_{h:02d}.tif"
            )
        )

    print(f"{season} completed.")

print("\nAll seasons processed.")