# Virma-Lipas type mapping

Documentation on the virma-lipas type mapping table.

***

## Overview

This table describes the mapping between the category types of Virma and Lipas systems. The purpose is to export data from Virma to Lipas, so the Virma category types wanted to be mapped to the Lipas types. Lipas has two different systems inside it, sports places and locations of interests, lois. Virma categories can map to both of these systems. Sports places have their corresponding type names and codes but the loi types are only differentiated by an enum (loi_type). The table has a many-to-many relationship. 

## The mapping

For each Virma category we aim to give a corresponding type from Lipas. Most of the Virma categories mapped to the Lipas sports places and hence they were the primary mapping target. If there was not a corresponding sports place type a loi_type was assigned to the Virma category. 

Because the many-to-many relationship some of the Virma categories correspond to multiple Lipas categories and likewise. For example a Virma category ***Yleisö-wc tai -puucee*** (eng. public toilet or dry-toilet) corresponds to Lipas categories ***wc*** and ***dry-toilet***. In this case the virma category will be mapped to both of these Lipas categories. Likewise when one Lipas category corresponds to multiple Virma categories they will all be mapped to the same Lipas category. For example Lipas category ***Veneilynpalvelupaikka*** (eng. boating service point) corresponds e.g.to Virma categories ***Vierassatama*** and ***Rantautumispaikka*** (eng. Guest Harbour and Berth). 

The table is written in human readable form because it has been edited and filled by hand.

## Usage notes

Once the mapping was completed, a join was performed in our database to assign the appropriate Lipas types to our data for the data export. Because the table has a many-tomany relationship, some manual review was still required after the join to ensure that the correct types were assigned. Commercial services, such as cafés or restaurants, are not intended to be exported, so they were not assigned corresponding LIPAS types.

## Columns

| Column Name       | Type          | Description                                                   |
|-------------------|---------------|---------------------------------------------------------------|
| `id`              | serial4       | Table ID                                                      |
| `virma_class2_fi` | varchar(254)  | Virma type category                                           |
| `lipas_type_name` | varchar(254)  | Corresponding Lipas sports place type                         |
| `lipas_type_code` | int4          | Type code for the Lipas sports places                         |
| `lipas_loi_type`  | varchar(254)  | Corresponding lipas loi-type if no corresponding sport place  |
| `confirmed`       | boolean       | Whether the mapping is valid or not                           |

