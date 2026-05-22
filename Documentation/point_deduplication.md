# Deduplication of point objects from Lipas data

## Overview

This deduplication tool implements a point object matching and deduplication pipeline designed to identify and link records that represent the same real-world locations across two different spatial datasets.

The primary use case is matching external hiking data with data from the [LIPAS](https://lipas.fi/liikuntapaikat) (a national service for sports and outdoor activity locations).

## Purpose

The goal of this pipeline is to:

- Identify duplicate or corresponding point objects across two datasets
- Match records that refer to the same physical location
- Reduce redundancy and improve data quality
- Support integration between different spatial systems

In this case, the focus is on **outdoor sports and hiking locations**, specially for point objects (e.g., shelter, or viewpoint) where the same place may exist in both datasets but with:

- different naming conventions
- slightly different coordinates
- different classification systems

## Workflow Overview

 1. Prepare your dataset and load it into QGIS as a layer
 7. Load [LIPAS](https://lipas.fi/liikuntapaikat) data into QGIS (via WFS)
 8. Perform a spatial distance search in QGIS (nearest neighbor analysis)
 9. Run the [point_deduplicator notebook](../notebooks/point_deduplicator/point_deduplicator.ipynb)
 10. Validate the matching results
 11. Update your own database with the validated matches

## Approach

### **1. Spatial Distance Search (external step)**

First, perform a spatial matching step in QGIS using **Join Attributes by Nearest**. <br>
**Set it up like this:**
- **Input layer** = your dataset (source points)
- **Join layer** = Lipas points
- Fields to transfer from the LIPAS layer (at least you can choose more if you like): 
    - ```id``` 
    - ```tyyppikoodi``` 
    - ```tyyppi_nimi_fi``` 
    - ```nimi_fi``` 
- Set **maximum number of nearest neighbors** (here we used 3)
- Set a **distance limit** (optional, e.g. 50m, here used 200m)
- Don't discard records which could not be joined, we want all of the points to preserve

This step generates candidate matches based on geographic proximity.

Using multiple nearest neighbors (e.g. 3 instead of 1) is important because:

- The closest point is not always the correct match
- Dense areas may contain multiple nearby features
- The correct match can be identified later using attribute and similarity checks

### **2. Category Mapping**

Create a mapping between:

- Your system’s category classification
- LIPAS category classification

This mapping enables meaningful comparison between datasets and is used as a key criterion in identifying matches.

- See [virma_lipas_type_mapping](./virma_lipas_type_mapping) as an example.

### **3. Duplicate Detection**

**Run the [point_deduplicator notebook](../notebooks/point_deduplicator/point_deduplicator.ipynb)**
- see [README](../notebooks/point_deduplicator/README.md) for more detailed instructions

This step:
- Processes candidate matches from the spatial search
- Applies category-based validation
- Uses name similarity (fuzzy matching) where needed
- Resolves duplicate candidates

### **4. Validation**

Review the obtained results, especially:
- Entries that had multiple candidate matches from the spatial search
- Entries that didn't get a mapped LIPAS category
- Entries that may represent the same real-world location but are categorized differently in the two systems
- Entries where the names differ significantly, even if the location is similar

**After validation:**

- Update your system with confirmed matches
- Store the matched LIPAS id in your system to keep track of which entries correspond to LIPAS records
- This enables:
    - traceability
    - future updates and synchronization

## Output & Usage
The results enable you to:
- Use for data integration between external GIS systems and LIPAS
- Avoid inserting duplicate entries into LIPAS
- Ensure that existing locations are correctly linked rather than recreated
- Improve overall data quality and consistency
- Review manually
- Export for further processing

## Requirements

 - PostGIS
 - QGIS
 - Python (deduplication)

## License

MIT

## Acknowledgements / Funding

**Project**: Developing interoperability of digital recreational data (Digiretki)


<img width="1536" height="343" alt="image" src="https://github.com/user-attachments/assets/9bf00b51-c1d7-4384-8b4b-1d66ff1f88bd" />
