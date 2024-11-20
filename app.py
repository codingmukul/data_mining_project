import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Data Mining Project",  # Sets the browser tab's title
    page_icon="📑",  # Optional: Add an emoji or icon for the browser tab
    layout="wide"  # Expands the content to use the full width of the page
)

# Load precomputed rules
apr_rules = pd.read_csv('Data/Apriori_rules.csv')  # Apriori rules file
fp_rules = pd.read_csv('Data/FP_rules.csv')  # FP Growth rules file

# Title of the app
st.title("Frequent Itemsets Mining and Association Rules 📈")

st.markdown("---")

# Sidebar
menu = st.sidebar.selectbox("#### Select Section", ["Algorithm Findings", "Plots and Analysis"])

# Algorithm Section
if menu == "Algorithm Findings":
    tabs = st.selectbox("#### Select an Algorithm", ["FP Growth", "Apriori"])
    st.markdown("---")
    if tabs == "Apriori":
        st.write(f"## Apriori Association Rule Explorer")
        st.sidebar.header("Filter Options")
        min_support = st.sidebar.slider("Min Support", 0.0, 0.008, 0.001, 0.001)
        min_confidence = st.sidebar.slider("Min Confidence", 0.0, 0.3, 0.05, 0.01)
        min_lift = st.sidebar.slider("Min Lift", 0.0, 2.18, 0.5, 0.1)

        filtered_rules = apr_rules[
            (apr_rules['support'] >= min_support) &
            (apr_rules['confidence'] >= min_confidence) &
            (apr_rules['lift'] >= min_lift)
        ]

        st.write(f"### {len(filtered_rules)} Apriori Rules Found")
        st.write(f'##### Minimum Support: {min_support}, Minimum Confidence: {min_confidence} and Minimum Lift: {min_lift}')
        st.dataframe(filtered_rules)

        st.write("### Lift vs. Confidence Plot")
        fig = px.scatter(
            filtered_rules,
            x="confidence",
            y="lift",
            color="support",
            color_continuous_scale="viridis",
            labels={"confidence": "Confidence", "lift": "Lift", "support": "Support"},
            title="Apriori Association Rule Metrics"
        )
        st.plotly_chart(fig)

    elif tabs == "FP Growth":
        st.write(f"## FP Growth Association Rule Explorer")
        st.sidebar.header("Filter Options")
        min_support = st.sidebar.slider("Min Support", 0.0, 0.008, 0.001, 0.001)
        min_confidence = st.sidebar.slider("Min Confidence", 0.0, 0.3, 0.05, 0.01)
        min_lift = st.sidebar.slider("Min Lift", 0.0, 2.18, 0.5, 0.1)


        filtered_rules = fp_rules[
            (fp_rules['support'] >= min_support) &
            (fp_rules['confidence'] >= min_confidence) &
            (fp_rules['lift'] >= min_lift)
        ]

        st.write(f"### {len(filtered_rules)} FP Growth Rules Found")
        st.write(f'##### Minimum Support: {min_support}, Minimum Confidence: {min_confidence} and Minimum Lift: {min_lift}')
        st.dataframe(filtered_rules)

        st.write("### Lift vs. Confidence Plot")
        fig = px.scatter(
            filtered_rules,
            x="confidence",
            y="lift",
            color="support",
            color_continuous_scale="viridis",
            labels={"confidence": "Confidence", "lift": "Lift", "support": "Support"},
            title="FP Growth Association Rule Metrics"
        )
        st.plotly_chart(fig)


plot_descriptions = {
    "Count of Customers vs Items in Basket": """
    Here, we can see 2 is the most frequent basket size and basket size above 6 are almost rare.
    """,

    "Items Sold Per Year": """
    Sales increased in 2015 as compared to 2014.
    """,

    "Most Purchased Items": """
    Milk and Vegetables are most purchased items.
    """,

    "Number of Items Sold Per Day": """
    1. **Fluctuating Sales**: The number of items sold daily varies significantly, ranging approximately from **20 to 100 items per day**. 
    2. **No Strong Trend**: There doesn't appear to be a clear upward or downward trend in the number of items sold over time. The sales seem to oscillate randomly within the range.
    3. **Seasonality**: There might be some **seasonal patterns**, as occasional spikes can be observed during certain periods (e.g., beginning of 2015). However, the patterns are not immediately obvious from this graph alone.
    4. **Sales Peaks**: There are noticeable spikes where sales exceed **90 items per day**. These may indicate specific events, promotions, or external factors influencing higher sales.
    5. **Steady Base Level**: Despite fluctuations, the daily sales hover mostly between **40 and 70 items per day**, suggesting a relatively stable baseline demand.
    """,

    "Number of Items Sold Per Month": """
    The sales in some particular months have been higher.
    """,

    "Number of Items Sold in 2014 and 2015": """
    There seems a positive small correlation between sales in 2014 and 2015 indicates a moderate positive correlation, it suggests that as sales in 2014 increased, sales in 2015 also tended to increase.

    The sales patterns in 2014 and 2015 may be influenced by similar factors, such as market trends, customer preferences, or seasonality. However, other factors also contribute, as the correlation is not very high.
    """,

    "Number of Times Each Item Was Sold": """
    There are some items who have been sold more than 75 times than of others.
    """,

    "Top Customers by Number of Items Purchased": """
    A customer who has bought 25-35 items in last year is a top customer.
    """
}



# Plot Section
if menu == "Plots and Analysis":
    st.header("Plots and Analysis")

    plot_options = ["Count of Customers vs Items in Basket", "Items Sold Per Year", "Most Purchased Items",
                    "Number of Items Sold Per Day", "Number of Items Sold Per Month",
                    "Number of Items Sold in 2014 and 2015", "Number of Times Each Item Was Sold",
                    "Top Customers by Number of Items Purchased"]
    
    plot_choice = st.selectbox("#### Select a Plot", plot_options)
    
    plot_path = f"Plots/{plot_choice}.html"
    
    st.components.v1.html(open(plot_path, 'r').read(), height=450)

    st.markdown(plot_descriptions[plot_choice])
