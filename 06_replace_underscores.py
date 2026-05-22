import pandas as pd
import os

def step_6_replace_underscores():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Jo aapne batayi - Step 5 ka output)
    input_file = os.path.join(folder_path, "05_cleaned_titles_data.csv") 
    
    # Output file (Step 6 ka final result)
    output_valid_file = os.path.join(folder_path, "06_cleaned_titles_no_underscores.csv")
    
    print("Step 6: '05_cleaned_titles_data.csv' se underscores (_) ko spaces ( ) mein badla ja raha hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 2. Underscores ko spaces se replace karna
        # str.replace() se exact '_' ko replace karenge
        df['Titles'] = df['Titles'].astype(str).str.replace('_', ' ', regex=False)
        
        # Extra spaces clean karna (Agar '_' hatane se double spaces ban gaye hon to single kar dena)
        df['Titles'] = df['Titles'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        # 3. Data save karna
        df.to_csv(output_valid_file, index=False)
        
        print("\n--- RESULTS ---")
        print("✅ Underscores kamyabi se replace ho gaye hain.")
        print(f"✅ Nayi file '{os.path.basename(output_valid_file)}' ban gayi hai.")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya pehle Step 5 ki script chala kar file generate karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_6_replace_underscores()