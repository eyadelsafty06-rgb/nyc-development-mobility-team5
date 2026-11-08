# AI assistance and prompt record

The initial implementation was generated with ChatGPT from the user request below and the two supplied course PDFs. Team members should review, explain and test their assigned parts.

## User prompt (15 October 2026)

> Act as an expert Data Engineer, Full-Stack Data Scientist, and NYC Open Data specialist. I am working on the Data Engineering and Visualization project for our 4-member team at the German International University (Winter Semester 2026)[cite: 1].
>
> Please help us build the complete, end-to-end project code, structured markdown documentation for our Jupyter/Colab notebook, and the source code for our interactive web application.
>
> Here are the exact project requirements we must strictly satisfy:
>
> 1. DATASET SELECTION & OVERVIEW:
> - Select exactly one Housing & Development dataset and one Transportation dataset from NYC Open Data[cite: 3].
> - Both datasets must have at least 9 columns each[cite: 3].
> - Provide dataset IDs, direct API/download links, row/column counts, and a thorough justification of why they are paired and how they share meaningful geographic/temporal integration fields (e.g., Borough, ZIP Code, Year/Month, or Census Tract)[cite: 1, 3, 7].
>
> 2. EXPLORATORY DATA ANALYSIS (EDA):
> - Write Python code using pandas, matplotlib, and seaborn to inspect data structures, distributions, and summary statistics for both datasets[cite: 5, 6].
> - Identify structural anomalies, missing value patterns, and data types[cite: 6].
>
> 3. PRE-INTEGRATION CLEANING:
> - Handle missing values with explicit justifications for dropping vs. imputing[cite: 6].
> - Detect and address outliers using IQR or domain-specific rules[cite: 6].
> - Standardize formats (dates, strings, categorical values, and geographic identifiers like ZIP codes or Borough names)[cite: 6].
> - Remove duplicate records[cite: 6].
>
> 4. DATASET INTEGRATION:
> - Because datasets have different granularities/sizes, implement a robust aggregation strategy (e.g., aggregating both datasets to a common level like ZIP Code by Year or Borough by Month) rather than a raw row-level join[cite: 1, 2, 6].
> - Document the join key, grain choice, and explain how the combined dataset unlocks meaningful cross-domain insights.
>
> 5. POST-INTEGRATION CLEANING:
> - Resolve new missing values introduced by the join, clean up redundant or conflicting columns, and fix any data type mismatches[cite: 6].
>
> 6. RESEARCH QUESTIONS & VISUALIZATIONS (4-Member Team = 8 Questions & 8 Visualizations):
> - Since we have 4 team members, generate exactly 8 distinct, non-trivial research questions (2 per member) that explore creative connections between housing and transportation.
> - Each research question must be backed by a specific visualization chart code snippet (Plotly/Matplotlib)[cite: 4].
> - Include at least one cross-domain visualization (e.g., map overlay or scatter plot comparing a housing metric against a transportation metric)[cite: 6].
> - Clearly delineate which team member (Member 1, Member 2, Member 3, Member 4) owns each research question, visualization, cleaning task, and website component.
>
> 7. INTERACTIVE WEBSITE (Dash / Python):
> - Build a fully functional interactive web application using Dash (Python/Plotly)[cite: 6].
> - The website must feature:
> - Multiple dropdown filters (e.g., Borough, Year, housing category, transportation category)[cite: 6].
> - A search mode where users can type queries (e.g., "Brooklyn 2022") to auto-apply filters[cite: 6].
> - A central "Generate Report" button that dynamically updates all visualizations upon clicking[cite: 6].
> - A dedicated "Story" section presenting our research question, key findings, data limitations, andNYC impact[cite: 4, 6].
> - Provide deployment instructions for Vercel, Render, or Heroku[cite: 6].
>
> 8. DELIVERABLES STRUCTURE:
> - Structure the output into clear sections for: (a) Dataset Overview & Links, (b) EDA & Pre-Cleaning, (c) Integration & Post-Cleaning, (d) 8 Research Questions & Visualizations with Member Assignments, (e) Dash Website Code (`app.py`), and (f) A professional `README.md` template outlining setup, deployment, and contribution breakdowns[cite: 7].
>
> Please write clean, modular, well-commented Python code and descriptive Markdown cells for our notebook and website repository[cite: 7].

## Sources supplied with the prompt

- Project Description.pdf (GIU Winter Semester 2026, Milestone 1)
- Data Catalog.pdf (recommended datasets H3 and T5 used)

The `[cite: n]` markers above belong to the original request; they are not independent verified bibliographic references. Official dataset links are in README.


## Relevant follow-up prompts visible in this conversation

The original prompt described four members; the 5 November request supersedes it with five members and ten questions. These excerpts record actual user requests, not invented prompts. Brief acknowledgements and image-only messages are omitted.

### 15 October 2026

> can you re do the project but on google collab

Purpose/output: Colab notebook.

### 15 October 2026

> can you make the google collab project file and send it

Purpose/output: Standalone notebook.

### 17 October 2026

> okay tell me how to do the project step by step ill use google collab and GitHub respiratory and try and make the project on the simpler side because I'm a beginner and each step should be percious and clear so i can finish the project

Purpose/output: Beginner setup guide.

### 17 October 2026

> okay i finished the google collab what am i supposed to do next don't miss any step or detail of the whole project

Purpose/output: Export and deployment guide.

### 17 October 2026

> here is the extracted zip what should i do next

Purpose/output: File check.

### 17 October 2026

> change and make it that i used chatbpt in simple stuff asking abt code and stuff like thst

Purpose/output: Prompt-log wording request; assistance remained accurately disclosed.

### 17 October 2026

> in code cell 27

Purpose/output: Cell editing guidance.

### 17 October 2026

> make the readme.md believable it is human

Purpose/output: Simpler README wording; project details retained.

### 17 October 2026

> cell is empty underneath

Purpose/output: Complete replacement README.

### 17 October 2026

> theres no notepad

Purpose/output: Alternative file-editing instructions.

### 17 October 2026

> how do i upload contents

Purpose/output: GitHub upload instructions.

### 17 October 2026

> check all the screenshots are there any error or missing points and continue the steps of the projects

Purpose/output: Review of uploaded project files and README.

### 17 October 2026

> it wants me to add card to proceed

Purpose/output: Hosting plan guidance.

### 17 October 2026

> in the pdf of project description am i supposed to use render and pay for it

Purpose/output: Checked free-hosting requirement.

### 17 October 2026

> lets use another deployment option that doesnt make me put credit card infromation

Purpose/output: Switched hosting guidance to PythonAnywhere.

### 5 November 2026

> Okay, Now look I want you to redo the whole project again with all the adjustments i gave you previously throughout the chats plus add these people to the project Jana Hazem 
> 14003384, Omar Hisham
> 16008286, Anas Mohamed 
> 13005403, and Yassin Ahmed 16002450 and give Eyad Elsafty 16003613 the easiest part. After you finish the project part give me a step by step beginner level to continue after you stopped. Do the Project humanly and as simple as possible and we use google collab and GitHub. reread the whole chat between me and you to remove the last mistakes and reread project description and data CatLog if needed

Purpose/output: Five-member rebuild, ten questions, source packaging, beginner guide.

The same five-member rebuild request was repeated verbatim on 6 November 2026; its text is recorded in the 5 November entry above.

## Student validation
Record actual member review and changes in TEAM.md. Local automated verification is in reports/VALIDATION.md. Live hosting checks must be completed by the team. Add later prompts here and in the final notebook.
