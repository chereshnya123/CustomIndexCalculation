import pandas as pd
import pathlib

input_file = 'moex_statuses.xlsx'
output_dir = pathlib.Path('/home/chereshnya/Me/Finance/MOEX_with_no_companies/data/moex_statuses/')
output_dir.mkdir(exist_ok=True)

excel_file = pd.ExcelFile(input_file)

for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in sheet_name)
    output_path = output_dir / f"{safe_name}.csv"
    df.to_csv(output_path, index=False, encoding='utf-8')

print(f"All {len(excel_file.sheet_names)} sheets are saved in {output_dir}")