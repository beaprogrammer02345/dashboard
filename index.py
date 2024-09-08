import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set the title of the app
st.title("Data Visualization Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your Dataset (CSV format)", type="csv")



# If a file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    # df = pd.read_csv(uploaded_file)
    df = pd.read_csv(uploaded_file, encoding='latin1')


    # Display the DataFrame
    st.write("### Preview of your data:", df.head())

    # Display summary statistics
    if st.checkbox("Show Summary Statistics"):
        st.write("### Summary Statistics:")
        st.write(df.describe())

    # Data Filtering
    st.write("### Filter Data:")
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Select Columns to Display", columns, default=columns)
    filtered_df = df[selected_columns]
    st.write("### Filtered Data:", filtered_df.head())

    # Select the type of plot
    st.write("### Select Visualization Type:")
    chart_type = st.selectbox("Choose the chart type", [
        "Bar Chart", "Line Chart", "Scatter Plot", "Heatmap", "Area Chart", 
        "Pie Chart", "Histogram", "Box Plot", "Violin Plot", "Pair Plot", 
        "Density Plot", "Geographical Map"
    ])

    # Plot according to the selected type
    if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Area Chart"]:
        st.write("### Select Columns for Plot:")
        x_col = st.selectbox("Choose X-axis", df.columns)
        y_col = st.selectbox("Choose Y-axis", df.columns)
        color = st.color_picker("Pick a color", "#1f77b4")
        if st.button(f"Generate {chart_type}"):
            plt.figure(figsize=(10, 5))
            if chart_type == "Bar Chart":
                sns.barplot(x=x_col, y=y_col, data=df, color=color)
            elif chart_type == "Line Chart":
                sns.lineplot(x=x_col, y=y_col, data=df, color=color)
            elif chart_type == "Scatter Plot":
                sns.scatterplot(x=x_col, y=y_col, data=df, color=color)
            elif chart_type == "Area Chart":
                plt.fill_between(df[x_col], df[y_col], color=color, alpha=0.4)
                plt.plot(df[x_col], df[y_col], color=color, alpha=0.6)

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Plot", buf, "plot.png", "image/png")

    elif chart_type == "Heatmap":
        if st.button("Generate Heatmap"):
            plt.figure(figsize=(10, 5))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm")

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Heatmap", buf, "heatmap.png", "image/png")

    elif chart_type == "Pie Chart":
        st.write("### Select Column for Pie Chart:")
        col = st.selectbox("Choose a Column", df.columns)
        if st.button("Generate Pie Chart"):
            plt.figure(figsize=(8, 8))
            plt.pie(df[col].value_counts(), labels=df[col].unique(), autopct='%1.1f%%', startangle=140)

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Pie Chart", buf, "pie_chart.png", "image/png")

    elif chart_type == "Histogram":
        st.write("### Select Column for Histogram:")
        col = st.selectbox("Choose a Column", df.columns)
        bins = st.slider("Select number of bins", min_value=10, max_value=100, value=20)
        if st.button("Generate Histogram"):
            plt.figure(figsize=(10, 5))
            plt.hist(df[col], bins=bins, color="purple", alpha=0.7)

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Histogram", buf, "histogram.png", "image/png")

    elif chart_type == "Box Plot":
        st.write("### Select Column for Box Plot:")
        col = st.selectbox("Choose a Column", df.columns)
        if st.button("Generate Box Plot"):
            plt.figure(figsize=(10, 5))
            sns.boxplot(data=df[col])

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Box Plot", buf, "box_plot.png", "image/png")

    elif chart_type == "Violin Plot":
        st.write("### Select Column for Violin Plot:")
        col = st.selectbox("Choose a Column", df.columns)
        if st.button("Generate Violin Plot"):
            plt.figure(figsize=(10, 5))
            sns.violinplot(data=df[col])

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Violin Plot", buf, "violin_plot.png", "image/png")

    elif chart_type == "Pair Plot":
        st.write("### Generating Pair Plot for Numerical Data:")
        if st.button("Generate Pair Plot"):
            sns.pairplot(df.select_dtypes(include=["float64", "int64"]))

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot()
            st.download_button("Download Pair Plot", buf, "pair_plot.png", "image/png")

    elif chart_type == "Density Plot":
        st.write("### Select Column for Density Plot:")
        col = st.selectbox("Choose a Column", df.columns)
        color = st.color_picker("Pick a color", "#1f77b4")
        if st.button("Generate Density Plot"):
            plt.figure(figsize=(10, 5))
            sns.kdeplot(df[col], shade=True, color=color)

            # Save plot to a BytesIO buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.pyplot(plt)
            st.download_button("Download Density Plot", buf, "density_plot.png", "image/png")

    elif chart_type == "Geographical Map":
        st.write("### Geographical Map:")
        st.map(df)

else:
    st.write("Please upload a CSV file to visualize the data.")
