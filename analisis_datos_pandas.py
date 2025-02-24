import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo de los graficos
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Cargar el CSV
df = pd.read_csv("mercadolibre_items.csv")

# Mostrar las primeras filas
print("Primeras filas:")
print(df.head())

# Estadisticas descriptivas para variables numericas:
print("Estadisticas descriptivas:")
print(df[['price', 'initial_quantity']].describe())

# Distribucion de la condicion del producto
print("Conteo de condiciones de producto:")
print(df['condition'].value_counts())

# Grafico de distribucion de precios
plt.figure()
sns.histplot(df['price'], bins=30, kde=True, color='skyblue')
plt.title("Distribucion de precios")
plt.xlabel("Precio (ARS)")
plt.ylabel("Frecuencia")
plt.show()

# Grafico de barras para la condicion del producto
plt.figure()
sns.countplot(x='condition', data=df, palette="Set2")
plt.title("Distribucion de la condicion del producto")
plt.xlabel("Condicion")
plt.ylabel("Cantidad de productos")
plt.show()

# Revisar los primeros registros de la columna de ciudad
print("Ejemplos de ciudad (seller_address):")
print(df["seller_address"].head())

# Agrupar por ciudad y contar la cantidad de items
city_counts = df["seller_address"].value_counts().dropna()

# Grafico de barra de las top 20 ciudades con sus cantidades
top_n = 20
top_cities = city_counts.head(top_n)

plt.figure(figsize=(12, top_n * 0.3))
sns.barplot(y=top_cities.index, x=top_cities.values, palette="viridis")
plt.title(f"Top {top_n} ciudades con mas items")
plt.xlabel("Cantidad de items")
plt.ylabel("Ciudad")
plt.yticks(fontsize=8)
plt.tight_layout()
plt.show()

# Porcentaje de items por ciudad
city_percentage = (city_counts / city_counts.sum()) * 100
print("Porcentaje de items por ciudad:")
print(city_percentage)

city_counts = df["seller_address"].value_counts()
# ciudades con al menos 6 items
valid_cities = city_counts[city_counts >= 6].index  
df_filtered = df[df["seller_address"].isin(valid_cities)]
# calculo promedio
avg_price_by_city = df_filtered.groupby("seller_address")["price"].mean().sort_values(ascending=False)
print("Precio promedio de los ítems por ciudad (de mayor a menor):")
print(avg_price_by_city)

plt.figure(figsize=(12, 6))
sns.barplot(x=avg_price_by_city.index, y=avg_price_by_city.values, palette="magma")
plt.title(f"Promedio de precio por cidudad")
plt.xlabel("Ciudad")
plt.ylabel("Precio promedio (ARS)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
