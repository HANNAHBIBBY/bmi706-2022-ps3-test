import altair as alt
import pandas as pd
import streamlit as st


### P1.2 ###

# Move this code into `load_data` function {{
cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

df = pd.merge(left=cancer_df, right=pop_df, how="left")
df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
df.dropna(inplace=True)

df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

# }}


@st.cache
def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    # st.write("testing loaddata")
    
    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
years_all = df["Year"].drop_duplicates()

slider_year = st.slider("Select year:", min_value = min(years_all), max_value = max(years_all))

year = slider_year
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
radio_gender = st.radio("Select gender:", ["M", "F"])

sex = radio_gender
subset = subset[subset["Sex"] == sex]
### P2.2 ###

### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]

countries_all = df["Country"].drop_duplicates()

multiselect_country = st.multiselect("Select Country:", countries_all, default = countries)

subset = subset[subset["Country"].isin(multiselect_country )]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox

select_cancer = st.selectbox("Select cancer:",df["Cancer"].drop_duplicates() )

cancer = select_cancer
subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Rate", title="Mortality rate per 100k"),
    color="Country",
    tooltip=["Rate"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###



chart2 = alt.Chart(subset).mark_rect().encode(
    x=alt.X('Age:O'),
    y=alt.Y('Country:O'),
    color=alt.Color('Rate:Q', scale=alt.Scale(type='log', domain=(0.005, 1), clamp=True))
)



st.altair_chart(chart, use_container_width=True)
st.altair_chart(chart2, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
