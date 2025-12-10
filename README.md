# Medication Assistant Multi-Agent System

**Academic Project – Hosei University (Tokyo, Japan)**
**Date:** December 2025

---

## 1. Overview

The Medication Assistant Multi-Agent System is an academic artificial intelligence project developed at Hosei University, Graduate School of Computer and Information Sciences (Tokyo, Japan).

The purpose of this project is to design and implement a complete, modular, and interpretable AI pipeline capable of:

* Collecting medication data from the OpenFDA public API.
* Enriching and restructuring this data using a Large Language Model (LLM).
* Retrieving relevant medications based on symptom queries using TF-IDF and cosine similarity.
* Verifying medication images through a YOLOv8 computer vision model.
* Providing a unified demonstration interface built with Tkinter.

The project is intended exclusively for academic and research purposes.

---

## 2. System Architecture

The system is organized into four agents, each responsible for a distinct part of the processing pipeline. This design ensures modularity, clarity, and maintainability.

### 2.1 ScrapingAgent

Retrieves raw medication data from the OpenFDA API (`https://api.fda.gov/drug/label.json`).
Its responsibilities include:

* Handling API pagination to collect approximately 500 medication entries.
* Normalizing heterogeneous fields such as indications, usage, or warnings.
* Exporting the data into a structured JSON file (`openfda_500.json`).

This agent manages real-world issues such as missing fields, inconsistent formatting, and API rate limits.

### 2.2 LLM Enricher Agent

Enhances the scraped dataset using a Large Language Model. The agent extracts:

* Symptoms associated with each medication.
* Clean, standardized descriptions of indications.
* Semantic tags.
* High-level categories.

To ensure reliability, the agent includes automatic retry logic, schema validation, and fallback structures.
The output is saved as `enriched_medications.json`.

### 2.3 RAGSearchAgent (TF-IDF and Cosine Similarity)

Implements a retrieval mechanism similar to RAG but using classical information retrieval techniques.

The process includes:

1. Building a TF-IDF matrix of all enriched medication descriptions.
2. Transforming the user symptom query into a TF-IDF vector.
3. Computing cosine similarity between the query vector and each medication vector.
4. Ranking and returning the most relevant medications.

The method is deterministic, interpretable, and suitable for small datasets.

### 2.4 VisionAgent (YOLOv8)

Uses a YOLOv8s model to detect whether an uploaded image contains a medication box.

Due to dataset limitations, the model was trained with a single class ("drug-name"), meaning it performs binary classification:

* Medication box detected
* Medication box not detected

It does not distinguish between different medications. This limitation reflects the difficulty of obtaining a multi-class dataset of medication packaging.

Performance summary:

* Precision: 0.67
* Recall: 0.67
* mAP50: 0.70
* mAP50–95: 0.43

These metrics are adequate for binary verification tasks within an academic prototype.

---

## 3. Graphical User Interface

The Tkinter GUI integrates all system components. It enables:

* Symptom input for medication recommendation.
* Image upload for YOLO-based verification.

The GUI provides a practical demonstration of how the multi-agent system functions as a unified application.

---

## 4. Project Structure

```
medication-assistant-multiagent/
│
├── agents/
│   ├── scraping_agent.py
│   ├── enrich_agent.py
│   ├── rag_search_agent.py
│   └── vision_agent.py
│
├── tools/
│   ├── search_engine.py
│   └── utils.py
│
├── data/
│   ├── openfda_500.json
│   └── enriched_medications.json
│
├── gui_app.py
├── requirements.txt
└── README.md
```

---

## 5. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/Majidoy/medication-assistant-multiagent.git
cd medication-assistant-multiagent
```

### Step 2: Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Linux and macOS
venv\Scripts\activate         # Windows
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Running the System

### 6.1 Scrape medication data

```bash
python agents/scraping_agent.py
```

### 6.2 Enrich the scraped dataset

```bash
python agents/enrich_agent.py
```

### 6.3 Test the RAG search engine manually

```bash
python tools/search_engine.py --query "headache fever"
```

### 6.4 Launch the graphical user interface

```bash
python gui_app.py
```

This launches the full multi-agent system, including symptom-based medication search and image verification through YOLO.

---

## 7. Limitations

* The YOLO model performs binary detection only, due to the lack of a multi-class medication dataset.
* The system does not include OCR extraction from medication boxes.
* Recommendations rely on textual similarity and do not replace professional medical advice.
* The dataset is dependent on the structure and completeness of OpenFDA entries.

---

## 8. Future Work

Potential improvements to strengthen the system include:

* Building or acquiring a multi-class dataset for medication box detection.
* Adding OCR capabilities for extracting text from packaging.
* Incorporating embedding-based retrieval (e.g., Sentence-BERT).
* Deploying the system as a web application.
* Expanding the knowledge base with additional medical sources.

---

## 9. Academic Context

This project was developed during the Practical Machine Learning course at Hosei University.
It serves as an applied exploration of multi-agent design, data engineering, information retrieval, and computer vision.

---

## 10. Repository

Full source code is available at:

[https://github.com/Majidoy/medication-assistant-multiagent](https://github.com/Majidoy/medication-assistant-multiagent)

