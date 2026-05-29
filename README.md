<div align="center">
  <h1>SUNB Data Cleaning Pipeline </h1>
  <p><b>Turning 1 lac+ rows of messy, scraped data into a flawless, production-ready database.</b></p>

  <!-- GitHub Badges -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
</div>

<br />

##  The Story Behind This Repo

Let's be honest: **web-scraped data is an absolute mess.** 

When I started building the **Smart Urdu Novel Bank**, I didn't just have a neat list of books. I had over 78,000 rows of pure chaos—broken links, titles stuffed with words like "PDF Download", weird symbols, missing data, and inconsistent capitalization. 

Doing this manually was impossible. So, I built this automated ETL (Extract, Transform, Load) pipeline. This repository is essentially the "engine room" that saved my sanity. It’s a carefully crafted sequence of Python and JavaScript scripts that takes a mountain of garbage data and refines it into pure gold.

##  The Cleaning Journey (How It Works)

I divided the chaos into a logical 15-step journey. Here is how the data transforms:

###  Phase 1: The Gathering (Scripts 01-04, 09, 10)
First, we bring everything together. 
* We merge scattered Excel and CSV files into one giant master dataset.
* We hunt down and destroy empty links or rows that make no sense.
* We fix broken Google Drive URLs and consolidate multiple links into a clean, single column format.

###  Phase 2: The Surface Scrub (Scripts 05-08)
Now, we make it look pretty.
* No more weird underscores (`_`) or hyphens (`-`). We replace them with clean spaces.
* We enforce strict `Title Case` across all 78,000 records.
* We strip away annoying file extensions like `.pdf` or `.txt` that scraped bots accidentally picked up.

###  Phase 3: The Deep Clean (Scripts 11-15)
This is where the real magic happens. Using Pandas, Regex and custom logic, we remove the "junk context".
* We filter out promotional fluff like "Urdu Novel", "Digest Library", and "Download from here".
* We remove irrelevant contextual tags (like Islamic keywords mixed with novel titles) to ensure the search engine only indexes the actual book names.


---

##  Execution & Workflow

This pipeline was custom-built for the SUNB dataset. The Python scripts are designed to be executed sequentially (from `01` to `15`) on a local machine. It processes large CSV files in seconds using **Pandas**, dropping the refined outputs into a dedicated clean data folder at each step, ensuring zero data loss during transformations.

---

##  About the Developer

Built with a lot of patience, coffee, and ❤️ by **TheUsmanDev**.
I love solving complex problems, building ETL pipelines, and turning chaotic data into meaningful, fast web experiences.