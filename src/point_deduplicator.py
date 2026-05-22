import pandas as pd
from rapidfuzz import fuzz


def build_mapping(mapping_df, key_col, value_col):
    return dict(zip(mapping_df[key_col], mapping_df[value_col]))



def find_duplicates(df, id_col):
    duplicated_ids = df[id_col][df[id_col].duplicated(keep=False)]
    duplicates_df = df[df[id_col].isin(duplicated_ids)]
    return duplicates_df



def apply_mapping(df, mapping_dict, class_col):
    """
    Map class column values to target categories using a mapping dictionary.
    Returns a COPY of the dataframe.
    """
    df = df.copy()
    df['mapped_lipas_category'] = df[class_col].map(mapping_dict)
    return df



def classify_matches(df, type_col, class_col, name1_col=None, name2_col=None):
    df = df.copy()

    condition = (
        (df[type_col] == df["mapped_lipas_category"]) |
        (df[type_col] == df[class_col])
    )

    if name1_col and name2_col:
        condition = condition | (df[name1_col] == df[name2_col])

    df["category_match"] = condition

    return df



def split_results(duplicates_df):
    true_matches = duplicates_df[duplicates_df["category_match"] == True]
    mismatches = duplicates_df[duplicates_df["category_match"] == False]

    needs_checking = mismatches[mismatches["mapped_lipas_category"].isna()]
    mismatches_clean = mismatches[~mismatches["mapped_lipas_category"].isna()]

    return true_matches, mismatches_clean, needs_checking


def keep_best_row_match(df, id_col, name1_col, name2_col, threshold=75):
    """
    For duplicate rows based on `id_col`, compare `name_2` to `name_1` and:
    - Keep only the row with the highest similarity to name_1
    - If neither meets threshold, move both rows to review_df
    
    Parameters:
    - df: pandas DataFrame
    - id_col: column identifying duplicates (e.g., 'gid')
    - name1_col: reference name column (e.g., 'name_1')
    - name2_col: mapped name column to compare (e.g., 'name_2')
    - threshold: similarity threshold (default 85)
    
    Returns:
    - filtered_df: DataFrame with rows meeting threshold
    - review_df: DataFrame with rows where neither duplicate met threshold
    """
    
    filtered_rows = []
    review_rows = []
    
    # Group by id
    grouped = df.groupby(id_col)
    
    for id, group in grouped:

        # If only one row keep it
        if len(group) == 1:
            row = group.iloc[0]
            filtered_rows.append(row)

        else:
            # Multiple duplicates → compute similarity for each row
            scores = group.apply(lambda row: fuzz.token_sort_ratio(str(row[name1_col]), str(row[name2_col])), axis=1)
            max_idx = scores.idxmax()
            max_score = scores[max_idx]
            
            if max_score >= threshold:
                # Keep only the row with the highest score
                filtered_rows.append(group.loc[max_idx])
            else:
                # Neither row good enough → move all duplicates to review
                review_rows.extend(group.to_dict('records'))
    
    filtered_df = pd.DataFrame(filtered_rows).reset_index(drop=True)
    review_df = pd.DataFrame(review_rows).reset_index(drop=True)
    
    return filtered_df, review_df


def compare_name_similarity(df, name1_col, name2_col, threshold=75):

    matching_rows = []
    mismatching_rows = []

    for idx, row in df.iterrows():
        score = fuzz.token_sort_ratio(str(row[name1_col]), str(row[name2_col]))
        if score > threshold:
            matching_rows.append(row)
        else:
            mismatching_rows.append(row)

    matching_rows_df = pd.DataFrame(matching_rows).reset_index(drop=True)
    mismatching_rows_df = pd.DataFrame(mismatching_rows).reset_index(drop=True)
    
    return matching_rows_df, mismatching_rows_df


def process_data(
    df,
    mapping_df,
    id_col,
    lipas_id_col,
    class_col,
    type_col,
    map_key,
    map_value,
    name1_col=None,
    name2_col=None
):
    

    # Validate columns
    required = [id_col, class_col, type_col]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column in data: {col}")

    if map_key not in mapping_df.columns or map_value not in mapping_df.columns:
        raise ValueError("Mapping file missing required columns")

    # Create a mapping directory
    mapping_dict = build_mapping(mapping_df, map_key, map_value)

    # Detect duplicate entries inside given dataframe
    duplicates_df = find_duplicates(df, id_col)

    # Map your system class category to Lipas category based on your mapping dict
    mapped_duplicates = apply_mapping(duplicates_df, mapping_dict, class_col)

    # Classify weather the entry that the distance search found (in QGIS) is valid based on the mapped values
    duplicates_df = classify_matches(mapped_duplicates, type_col, class_col, name1_col, name2_col)

    # Split results accordingly based on classification
    true_matches, mismatches, needs_checking = split_results(duplicates_df)

    # Drop entries in other DataFrames if there is a match found for them 
    needs_checking = needs_checking[~needs_checking[id_col].isin(true_matches[id_col].unique())]
    mismatches = mismatches[~mismatches[id_col].isin(true_matches[id_col].unique())]

    # Detect duplicate entries inside split results
    duplicates_in_true_matches = find_duplicates(true_matches, id_col)
    duplicates_in_mismatches = find_duplicates(mismatches, id_col)
    duplicates_in_true_needs_checking = find_duplicates(needs_checking, id_col)

    # Drop the duplicate entries from true_matches
    true_matches = true_matches[~true_matches[id_col].isin(duplicates_in_true_matches[id_col].unique())]

    # compare duplicate matches
    matches_in_true_duplicates, true_matches_duplicates = keep_best_row_match(duplicates_in_true_matches, id_col, name1_col, name2_col)
    matches_in_duplicate_mismatches, review_mismatches_duplicates = keep_best_row_match(duplicates_in_mismatches, id_col, name1_col, name2_col)
    matches_in_needs_checking_duplicates, review_needs_checking_duplicates = keep_best_row_match(duplicates_in_true_needs_checking, id_col, name1_col, name2_col)


    # Add the true matches from the duplicate match entries to true_matches
    true_matches = pd.concat([true_matches, matches_in_true_duplicates], ignore_index=True)
    true_matches = pd.concat([true_matches, matches_in_duplicate_mismatches], ignore_index=True)
    true_matches = pd.concat([true_matches, matches_in_needs_checking_duplicates], ignore_index=True)

    # clear the mismatches dataframe
    mismatches = mismatches[~mismatches[id_col].isin(duplicates_in_mismatches[id_col].unique())]

    # drop the found matches from needs checking
    needs_checking = needs_checking[~needs_checking[id_col].isin(matches_in_needs_checking_duplicates[id_col].unique())]
    
    print(f"found true matches so far {true_matches.shape}")

    # Drop duplicate entries from original dataframe
    df = df[~df[id_col].isin(duplicates_df[id_col])]


    # Make a dataframe for those entries that the distance search didn't find any corresponding entries
    not_matched = df[df[lipas_id_col].isna()]

    # Drop those again from original dataframe
    df = df[~df[id_col].isin(not_matched[id_col])]


    # Repeat process for rest of unprocessed original dataframe (not duplicate entries)
    mapped_original_df = apply_mapping(df, mapping_dict, class_col)
    classified_original = classify_matches(mapped_original_df, type_col, class_col, name1_col, name2_col)
    true_matches_original, mismatches_original, needs_checking_original = split_results(classified_original)


    # Add the found matches to true_matches
    true_matches = pd.concat([true_matches, true_matches_original], ignore_index=True)
    print(f"found true matches so far {true_matches.shape}")


    # check if there is matches found in mismatches or needs checking
    matches_original_mismatches, mismatching_rows_original = compare_name_similarity(mismatches_original, name1_col, name2_col)
    matches_original_needs_checking, mismatching_rows_original_needs_checking = compare_name_similarity(needs_checking_original, name1_col, name2_col)


    # Add the found matches from the original mismatching rows to true_matches
    true_matches = pd.concat([true_matches, matches_original_mismatches], ignore_index=True)
    true_matches = pd.concat([true_matches, matches_original_needs_checking], ignore_index=True)

    # concatanate results
    mismatches = pd.concat([mismatches, mismatching_rows_original], ignore_index=True)
    needs_checking = pd.concat([needs_checking, mismatching_rows_original_needs_checking], ignore_index=True)

    # results
    print(f"true_matches: {true_matches.shape}")
    print(f"true_matches duplicates: {true_matches_duplicates.shape}")
    print(f"mismatches: {mismatches.shape}")
    print(f"needs_checking: {needs_checking.shape}")
    print(f"mismatches_duplicates: {review_mismatches_duplicates.shape}")
    print(f"no matches found: {not_matched.shape}")

    # let's check that we have correct number of entries
    all_gids = pd.concat([
    true_matches[id_col],
    true_matches_duplicates[id_col],
    mismatches[id_col],
    needs_checking[id_col],
    review_mismatches_duplicates[id_col],
    not_matched[id_col],
    ], ignore_index=True)
    print("Total unique entries:", all_gids.nunique())

    dataframes = [true_matches, true_matches_duplicates, mismatches, needs_checking, review_mismatches_duplicates, not_matched]

    # assign correct dtypes
    for df in dataframes:
        df[id_col] = df[id_col].astype("Int64")

    return true_matches, true_matches_duplicates, mismatches, review_mismatches_duplicates, needs_checking, not_matched

