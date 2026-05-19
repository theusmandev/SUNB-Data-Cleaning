import pandas as pd
import glob
import os

def merge_excel_files():
    # --- YAHAN APNA EXACT FOLDER PATH DAALEN ---
    # 'r' lagana zaroori hai taake windows ke slashes (\) ka error na aaye
    folder_path = r"E:\Smart Urdu Novel Bank\same columns"
    
    print(f"'{folder_path}' se files merge ho rahi hain...\n")
    
    # Folder path ke sath .xlsx files search karna
    search_pattern = os.path.join(folder_path, "*.xlsx")
    excel_files = glob.glob(search_pattern)
    
    if len(excel_files) == 0:
        print(f"Koi Excel file nahi mili. Kripya check karein ki folder path sahi hai: {folder_path}")
        return

    print(f"Total {len(excel_files)} files mili hain...\n")
    
    all_dataframes = []
    
    # Har file ko read karke list mein add karna
    for file in excel_files:
        try:
            # Excel file ko read karna
            df = pd.read_excel(file)
            all_dataframes.append(df)
            
            # Sirf file ka naam print karwayenge, poora lamba path nahi
            file_name = os.path.basename(file)
            print(f"Success: '{file_name}' read ho gayi.")
        except Exception as e:
            file_name = os.path.basename(file)
            print(f"Error: '{file_name}' ko read karne mein masla aya - {e}")
            
    # Sabhi dataframes ko ek single dataframe mein combine (merge) karna
    print("\nSabhi files ko ek master table mein jora ja raha hai...")
    master_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Merged data ko usi hardcoded folder mein nayi CSV file ke taur par save karna
    output_filename = os.path.join(folder_path, "merged_novels_data.csv")
    master_df.to_csv(output_filename, index=False)
    
    print(f"\nZabardast! Saari files merge ho kar iss path par save ho gayi hain:")
    print(output_filename)
    print(f"Total Rows (Records) in Master File: {len(master_df)}")

if __name__ == "__main__":
    merge_excel_files()