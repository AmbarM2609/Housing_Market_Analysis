

## Housing Market Analysis – Multi-Perspective Project
Instead of just predicting prices, the project explains **who should care and why**.
* Customer (buyer)
* Investor
* Builder
* Banker
* City planner
---
* Price distribution
<img width="854" height="473" alt="image" src="https://github.com/user-attachments/assets/7bd0a0aa-aec3-487f-a14d-4b1622bc3fa5" />

* Deal categories
<img width="707" height="473" alt="image" src="https://github.com/user-attachments/assets/8a64d2fd-a28f-4893-ab8c-d1ff5ab7cd40" />

* Quality vs price
<img width="870" height="550" alt="image" src="https://github.com/user-attachments/assets/3326e95e-5f31-4285-bd52-da1a0dea4d46" />

* Value gaps
<img width="875" height="550" alt="image" src="https://github.com/user-attachments/assets/34829603-c54c-4367-9852-a18c8e418e0a" />

* Neighborhood inequality
<img width="1051" height="858" alt="image" src="https://github.com/user-attachments/assets/99cd1ff8-b7cd-4675-b52a-f046641ef2af" />

---
The market is dominated by fairly priced, middle-class homes typically selling for around $150k. While most houses are affordable, building quality is the main reason prices shoot up; luxury homes (quality levels 9–10) see massive price jumps compared to standard builds. Location also plays a huge role, with neighborhoods like NoRidge and NridgHt being significantly more expensive than areas like MeadowV. Finally, while most homes are priced correctly, investors can still find rare bargains that sell for less than their predicted value.
---
Kaggle :- https://www.kaggle.com/code/ai21ambarmestry/housing-market-decisions-making

---
### How the project works

#### 1. Data loading

Raw housing data is loaded from CSV.

#### 2. Preprocessing

* Columns with too many missing values are dropped
* Numeric values are filled using median
* Categorical quality fields are converted into numeric scores
  This keeps the data usable and realistic.

#### 3. Feature engineering

New features are created for real use cases, for example:

* House age
* Total area
* Land utilization
* Renovation gap
* Lifestyle space (porch, deck, etc.)

Each feature exists for a **clear business reason**.

#### 4. Modeling

* A Random Forest model is trained
* The target is `log(SalePrice)` to reduce price skew
* Only numeric features are used
  This mimics common industry practice.

#### 5. Scoring (Stakeholder POVs)

* **Customer POV**
  Compares predicted price vs actual price
  Labels homes as *Bargain*, *Fair*, or *Overpriced*

* **Investor POV**
  Finds homes where predicted value is much higher than current price

* **Builder POV**
  Shows how sale price changes with construction quality

* **Banker POV**
  Computes a risk score using age, condition, and price efficiency

* **City Planner POV**
  Analyzes price inequality across neighborhoods

Each POV uses the *same data*, interpreted differently.

#### 6. Visualization

Simple charts show:

* Price distribution
* Deal categories
* Quality vs price
* Value gaps
* Neighborhood inequality

---




