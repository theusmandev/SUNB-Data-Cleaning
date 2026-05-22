import pandas as pd
import os

def step_7_clean_hyphens_and_capitalize():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 6 ka final output)
    input_file = os.path.join(folder_path, "06_cleaned_titles_no_underscores.csv") 
    
    # Output file (Step 7 ka final result)
    output_valid_file = os.path.join(folder_path, "07_cleaned_titles_titlecase.csv")
    
    print("Step 7: Hyphens (-) ko spaces se badla ja raha hai aur Capitalization apply ho rahi hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        print(f"File read ho gayi. Total rows: {len(df)}")
        
        # 2. Asal Kaam 1: Hyphens (-) ko spaces se replace karna
        df['Titles'] = df['Titles'].astype(str).str.replace('-', ' ', regex=False)
        
        # Extra spaces clean karna (agar '-' hatane se zyada spaces ban gaye hon)
        df['Titles'] = df['Titles'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        # 3. Asal Kaam 2: Har word ka first letter Capital karna (Title Case)
        # .str.title() function automatic har lafz ka pehla character bara kar deta hai
        df['Titles'] = df['Titles'].str.title()
        
        # 4. Data save karna
        df.to_csv(output_valid_file, index=False)
        
        print("\n--- RESULTS ---")
        print("✅ Hyphens kamyabi se replace ho gaye hain.")
        print("✅ Har word ka first letter capital ho gaya hai (e.g., 'Ghazi Ilm Deen Shaheed By Zafar Iqbal Nagina').")
        print(f"✅ Final saaf data '{os.path.basename(output_valid_file)}' mein save ho gaya hai.")
        print("===============")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Kripya pehle Step 6 ki script chala kar file generate karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_7_clean_hyphens_and_capitalize()