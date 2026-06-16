# 🌬️ Wind Climate Raster Exporter

This repository processes long-term climate reanalysis data into seasonal, hourly wind climatologies for geospatial analysis. It transforms large NetCDF datasets into structured raster outputs to support GIS-based environmental and route modelling in marine contexts.

A Python script that takes years of hourly wind data and turns them into **seasonal wind maps** — one map per hour of the day, per season. The output files can be opened in any GIS software (like QGIS or ArcGIS) to visualize wind patterns across a region.

---

## 🧭 What Does This Script Actually Do?

Imagine you have several years of wind measurements recorded every hour, covering a geographic region. This script answers the question:

> *"On a typical summer afternoon at 3 PM, which direction is the wind blowing across this area — and how strong is it?"*

It does this for **every hour of the day** (midnight, 1 AM, 2 AM ... 11 PM) and for **all four seasons** (spring, summer, autumn, winter).

The result is a collection of map files — one per hour per season — that show the wind's **east–west pull** (`u10`) and **north–south pull** (`v10`) averaged across all the years in your dataset. Together, these two components fully describe the wind's speed and direction at any point on the map.

These maps are useful for:
- Wind energy site assessments
- Urban planning and ventilation studies
- Climate research
- Environmental impact analysis

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

## 🖥️ How to Run the Script

### Step 1 — Make sure Python is installed

You need **Python 3.8 or later**. To check, open a terminal and run:

```bash
python --version
```

### Step 2 — Install the required libraries

Run this command once to install all dependencies:

```bash
pip install xarray rioxarray rasterio netcdf4 scipy
```

> 💡 If you're using a Mac and run into issues, try `pip3` instead of `pip`.

### Step 3 — Place your data

Put all your `.nc` wind files inside the `data/` folder.

### Step 4 — Run the script

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
| `ModuleNotFoundError` | Run `pip install xarray rioxarray rasterio netcdf4 scipy` again |
| Script runs but output is empty | Make sure the files contain `u10` and `v10` variables |

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `xarray` | Reading and processing NetCDF climate data |
| `rioxarray` | Adding geospatial/GIS capabilities to xarray |
| `rasterio` | Writing GeoTIFF raster files |
| `netcdf4` | Backend engine for reading `.nc` files |
| `scipy` | Used internally by xarray for some operations |

---

## 📄 License

MIT License — free to use, modify, and share.
