import pandas as pd
import os
import re

def step_11_clean_titles_advanced():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 10 ka output)
    input_file = os.path.join(folder_path, "10_cleaned_single_links.csv") 
    
    # Output files
    output_valid_file = os.path.join(folder_path, "11_cleaned_final_titles.csv")
    output_log_file = os.path.join(folder_path, "title_cleaning_log.csv")
    
    print("Step 11: Titles ke shuru ki spaces, aakhir ke junk words, aur dots (.) saaf kiye ja rahe hain...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        df['Titles'] = df['Titles'].astype(str)
        
        # 2. TITLE CLEANING FUNCTION
        def fully_clean_title(title):
            # Step 1: Shuru (leading) aur aakhir (trailing) ki extra spaces hatana
            cleaned = title.strip()
            
            # Step 2: Title ke aakhir se "pdf", "download", "free", "znz", "read online" aur unke combinations ko hatana
            # (?i) = case insensitive
            pattern = r'(?i)(?:[\s\.\-\_]*(?:pdf|download|free|znz|read\s+online))+[\s\.\-\_]*$'
            cleaned = re.sub(pattern, '', cleaned)
            
            # Step 3: Aakhir mein bache hue extra dots (.) ko hatana
            cleaned = re.sub(r'[\.\s]+$', '', cleaned)
            
            # Step 4: Ek aakhri safety strip taake koi bhi hidden space shuru ya aakhir mein na bache
            return cleaned.strip()

        # 3. Naya column 'Cleaned_Title' banana
        df['Cleaned_Title'] = df['Titles'].apply(fully_clean_title)
        
        # 4. Filter karna ke kitni rows actually change hui hain (Auditing ke liye)
        changed_mask = df['Titles'] != df['Cleaned_Title']
        rows_fixed_count = changed_mask.sum()
        
        # 5. SEPARATE LOG FILE TAYYAR KARNA
        df_log = df[changed_mask].copy()
        if not df_log.empty:
            # Sirf 3 columns log file mein save karenge taake check karne mein asani ho
            df_log = df_log[['Titles', 'Links', 'Cleaned_Title']]
            df_log.to_csv(output_log_file, index=False)
        
        # 6. ORIGINAL FINAL FILE TAYYAR KARNA
        df_final = df.copy()
        df_final['Titles'] = df_final['Cleaned_Title']  # Purane title ko naye saaf title se replace karna
        df_final = df_final.drop(columns=['Cleaned_Title'])  # Extra column drop karna
        df_final.to_csv(output_valid_file, index=False)
        
        # 7. TERMINAL SUMMARY DISPLAY
        print("=" * 65)
        print("📊 STEP 11: FULL TITLE CLEANING SUMMARY REPORT")
        print("=" * 65)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"✨ Titles Cleaned (Spaces, Dots & Junk Words)  : {rows_fixed_count}")
        print("-" * 65)
        print(f"📝 Audit Log Saved (For your verification)     :")
        print(f"   '{os.path.basename(output_log_file)}'")
        print(f"💾 Main Cleaned File Saved                     :")
        print(f"   '{os.path.basename(output_valid_file)}'")
        print("=" * 65)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 10 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_11_clean_titles_advanced()