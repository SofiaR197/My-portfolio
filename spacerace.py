import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry


sns.set(style="whitegrid")


CSV_FILE = "mission_launches.csv"


df = pd.read_csv(CSV_FILE, low_memory=False)


df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]


if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
else:
    for cand in ['launch_date', 'time']:
        if cand in df.columns:
            df['date'] = pd.to_datetime(df[cand], errors='coerce')
            break

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()


for col_hint in ['company','organization','organisation','org','operator']:
    if col_hint in df.columns:
        df['organization'] = df[col_hint].astype(str).fillna('Unknown')
        break
if 'organization' not in df.columns:
    df['organization'] = 'Unknown'


if 'mission_status' in df.columns:
    df['mission_status'] = df['mission_status'].astype(str).str.strip().str.lower()
elif 'status' in df.columns:
    df['mission_status'] = df['status'].astype(str).str.strip().str.lower()


if 'price' in df.columns:
    df['price_num'] = pd.to_numeric(df['price'].astype(str).str.replace('[^0-9.]','', regex=True), errors='coerce')
else:
    df['price_num'] = np.nan


if 'country' not in df.columns:
    if 'location' in df.columns:
        df['country'] = df['location'].astype(str).apply(lambda s: s.split(",")[-1].strip() if pd.notna(s) else '')
    else:
        df['country'] = 'Unknown'


def country_to_iso3(name):
    try:
        c = pycountry.countries.search_fuzzy(name)[0]
        return c.alpha_3
    except Exception:
        return None


success_keywords = ['success','successful','succeeded','operational','completed']
df['is_success'] = df['mission_status'].fillna('').str.lower().apply(
    lambda s: any(k in s for k in success_keywords)
)
df['mission_result'] = df['is_success'].map({True:'success', False:'failure', np.nan:'unknown'})


top_orgs = df['organization'].value_counts().head(8).index.tolist()
df_top = df[df['organization'].isin(top_orgs)]
count_year_org = df_top.groupby(['year','organization']).size().reset_index(name='launches').dropna(subset=['year'])

fig1 = px.bar(count_year_org, x='year', y='launches', color='organization',
              title='Launches by Organization (Top 8) per Year')
fig1.show()


price_by_year = df.dropna(subset=['price_num']).groupby('year')['price_num'].agg(['median','mean']).reset_index()
plt.figure(figsize=(10,5))
plt.plot(price_by_year['year'], price_by_year['median'], marker='o', label='Median')
plt.plot(price_by_year['year'], price_by_year['mean'], marker='.', linestyle='--', label='Mean')
plt.xlabel('Year'); plt.ylabel('Cost (dataset units)')
plt.title('Mission Cost Evolution Over Time')
plt.legend()
plt.show()


month_order = ['January','February','March','April','May','June','July',
               'August','September','October','November','December']
month_counts = df['month_name'].value_counts().reindex(month_order, fill_value=0)
plt.figure(figsize=(10,4))
sns.barplot(x=month_counts.index, y=month_counts.values)
plt.xticks(rotation=45)
plt.title('Launches by Month')
plt.show()


success_by_year = df.groupby('year')['is_success'].agg(['sum','count']).reset_index().dropna(subset=['year'])
success_by_year['success_rate'] = success_by_year['sum'] / success_by_year['count']
plt.figure(figsize=(10,5))
plt.plot(success_by_year['year'], success_by_year['success_rate'], marker='o')
plt.ylim(0,1)
plt.title('Mission Success Rate per Year')
plt.xlabel('Year'); plt.ylabel('Success Rate')
plt.show()


country_counts = df['country'].fillna('Unknown').value_counts().reset_index()
country_counts.columns = ['country','launches']
country_counts['iso3'] = country_counts['country'].apply(country_to_iso3)
map_df = country_counts.dropna(subset=['iso3'])
fig2 = px.choropleth(map_df, locations='iso3', color='launches',
                     hover_name='country', color_continuous_scale=px.colors.sequential.Plasma,
                     title='Total Launches by Country')
fig2.show()


top_orgs_sunburst = df['organization'].value_counts().head(10).index.tolist()
sb_df = df[df['organization'].isin(top_orgs_sunburst)].copy()
fig3 = px.sunburst(sb_df, path=['organization', 'country', 'mission_result'],
                   title='Organization -> Country -> Result')
fig3.show()


print("\n=== Summary ===")
print("Total missions:", len(df))
print("Missions with known cost:", df['price_num'].notna().sum())
print("Missions with valid date:", df['date'].notna().sum())
print("Dataset columns:", df.columns.tolist())


