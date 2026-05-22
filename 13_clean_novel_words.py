import pandas as pd
import os
import re

def step_13_clean_novel_words():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 12 ka output)
    input_file = os.path.join(folder_path, "12_cleaned_long_titles.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "13_cleaned_novel_words.csv")
    output_log_file = os.path.join(folder_path, "title_cleaning_log.csv")
    
    print("Step 13: Titles ke shuru aur aakhir se 'Novel', 'Urdu Novel', aur 'Download' saaf kiye ja rahe hain...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Titles'] = df['Titles'].astype(str)
        
        # 2. TITLE CLEANING FUNCTION (Start aur End ke liye)
        def clean_novel_keywords(title):
            # Regex patterns (Case insensitive)
            # Shuru mein aane wale words:
            pattern_start = r'(?i)^[\s\.\-\_]*(urdu\s+novel|novel|download)[\s\.\-\_]*'
            # Aakhir mein aane wale words:
            pattern_end = r'(?i)[\s\.\-\_]*(urdu\s+novel|novel|download)[\s\.\-\_]*$'
            
            cleaned = title.strip()
            
            # Jab tak shuru ya aakhir mein ye lafz milte rahen, inko saaf karte raho
            # (Ye loop isliye hai taake "Download Novel" jaisi double mistakes bhi theek ho jayen)
            prev_cleaned = ""
            while cleaned != prev_cleaned:
                prev_cleaned = cleaned
                cleaned = re.sub(pattern_start, '', cleaned)
                cleaned = re.sub(pattern_end, '', cleaned)
            
            return cleaned.strip()

        # 3. Naya column 'Cleaned_Title' banana
        df['Cleaned_Title'] = df['Titles'].apply(clean_novel_keywords)
        
        # 4. Filter karna ke kitni rows exactly change hui hain
        changed_mask = df['Titles'] != df['Cleaned_Title']
        rows_fixed_count = changed_mask.sum()
        
        # 5. SEPARATE LOG FILE MEIN APPEND KARNA
        df_log = df[changed_mask].copy()
        if not df_log.empty:
            df_log = df_log[['Titles', 'Links', 'Cleaned_Title']]
            
            # Agar log file pehle se majood hai to sirf naya data append karo bina header ke
            file_exists = os.path.isfile(output_log_file)
            df_log.to_csv(output_log_file, mode='a', index=False, header=not file_exists)
        
        # 6. ORIGINAL FINAL FILE TAYYAR KARNA
        df_final = df.copy()
        df_final['Titles'] = df_final['Cleaned_Title']  # Purane title ko replace karna
        df_final = df_final.drop(columns=['Cleaned_Title'])  # Cleaned_Title column drop karna
        df_final.to_csv(output_valid_file, index=False)
        
        # 7. TERMINAL SUMMARY DISPLAY
        print("=" * 65)
        print("📊 STEP 13: NOVEL/DOWNLOAD KEYWORDS CLEANING REPORT")
        print("=" * 65)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"✨ Titles Cleaned (Start/End Keywords Removed) : {rows_fixed_count}")
        print("-" * 65)
        print(f"📝 Appended to Audit Log                       :")
        print(f"   '{os.path.basename(output_log_file)}'")
        print(f"💾 Main Cleaned File Saved                     :")
        print(f"   '{os.path.basename(output_valid_file)}'")
        print("=" * 65)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 12 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_13_clean_novel_words()