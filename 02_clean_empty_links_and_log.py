import pandas as pd
import numpy as np
import os

def step_2_clean_and_log():
    # Aapka exact folder path
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Jo aapke paas pehle se majood hai)
    input_file = os.path.join(folder_path, "merged_novels_data.csv")
    
    # Output files
    output_valid_file = os.path.join(folder_path, "02_cleaned_novels_data.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 2: Cleaning process aur logging start ho rahi hai...\n")
    
    try:
        # 1. Read input CSV
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(input_file, encoding='cp1252')
            except UnicodeDecodeError:
                df = pd.read_csv(input_file, encoding='latin1')
                
        print(f"Original file mein total rows: {len(df)}")
        
        # 2. Fazool columns ko nikalna (Sirf pehle 3 columns rakhna)
        df = df.iloc[:, :3]
        cols = df.columns
        title_col = cols[0]
        gdrive_col = cols[1]
        mediafire_col = cols[2]
        
        # 3. Missing links ko dhoondhne ke liye working copy banana
        df_working = df.copy()
        
        # Jinki jagah "No Google Drive Link" ya "No Mediafire Link" likha hai, unko empty (NaN) bana do
        df_working[gdrive_col] = df_working[gdrive_col].replace(r'(?i).*No Google Drive Link.*', np.nan, regex=True)
        df_working[mediafire_col] = df_working[mediafire_col].replace(r'(?i).*No Mediafire Link.*', np.nan, regex=True)
        
        # Jinki jagah sirf space hai, unko bhi NaN bana do
        df_working[gdrive_col] = df_working[gdrive_col].replace(r'^\s*$', np.nan, regex=True)
        df_working[mediafire_col] = df_working[mediafire_col].replace(r'^\s*$', np.nan, regex=True)
        
        # 4. Pata lagana ke kaunsi rows delete karni hain (Jahan dono links khali hain)
        mask_to_delete = df_working[gdrive_col].isna() & df_working[mediafire_col].isna()
        
        # 5. Data ko Split Karna
        # Valid data
        df_valid = df_working[~mask_to_delete]
        
        # Delete hone wala data (original dataframe se lenge taake original text log mein jaye)
        df_deleted = df[mask_to_delete].copy()
        
        # 6. Tracking Column Add Karna
        df_deleted['Deletion_Step'] = 'Step 2: No Links Found'
        
        # 7. Valid Data Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # 8. Log File mein Append Karna
        file_exists = os.path.isfile(deleted_log_file)
        df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        print("\n--- RESULTS ---")
        print(f"✅ Saaf (Valid) Rows: {len(df_valid)} -> Saved in '02_cleaned_novels_data.csv'")
        print(f"🗑️ Delete ki gayi Rows: {len(df_deleted)} -> Appended to 'deleted_rows_log.csv'")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya path aur file ka naam check karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_2_clean_and_log()