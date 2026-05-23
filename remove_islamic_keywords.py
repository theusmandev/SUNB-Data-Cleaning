import pandas as pd
import re
import os

def step_5_remove_islamic_books():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    input_file = os.path.join(folder_path, "Smart UNB Upgradation.csv")
    output_valid_file = os.path.join(folder_path, "05_cleaned_novels_only.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_rows_log.csv")
    
    print("Step 5: Islamic keywords wali rows ko filter kiya ja raha hai...\n")
    
    # Aapki di gayi keywords ki mukammal list
    islamic_keywords = [
        "allah", "islam", "islami", "islamic", "muslim", "deen", "imaan", "akhirat", "aakhirat",  "jahannam",
        "quran", "qur'an", "quraan", "surah", "ayat", "aayat", "tafseer", "tafsir", "tafhim", "tafheem", "uloom-ul-quran", "asbab-e-nuzool",
        "hadith", "hadees", "ahadith", "sahih", "sahi", "tirmidhi", "tirmizi", "abu dawood", "abu dawud", "nasai",
        "ibn majah", "sunan", "fiqh", "shariat", "shariah", "masail", "namaz", "salah", "salat", "roza", "sawm", "zakat",
        "hajj", "umrah", "tasbeeh", "dua", "wazifa", "zikr", "zikir", "hazrat", "hadrat", "imam", "aalim", "alim", "maulana",
        "molana", "mufti",  "shaykh", "qari", "hafiz", "sahabi", "tabi", "auliya", "seerat", "seerah", "sirat",
        "khulafa", "R.A", "PBUH", "rashideen", "sahaba", "ahle-bait", "islamic history", "tareekh-e-islam", "islam ka", "deen e islam",
        "islami taleem", "islami zindagi", "islami soch", "paighambar", "rasool", "nabi", "masjid", "madarsa", "madrasa",
        "fatwa", "halal","nikah", "talaq"
    ]
    
    try:
        # 1. File read karna (Encoding fallback ke sath taake special characters par error na aaye)
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 2. Regex Pattern banana
        # re.escape() special characters (jaise ' ya .) ko safe banata hai
        # \b word boundaries define karta hai taake sirf exact words match hon
        escaped_keywords = [re.escape(kw) for kw in islamic_keywords]
        pattern = r'(?i)\b(?:' + '|'.join(escaped_keywords) + r')\b'
        
        # 3. Mask banana (Kahan kahan pattern match ho raha hai)
        # na=False ka matlab hai agar koi title khali (empty) hai to usay ignore karo
        mask = df['Titles'].astype(str).str.contains(pattern, case=False, na=False, regex=True)
        
        # 4. Data ko alag alag karna
        df_deleted = df[mask].copy()
        df_valid = df[~mask].copy()
        
        # 5. Log file ke liye column add karna
        if not df_deleted.empty:
            df_deleted['Deletion_Step'] = 'Step 5: Islamic Keyword Filter'
        
        # 6. Valid Data (Sirf Novels) Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # 7. Delete hone wala data Log mein dalna
        file_exists = os.path.isfile(deleted_log_file)
        if not df_deleted.empty:
            df_deleted.to_csv(deleted_log_file, mode='a', index=False, header=not file_exists)
        
        print("\n--- RESULTS ---")
        print(f"✅ Baki bachi saaf Rows (Novels): {len(df_valid)} -> Saved in '05_cleaned_novels_only.csv'")
        print(f"🗑️ Delete ki gayi Islamic Books: {len(df_deleted)} -> Appended to 'deleted_rows_log.csv'")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' nahi mili. Kripya apna path check karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_5_remove_islamic_books()