# Deduplication of point objects pipeline

## Overview

This deduplication tool implements a **point object matching and deduplication pipeline** designed to identify and link records that represent the same real-world locations across two different spatial datasets.

The primary use case is matching external hiking data with data from the [LIPAS](https://lipas.fi/liikuntapaikat) (a national service for sports and outdoor activity locations).

## Purpose

The goal of this pipeline is to:

- Identify duplicate or corresponding point objects across two datasets
- Match records that refer to the same physical location
- Reduce redundancy and improve data quality
- Support integration between different spatial systems

In this case, the focus is on **outdoor sports and hiking locations**, especially for point objects (e.g., shelter, or viewpoint) where the same place may exist in both datasets but with:

- different naming conventions
- slightly different coordinates
- different classification systems

## Documentation

For a more detailed description of the workflow and methodology, see:  
👉 [point_deduplication.md](../Documentation/point_deduplication.md)

This file demonstrates the technical usage of the pipeline.

## Setup and Usage

### 1. Preprocessing (QGIS)

Before running the notebook:

- Perform a **spatial distance search** in QGIS to identify potential matches (see detailed documentation)  
- Use *Join Attributes by Nearest* to generate candidate matches 
- Export the result as a file for further processing  

---

### 2. Prepare Mapping Table

Create a **category mapping table** that maps:

- your dataset categories → LIPAS categories  

This is required for category-based validation.

---

### 3. Configure the Notebook

Set up the datapath and category table mapping path according to your data.

Set the following variables according to your dataset:
- ```ID_COL``` <br>
Unique identifier in your dataset

- ```LIPAS_ID_COL``` <br>
Identifier from the spatial match (produced in QGIS, e.g. id or id_2)

- ```CLASS_COL``` <br>
Category of your data point

- ```TYPE_COL_LIPAS``` <br>
Category of the matched LIPAS point (e.g. tyyppi_nimi_fi)

- ```MAP_KEY``` <br>
Column in the mapping table representing your dataset category

- ````MAP_VALUE```` <br>
Corresponding LIPAS category in the mapping table

- ```NAME1_COL``` <br>
Name of your data point

- ```NAME2_COL``` <br>
Name of the matched LIPAS point (from spatial search, e.g. nimi_fi)


## Pipeline logic

### Duplicate Detection

- Rows are grouped by the unique identifier (``ID_COL``) to identify cases where:

  - one input point has multiple candidate matches (from spatial search)

These are treated as duplicate candidate groups.

---

### Initial Match Classification

Each candidate pair is classified using rule-based logic:

A match is considered valid if **any of the following is true**:

- LIPAS category == mapped category
- LIPAS category == original category
- Names are exactly equal

This produces a boolean flag:

``category_match = True / False``

---

### Resolving Duplicate Candidates

If multiple candidates exist for the same point:

- Name similarity is calculated using fuzzy matching (``rapidfuzz.token_sort_ratio``)
- Only the **best match above a threshold** is kept
- If no candidate meets the threshold:
  - all candidates are moved to manual review

---

### Processing Non-Duplicate Entries

Entries without duplicate candidates are processed separately:

- Apply the same classification logic
- Use fuzzy matching to recover additional matches from:
  - points that weren't recognized as a match based on the logic

## Run the notebook
- Run each code block in [point_deduplicator.ipynb](point_deduplicator.ipynb) 

## Final Result 

The pipeline produces the following outputs:

- **`true_matches`**  
  High-confidence matches  

- **`true_matches_duplicates`**  
  Matches resolved from duplicate candidates using similarity  

- **`mismatches`**  
  Candidate matches that do not correspond  

- **`review_mismatches_duplicates`**  
  Duplicate candidates where no reliable match was found → require manual review  

- **`needs_checking`**  
  Cases with missing category mapping or unclear classification → require manual review  

- **`not_matched`**  
  Entries with no spatial candidate  


## Notes
- Always validate results before updating your database
- Pay special attention to:
  - multiple spatial candidates
  - differing categories between systems
  - significantly different names


## Installation

```bash
pip install -r requirements.txt