# Wind Climate Raster Exporter

This repository processes long-term climate reanalysis data into seasonal, hourly wind climatologies for geospatial analysis. It transforms large NetCDF datasets into structured raster outputs to support GIS-based environmental and route modelling in marine contexts.

---

## 📋 What Does This Script Do?

Given multi-year hourly wind records covering a geographic region, this script computes the **climatological mean wind field** for each hour of the day across each season, across all 24 hours and all four seasons, producing a structured set of geospatial raster files representing the mean **eastward** (`u10`) and **northward** (`v10`) wind components at 10 metres above surface. Together, these two components fully describe wind speed and direction at any point in the domain.

Typical applications include:
- Marine route optimisation and environmental modelling
- Wind energy resource assessment
- Climate and reanalysis data post-processing
- GIS-based environmental impact studies

---

## 📁 Required Folder Structure

Before running the script, your project folder must look like this:

```
your-project-folder/
│
├── process_wind.py       ← the script
│
├── data/                 ← PUT YOUR .nc FILES HERE
│   ├── wind_2018.nc
│   ├── wind_2019.nc
│   └── wind_2020.nc
│
└── output/               ← will be created automatically
```

> ✅ You only need to create the `data/` folder manually and place your `.nc` files inside it. The `output/` folder and everything inside it will be **created automatically** when you run the script.

---

## 🗂️ What Are `.nc` Files?

`.nc` stands for **NetCDF** — a file format used by meteorologists and climate scientists to store large amounts of geographic and time-series data efficiently. If you downloaded wind data from [Copernicus / ERA5](https://cds.climate.copernicus.eu/), NOAA, or a similar source, your files are likely already in this format.

The script specifically expects each file to contain:
- `u10` — wind speed in the **east–west direction** (positive = blowing eastward)
- `v10` — wind speed in the **north–south direction** (positive = blowing northward)
- A time coordinate named either `time` or `valid_time`
- `latitude` and `longitude` coordinates

---

## ⚙️ Changing Folder Names (Optional)

If you want to use different folder names instead of `data/` and `output/`, open the script and find these two lines near the top:

```python
INPUT_FOLDER = "data"
OUTPUT_FOLDER = "output"
```

Change them to whatever folder names you prefer. For example:

```python
INPUT_FOLDER = "my_wind_files"
OUTPUT_FOLDER = "results"
```

Then create a folder with that name and place your `.nc` files inside it.

---

## ⚙️ Environment Setup

This project uses a Conda environment to ensure reproducibility across different machines.

### Step 1 — Create the environment

```bash
conda create -n windproj python=3.11
conda activate windproj
```

### Step 2 — Install dependencies

```bash
conda install -c conda-forge xarray dask netcdf4 rioxarray rasterio scipy
```

---

## 🖥️ How to Run the Script

### Step 1 — Activate the environment

```bash
conda activate windproj
```

### Step 2 — Place your data

Put all your `.nc` wind files inside the `data/` folder.

### Step 3 — Run the script

From inside your project folder, run:

```bash
python process_wind.py
```

You'll see progress printed in the terminal:

```
Found 3 NetCDF files.

Processing spring...
spring completed.

Processing summer...
summer completed.

Processing autumn...
autumn completed.

Processing winter...
winter completed.

All seasons processed.
```

---

## 📤 Output Structure

After running, the `output/` folder will be organized like this:

```
output/
├── spring/
│   ├── u/
│   │   ├── spring_u_00.tif   ← east-west wind at midnight (spring average)
│   │   ├── spring_u_01.tif   ← east-west wind at 1 AM
│   │   └── ... (up to spring_u_23.tif)
│   └── v/
│       ├── spring_v_00.tif   ← north-south wind at midnight (spring average)
│       └── ... (up to spring_v_23.tif)
├── summer/
│   ├── u/ ...
│   └── v/ ...
├── autumn/
│   ├── u/ ...
│   └── v/ ...
└── winter/
    ├── u/ ...
    └── v/ ...
```

In total: **4 seasons × 24 hours × 2 components = 192 `.tif` files**

Each `.tif` file is a **GeoTIFF** — a standard map image format compatible with GIS software. The coordinate system used is **WGS84 (EPSG:4326)**, the same system used by GPS.

---

## 🗓️ How Seasons Are Defined

| Season | Months Included |
|--------|----------------|
| Spring | March, April, May |
| Summer | June, July, August |
| Autumn | September, October, November |
| Winter | December, January, February |

---

## ❗ Troubleshooting

| Problem | Solution |
|--------|----------|
| `No .nc files found in data folder` | Make sure your `.nc` files are inside the `data/` folder and have the `.nc` extension |
| `Could not find time coordinate` | Your NetCDF file uses a non-standard time variable name. Open an issue or check the file with a tool like [Panoply](https://www.giss.nasa.gov/tools/panoply/) |
| `ModuleNotFoundError` or missing packages | Ensure the environment is activated (`conda activate windproj`) and reinstall dependencies via conda-forge |
| Dask-related errors | Ensure environment is activated: `conda activate windproj` and reinstall dependencies via conda-forge |
| Script runs but output is empty | Make sure the files contain `u10` and `v10` variables |

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `xarray` | NetCDF processing |
| `dask` | Handles multi-file / parallel computation |
| `netcdf4` | Reads `.nc` climate datasets |
| `rioxarray` | GIS / raster export |
| `rasterio` | GeoTIFF writing |
| `scipy` | Scientific backend utilities |

---

## ⚠️ Important Environment Note

This project must be run inside the Conda environment (`windproj`). Do not use system Python or pip installs outside Conda, as this may cause missing Dask backend errors, NetCDF reading issues, or inconsistent xarray behaviour.

---

## 🔁 Reproducibility

To export the exact environment used in this project for sharing with collaborators:

```bash
conda env export > environment.yml
```

To recreate it from that file:

```bash
conda env create -f environment.yml
conda activate windproj
```

---

## 📄 License

MIT License — free to use, modify, and share.
