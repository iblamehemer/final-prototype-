# BrandSphere AI — NovaTech Automated Branding Assistant
**CRS Capstone 2025-26 | Scenario 1 | AI-Powered Automated Branding Assistant for Businesses**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange.svg)](https://aistudio.google.com)

---

## Project Overview

BrandSphere AI is a fully deployed AI-powered branding platform built for **NovaTech** — an enterprise AI automation company. It automatically generates complete brand identities using Computer Vision, NLP, and Generative AI.

---

## NovaTech Brand Identity

| Element | Value |
|---|---|
| Logo | Minimalist falcon-wing emblem (`data/novatech_logo.svg`) |
| Primary Colour | Onyx Black `#1A1A1A` |
| Accent Colour | Electric Blue `#5055D8` |
| Deep Colour | Deep Navy `#0D1B3E` |
| Primary Font | Optima / Space Grotesk |
| Tone | Tech-Forward & Innovative, Minimalist |

---

## Datasets

> ⚠️ Large files are **not stored in this repo** (GitHub 25 MB limit). See download instructions below.

| File | Size | In Repo? | Columns |
|---|---|---|---|
| `marketing_campaign_dataset.csv` | 26 MB | ❌ Download | `Campaign_ID, Company, Campaign_Type, Target_Audience, Duration, Channel_Used, Conversion_Rate, Acquisition_Cost, ROI, Location, Language, Clicks, Impressions, Engagement_Score, Customer_Segment, Date` |
| `startups.csv` | 8.8 MB | ❌ Download | `name, city, tagline, description` |
| `sloganlist.csv` | 42 KB | ✅ Included | `Company, Slogan` |
| Logo Dataset (Kaggle) | ~2 GB | ❌ Kaggle | Class-labelled image folders |
| Font Dataset (Kaggle) | varies | ❌ Kaggle | Class-labelled image folders |

### Download Large Files

**marketing_campaign_dataset.csv & startups.csv:**
Download from the shared Google Drive folder and place in `data/`.

**Logo Dataset (Kaggle):**
https://www.kaggle.com/datasets/siddharthkumarsah/logo-dataset-2341-classes-and-167140-images

**Font Dataset (Kaggle):**
https://www.kaggle.com/datasets/muhammadardiputra/font-recognition-data

### Google Drive Setup for Colab
All notebooks load from:
```
MyDrive/BrandSphere/
    ├── marketing_campaign_dataset.csv
    ├── sloganlist.csv
    ├── startups.csv
    ├── logo_dataset/
    └── font_dataset/
```

---

## 5 Core Modules

| # | Module | AI / ML | Dataset |
|---|---|---|---|
| 1 | 🎨 Logo & Design Studio | CNN (TensorFlow/Keras), KMeans colour extraction (OpenCV) | Logo Dataset |
| 2 | ✍️ Creative Content Hub | Gemini 1.5 Flash, NLTK, Sentence Transformers | sloganlist.csv, startups.csv |
| 3 | 📊 Campaign Studio | Ridge Regression, domain benchmarks, Plotly | marketing_campaign_dataset.csv |
| 4 | 🌍 Multilingual Generator | Gemini 1.5 Flash API | Gemini API |
| 5 | 💬 Feedback Intelligence | Pandas, Plotly, Gemini sentiment analysis | feedback_data.csv |

---

## Repository Structure

```
IADAI205-[IDs]/
├── README.md
├── .gitignore
├── notebooks/
│   ├── Week1_EDA_Data_Understanding.ipynb
│   ├── Week2_Logo_CNN_Design_Studio.ipynb
│   ├── Week3_Font_Recommendation_Engine.ipynb
│   ├── Week4_Creative_Content_GenAI_Hub.ipynb
│   ├── Week5_Colour_Palette_Visual_Harmony.ipynb
│   ├── Week6_Animated_Visuals_Studio.ipynb
│   ├── Week7_Campaign_Studio_Prediction.ipynb
│   ├── Week8_Multilingual_Campaign_Generator.ipynb
│   └── Week9_Feedback_Intelligence.ipynb
├── streamlit_app/
│   ├── app.py                        ← Main application (7 tabs)
│   └── .streamlit/config.toml        ← NovaTech brand theme
├── models/
│   ├── model_CTR.pkl                 ← Ridge Regression (0.5 KB)
│   ├── model_ROI.pkl                 ← Ridge Regression (0.5 KB)
│   ├── model_Engagement_Score.pkl    ← Ridge Regression (0.5 KB)
│   ├── scaler.pkl                    ← StandardScaler (1 KB)
│   ├── label_encoders.json           ← Categorical encoding map
│   ├── model_config.json             ← Feature configuration
│   ├── analytics_summaries.json      ← Pre-computed dashboard data
│   ├── benchmarks.json               ← Industry benchmark values
│   └── slogan_reference.json         ← NLP reference data
├── data/
│   ├── README.md                     ← Download instructions for large files
│   ├── novatech_logo.svg             ← Official NovaTech logo (✅ in repo)
│   ├── sloganlist.csv                ← 1,162 brand slogans (✅ in repo)
│   └── slogans_processed.csv         ← Cleaned slogans (✅ in repo)
├── config/
│   └── requirements.txt
└── deployment/
    └── secrets_template.toml
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Generative AI | Gemini 1.5 Flash API |
| Deep Learning | TensorFlow / Keras (CNN for logos) |
| Machine Learning | scikit-learn (Ridge, KNN, KMeans) |
| Computer Vision | OpenCV, PIL |
| NLP | NLTK, Sentence Transformers |
| Frontend | Streamlit Cloud |
| Visualisation | Plotly |
| Animation | Pillow, imageio |
| Language | Python 3.10+ |
| Deployment | Streamlit Community Cloud |
| Version Control | GitHub |

---

## Quick Start — Local

```bash
# 1. Clone the repository
git clone https://github.com/<username>/IADAI205-<IDs>.git
cd IADAI205-<IDs>

# 2. Install dependencies
pip install -r config/requirements.txt

# 3. Add Gemini API key (free at aistudio.google.com)
#    Create file: streamlit_app/.streamlit/secrets.toml
#    Add line:    GEMINI_API_KEY = "your_key_here"

# 4. Run the app
cd streamlit_app
streamlit run app.py
```

---

## Deployment — Streamlit Cloud

1. Push this repo to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) → **New App**
3. Select your repo → Main file: `streamlit_app/app.py`
4. **Advanced settings → Secrets** — add:
   ```
   GEMINI_API_KEY = "your_gemini_key_here"
   ```
5. Click **Deploy** — live in ~2 minutes

---

## 10-Week Timeline

| Week | Focus | Deliverables |
|---|---|---|
| 1 | EDA & Data Understanding | Column mapping, visualisations, stats |
| 2 | Logo CNN Design Studio | CNN training, embeddings, colour extraction |
| 3 | Font Recommendation Engine | KNN classifier, personality mapping |
| 4 | Creative Content & Gen AI | Gemini taglines, narrative, positioning |
| 5 | Colour Palette Engine | KMeans extraction, psychology mapping |
| 6 | Animated Visuals Studio | Logo + tagline GIF animation |
| 7 | Campaign Studio | ML models, Plotly dashboards, Gemini posts |
| 8 | Multilingual Generator | 7-language translation pipeline |
| 9 | Feedback Intelligence | Rating forms, sentiment analytics |
| 10 | Integration & Deployment | Full Streamlit app, Streamlit Cloud live |

---

## Team Members

| Student ID | Name |
|---|---|
| [ID1] | [Name 1] |
| [ID2] | [Name 2] |
| [ID3] | [Name 3] |
| [ID4] | [Name 4] |

**Repository naming convention:**
`IADAI205-[ID1]-[Name1]-[ID2]-[Name2]-[ID3]-[Name3]-[ID4]-[Name4]`

---

## Acknowledgements

- Google AI Studio — Gemini 1.5 Flash API
- Streamlit Community Cloud — free deployment
- Kaggle — Logo & Font datasets
- TensorFlow, scikit-learn, OpenCV communities
- CRS Facilitators and WACP Panel

---
*BrandSphere AI · CRS Capstone 2025-26 · Scenario 1 · NovaTech*
