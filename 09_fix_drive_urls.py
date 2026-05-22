import pandas as pd
import os
import re

def step_9_fix_drive_urls_with_log():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 8 ka output)
    input_file = os.path.join(folder_path, "08_cleaned_extensions_and_special_chars.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "09_fixed_drive_urls.csv")
    output_log_file = os.path.join(folder_path, "fixed_urls_log.csv")
    
    print("Step 9: Google Drive URLs ko fix kiya ja raha hai aur log file tayyar ki ja rahi hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Links'] = df['Links'].astype(str)
        
        # 2. URL Fix karne wala function
        def fix_drive_url(url):
            if 'drive.google.com' in url and 'id=' in url:
                match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
                if match:
                    file_id = match.group(1)
                    return f"https://drive.google.com/file/d/{file_id}/view"
            return url
        
        # 3. Naya column 'Fixed_URL' banana aur usme safe links dalna
        df['Fixed_URL'] = df['Links'].apply(fix_drive_url)
        
        # Extra safety check for remaining &amp;
        df['Fixed_URL'] = df['Fixed_URL'].str.replace('&amp;', '&', regex=False)
        
        # 4. Filter karna ke sach mein kitni rows fix hui hain (Auditing)
        # Agar original link aur fixed link alag hain, iska matlab row fix hui hai
        changed_mask = df['Links'] != df['Fixed_URL']
        rows_fixed_count = changed_mask.sum()
        
        # 5. SEPARATE LOG FILE TAYYAR KARNA (Aapki requirement ke mutabiq)
        df_fixed_log = df[changed_mask].copy()
        if not df_fixed_log.empty:
            # Is log file mein Columns ka sequence hoga: Titles, Links (Original), Fixed_URL
            df_fixed_log.to_csv(output_log_file, index=False)
        
        # 6. ORIGINAL FINAL FILE TAYYAR KARNA
        # Original file mein 'Links' column ko 'Fixed_URL' se replace kar dena hai
        df_original_final = df.copy()
        df_original_final['Links'] = df_original_final['Fixed_URL']
        df_original_final = df_original_final.drop(columns=['Fixed_URL']) # Extra column drop kar diya
        df_original_final.to_csv(output_valid_file, index=False)
        
        # 7. TERMINAL SUMMARY DISPLAY
        print("=" * 60)
        print("📊 STEP 9: DRIVE URL FIX & LOG SUMMARY REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"🔧 Total Malformed/Broken URLs Fixed           : {rows_fixed_count}")
        print("-" * 60)
        print(f"📝 Separate Log File Saved (With Old & New URL):")
        print(f"   '{os.path.basename(output_log_file)}' (Rows: {rows_fixed_count})")
        print(f"💾 Main Cleaned File Saved (URLs Replaced)     :")
        print(f"   '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 8 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_9_fix_drive_urls_with_log()