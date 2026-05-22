import pandas as pd
import os

def remove_digest_library_rows():
    # Folder path
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Yahan aap jis file se delete karna chahte hain uska naam likhein)
    input_file = os.path.join(folder_path, "Smart UNB Upgradation.csv")
    
    # Output files (Naye naam taake purana data mix na ho)
    output_valid_file = os.path.join(folder_path, "without_digest_library.csv")
    deleted_log_file = os.path.join(folder_path, "deleted_digest_library_log.csv")
    
    print("Process Start: 'Digest Library' wale titles dhoonde ja rahe hain...\n")
    
    try:
        # File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 'Digest Library' dhoondne ke liye mask banana (case=False matlab chote bade lafz sab pakdega)
        mask_to_delete = df['Titles'].astype(str).str.contains('Digest Library', case=False, na=False)
        
        # Data ko Split Karna
        df_deleted = df[mask_to_delete].copy()
        df_valid = df[~mask_to_delete].copy()
        
        # Valid Data Save Karna
        df_valid.to_csv(output_valid_file, index=False)
        
        # Delete hone wala data alag log mein save karna
        if not df_deleted.empty:
            df_deleted.to_csv(deleted_log_file, index=False)
        
        print("\n--- RESULTS ---")
        print(f"✅ Theek Rows (Bina Digest Library): {len(df_valid)} -> Saved in 'without_digest_library.csv'")
        print(f"🗑️ Delete kiye gaye Titles: {len(df_deleted)} -> Saved in 'deleted_digest_library_log.csv'")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya file aur path ka naam check karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    remove_digest_library_rows()