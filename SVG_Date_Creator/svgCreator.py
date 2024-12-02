from datetime import datetime, timedelta
import os
import subprocess

script_dir = os.path.abspath(os.path.dirname(__file__))

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

# Starting date for 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
delta = timedelta(days=1)

# Loop through all dates in 2025
current_date = start_date
while current_date <= end_date:
    day = current_date.strftime("%d")  # Day with leading zero
    month = month_map[current_date.month]
    year = current_date.strftime("%Y")

    # Fill in the template with the current date
    svg_content = svg_template.format(day=day, month=month, year=year)

    # Save the SVG content to a file named by the date
   # with open(os.path.join(script_dir, f'output_data\\{output_file}'), 'w') as f:

    #filename =  
    with open(os.path.join(script_dir, f'output\\date_{year}{current_date.month}{day}.svg'), "w") as file:
        file.write(svg_content)

    # Move to the next day
    current_date += delta

print("SVG files for all days in 2025 have been generated.")


# Define the path to the output folder
output_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "output\\").replace("\\", "/")

output_paths_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "output_paths\\").replace("\\", "/")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)
# Ensure output paths folder exists
os.makedirs(output_paths_folder, exist_ok=True)

# Path to the Inkscape executable
inkscape_path = r"C:/Program Files/Inkscape/bin/inkscape.exe"

# Define the PowerShell command as a multi-line string with a 5-second delay between files
# PowerShell command as a single line to avoid formatting issues
powershell_script = f'foreach ($file in Get-ChildItem -Path "{output_folder}" -Filter "date_2025*.svg") ' \
                    f'{{ & "{inkscape_path}" $file.FullName --export-text-to-path ' \
                    f'--export-filename=("{output_paths_folder}path_" + $file.Name)}}'

#current
# foreach ($file in Get-ChildItem -Path "c:/Users/dilvan/OneDrive - TUM/Desktop/DateCreator/output/" -Filter "date_2025_*.svg") 
# { & "C:/Program Files/Inkscape/bin/inkscape.exe" $file.FullName --export-text-to-path --export-filename=("path_" + $file.Name)}

#foreach ($file in Get-ChildItem -Filter "date_2025_*.svg") 
#{ & "C:/Program Files/Inkscape/bin/inkscape.exe" $file.FullName --export-text-to-path --export-filename=("path_" + $file.Name)}


# working
# foreach ($file in Get-ChildItem -Filter "date_2025*.svg") {
#& "C:/Program Files/Inkscape/bin/inkscape.exe" $file.FullName --export-text-to-path --export-filename=("path_" + $file.Name)}

print(powershell_script)
# Run the PowerShell script from Python
subprocess.run(["powershell", "-Command", powershell_script], shell=True)

print("Text-to-path conversion completed for all SVG files in the output folder.")