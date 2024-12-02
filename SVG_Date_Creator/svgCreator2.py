from datetime import datetime, timedelta
import os
import subprocess
import shutil
import time
import sys
import errno, stat

# Function to parse user input and determine date range
def get_date_range():
    print("Entering a day (YYYYMMDD) will generate that day, entering (YYYYMM) will generate the entire month, and (YYYY) will generate the entire year")
    user_input = input("Enter a date (YYYY, YYYYMM, or YYYYMMDD): ").strip()

    try:
        if len(user_input) == 4:  # Year only (e.g., "2025")
            year = int(user_input)
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
        elif len(user_input) == 6:  # Year and month (e.g., "202501")
            year = int(user_input[:4])
            month = int(user_input[4:])
            start_date = datetime(year, month, 1)
            # Calculate the last day of the month
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        elif len(user_input) == 8:  # Year, month, and day (e.g., "20250101")
            start_date = end_date = datetime.strptime(user_input, "%Y%m%d")
        else:
            raise ValueError("Invalid date format")
        return start_date, end_date
    except ValueError as e:
        print(f"Error: {e}")
        return None, None

# Get the date range from user input
start_date, end_date = get_date_range()
if start_date is None or end_date is None:
    print("Invalid input. Please enter a valid date.")
    exit()


#print( 'bundle dir is', bundle_dir )
#print( 'sys.argv[0] is', sys.argv[0] )
#print( 'sys.executable is', sys.executable )


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable sys._MEIPASS'.
    script_dir = os.getcwd()
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
# Template for the SVG content with placeholders for day, month, and year
svg_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="240"
   height="90"
   viewBox="0 0 63.499995 23.812501"
   version="1.1"
   id="svg5"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    <g
       id="g43464"
       transform="translate(-0.04668737)">
      <g
         id="g99"
         transform="translate(0,0.02337074)">
        <text
           xml:space="preserve"
           style="font-size:31.75px;line-height:1.25;font-family:Arial;stroke-width:0.264583"
           x="-1.2710617"
           y="23.091497"
           id="text3927"><tspan
             id="tspan3925"
             style="font-size:31.75px;stroke-width:0.264583"
             x="-1.2710617"
             y="23.091497">{day}</tspan></text>
        <text
           xml:space="preserve"
           style="font-size:13.2292px;line-height:1.05;font-family:Arial;text-align:start;text-anchor:start;stroke-width:0.264583"
           x="34.982468"
           y="9.9874563"
           id="text8977"><tspan
             style="font-size:13.2292px;text-align:start;text-anchor:start;stroke-width:0.264583"
             x="34.982468"
             y="9.9874563"
             id="tspan20801">{month}</tspan></text>
        <text
           xml:space="preserve"
           style="font-size:13.2292px;line-height:1.25;font-family:Arial;stroke-width:0.264583"
           x="34.756382"
           y="23.162981"
           id="text42223"><tspan
             id="tspan42221"
             style="font-size:13.2292px;stroke-width:0.264583"
             x="34.756382"
             y="23.162981">{year}</tspan></text>
      </g>
    </g>
  </g>
</svg>'''

# Mapping of month numbers to abbreviations
month_map = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}

# Loop through the specified date range
current_date = start_date
while current_date <= end_date:
    day = current_date.strftime("%d")
    month = month_map[current_date.month]
    year = current_date.strftime("%Y")

    # Fill in the template with the current date
    svg_content = svg_template.format(day=day, month=month, year=year)

    # Save the SVG content to a file named by the date
    output_folder = os.path.join(script_dir, "temp")
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f'{year}{current_date.month:02}{day}.svg')
    with open(file_path, "w") as file:
        file.write(svg_content)

    # Move to the next day
    current_date += timedelta(days=1)

print("Step 1 Finished. SVG files for the specified date range have been generated.")
print("Step 2 In Progress. converting Text-to-path, this might take a while!")

# Define the paths for conversion
output_paths_folder = os.path.join(script_dir, "output")
os.makedirs(output_paths_folder, exist_ok=True)
inkscape_path = r"C:/Program Files/Inkscape/bin/inkscape.exe"

# Define the PowerShell command as a multi-line string
powershell_script = f'foreach ($file in Get-ChildItem -Path "{output_folder}" -Filter "*.svg") ' \
                    f'{{ & "{inkscape_path}" $file.FullName --export-text-to-path ' \
                    f'--export-filename=("path_"+$file.Name);Start-Sleep -Seconds 3}}'

# Run the PowerShell script
subprocess.run(["powershell", "-Command", powershell_script], shell=True)

print("Step 2 Finished. Text-to-path conversion completed for the generated SVG files.")

# Wait for 15 seconds before continuing
time.sleep(15)

# Loop through each file in output_folder
for filename in os.listdir(output_folder):
    if filename.endswith("_out.svg"):
        # Create the new filename by replacing "_out" with "p"
        new_filename = filename.replace("_out", "p")
        
        # Define full paths for source and destination
        source_path = os.path.join(output_folder, filename)
        destination_path = os.path.join(output_paths_folder, new_filename)
        
        # Move and rename the file
        shutil.move(source_path, destination_path)

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

shutil.rmtree(output_folder, ignore_errors=False, onerror=handleRemoveReadonly) 

print("Step 3 Finished. Path files have been renamed and moved to /output.\n All done!")
input("Press enter to quit program")