# Implement an RDMO Questionary

 Property key | value        |
|--------------|-|
 Date         | 2026-03-16 | 
 Target       | steward |     

## The six parts of a DMP

To build an RDMO (Research Data Management Organiser) questionnaire that aligns perfectly with the **RDA DMP Common Standard**, you need to map the attributes of the JSON classes to human-readable questions.

RDMO uses a hierarchical "Catalog" structure. Below is a breakdown of the core **maDMP properties** and the corresponding questions you should include in your RDMO attributes.

---

### 1. General Metadata (`dmp` class)

These questions establish the high-level identity of the plan.

* **Title:** What is the full title of this Data Management Plan?
* **Language:** In what language is the dataset documentation primarily written? (Use ISO 639-3 codes).
* **Ethical Issues:** Are there any ethical issues associated with the data collection (Yes/No/Unknown)?
* **Ethical Report:** If yes, provide a URL to the ethical committee’s report or workspace.

### 2. People and Organizations (`contact`, `contributor`)

The maDMP standard relies heavily on **PIDs** (Persistent Identifiers).

* **Contact Person:** Who is the primary point of contact for this DMP? (Request **ORCID**).
* **Contact Email:** What is the functional email address for data inquiries?
* **Contributors:** List all people involved. What are their specific roles? (e.g., *DataCurator*, *ProjectManager*, *Researcher*).
* **Host Institution:** Which organization is responsible for the data? (Request **ROR ID**).

### 3. Project & Funding (`project`, `funding`)

This links the data to the money and the timeline.

* **Project Title:** What is the name of the research project?
* **Project Description:** Provide a brief abstract of the project goals.
* **Funder:** Who is the funding body? (Request **Crossref Funder ID**).
* **Grant ID:** What is the formal grant number or identifier?
* **Funding Status:** Is the funding *Planned*, *Applied*, or *Granted*?

### 4. Dataset Specification (`dataset`)

This is the "meat" of the maDMP. You need a question for each technical property.

| maDMP Property | RDMO Question |
| --- | --- |
| **Type** | What is the nature of the data? (e.g., *Dataset*, *Software*, *Model*). |
| **Personal Data** | Does this dataset contain Personal Identifiable Information (PII)? |
| **Sensitive Data** | Does this dataset contain sensitive data (e.g., medical, endangered species)? |
| **Issued Date** | When is the data expected to be formally released? |
| **Keywords** | Provide 3–5 tags or keywords describing the data content. |

### 5. Technical Distribution (`distribution`)

This describes where the data "lives" and how it is protected.

* **Data Access:** Is the data *Open*, *Shared* (restricted), or *Closed*?
* **License:** Under which license will the data be released? (Provide a dropdown for **SPDX** licenses like CC-BY-4.0).
* **Format:** What file formats are used? (e.g., `text/csv`, `application/json`).
* **Byte Size:** What is the estimated total volume of the data (in GB or TB)?
* **Host/Repository:** Which repository will host the data? (Request a URL or **Re3data** ID).

### 6. Costs (`cost`)

* **Cost Type:** What is the category of the expense? (e.g., *Storage*, *Personnel*, *Archiving*).
* **Amount:** What is the estimated cost in a specific currency?
* **Description:** Briefly justify why this cost is necessary for the RDM process.

---

### Implementation Tip for RDMO

When setting these up in the RDMO **Control Panel**:

1. Ensure each question is linked to an **Attribute** that follows the maDMP logic (e.g., `project/funding/funder_id`).
2. Use **Value Types** like `Entity` for creators so you can capture multiple people.
3. Use **Option Sets** for things like "Data Access" (Open/Closed/Restricted) so the output matches the standard's controlled vocabulary.

### [Repo for the standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard/tree/master)
- Examples of json files are presented in this repo

## Implementation Steps

Building a questionnaire in RDMO is a bit like building a database: you have to define the "containers" for the data before you can write the questions that fill them. If you try to create a question without an attribute, RDMO will have nowhere to store the answer.

To align with the **RDA maDMP standard**, you should follow this specific logical order:

---

### 1. The Attributes (The "Data Model")

**First**, define your **Attributes** in the Domain section. These are the internal variables that map to the RDA JSON properties.

* **Why:** Every question must be linked to an attribute.
* **RDA Alignment:** Use a nested structure that mimics the standard, such as:
* `project/dataset/distribution/license`
* `project/funding/funder_id`


* **Pro Tip:** If a dataset can have multiple licenses, ensure the attribute is marked as **"is collection"** in RDMO.

### 2. Option Sets (The "Controlled Vocabularies")

**Second**, create your **Option Sets**. The RDA standard requires specific values (e.g., for data access rights or currency codes).

* **Why:** Instead of letting researchers type "Creative Commons," you want them to select the exact URI or label (like `CC-BY-4.0`) that a machine can read.
* **Action:** Create option sets for:
* **Licenses** (SPDX identifiers)
* **Data Access** (open, closed, shared)
* **Contributor Roles** (using the DataCite or CReDiT taxonomy)



### 3. Conditions (The "Logic")

**Third**, define any **Conditions** if you want a dynamic questionnaire.

* **Why:** You don’t want to ask for an "Ethical Report URL" if the user answered "No" to having ethical issues.
* **Action:** Create a condition like `has_ethical_issues == True`.

### 4. The Questionnaire Structure (Catalog, Sections, Subsections)

**Fourth**, build the skeleton of your **Catalog**.

* **Why:** This organizes the user experience.
* **RDA Alignment:** I recommend creating a section for each major RDA class:
1. **Administrative Data** (Contact, Project, Funding)
2. **Dataset Description** (Type, Metadata, Security)
3. **Host & Storage** (Repositories, Distributions)
4. **Costs & Legal** (Budget, Licenses)



### 5. Questions (The "User Interface")

**Finally**, create the **Questions** and place them within your subsections.

* **Action:** For each question:
1. Assign the **Attribute** (from Step 1).
2. Assign the **Option Set** (from Step 2) if it’s a dropdown/radio choice.
3. Assign the **Condition** (from Step 3) if it should only appear sometimes.
4. Add **Help Text** that explains the RDA requirement (e.g., "Please provide your ORCID in the format 0000-0000-0000-0000").



---

### Summary Checklist

1. **Domain (Attributes):** Create the "folders" for the data.
2. **Options:** Create the "pick-lists."
3. **Conditions:** Create the "if/then" rules.
4. **Catalog:** Build the "chapters" and "pages."
5. **Questions:** Write the actual prompts and link them to 1, 2, and 3.

**Would you like me to generate a small XML import file for the "Funding" section so you can test how these components link together in your RDMO instance?**