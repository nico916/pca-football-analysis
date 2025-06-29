# PCA for Football Player Profiling

![Language](https://img.shields.io/badge/language-Python%20%26%20MATLAB-blue.svg)
![Libraries](https://img.shields.io/badge/libraries-Pandas%2C%20Scikit--learn-orange.svg)
![Environment](https://img.shields.io/badge/environment-Academic%20Project-lightgrey.svg)

This academic project is a deep dive into **Principal Component Analysis (PCA)** applied to football player statistics from the 2022-2023 season. The goal was to reduce the high dimensionality of player data to visualize and interpret different player profiles and styles of play.

This analysis served as the direct inspiration and foundation for my personal project, an **[Interactive Player Comparison Tool]([https://github.com/[your-github-username]/Comparateur-de-profils](https://github.com/nico916/Comparateur-de-profils))**.


## Table of Contents

- [About The Project](#about-the-project)
- [Project Workflow](#project-workflow)
  - [Phase 1: Data Pre-processing (Python)](#phase-1-data-pre-processing-python)
  - [Phase 2: PCA and Visualization (MATLAB)](#phase-2-pca-and-visualization-matlab)
- [Key Findings & Interpretation](#key-findings--interpretation)
- [From Analysis to Application](#from-analysis-to-application)
- [Technical Reflections & Lessons Learned](#technical-reflections--lessons-learned)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Dataset](#dataset)
  - [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About The Project

The core objective of this project was to leverage PCA to distill over 100 raw statistical variables per player into a simple 2D map. This map aims to answer questions like:
-   Can we mathematically identify distinct player roles (e.g., finisher, playmaker, defensive rock)?
-   What are the key stats that define a "creative" player versus a "direct" one?
-   How similar are the statistical profiles of top players?

Football data was chosen for its high dimensionality and its intuitive interpretability, making it a perfect case study for dimensionality reduction techniques.

## Project Workflow

The project was structured in two main phases, using the best tool for each job.

### Phase 1: Data Pre-processing (Python)

Before any analysis, a significant data cleaning and preparation effort was required. Using **Python** with the **Pandas** library, I performed the following steps:
-   **Data Filtering**: Removed goalkeepers and players with insufficient game time (< 500 minutes) to ensure statistical relevance.
-   **Handling Player Transfers**: Aggregated stats for players who moved clubs mid-season to create a single, unified profile for the entire season.
-   **Feature Engineering**: Recategorized detailed positions into three main roles (FW, MF, DF) for clearer visualization.
-   **Feature Selection**: Drastically reduced the number of features from over 100 to a core set of the most discriminative stats, removing redundancy and noise.

### Phase 2: PCA and Visualization (MATLAB)

With a clean dataset, I used **MATLAB** to perform the core analysis:
-   **Standardization**: Scaled the data so that each variable contributes equally to the analysis.
-   **PCA Implementation**: Calculated the covariance matrix, its eigenvectors, and eigenvalues to determine the principal components.
-   **Data Projection**: Projected the player data onto the first two principal components (PC1 and PC2).
-   **Interactive Visualization**: Created an interactive plot with features like hover-to-display-name and a context menu to filter by position.

## Key Findings & Interpretation

The PCA successfully separated players into distinct clusters corresponding to their roles on the pitch. By analyzing the variable contributions (loadings), I was able to interpret the two main axes:

-   **PC1 (Horizontal Axis - The Offensive/Defensive Spectrum)**: This axis clearly separates attacking players from defensive ones. It is positively correlated with stats like `Shots`, `Shot-Creating Actions (SCA)`, and `Assists`.
-   **PC2 (Vertical Axis - The Creative/Direct Spectrum)**: This axis distinguishes playmakers from more direct players. It is positively correlated with creative stats like `Assists` and `SCA`, and negatively with stats indicating a less involved playstyle.

## From Analysis to Application

> "While working on this PCA project, I saw the players represented as a cloud of points in a 2D space. Since each point is a summary of a player's stats, I realized I could use the Euclidean distance between any two points to measure their similarity. This insight was the spark for my next project: an interactive tool that connects this statistical representation to real-world player comparisons."

This academic analysis directly led to the development of my **[Interactive Player Comparison Tool]([https://github.com/[your-github-username]/Comparateur-de-profils](https://github.com/nico916/Comparateur-de-profils))**, built with Streamlit and deployed online.

## Technical Reflections & Lessons Learned

This project was a crucial learning experience. Reflecting on it, I identified key areas of growth that align with data science best practices:

-   **Challenge**: From "Black Box" Functions to Mathematical Understanding.
    -   My initial implementation relied heavily on high-level library functions like `cov()`. While functional, this approach hid the underlying mechanics of PCA.
    -   **Lesson Learned**: True mastery of an algorithm comes from the ability to implement it from its mathematical foundations. A correct matrix-based approach is not only more performant but also ensures a complete understanding of the results and their limitations.

-   **Challenge**: Rigor in Data Visualization.
    -   The resulting plot was informative but lacked standard analytical tools like a **correlation circle**. Furthermore, aspects like axis scaling and vector norms were not perfectly calibrated, which could lead to misinterpretation.
    -   **Lesson Learned**: A data visualization is an analytical tool, not just an illustration. Its mathematical accuracy is paramount. Every graphical element must be intentional and correct to support reliable conclusions.

## Getting Started

### Prerequisites
-   Python 3.x with Pandas
-   MATLAB

### Dataset
The data used for this analysis is the **"2022/2023 Football Player Stats"** dataset, available on Kaggle.
-   [Link to the dataset on Kaggle](https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats)

### Usage
1.  **Pre-process the data**: Run the Python script (`data_preprocessing.py`) on the raw CSV file. This will generate a new file named `player_stats_processed.csv`.
    ```sh
    python data_preprocessing.py
    ```
2.  **Run the PCA analysis**: Open MATLAB and run the main script (`PCA.m`). The script will automatically load `player_stats_processed.csv` to perform the analysis and generate the visualization.

## License

Distributed under the MIT License. See `LICENSE` file for more information.

## Acknowledgments
-   This project was completed as part of my academic curriculum.
-   Data provided by [Vincenzo Vivona on Kaggle](https://www.kaggle.com/vivovinco).
