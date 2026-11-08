# Start here — five-member project

This is the rebuilt version for Eyad, Jana, Omar, Anas and Yassin. It has ten
research questions, ten research charts, complete documentation and a Colab
notebook that creates its own source files.

The code and local verification are finished. Your remaining work is to run
and review it in your Google account, record actual team contributions, upload
the final version to GitHub, deploy it, test the live website, and submit.
The generated work has not been deployed or emailed on your behalf.

## A. Run the notebook in Google Colab

1. Download `NYC_Team5_Colab.ipynb` from the chat. Also keep the supplied
   `NYC_Team5_Project.zip` for the snapshot import in step 9. Do not overwrite your old work.
2. Open https://colab.research.google.com/ and sign in.
3. Choose File → Upload notebook → Browse. Select `NYC_Team5_Colab.ipynb`.
4. Choose File → Save a copy in Drive. Work in that copy.
5. Click Connect. Use a CPU runtime. No local Python installation is needed.
6. Read the opening instructions. All five names and IDs are already filled in.
7. Run the setup code cell by clicking its triangle. Wait until it finishes.
   It installs packages into Colab. If Colab explicitly asks to restart the
   session, restart, reconnect, and run the setup again before continuing.
8. Run the project-files cell. It creates README.md, PROMPTS.md, source code,
   CSS, deployment instructions and the team files. You should see a list of
   files and a success message. Do not replace this cell with an empty
   `%%writefile` command.
9. For your first run, use the supplied snapshot. In the optional import cell,
   set `IMPORT_SNAPSHOT = True`, click its triangle, then choose the downloaded
   `NYC_Team5_Project.zip`. Select the ZIP itself without extracting it. Wait for
   “Snapshot imported.” To download current source records instead, leave the
   setting at `False`; results may then differ.
10. Run the data-loading cell with `REFRESH = False`. It reuses a verified cache
    if present; otherwise it downloads all records in the 2022–2024 window.
    Wait for both downloads. Do not run later cells before this finishes.
11. Check the displayed table: two datasets, IDs, source/extract row and column
    counts, download dates, geographic fields and event dates. Counts may differ
    after a refresh. Do not copy old results over new results.
12. Run the raw EDA cells. Read the missing-value tables, raw category values,
    duplicates and plots. All raw fields load as strings initially to preserve IDs.
13. Run the cleaning cell. Read the audit: which rows were removed and which
    values became missing? Read the written justifications directly above it.
14. Run the aggregation/integration cell. With the supplied snapshot, expect
    “Calendar rows: 180 | Paired rows: 180”. These are five boroughs × 36 months.
    The cell checks that the join did not multiply the counts.
15. Run the sensitivity cell. It compares different counting and delay rules.
16. Run the research-chart setup, then each Q1–Q10 chart cell. Each has a named
    owner, question, computed finding, limitation and practical interpretation.
    Your team should review the findings and add any corrections in text cells.
17. Run the findings and validation cells. The delivered version passed eight
    automated tests. Look for “8 passed”; a package warning alone is not a failed
    test. Record the output of your own run too.
18. Run the dashboard cell. Click Generate Report with all default selections.
    Then test borough, year, each category and `Brooklyn 2022 heavy traffic`.
    There should be ten charts. Narrow filters can legitimately leave too few
    observations for yearly or lag comparisons.
19. If you see a red traceback, stop at that cell and copy the complete error.
    Fix it before exporting. API timeouts are not proof the datasets are missing;
    use the supplied snapshot import option or retry later.

The Colab website preview ends when the runtime disconnects. Permanent hosting
is a separate step below. Save your notebook in Drive with Ctrl+S.

## B. Save the finished work

20. Run the final export cell. It checks that the required files exist and creates
    `NYC_Team5_Export.zip`. In Colab it starts a browser download. Allow it.
21. Separately choose File → Download → Download .ipynb. This saves your executed
    notebook and any edits. Colab's live notebook is not automatically included
    in the runtime ZIP.
22. On Windows, open Downloads, right-click `NYC_Team5_Export.zip` → Extract All.
23. Open its `nyc_team5` folder. You should see app.py, requirements.txt, README.md,
    PROMPTS.md, TEAM.md, assets, data and reports.
24. Copy the notebook downloaded in step 21 into this folder. Name it
    `NYC_Team5_Colab.ipynb`; replace the older copy only if one exists there.
25. Open data → processed and check housing_monthly.csv, transport_monthly.csv,
    integrated.csv and provenance.json. Open reports and check FINDINGS.md.
26. Record actual contributions in TEAM.md. Do not mark unperformed work complete.
    Eyad owns the easiest charts Q1–Q2 and basic checks/labels. Each of the other
    members owns the next two questions as listed in TEAM.md.
27. You can edit documentation in GitHub's pencil editor later. No Notepad
    installation is required. Keep the notebook's documentation consistent with
    final GitHub edits before submitting.

## C. Upload to GitHub

28. Keep the previous repository as a backup. Create a new repository named
    `nyc-development-mobility-team5` under `eyadelsafty06-rgb` at https://github.com/new .
29. Set the visibility your instructor requires. The easy clone workflow below
    assumes Public, as in your earlier project repository. Leave “Add README”
    unchecked because the project contains one. Click Create repository.
30. Click “uploading an existing file”.
31. In File Explorer open the inner nyc_team5 folder so you can see app.py.
    Select the files and folders inside it, including the executed notebook.
32. Drag those contents onto GitHub's upload area. Do not upload just the ZIP
    or an extra enclosing folder. Wait for the upload to finish.
33. The source snapshots are compressed; each supplied raw file is under the
    browser's 25 MiB per-file limit. If a refreshed file exceeds that limit,
    keep it in your backup, upload the remaining source/processed files and
    distribute that raw snapshot through a GitHub Release. Do not drop the
    processed data or accept an incomplete upload silently.
34. Enter `Add five-member NYC project` as the commit message and commit.
35. Verify app.py, requirements.txt and README.md appear directly on the main
    repository page. Verify the notebook, assets/style.css and data/processed.
36. Open README.md → pencil icon. Enter the actual new GitHub link in Submission
    status. Complete the actual team work log and commit your edits.
37. Give teammates collaborator access if they need to edit. Use their verified
    GitHub usernames. Each should review and explain their assigned parts.

## D. Deploy on PythonAnywhere without a paid upgrade

Your existing account is `eyadelsafty`. Its Beginner plan supports one web app.
We use the same account. The website target is
https://eyadelsafty.pythonanywhere.com . It is not verified live by this package.

38. Sign in at https://www.pythonanywhere.com/ . Do not select Upgrade Account.
39. Open Consoles → Bash, or reopen your existing Bash console. The commands
    below go in PythonAnywhere's Bash terminal, not in Colab or Windows search.
40. Run each command separately, waiting for the prompt to return:

```bash
cd ~
git clone --depth 1 https://github.com/eyadelsafty06-rgb/nyc-development-mobility-team5.git nyc_team5
cd ~/nyc_team5
ls data/processed
```

Expected: the four processed files listed in step 25. If `nyc_team5` already
exists, stop and inspect it; do not delete it or repeat the clone blindly.
If cloning asks for a password or says repository not found, first check that
the new public repository exists and its spelling is correct.

41. Create and activate the environment:

```bash
python3.12 -m venv --system-site-packages ~/nyc-team5-env
source ~/nyc-team5-env/bin/activate
```

42. Install only the website packages, then check the import:

```bash
python -m pip install --no-cache-dir -r requirements.txt
python -c "from app import LOAD_ERROR; assert not LOAD_ERROR, LOAD_ERROR; print('Dashboard ready')"
```

Expected: `Dashboard ready`. Stop and inspect any traceback.
Do not install requirements-analysis.txt on this free web host; the analysis
runs in Colab. Keep an eye on the storage meter if you already installed older
project environments. Do not delete an old environment until you confirm that
no existing website is using it.

43. Click Web. If no web app exists: Add a new web app → continue with the free
    account address → Manual configuration → Python 3.12.
    If a web app already exists from the earlier attempt, open its configuration
    instead. Record its old paths before switching it to this new project.
44. Under Code set both Source code and Working directory to:

```text
/home/eyadelsafty/nyc_team5
```

45. Under Virtualenv enter:

```text
/home/eyadelsafty/nyc-team5-env
```

Save each field. The web app and virtualenv must both use Python 3.12. If an
existing app uses a different Python version and you cannot change it, stop
and get help before deleting or recreating that app.

46. Click the WSGI configuration file link. Save a copy of its previous contents
    if it belongs to an older working site. Replace its text with:

```python
import os
import sys

project_path = '/home/eyadelsafty/nyc_team5'
if project_path not in sys.path:
    sys.path.insert(0, project_path)
os.chdir(project_path)
from app import server as application
```

47. Save. Return to Web and click Reload. Open the website link displayed there.
    Do not run python app.py or a Gunicorn command on PythonAnywhere.
48. If you see “Something went wrong”, open Web → Log files → Error log, scroll
    to the latest lines and copy the traceback. A missing long_delay_n column
    means older processed data was uploaded; use this five-member export.
49. The free web app has an expiry/renewal date. Use the Web page's available
    extension control and keep it active through grading. Renewal is separate
    from upgrading to a paid plan.

## E. Verify the live site and submit

50. On the live URL click Generate Report with all selections. Check ten charts,
    readable labels, hover/zoom, the five-member list and source links.
51. Select Brooklyn; generate again. Select 2022; generate again. Test work-type
    and incident-reason filters. Try the search example and confirm all controls,
    charts and Story reflect the selection. Empty/too-small subsets should show
    explanatory messages, not a server error.
52. Test on a phone or a narrow browser window. Record the date, URL, results and
    any unresolved issue in reports/VALIDATION.md. Local tests are not a substitute
    for this check. Keep your own screenshots if useful; no screenshot requirement
    was stated in the supplied PDF.
53. Put the verified live URL and actual repository URL into README.md and the
    final notebook. In your Drive copy, double-click the last text cell, fill
    in the final link lines, then press Ctrl+S. Download it and upload it to
    GitHub again under the same filename. Commit and open it to check both links.
54. Confirm that all five names and IDs match everywhere:
    Eyad Elsafty 16003613; Jana Hazem 14003384; Omar Hisham 16008286;
    Anas Mohamed 13005403; Yassin Ahmed 16002450.
55. Check REQUIREMENTS_CHECKLIST.md. Every research question needs its own chart
    and an explanation grounded in actual results. Each member should be able
    to explain their two questions, cleaning decisions and website contribution.
56. The supplied Project Description.pdf gives the deadline as 9 November 2026.
    One team email to ICS503Data@gmail.com must contain all five IDs, the GitHub
    repository link, the deployed website link and both source dataset links.
    Send it using your own email account before the deadline. No email has been
    sent by the project generator. Changes after the deadline are not considered.
57. Keep a backup of the final executed notebook, export ZIP and submission email.

## Where preparation stops

The deliverables include complete code, the executed snapshot analysis,
computed findings, team assignments, documentation and local test evidence.
Google-account execution, member review, GitHub upload, public deployment,
renewal, live-site testing and submission are your team's remaining steps.

## Official references (checked 5 November 2026)

- Colab: https://research.google.com/colaboratory/faq.html
- Dash notebooks: https://dash.plotly.com/dash-in-jupyter
- GitHub uploads: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- PythonAnywhere free signup: https://www.pythonanywhere.com/registration/register/beginner/
- Free-plan limits: https://help.pythonanywhere.com/pages/FreeAccountsFeatures/
- Hosting configuration: https://help.pythonanywhere.com/pages/Flask/
- Dash WSGI: https://help.pythonanywhere.com/pages/DashWSGIConfig
