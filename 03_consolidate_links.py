import pandas as pd
import numpy as np
import os

def step_3_consolidate_links():
    # Folder path
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 2 se aane wali saaf file)
    input_file = os.path.join(folder_path, "02_cleaned_novels_data.csv")
    
    # Output file (Jisme sirf 2 columns honge)
    output_file = os.path.join(folder_path, "03_consolidated_links_data.csv")
    
    print("Step 3: Links ko consolidate (merge) kiya ja raha hai...\n")
    
    try:
        # 1. Read input CSV
        df = pd.read_csv(input_file)
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # Columns ko identify karna
        cols = df.columns
        title_col = cols[0]
        gdrive_col = cols[1]
        mediafire_col = cols[2]
        
        # 2. Safety Check: Agar kisi wajah se khali spaces reh gaye hon to unhe NaN (empty) bana dein
        df[gdrive_col] = df[gdrive_col].replace(r'^\s*$', np.nan, regex=True)
        df[mediafire_col] = df[mediafire_col].replace(r'^\s*$', np.nan, regex=True)
        
        # 3. Main Logic: GDrive link ko prefer karo, agar wo nahi hai to Mediafire link le lo
        # fillna() ka matlab hai: Agar pehli value (GDrive) khali hai, to dusri (Mediafire) se bhar do
        df['Final_Link'] = df[gdrive_col].fillna(df[mediafire_col])
        
        # 4. Sirf kaam ke 2 columns rakhna (Title aur Final_Link)
        df_final = df[[title_col, 'Final_Link']].copy()
        
        # 5. Columns ka naam Supabase database ke hisab se set karna
        df_final.rename(columns={title_col: 'Titles', 'Final_Link': 'Links'}, inplace=True)
        
        # 6. File ko save karna
        df_final.to_csv(output_file, index=False)
        
        print("\n--- RESULTS ---")
        print("✅ Dono links columns ko mila kar ek single 'Links' column bana diya gaya hai.")
        print(f"✅ Google Drive ko tarjeeh di gayi hai.")
        print(f"✅ Data '{os.path.basename(output_file)}' mein save ho gaya hai.")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya pehle Step 2 ki script run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_3_consolidate_links()