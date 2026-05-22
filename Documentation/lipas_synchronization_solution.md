# Own Data to Lipas Synchronization Solution

### Purpose

How to synchronize own GIS routes / points to Lipas (and keep them up to date).

### Architecture

![tp1.1-arch-help.svg](tp1.1-arch-help.svg)

### Workflow Overview

 1. Add these columns to your preferred data storage eg. database
     * ```lipas_id```, ```lipas_checked``` and ```last_modif```
 6. Prepare your own data to load it to QGIS
 7. Load lipas data to QGIS (WFS)
 8. Deduplicate (see [Lipas Deduplication Process Documentation](lipas_deduplication))
 9. Populate ```lipas_id``` based on deduplication results
 10. Make data transfer (see [Lipas Data Transfer to Lipas Documentation](lipas_data_transfer))
 11. Check metadata correctness inside lipas UI
     * Update ```lipas_checked``` timestamp

### Data Model

In order to synchronize external data to Lipas the tables that store your point and route data must include the following columns. If database tables are not wished to be edited or not possible views can also be used.

| Column      | Data Type | Description | Example |
| ----------- | ----------- | -------- | --- |
|  ```lipas_id``` | int |The ID for a corresponding entry from Lipas <br> for your entry, if found. | ```12345``` |
| ```lipas_checked``` | Timestamp |Timestamp when the metadata between <br> lipas and the external data source was verified.| ```2025-10-29T12:43:00``` |
| ```last_modif``` | Date |Timestamp of the most recent changes in your local data.| ```2023-08-02``` |

#### ```lipas_id```
```lipas_id``` can be populated by the results obtained from the deduplication process. (see [Lipas Deduplication Process Documentation](lipas_deduplication))

States:
 - null = unprocessed
 - ```lipas_id``` = 0 if no match found
 - ```lipas_id``` = Lipas ID of found matching entity

If ```lipas_id``` = 0, the entry must be transferred to Lipas. <br>
If ```lipas_id``` = 1, found matching LOI entity. LOI id saved in ```lipas_loi_id```. 

#### ```lipas_checked```
Once the data transfer to Lipas is complete (see [Lipas Data Transfer to Lipas Documentation](lipas_data_transfer)) the metadata between the new lipas entries and your local data must be manually confirmed trough the lipas UI. When confirmed the ```lipas_checked``` is to be set to the current timestamp and the IDs of the new entries in Lipas can be updated into your table in the ```lipas_id``` column.

- Oliko tarkotus tarkistaa Lippaan käyttöliittymässä/QGississä vai molemmissa?
- Pitääkö kaikki tarkistaa, myös joille löytyi duplikaatti?
    - vai vertaillaanko päivämääriä, jos virmassa viimeksi muokattu -> pitää tarkistaa?, muuten ok? voidaan laittaa lipas_cheked tähän päivään


### Keeping Data Up to Date
If your data gets modified in your database in the future, you can still ensure its up-to-dateness also in Lipas by taking the following steps.

#### Adding new entries

If new items are added to your database, they can be identified from the unprocessed ```lipas_id```. <br>

| `lipas_id = NULL` | New entry not yet synchronized |
|--------------------|--------------------------------|

If new entries are detected, the synchronization process can be rerun. <br>
This ensures that all new routes and points are included in the next Lipas data transfer. 

#### Updating excisting data

If existing data is modified (not adding entirely new items), the date of the last modification can be compared with the synchronization timestamp. <br>
| Column | Purpose |
|--------|----------|
|```last_modif```|Timestamp of the most recent changes in your local data |
|```lipas_checked``` |Timestamp when the entry was last synchronized with Lipas. |

If the ```last_modif``` is **more recent** than the ```lipas_checked```, the metadata can be updated in Lipas either:
- Manually through Lipas UI
- Doing new data transfer with the updated metadata.

In the case of the data transfer the metadata needs to be verified manually again and in both cases the ```lipas_checked``` needs to be updated to the correct timestamp. 

#### Periodic Synchronization

The identification for the new entries and the comparison between the timestamps must be done periodically (eg. yearly or quarterly), in order to maintain up-to-dateness in the data also in Lipas. <br>

### Requirements

 - PostGIS
 - QGIS
 - Lipas credentials
 - Python (deduplication)

### License

MIT

### Acknowledgements / Funding

**Project**: Developing interoperability of digital recreational data (Digiretki)


<img width="1536" height="343" alt="image" src="https://github.com/user-attachments/assets/9bf00b51-c1d7-4384-8b4b-1d66ff1f88bd" />
