# Requirement check against Project Description.pdf and Data Catalog.pdf

Checked against the supplied PDFs on 5 and 6 November 2026. The PDF deadline is 9 November 2026.

| Requirement | Delivered evidence | Final team check |
|---|---|---|
| Exactly two domains, at least nine columns each | H3 rbx6-tga4 (14 extracted), T5 ez4e-fazm (12 extracted) | Review source table |
| IDs, URLs, counts, selection rationale | Notebook and reports/DATASET_OVERVIEW.md | Use final snapshot counts |
| Raw EDA, structure, missingness, statistics | Notebook EDA; eda.py; profile CSVs/PNGs | Review outputs |
| Pre-cleaning with justified missing/outlier/duplicate rules | pipeline.py; notebook; cleaning_audit.csv | Explain decisions |
| Inconsistent formats and geography | Dates, categories, borough aliases, ZIP strings, coordinates | Review flags |
| Meaningful integration and aggregation | Unique borough-month join; category aggregation | Explain common grain |
| Required post-integration cleaning | Coverage audit, zero/null rules, weighted means, dtype/count assertions | Confirm checks pass |
| Five members: ten questions and charts | Q1–Q10, team.py, TEAM.md, notebook and website | Each member reviews two |
| Individual cleaning/integration/website work | TEAM.md assignments and actual work log | Complete actual log |
| Cross-domain interactive visuals | All ten compare permits with transport measures | Check hover/zoom |
| Multiple dropdowns and search | app.py four filters + query parser | Test hosted app |
| Generate Report updates charts | One report callback returns ten charts and findings | Test hosted app |
| Story: question, discovery, limits, impact | Website Story and chart findings; reports/FINDINGS.md | Review narrative |
| Notebook Markdown and code comments | Explanations for each step and complex rule | Understand code |
| AI prompts and dataset links in notebook | Prompt appendix and source overview | Add later prompts |
| README setup/deployment/contributions | README.md and START_HERE.md | Fill final URLs |
| Free deployed working site | PythonAnywhere files and guide | Deploy, renew and test |
| Complete source/notebook on GitHub | Packaged project | Upload and check files |
| Submission email IDs/repo/site/datasets | START_HERE.md step 56 | Team sends email |

Maps, prediction accuracy, paid hosting, screenshots and a specific named host
are not mandatory in the supplied PDF. The site must nevertheless be deployed
and fully functional; an inline Colab preview alone is not the final deployment.
