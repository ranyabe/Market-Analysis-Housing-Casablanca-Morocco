import pandas as pd 
import numpy as np

df = pd.read_csv(
    r"C:\Users\R.BENZARIA\Desktop\ML\Market analysis Casa\mubawab_listings.csv",
    dtype=object
)


df['Type'] = df['Type'].apply(lambda x: str(x).split(' ')[0])

df['Localisation'] = df['Localisation'].apply(lambda x: x.split('à')[0])


df = df.dropna(subset=['Price']).reset_index(drop=True)

df['Price'] = df['Price'].str.replace(r'\D+', '', regex=True)


df = df[df['Price'] != ''].reset_index(drop=True)

df['Price'] = df['Price'].astype(int)




df['Tags'] = df.Tags.apply(eval)


for i in range(len(df)):
    tags = df.loc[i,'Tags']
    to_pop = []
    for t in range(len(tags)):
        if "m²" in tags[t]:
            df.loc[i,'Area'] = tags[t]
            to_pop.append(t)

        if "Pièces" in tags[t] or "Pièce" in tags[t]:
            df.loc[i,'Rooms'] = tags[t]
            to_pop.append(t)
        if "Chambres" in tags[t] or "Chambre" in tags[t]:
            df.loc[i,'Bedrooms'] = tags[t]
            to_pop.append(t)
        if "Salles de bains" in tags[t] or "Salle de bain" in tags[t]:

            df.loc[i,'Bathrooms'] = tags[t]
            to_pop.append(t)
        if "étage" in tags[t]:
            df.loc[i,'Floor'] = tags[t]
            to_pop.append(t)

    Other_tags = list([tags[k] for k in range(len(tags)) if k not in to_pop])
    df.loc[i,'Other_tags'] = str(Other_tags)
    
df['Area'] = (
    df['Area']
      .str.replace(r'\D+', '', regex=True)  
      .astype(float)
)

df['Rooms'] = (
    df['Rooms']
      .str.replace(r'\D+', '', regex=True)
      .astype(float)
)
df['Bedrooms'] = (
    df['Bedrooms']
      .str.replace(r'\D+', '', regex=True)
      .astype(float)
)

df['Bathrooms'] = (df['Bathrooms'].str.replace(r'\D+', '', regex=True).astype(float))

df['Floor'] = (df['Floor'].str.replace(r'\D+', '', regex=True).astype(float))

df = df.drop(['Tags'],axis=1).reset_index(drop = True)


df = df.replace('nan',np.nan)

missing_type = df['Type'].isna()[df['Type'].isna()].index

for idx in missing_type:
    if df.loc[idx,'Title'].lower().find('appartement') != -1:
        df.loc[idx,'Type'] = 'Appartements' 
    if df.loc[idx,'Title'].lower().find('villa') != -1:
        df.loc[idx,'Type'] = 'Villas' 
    if df.loc[idx,'Title'].lower().find('maison') != -1:
        df.loc[idx,'Type'] = 'Maisons' 
    if df.loc[idx,'Title'].lower().find('riad') != -1:
        df.loc[idx,'Type'] = 'Riad' 


df = df.dropna(subset = ['Type']).reset_index(drop = True)



df.duplicated(subset = ['Type', 'Area', 'Price', 'Localisation']).sum()
df = df.drop_duplicates(subset = ['Type', 'Area', 'Price', 'Localisation']).reset_index(drop= True)


df['Localisation'] = df.Localisation.str.strip()

df.loc[df[df['Type' ]!= 'Appartements'].index ,'Floor'] = 0


df = df.drop(['Title'],axis=1)


df['Price_m2'] = df['Price']/df['Area']


df = df.drop(['Latitude','Longitude'],axis=1)

df = df.dropna().reset_index(drop=True)

df.to_csv('mubawab_listings_clean.csv',index=False)