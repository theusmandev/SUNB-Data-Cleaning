import pandas as pd
import re
import os

def step_14_remove_islamic_keywords():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 13 ka output)
    input_file = os.path.join(folder_path, "13_cleaned_novel_words.csv")
    
    # Output files
    output_valid_file = os.path.join(folder_path, "14_cleaned_no_islamic_keywords.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 14: Islamic keywords wali rows ko filter kiya ja raha hai...\n")
    
    # Aapki di gayi exact keywords ki list
    islamic_keywords = [
        "akhirat", "aakhirat", "jahannam",
        "quran", "qur'an", "quraan", "surah", "ayat","ayaat", "aayat", "tafseer", "tafsir", "tafhim", "tafheem", "uloom-ul-quran", "asbab-e-nuzool",
        "hadith", "hadees", "ahadith", "sahih", "tirmidhi", "tirmizi", "abu dawood", "abu dawud", "nasai",
        "ibn majah", "sunan", "fiqh", "shariat", "shariah", "masail", "namaz", "salah", "salat", "roza", "sawm", "zakat",
        "hajj", "umrah", "tasbeeh","wazifa", "zikr", "zikir", "hazrat", "hadrat", "imam", "aalim", "alim", "maulana",
      "qari",  "sahabi", "tabi", "auliya", "seerat", "seerah",
        "khulafa", "R.A", "PBUH", "rashideen", "sahaba", "ahle-bait",  "tareekh-e-islam", "islam ka", "deen e islam",
        "islami taleem", "islami zindagi", "islami soch", "paighambar", "rasool", "nabi", "masjid", "madarsa", "madrasa",
        "fatwa", "halal", "nikah", "talaq"
    ]
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        print(f"File read ho gayi. Total rows: {total_rows}")
        
        # 2. Regex Pattern banana
        # re.escape() special characters ko safe banata hai
        # \b word boundaries define karta hai taake sirf exact words match hon
        escaped_keywords = [re.escape(kw) for kw in islamic_keywords]
        pattern = r'(?i)\b(?:' + '|'.join(escaped_keywords) + r')\b'
        
        # 3. Mask banana (Kahan kahan pattern match ho raha hai)
        # na=False ka matlab hai agar koi title khali hai to usay ignore karo
        mask = df['Titles'].astype(str).str.contains(pattern, case=False, na=False, regex=True)
        
        # 4. Data ko alag alag karna
        df_deleted = df[mask].copy()
        df_valid = df[~mask].copy()
        
        # 5. Log file ke liye tracking column add karna
        if not df_deleted.empty:
            df_deleted['Deletion_Step'] = 'Step 14: Islamic Keyword Filter'
        
        # 6. Valid Data Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # 7. Delete hone wala data Central Log mein dalna
        if not df_deleted.empty:
            file_exists = os.path.isfile(deleted_log_file)
            df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        # 8. TERMINAL SUMMARY DISPLAY
        print("=" * 60)
        print("📊 STEP 14: ISLAMIC KEYWORDS FILTERING REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"🗑️ Islamic Books Deleted                       : {len(df_deleted)}")
        print(f"✅ Safe Novel Rows Remaining                   : {len(df_valid)}")
        print("-" * 60)
        print(f"📝 Appended to Central Log File : '{os.path.basename(deleted_log_file)}'")
        print(f"💾 Main Cleaned File Saved      : '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' nahi mili. Kripya pehle Step 13 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_14_remove_islamic_keywords()