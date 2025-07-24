# 📰 News Topic Classifier

A machine learning project to automatically classify news articles into predefined categories using natural language processing.

## 🧾 Overview

This project collects and labels news articles from multiple news sources, processes them, and trains machine learning models to classify them into the following categories:

- Politics
- Business
- Health
- Technology
- Culture

## 📁 Structure

```
ds-project/
└── news-topic-classifier/                          # News classification project
    ├── data/                                       # Raw and processed data
    ├── scrapers/                                   # Web scrapers for each news source
    ├── src/                                        # Preprocessing, training, evaluation code
        ├── news-topic-classifier/                  # Raw and processed data
            ├── apis/                               # Web scrapers for each news source
            ├── model/                              # Preprocessing, training, evaluation code
            ├── utils/                              # Web scrapers for each news source
            ├── main.py                             # Preprocessing, training, evaluation code
    ├── notebooks/                                  # EDA and experiments
    ├── models/                                     # Trained models
    ├── requirements.txt                            # Project dependencies
    └── README.md                                   # Project documentation
```

## 🔧 Tech Stack

- **Python 3.12** - Core language
- **Scraping** - `requests`
- **ML & Data** - `pandas`, `scikit-learn`
- **Preprocessing** - `NLTK`

## 🚧 Status

- [x] Project folder initialized
- [x] Get news source (APIs)
- [ ] Build initial dataset
- [ ] Train baseline classifier

## 🎯 Goals

- Build a custom dataset from news
- Train and evaluate topic classification models

## 📄 License

This project is covered under the [MIT License](../LICENSE), as specified in the root of this repository.

## 🤝 Contact

Created by [julioklau](https://github.com/julioklau) — feel free to reach out if you have questions or feedback!
- 🔗 [GitHub](https://github.com/julioklau)
- 💼 [LinkedIn](https://linkedin.com/in/julio-lau)
- 📧 julioklau97@gmail.com