import pandas as pd
import numpy as np

def clean_invalid_links():
    input_file = r"E:\Smart Urdu Novel Bank\merged_novels_data.csv"
    output_file = r"E:\Smart Urdu Novel Bank\merged_novels_data_2.csv"
    
    print("Cleaning process start ho raha hai...\n")
    
    try:
        # 1. CSV file ko read karna (Encoding error ko handle karte hue)
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            print("Warning: UTF-8 encoding fail ho gayi. Alternative encoding (cp1252/latin1) try kar raha hun...")
            try:
                df = pd.read_csv(input_file, encoding='cp1252')
            except UnicodeDecodeError:
                df = pd.read_csv(input_file, encoding='latin1')

        print(f"Original file mein total rows: {len(df)}")
        
        # 2. Columns ko identify karna
        cols = df.columns
        title_col = cols[0]
        gdrive_col = cols[1]
        mediafire_col = cols[2]
        
        # 3. "No Google Drive Link" aur "No Mediafire Link" ko empty (NaN) bananana
        df[gdrive_col] = df[gdrive_col].replace(r'(?i).*No Google Drive Link.*', np.nan, regex=True)
        df[mediafire_col] = df[mediafire_col].replace(r'(?i).*No Mediafire Link.*', np.nan, regex=True)
        
        # Agar kisi cell mein sirf white space (khali jagah) hai, usko bhi NaN kar dein
        df[gdrive_col] = df[gdrive_col].replace(r'^\s*$', np.nan, regex=True)
        df[mediafire_col] = df[mediafire_col].replace(r'^\s*$', np.nan, regex=True)
        
        # 4. Un rows ko delete karna jahan DONO columns (GDrive aur Mediafire) khali (NaN) hon
        df_cleaned = df.dropna(subset=[gdrive_col, mediafire_col], how='all')
        
        # 5. Result ko nayi CSV file mein save karna
        df_cleaned.to_csv(output_file, index=False)
        
        deleted_rows = len(df) - len(df_cleaned)
        print(f"\nZabardast! {deleted_rows} useless rows delete kar di gayi hain.")
        print(f"Cleaned file mein ab {len(df_cleaned)} rows bachi hain.")
        print(f"Data '{output_file}' ke naam se save ho gaya hai.")
        
    except FileNotFoundError:
        print(f"Error: '{input_file}' nahi mili. Kripya check karein ki path theek hai.")
    except Exception as e:
        print(f"Error aagaya: {e}")

if __name__ == "__main__":
    clean_invalid_links()