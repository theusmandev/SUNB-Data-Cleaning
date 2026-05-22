import pandas as pd
import os
import re

def step_5_remove_invalid_titles():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    input_file = os.path.join(folder_path, "Smart UNB Upgradation.csv")
    output_valid_file = os.path.join(folder_path, "05_cleaned_titles_data.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 5: Blank aur '????' wale titles ko filter kiya ja raha hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 2. Titles column ko saaf/check karne ke liye string mein convert karna
        # strip() use kar rahe hain taake agar title mein sirf spaces hon to wo bhi empty count ho
        titles_str = df['Titles'].astype(str).str.strip()
        
        # 3. Masks (Conditions) banana
        # Condition 1: Title khali hai (NaN, Null, ya bilkul empty string)
        mask_empty = df['Titles'].isna() | (titles_str == "") | (titles_str.str.lower() == "nan")
        
        # Condition 2: Title mein sirf question marks hain (e.g., "?", "???", "????")
        # Regex r'^\?+$' ka matlab hai start (^) se end ($) tak sirf '?' hone chahiye (1 ya us se zyada)
        mask_question_marks = titles_str.str.contains(r'^\?+$', regex=True, na=False)
        
        # Dono conditions ko mila dena (Agar khali ho YA question marks hon)
        mask_to_delete = mask_empty | mask_question_marks
        
        # 4. Data ko Split Karna
        # Delete hone wala data
        df_deleted = df[mask_to_delete].copy()
        
        # Valid (theek) data
        df_valid = df[~mask_to_delete].copy()
        
        # 5. Tracking Column Add Karna
        if not df_deleted.empty:
            df_deleted['Deletion_Step'] = 'Step 5: Blank or Question Marks Title'
        
        # 6. Valid Data Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # 7. Log File mein Append Karna
        if not df_deleted.empty:
            file_exists = os.path.isfile(deleted_log_file)
            df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        print("\n--- RESULTS ---")
        print(f"✅ Theek (Valid) Titles: {len(df_valid)} -> Saved in '05_cleaned_titles_data.csv'")
        print(f"🗑️ Delete kiye gaye Invalid Titles: {len(df_deleted)} -> Appended to 'deleted_rows_log.csv'")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya file aur path ka naam check karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_5_remove_invalid_titles()