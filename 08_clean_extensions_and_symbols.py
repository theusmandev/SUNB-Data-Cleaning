import pandas as pd
import os
import re

def step_8_clean_extensions_and_symbols():
    # Folder path aur files
    folder_path = r"E:\Smart Urdu Novel Bank"
    
    # Input file (Step 7 ka final output)
    input_file = os.path.join(folder_path, "07_cleaned_titles_titlecase.csv") 
    
    # Output file (Step 8 ka result)
    output_valid_file = os.path.join(folder_path, "08_cleaned_extensions_and_special_chars.csv")
    
    print("Step 8: File extensions aur Special Characters ki safai shuru ho rahi hai...\n")
    
    try:
        # 1. File read karna
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='cp1252')
            
        total_rows = len(df)
        
        # Titles ko string mein convert karna safe execution ke liye
        df['Titles'] = df['Titles'].astype(str)
        
        # 2. FILE EXTENSIONS SUMMARY & CLEANING
        # Pattern jo end mein .pdf, .zip, .rar wagaira check karega
        ext_pattern = r'\.(pdf|zip|rar|epub|mobi|txt|docx|html)$'
        
        # Pehle count check karna summary ke liye
        has_extension = df['Titles'].str.contains(ext_pattern, case=False, regex=True, na=False)
        rows_with_extensions = has_extension.sum()
        
        # Extensions ko mita dena
        df['Titles'] = df['Titles'].str.replace(ext_pattern, '', case=False, regex=True)
        
        
        # 3. SPECIAL CHARACTERS & BRACKETS SUMMARY & CLEANING
        # Pattern jo brackets aur baki symbols ko target karega
        spec_pattern = r'[\[\]\(\)\{\}@#\$%\^&\*\+=\\|<>\/\?]'
        
        # Pehle count check karna summary ke liye
        has_special_chars = df['Titles'].str.contains(spec_pattern, regex=True, na=False)
        rows_with_special_chars = has_special_chars.sum()
        
        # Special characters ko mita kar khali jagah (space) lagana
        df['Titles'] = df['Titles'].str.replace(spec_pattern, ' ', regex=True)
        
        
        # 4. FINAL POST-CLEANING POLISH
        # Double ya triple spaces ko single space banana aur sides se strip karna
        df['Titles'] = df['Titles'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        # Ek baar phir titlecase ensure karna agar symbols hatne se spacing tabdeel hui ho
        df['Titles'] = df['Titles'].str.title()
        
        
        # 5. Data save karna
        df.to_csv(output_valid_file, index=False)
        
        
        # 6. TERMINAL SUMMARY DISPLAY (Aapki requirement ke mutabiq)
        print("=" * 60)
        print("📊 STEP 8: DATA CLEANING SUMMARY REPORT")
        print("=" * 60)
        print(f"📁 Total Rows Processed                        : {total_rows}")
        print(f"📄 Rows containing File Extensions (.pdf/.zip) : {rows_with_extensions}")
        print(f"✨ Rows containing Special Characters/Brackets : {rows_with_special_chars}")
        print("-" * 60)
        print(f"✅ Cleaned data successfully saved in:")
        print(f"   '{os.path.basename(output_valid_file)}'")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle Step 7 run karein.")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    step_8_clean_extensions_and_symbols()