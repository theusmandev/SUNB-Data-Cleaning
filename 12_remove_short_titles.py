import pandas as pd
import os

def step_12_remove_short_titles():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 11 ka output)
    input_file = os.path.join(folder_path, "11_cleaned_final_titles.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "12_cleaned_long_titles.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 12: 1 ya 2 lafzon (words) wale titles ko filter kiya ja raha hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Titles'] = df['Titles'].astype(str)
        
        # 2. WORD COUNT LOGIC
        # str.split() title ko spaces ke hisab se tor kar list banata hai
        # str.len() us list ke items (words) ki ginti karta hai
        word_counts = df['Titles'].str.split().str.len()
        
        # Mask banana un rows ke liye jinke words 2 ya us se kam hain (0, 1, ya 2)
        short_titles_mask = word_counts <= 2
        
        # 3. Data ko Split (Alag) karna
        df_deleted = df[short_titles_mask].copy()
        df_valid = df[~short_titles_mask].copy()
        
        # 4. Tracking column add karna central log file ke liye
        if not df_deleted.empty:
            df_deleted['Deletion_Step'] = 'Step 12: Title with 1 or 2 words'
        
        # 5. Valid data save karna (Jisme 3 ya us se zyada words hain)
        df_valid.to_csv(output_valid_file, index=False)
        
        # 6. Delete hone wala data Central Log file mein append karna
        if not df_deleted.empty:
            file_exists = os.path.isfile(deleted_log_file)
            df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        # 7. TERMINAL SUMMARY DISPLAY
        print("=" * 60)
        print("📊 STEP 12: SHORT TITLES REMOVAL SUMMARY REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"🗑️ Rows Deleted (1 or 2 words in title)        : {len(df_deleted)}")
        print(f"✅ Safe Rows Remaining (3+ words in title)     : {len(df_valid)}")
        print("-" * 60)
        print(f"📝 Appended to Central Log File : '{os.path.basename(deleted_log_file)}'")
        print(f"💾 Main Cleaned File Saved      : '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 11 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_12_remove_short_titles()