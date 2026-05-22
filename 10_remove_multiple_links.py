import pandas as pd
import os
import re

def step_10_remove_multiple_links():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 9 ka output)
    input_file = os.path.join(folder_path, "09_fixed_drive_urls.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "10_cleaned_single_links.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 10: Ek hi row mein ek se zyada links wali rows ko filter kiya ja raha hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Links'] = df['Links'].astype(str)
        
        # 2. MULTIPLE LINKS CHECK KARNE WALA FUNCTION
        # Yeh function cell mein 'http://' ya 'https://' ki ginti (count) check karega
        def has_multiple_links(url_string):
            # 'http://' ya 'https://' ke saare matches dhoondna
            found_urls = re.findall(r'https?://', url_string, re.IGNORECASE)
            return len(found_urls) > 1

        # Mask banana un rows ke liye jahan 1 se zyada links hain
        multiple_links_mask = df['Links'].apply(has_multiple_links)
        
        # 3. Data ko Split (Alag) karna
        df_deleted = df[multiple_links_mask].copy()
        df_valid = df[~multiple_links_mask].copy()
        
        # 4. Tracking column add karna central log file ke liye
        if not df_deleted.empty:
            df_deleted['Deletion_Step'] = 'Step 10: Multiple Links in Single Row'
        
        # 5. Valid data save karna (Jisme sirf single link hai)
        df_valid.to_csv(output_valid_file, index=False)
        
        # 6. Delete hone wala data Central Log file mein append karna
        if not df_deleted.empty:
            file_exists = os.path.isfile(deleted_log_file)
            df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        # 7. TERMINAL SUMMARY DISPLAY (Aapki requirement ke mutabiq)
        print("=" * 60)
        print("📊 STEP 10: MULTIPLE LINKS REMOVAL SUMMARY REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"🗑️ Rows with Multiple Links Deleted            : {len(df_deleted)}")
        print(f"✅ Safe Rows Remaining (Single Link Only)      : {len(df_valid)}")
        print("-" * 60)
        print(f"📝 Appended to Central Log File : '{os.path.basename(deleted_log_file)}'")
        print(f"💾 Main Cleaned File Saved      : '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 9 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_10_remove_multiple_links()