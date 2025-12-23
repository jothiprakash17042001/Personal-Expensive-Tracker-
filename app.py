import streamlit as st
import pandas as pd

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💳",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>💳 Personal Finance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Track • Control • Analyze your spending</p>", unsafe_allow_html=True)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload Expense CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("expenses.csv")

# ------------------------------------------------
# DATA CLEANING (SAFE)
# ------------------------------------------------
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

df = df.dropna(subset=['date', 'amount'])

# ------------------------------------------------
# EXPENSE CATEGORIZATION
# ------------------------------------------------
def categorize_expense(text):
    text = str(text).lower()
    if any(x in text for x in ["uber", "ola", "rapido"]):
        return "Transport"
    elif any(x in text for x in ["grocery", "supermarket"]):
        return "Groceries"
    elif any(x in text for x in ["electricity", "bill", "water"]):
        return "Utilities"
    elif any(x in text for x in ["restaurant", "food", "zomato", "swiggy"]):
        return "Food"
    elif any(x in text for x in ["movie", "netflix"]):
        return "Entertainment"
    elif any(x in text for x in ["amazon", "flipkart", "shopping"]):
        return "Shopping"
    else:
        return "Others"

df['category'] = df['description'].apply(categorize_expense)

# ------------------------------------------------
# DATE FEATURES
# ------------------------------------------------
df['month'] = df['date'].dt.to_period("M")

# ------------------------------------------------
# KPI SECTION
# ------------------------------------------------
st.markdown("## 📊 Financial Overview")

total_spent = df['amount'].sum()
avg_transaction = df['amount'].mean()

col1, col2 = st.columns(2)

with col1:
    st.metric("💸 Total Spent", f"₹ {int(total_spent)}")

with col2:
    st.metric("📈 Avg Transaction", f"₹ {int(avg_transaction)}")

# ------------------------------------------------
# SPENDING ANALYTICS (SMART LOGIC)
# ------------------------------------------------
st.markdown("## 📈 Spending Analytics")

unique_months = df['month'].nunique()

if unique_months > 1:
    # MULTI-MONTH VIEW
    st.subheader("📅 Monthly Spend (Calendar Wise)")

    monthly_expense = (
        df.groupby(df['month'].dt.strftime('%b %Y'))['amount']
        .sum()
    )

    st.bar_chart(monthly_expense)

else:
    # SINGLE MONTH VIEW → DAILY TREND
    st.subheader("📆 Daily Spend Trend (Current Month)")

    daily_expense = (
        df.groupby(df['date'].dt.day)['amount']
        .sum()
    )

    st.line_chart(daily_expense)

# ------------------------------------------------
# CATEGORY ANALYTICS
# ------------------------------------------------
st.subheader("📊 Category-wise Spend")

category_expense = df.groupby('category')['amount'].sum()
st.bar_chart(category_expense)

# ------------------------------------------------
# TRANSACTION DETAILS
# ------------------------------------------------
st.markdown("## 📄 Transaction Details")

st.dataframe(
    df.sort_values(by="date", ascending=False),
    use_container_width=True
)

# ------------------------------------------------
# TOTAL EXPENSE AT BOTTOM (FIXED)
# ------------------------------------------------
st.markdown("---")

st.markdown(
    f"""
    <h3 style='text-align:right;'>
        💰 Total Expense: ₹ {int(total_spent)}
    </h3>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown(
    "<hr><p style='text-align:center;color:gray;'>Expense Dashboard • Junior AI/ML Engineer | Prakash shanmugam |Project</p>",
    unsafe_allow_html=True
)
