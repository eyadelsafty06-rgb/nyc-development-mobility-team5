NYC Project: Simple Steps

Already uploaded to GitHub? Check steps 9–10, then continue from step 11.

GOOGLE COLAB

Open https://colab.research.google.com. Choose File → Upload notebook and select NYC_Team5_Colab.ipynb. Then choose File → Save a copy in Drive and click Connect.

Run the setup cell, then the project-files cell. Click the triangle beside each cell and wait for it to finish. The second cell creates the code and documents for you.

In the snapshot cell, use IMPORT_SNAPSHOT = True. Run it and upload NYC_Team5_Project.zip without extracting it. Wait for “Snapshot imported.” Run the data-loading cell with REFRESH = False.

Run the remaining cells in order. Read the cleaning results and all ten charts. With the supplied data, look for “Calendar rows: 180 | Paired rows: 180” and “8 passed.” Test Generate Report and the filters. If a cell shows an error, fix it before continuing. Press Ctrl+S to save.

SAVE YOUR WORK

Run the final export cell to download NYC_Team5_Export.zip.

Separately choose File → Download → Download .ipynb. This saves the notebook with your results.

In Downloads, right-click the export ZIP → Extract All. Open the nyc_team5 folder and copy your downloaded notebook into it as NYC_Team5_Colab.ipynb. Check that data/processed contains housing_monthly.csv, transport_monthly.csv, integrated.csv and provenance.json.

GITHUB

If needed, create a repository at https://github.com/new named nyc-development-mobility-team5. The commands below assume a public repository. Leave “Add README” unchecked because the project already has one.

Upload the files and folders inside nyc_team5, including your saved notebook. Click Commit changes. The main repository page should show app.py, requirements.txt, README.md, the notebook, assets, data and reports.

Open README.md and use the pencil icon to add your repository link. Update TEAM.md with work each person has actually completed. Save by clicking Commit changes. Add teammates as collaborators if they need to edit.

PYTHONANYWHERE

Sign in at https://www.pythonanywhere.com using eyadelsafty. Open Consoles → Bash. Run each line below separately. If your GitHub link differs, change it in the clone command.

cd ~
git clone --depth 1 https://github.com/eyadelsafty06-rgb/nyc-development-mobility-team5.git nyc_team5_v2
cd ~/nyc_team5_v2
ls data/processed

You should see the four files from step 7. If nyc_team5_v2 already exists, check what is inside before continuing.

In the same Bash console, run these lines one at a time:

python3.12 -m venv --system-site-packages ~/nyc-team5-env
source ~/nyc-team5-env/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
python -c "from app import LOAD_ERROR; assert not LOAD_ERROR, LOAD_ERROR; print('Dashboard ready')"

Wait for “Dashboard ready.” Install requirements.txt here; the analysis packages run in Colab.

Open Web → Add a new web app → Manual configuration → Python 3.12. Use the free address. If you already have a web app, open its settings and save its old paths before changing them. Its Python version must also be 3.12.

Enter these paths and save each field:

Source code and Working directory:
/home/eyadelsafty/nyc_team5_v2

Virtualenv:
/home/eyadelsafty/nyc-team5-env

Open the WSGI configuration file. Keep a copy of its old text, then replace it with:

import os
import sys

project_path = '/home/eyadelsafty/nyc_team5_v2'
if project_path not in sys.path:
    sys.path.insert(0, project_path)
os.chdir(project_path)
from app import server as application

Save, return to Web and click Reload. Open the website link shown there. If it fails, open Web → Error log and copy the latest error for help. Check the expiry date and renew the free app through grading.

FINAL CHECKS AND SUBMISSION

On the live website, click Generate Report and check all ten charts. Test borough, year and category filters, then search “Brooklyn 2022 heavy traffic.” Check that the charts and Story update. Try it on your phone too. Record your results in reports/VALIDATION.md.

Add the working website link and repository link to README.md and the notebook’s final text cell. Save the notebook, download it again and replace the GitHub copy. Commit the changes.

Check REQUIREMENTS_CHECKLIST.md and confirm the team details:

Eyad Elsafty — 16003613 — Q1–Q2
Jana Hazem — 14003384 — Q3–Q4
Omar Hisham — 16008286 — Q5–Q6
Anas Mohamed — 13005403 — Q7–Q8
Yassin Ahmed — 16002450 — Q9–Q10

