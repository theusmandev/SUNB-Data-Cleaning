import pandas as pd
import os

def step_4_remove_multiple_links():
    # Folder path
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 3 se aane wali file jisme 2 columns hain)
    input_file = os.path.join(folder_path, "03_consolidated_links_data.csv")
    
    # Output file (Clean data jisme sirf single links honge)
    output_valid_file = os.path.join(folder_path, "04_cleaned_single_links_data.csv")
    
    # Master Log File
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 4: Comma separated links ko remove aur log kiya ja raha hai...\n")
    
    try:
        # 1. Read input CSV
        df = pd.read_csv(input_file)
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 2. Pata lagana ke kin rows ke 'Links' column mein comma (',') hai
        # Na/NaN values ko empty string se fill kar rahe hain safety ke liye, taake error na aaye
        mask_to_delete = df['Links'].fillna('').astype(str).str.contains(',')
        
        # 3. Data ko Split Karna
        # Valid data wo hai jisme comma nahi hai
        df_valid = df[~mask_to_delete]
        
        # Delete hone wala data (jisme commas hain)
        df_deleted = df[mask_to_delete].copy()
        
        # 4. Tracking Column Add Karna
        df_deleted['Deletion_Step'] = 'Step 4: Comma Separated Links'
        
        # 5. Valid Data Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # 6. Log File mein Append Karna
        # Check karte hain ke file exist karti hai ya nahi (taake headers set ho sakein)
        file_exists = os.path.isfile(deleted_log_file)
        df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        print("\n--- RESULTS ---")
        print(f"✅ Saaf (Single Link) Rows: {len(df_valid)} -> Saved in '04_cleaned_single_links_data.csv'")
        print(f"🗑️ Delete ki gayi Multiple Link Rows: {len(df_deleted)} -> Appended to 'deleted_rows_log.csv'")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya pehle Step 3 ki script run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_4_remove_multiple_links()