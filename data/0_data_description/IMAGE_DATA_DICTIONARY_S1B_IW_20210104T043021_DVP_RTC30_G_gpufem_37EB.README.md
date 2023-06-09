ASF RTC Data Package (GAMMA)
============================

This folder contains Radiometric Terrain Corrected (RTC) products and their associated files. This data was processed by ASF DAAC HyP3 2022 using the hyp3_gamma plugin version 5.4.0 running GAMMA release 20210701. They are projected to WGS 84 / UTM zone 5N, and the pixel spacing is 30.0 m.

Processing Date/Time: 2022-06-03T16:29:51+00:00

The folder and each of its contents all share the same base name, using the following convention:
```
S1x_yy_aaaaaaaaTbbbbbb_ppo_RTCzz_u_defklm_ssss
x:          Sentinel-1 Mission (A or B)
yy:         Beam Mode
aaaaaaaa:   Start Date of Acquisition (YYYYMMDD)
bbbbbb:     Start Time of Acquisition (HHMMSS)
pp:         Polarization: Dual-pol (D) vs. Single-pol (S), primary polarization (H vs. V)
o:          Orbit Type: Precise (P), Restituted (R), or Original Predicted (O)
zz:         Terrain Correction Pixel Spacing
u:          Software Package Used: GAMMA (G)
d:          Gamma-0 (g) or Sigma-0 (s) Output
e:          Power (p) or Decibel (d) or Amplitude (a) Output
f:          Unmasked (u) or Water Masked (w)
k:          Not Filtered (n) or Filtered (f)
l:          Entire Area (e) or Clipped Area (c)
m:          Dead Reckoning (d) or DEM Matching (m)
ssss:       Product ID
```

The source granule used to generate the products contained in this folder is:
S1B_IW_GRDH_1SDV_20210104T043021_20210104T043046_025000_02F9AC_9F93

<!-- Consider opening this document in a Markdown editor/viewer for easier reading -->

### Using this data ###

Please refer to the ASF Sentinel-1 RTC Product Guide for in-depth guidance on the use of this dataset:
* https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/

When using this data as an image in a publication such as journal papers, articles, presentations, posters, and websites, please include the following credit with the image (portions in square brackets are optional):

    [RTC product processed by ]ASF DAAC HyP3 2022[ using GAMMA software]. Contains modified Copernicus Sentinel data 2021, processed by ESA.

When using this data in a manuscript and/or crediting datasets used for analysis, an acknowledgement including the software versions may be appropriate:

    ASF DAAC HyP3 2022 using the hyp3_gamma plugin version 5.4.0 running GAMMA release 20210701. Contains modified Copernicus Sentinel data 2021, processed by ESA.

DOIs are also provided for citation when discussing the HyP3 software or plugins:
* HyP3 processing environment, DOI: [10.5281/zenodo.3962581](https://doi.org/10.5281/zenodo.3962581)
* HyP3 GAMMA plugin, DOI: [10.5281/zenodo.3962936](https://doi.org/10.5281/zenodo.3962936)

For information on GAMMA SAR software, please see: https://gamma-rs.ch/

*************
# Product Contents #

The side-looking geometry of SAR imagery leads to geometric and radiometric distortions, causing foreshortening, layover, shadowing, and radiometric variations due to terrain slope. Radiometric terrain correction converts unprocessed SAR data into geocoded TIFF images with values directly relating to physical properties, alleviating the  inherent SAR distortions. The process improves backscatter estimates and provides geolocation information, so images can be used as input for applications such as the monitoring of deforestation, land-cover classification, and delineation of wet snow-covered areas.

The files generated in this process include:

1. Radiometric Terrain Corrected GeoTIFF data files for each polarization available
2. Browse images (PNG and KMZ format) in grayscale and color (when dual-pol is available)
3. A copy of the DEM used to correct the data (included in standard products; you can choose to omit this layer when custom ordering imagery)
4. An incidence angle map (included in standard products; you can choose to omit this layer when custom ordering imagery)
5. A local scattering area map (included in standard products; you can choose to omit this layer when custom ordering imagery)
6. A layover-shadow mask
7. A false-color RGB decomposition GeoTIFF (omitted in standard products; you can choose to include this layer when custom ordering imagery)
8. An ArcGIS xml metadata file for each raster layer, displayed in the Item Description (ArcGIS Desktop) or Metadata (ArcGIS Pro)
9. A shapefile indicating the RTC data extent
10. Log file

See below for detailed descriptions of each of the products.

-------------
## 1. Radiometric Terrain Corrected data files

GeoTIFF files are generated for each polarization available in the source granule. Each filename will include the polarization: VV or HH for primary polarization, and VH or HV for cross-polarization. To learn more about polarimetry, refer to https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/product-overview/polarimetry

These files have been processed to output gamma-0 power.

A speckle filter has been applied to the RTC images. The default is to not apply a speckle filter, but the user can choose to apply a filter when ordering the RTC imagery. When the filtering option is selected, an Enhanced Lee filter is applied during RTC processing to remove speckle while preserving edges. When applied, the filter is set to a dampening factor of 1, with a box size of 7x7 pixels and 180 looks.

-------------
## 2. Browse images in grayscale and color

PNG files are generated for quick visualization of the backscatter data. Each png browse image is accompanied by an aux file containing the projection and geocoding information for the file.

All products will include a grayscale png browse image. It is a rendering of the primary polarization data, scaled to an ASF standard to display nicely in grayscale. The image is designated by a simple .png extension.

For dual-pol products, a false-color png browse image is generated. It is a rendering of the primary and cross-polarization data, scaled to an ASF standard to display nicely in color. These files are additionally tagged with _rgb, but otherwise have the same tags/extensions as the grayscale browse images.

KMZ files are generated for use in Google Earth and other compatible applications. All products will include a grayscale kmz image, and dual-pol products will also include a color browse kmz image.

-------------
## 3. DEM used to correct the data

The Digital Elevation Model (DEM) layer is included with standard products, but is optional when placing a custom order for imagery. This layer is tagged with _dem.tif, and is provided in 16-bit signed integer format. Note that the actual RTC correction is performed using a 32-bit float version, but this file has been converted to 16-bit to reduce file size.

The source DEM has a geoid correction applied before it is used for RTC, so elevation values in this file will differ from the source DEM. It is provided in the same pixel spacing/alignment as the RTC product.

The DEM used for this product is GLO-30, which has a native pixel spacing of 1 arc second (about 30 meters). The Copernicus DEM GLO-30 is a global Digital Surface Model (DSM) derived from the WorldDEM. The WorldDEM is based on radar satellite data acquired by the TanDEM-X mission, which was funded by the German Aerospace Center (DLR) and Airbus Defence and Space, and edited to flatten water bodies, provide consistent flow of rivers, and apply corrections to shore/coastlines and special features. For an overview of the dataset, visit https://spacedata.copernicus.eu/explore-more/news-archive/-/asset_publisher/Ye8egYeRPLEs/blog/id/434960. The product handbook is available at https://spacedata.copernicus.eu/documents/20126/0/GEO1988-CopernicusDEM-SPE-002_ProductHandbook_I1.00.pdf.

*Refer to the _dem.tif.xml file for additional information about the specific DEM included with this product, including use and citation requirements.*

-------------
## 4. Incidence angle map

The incidence angle map is included with standard products, but is optional when placing a custom order for imagery. This layer is tagged with _inc_map.tif

This map records the local incidence angle for each pixel in the RTC image. The local incidence angle is the angle between the incident radar beam and the direction perpendicular to the ground surface, expressed in radians.

-------------
## 5. Scattering area map

The scattering area map is included with standard products, but is optional when placing a custom order for imagery. This layer is tagged with _area.tif

This map records the scattering area for each pixel in the RTC image. The scattering area was calculated based on the effectively illuminated gamma-0 terrain surface using a digital elevation model, expressed in square meters.

-------------
## 6. Layover-shadow mask

The layover/shadow mask indicates which pixels in the RTC image have been affected by layover and shadow. This layer is tagged with _ls_map.tif

The pixel values are generated by adding the following values together to indicate which layover and shadow effects are impacting each pixel:
0  Pixel not tested for layover or shadow
1  Pixel tested for layover or shadow
2  Pixel has a look angle less than the slope angle
4  Pixel is in an area affected by layover
8  Pixel has a look angle less than the opposite of the slope angle
16 Pixel is in an area affected by shadow

_There are 17 possible different pixel values, indicating the layover, shadow, and slope conditions present added together for any given pixel._

**The values in each cell can range from 0 to 31:**
0  Not tested for layover or shadow
1  Not affected by either layover or shadow
3  Look angle < slope angle
5  Affected by layover
7  Affected by layover; look angle < slope angle
9  Look angle < opposite slope angle
11 Look angle < slope and opposite slope angle
13 Affected by layover; look angle < opposite slope angle
15 Affected by layover; look angle < slope and opposite slope angle
17 Affected by shadow
19 Affected by shadow; look angle < slope angle
21 Affected by layover and shadow
23 Affected by layover and shadow; look angle < slope angle
25 Affected by shadow; look angle < opposite slope angle
27 Affected by shadow; look angle < slope and opposite slope angle
29 Affected by shadow and layover; look angle < opposite slope angle
31 Affected by shadow and layover; look angle < slope and opposite slope angle

-------------
## 7. False-color RGB decomposition

The RGB decomposition GeoTIFF is not included with standard products, but is optional when placing a custom order for imagery. This layer is tagged with _rgb.tif, and has the same pixel spacing as the RTC products.

If you do not require a full-resolution decomposition raster, you can omit this product and simply refer to the lower-resolution color browse image included in the product package.

This option is only available for dual-pol products, as it combines the co- and cross-polarized RTC values to generate a false-color image. In general, blue indicates areas with low backscatter in both co- and cross-polarizations (calm water, dry sand, frozen ground), green indicates high cross-pol values (vegetation or other volume scatterers), and red indicates areas with low cross-pol but relatively high co-pol values (urban areas). A full description of the approach used for generating this particular decomposition is available [here](https://github.com/ASFHyP3/hyp3-lib/blob/develop/docs/rgb_decomposition.md).

-------------
## 8. ArcGIS-compatible xml metadata files

Each raster in this folder has an associated xml file. It is named with the same filename as the raster, but also includes a .xml extension. When any of the rasters are viewed in ArcGIS, the associated xml file is recognized by the software, and the contents will display in the Item Description (ArcGIS Desktop) or Metadata (ArcGIS Pro) for that raster. Once the file is viewed in ArcGIS, the software will update the xml file to include metadata inherent to the raster (geographic extent, raster format, etc.) along with the descriptive metadata included in the original xml file.

ArcGIS users should take care not to edit the xml files directly, or to change filenames outside of the ArcGIS environment, as it may render the metadata files unreadable by ArcGIS.

Users who do not use ArcGIS to interact with the data may still find the information included in the individual xml files very useful, although the xml tag system makes it look cluttered in a text editor or browser window.

-------------
## 9. Shapefile

The shapefile (comprised of the four files tagged with _shape) contains a polygon indicating the extent of actual data (pixels with values other than NoData).

-------------
## 10. Log file

A textfile is generated during processing, which includes the parameters used and step-by-step processing history for the product. It has a .log extension.

*************
### RTC Processing ###

The basic steps in the radiometric terrain correction process are as follows:

1. Data granule is ingested into the format required by GAMMA software - calibration is done during this step.
2. If required, data is multi-looked to the desired number of looks (default for 30-m products is 6 looks for GRD granules and 3 for SLC; 10-m products default to one look). This product used 6 look(s).
3. A DEM is extracted from the ASF DEM heap covering the granule to be corrected.
4. A mapping function is created, mapping from DEM space into SAR space.
5. By default, DEM coregistration is not used. When the DEM Matching option is selected for a custom order, the following steps will be performed. *By default the process will skip from step 4 to step 6.*
    1. A simulated SAR image is created.
    2. The simulated SAR image and the real SAR image are coregistered.
    3. The mapping function is updated with the coregistration information.
6. The SAR image is radiometrically corrected using a pixel integration approach to remove radiometric distortions in foreshortening or layover areas.
7. The inversion of the mapping function is used to terrain correct and geocode the radiometrically corrected SAR image.
8. Post processing creates GeoTIFF, PNG and KMZ files, along with associated metadata.

*************
### The Sentinel-1 mission ###

The Sentinel-1A satellite was launched April 3, 2014, and the Sentinel-1B satellite was launched April 25, 2016. The satellites each have a 12-day repeat cycle.

More information about the mission is available at:
https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-1

Additional information about Sentinel-1 data, imagery, tools and applications is available at:
https://asf.alaska.edu/data-sets/sar-data-sets/sentinel-1/

*************
For assistance, contact the Alaska Satellite Facility:
uso@asf.alaska.edu
907-474-5041

-------------
Metadata version: 5.4.0
