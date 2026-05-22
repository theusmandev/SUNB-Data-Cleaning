import pandas as pd
import os
import re

def step_9_fix_drive_urls_ultimate():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 8 ka output)
    input_file = os.path.join(folder_path, "08_cleaned_extensions_and_special_chars.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "09_fixed_drive_urls.csv")
    output_log_file = os.path.join(folder_path, "fixed_urls_log.csv")
    
    print("Step 9 [Ultimate]: Google Drive URLs ko fix aur tracking parameters ko saaf kiya ja raha hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Links'] = df['Links'].astype(str)
        
        # 2. ADVANCE URL FIXING LOGIC
        def fix_drive_url_ultimate(url):
            if 'drive.google.com' in url:
                # Rule A: Agar url mein id= hai (uc?id= ya open?id=) to ID nikalo aur standard link banao
                if 'id=' in url:
                    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
                    if match:
                        file_id = match.group(1)
                        return f"https://drive.google.com/file/d/{file_id}/view"
                
                # Rule B: Agar url pehle se file/d/ format mein hai par aakhir mein ?usp=... hai to use saaf karo
                if '/file/d/' in url and '?usp=' in url:
                    return url.split('?')[0]  # Question mark ke baad ka sab mita do
                    
            return url
        
        # 3. Apply checking and clean remaining &amp;
        df['Fixed_URL'] = df['Links'].apply(fix_drive_url_ultimate)
        df['Fixed_URL'] = df['Fixed_URL'].str.replace('&amp;', '&', regex=False)
        
        # 4. Counting for Summary
        changed_mask = df['Links'] != df['Fixed_URL']
        rows_fixed_count = changed_mask.sum()
        
        # Tracking specific usp kachra for summary
        usp_cleaned_count = df['Links'].str.contains(r'\?usp=', regex=True, na=False).sum()
        
        # 5. SEPARATE LOG FILE SAVE
        df_fixed_log = df[changed_mask].copy()
        if not df_fixed_log.empty:
            df_fixed_log.to_csv(output_log_file, index=False)
        
        # 6. ORIGINAL FINAL FILE SAVE
        df_original_final = df.copy()
        df_original_final['Links'] = df_original_final['Fixed_URL']
        df_original_final = df_original_final.drop(columns=['Fixed_URL'])
        df_original_final.to_csv(output_valid_file, index=False)
        
        # 7. TERMINAL SUMMARY DISPLAY
        print("=" * 60)
        print("📊 STEP 9: ULTIMATE DRIVE URL CLEANING REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"🔗 Malformed URLs Reconstructed (uc?id= / etc) : {rows_fixed_count - usp_cleaned_count if (rows_fixed_count - usp_cleaned_count) > 0 else rows_fixed_count}")
        print(f"🧹 Links Cleaned from Tracking (?usp=drivesdk) : {usp_cleaned_count}")
        print(f"✨ Total Rows Affected/Modified                : {rows_fixed_count}")
        print("-" * 60)
        print(f"📝 Audit Log Saved    : '{os.path.basename(output_log_file)}'")
        print(f"💾 Main Cleaned File  : '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 8 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_9_fix_drive_urls_ultimate()