# Data Folder

## Files Included in This Repo (small, safe for GitHub)

| File | Size | Description |
|---|---|---|
| `novatech_logo.svg` | 1.5 KB | Official NovaTech brand logo |
| `sloganlist.csv` | 42 KB | 1,162 real brand slogans — columns: `Company`, `Slogan` |
| `slogans_processed.csv` | 78 KB | Cleaned version with tokenised text |

---

## Files NOT in This Repo (too large for GitHub — download separately)

### 1. Marketing Campaign Dataset (26 MB)
**Columns:** `Campaign_ID, Company, Campaign_Type, Target_Audience, Duration, Channel_Used, Conversion_Rate, Acquisition_Cost, ROI, Location, Language, Clicks, Impressions, Engagement_Score, Customer_Segment, Date`

📥 Download from the project Google Drive and place here as:
```
data/marketing_campaign_dataset.csv
```

### 2. Startups Dataset (8.8 MB)
**Columns:** `name, city, tagline, description`

📥 Download from the project Google Drive and place here as:
```
data/startups.csv
```

### 3. Logo Dataset — Kaggle (167,140 images, ~2 GB)
📥 Download from Kaggle:
https://www.kaggle.com/datasets/siddharthkumarsah/logo-dataset-2341-classes-and-167140-images

Place extracted folder as:
```
data/logo_dataset/
    ├── class_1/
    │   ├── image1.jpg
    │   └── image2.jpg
    ├── class_2/
    └── ...
```

### 4. Font Dataset — Kaggle
📥 Download from Kaggle:
https://www.kaggle.com/datasets/muhammadardiputra/font-recognition-data

Place extracted folder as:
```
data/font_dataset/
    ├── serif/
    ├── sans_serif/
    └── ...
```

---

## Google Drive Setup for Colab Notebooks

All notebooks expect files at this path in your Google Drive:
```
MyDrive/BrandSphere/
    ├── marketing_campaign_dataset.csv
    ├── sloganlist.csv
    ├── startups.csv
    ├── logo_dataset/
    └── font_dataset/
```
