# Mapping and export pipeline

## Overview

This mapping tool implements mapping pipeline from deduplicated source data designed to prepare external outdoor recreation data for LIPAS-compatible export.

The primary use case is mapping source data to:

- existing LIPAS records found during deduplication
- LIPAS type categories
- LIPAS LOI categories for objects that do not have a normal LIPAS type

This notebook is intended to be used after deduplication. The deduplication result tells which source rows already exist in LIPAS and should be removed from the final export.

## Purpose

The goal of this pipeline is to:

- join original source data with deduplication results
- remove rows that already have an existing LIPAS match
- map remaining source categories to LIPAS or LOI categories
- manually handle source categories that cannot be mapped automatically
- remove categories that should not be exported
- produce a clean CSV for further import or review

The workflow is necessary when the source data and LIPAS use different category systems. For example, one source category may need to be split into several LIPAS categories.

## Input files

The notebook expects three main input files.

### 1. Original source data

This is the full source dataset.

Example:

```text
source_data.csv
```

The source data should contain a unique identifier, for example:

```text
source_id
```

The workflow also expects category and name columns.

### 2. Deduplication result

This file identifies which source rows already exist in LIPAS.

Expected structure:

```text
source id -> mapped LIPAS id
```

Example:

```text
source id,mapped_lipas_id
1,0
2,123456
3,0
```

Meaning:

- `mapped_lipas_id > 0` = this source object already exists in LIPAS and is removed from the export
- `mapped_lipas_id = 0` = no LIPAS duplicate was found and the row is kept for category mapping


### 3. Mapping table

This table maps source categories to LIPAS and/or LOI categories.

Example columns:

```text
id
source_type
lipas_type_name
lipas_type_code
confirmed (Boolean)
lipas_loi_type
```

In this workflow, `confirmed = True` means that the row or category still needs manual handling. After manual handling, the flag is set to `False`.

## Setup and usage

Example usage of this workflow can be seen in notebooks_with_exampl_data/mapping

### 1. Run deduplication first

- Before using this notebook, create a deduplication result file.
- For point data, this is produced by the point deduplication workflow.
- For route data, this is produced by the route deduplication workflow. Note: Untested and WIP.  
- The important requirement is that the deduplication file has **one row per source object**. 

---

### 2. Configure file paths

Set the input paths:

```python
ORIGINAL_DATA_PATH = "source_data.csv"
DEDUP_PATH = "deduplication_data.csv"
MAPPING_PATH = "mapping_table.csv"
```

---

### 3. Configure column names

Set the variables according to the source data, deduplication result and mapping table.

- `SOURCE_ID_COL`  
  Stable unique identifier in the original source data

- `SOURCE_TYPE_COL`  
  Source category/type column

- `SOURCE_NAME_COL`  
  Source object name column

- `DEDUP_SOURCE_ID_COL`  
  Source identifier column in the deduplication result

- `DEDUP_LIPAS_ID_COL`  
  Existing LIPAS ID from the deduplication result

- `MAP_SOURCE_TYPE_COL`  
  Source category key in the mapping table

- `MAP_LIPAS_NAME_COL`  
  LIPAS category name column

- `MAP_LIPAS_CODE_COL`  
  LIPAS numeric type code column

- `MAP_LOI_TYPE_COL`  
  LOI type column

- `MAP_NEEDS_CHECK_COL`  
  Manual review flag column

## Pipeline logic

### Join deduplication result

The original source data is joined with the deduplication result, this adds the mapped LIPAS ID to each source row.

---

### Remove existing LIPAS duplicates

Rows with an existing LIPAS match are removed from the export, the rows can be found in `duplicates_df` for review.

---

### Join category mapping

The remaining rows are joined with the mapping table. Rows should normally have either `lipas_type_code` or `lipas_loi_type` but not both.

### Review rows needing manual mapping

Rows where the mapping flag is still `True` are selected for review. These rows require one of the following actions:

- map selected rows to a LIPAS category(s)
- map selected rows to a LOI category(s)
- remove the source category from export

---

### Remove unwanted source categories

Some source categories may not belong in the final export. Rows with these source categories are removed from `clean_df` and stored in `removed_category_rows_df`.

---

### Manual LIPAS category mapping

One source category can be split into one or many LIPAS categories by listing the source IDs that belong to each target category.

Example:

```python
source_category_to_map = "category_name"

lipas_category_rules = [
    {
        "source_ids": [0],
        "lipas_type_name": "Name",
        "lipas_type_code": 0000,
    },
]
```

For each rule, the notebook:

- finds rows with the selected source category and listed source IDs
- fills `lipas_type_name`
- fills `lipas_type_code`
- sets the manual review flag to `False`

This makes it possible to split broad source categories into specified LIPAS categories. Copy the cell for as many source categories as needed.

---

### Manual LOI mapping

Some objects are not normal LIPAS sports facility types but still belong in the LIPAS Location of interest classification.

Example:

```python
source_category_to_map = "category_name"

loi_category_rules = [
    {
        "source_ids": [0],
        "lipas_loi_type": "loi-name",
    },
]
```

For each rule, the notebook:

- fills `lipas_loi_type`
- sets the manual review flag to `False`

Copy the cell for as many source categories as needed

## Sanity checks

Before exporting, the notebook checks:

- original row count
- number of duplicate rows removed
- number of unwanted rows removed
- expected final row count
- actual final row count
- duplicate source IDs
- rows still marked as needing manual check
- rows missing both LIPAS and LOI category
- rows that have both LIPAS and LOI category

These checks should pass before the final CSV is exported.

## Export

Helper columns from joins and other unwanted columns can be removed before export.

The pipeline produces:

- `duplicates_df`  
  Source rows that already exist in LIPAS and are removed from the final export

- `removed_category_rows_df`  
  Rows removed because their source category should not be exported

- `clean_df`  
  Deduplicated and category-mapped rows that are kept for export

- final CSV export from `final_export_df`
  Cleaned, deduplicated and mapped data
