import pandas as pd
import matplotlib.pyplot as plt


def yillik_gelir(year):
    data = pd.read_csv("database/gelir.txt", sep=' ', header=None, names=['Year', 'Month', 'Price'])

    data = data[data['Year'] == year]

    data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(day=1))

    aggregated_data = data.groupby('Date')['Price'].sum().reset_index()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(aggregated_data['Date'], aggregated_data['Price'], marker='o')
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Gelir')
    ax.set_title(f'{year} Yılının Gelir Tablosu')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    ax.grid(True)

    return fig


def yillik_gider(year):
    data = pd.read_csv("database/gider.txt", sep=' ', header=None, names=['Year', 'Month', 'Price'])

    data = data[data['Year'] == year]

    data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(day=1))

    aggregated_data = data.groupby('Date')['Price'].sum().reset_index()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(aggregated_data['Date'], aggregated_data['Price'], marker='o')
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Gider')
    ax.set_title(f'{year} Yılının Gider Tablosu')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    ax.grid(True)

    return fig


def yillik_gelir_gider(year):
    income_data = pd.read_csv("database/gelir.txt", sep=' ', header=None, names=['Year', 'Month', 'Income'])
    outcome_data = pd.read_csv("database/gider.txt", sep=' ', header=None, names=['Year', 'Month', 'Outcome'])

    income_data = income_data.groupby(['Year', 'Month']).sum().reset_index()
    outcome_data = outcome_data.groupby(['Year', 'Month']).sum().reset_index()

    merged_data = pd.merge(income_data, outcome_data, on=['Year', 'Month'], how='outer').fillna(0)

    merged_data['Difference'] = merged_data['Income'] - merged_data['Outcome']

    merged_data['Date'] = pd.to_datetime(merged_data[['Year', 'Month']].assign(day=1))

    merged_data = merged_data[merged_data['Year'] == year]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(merged_data['Date'], merged_data['Difference'], marker='o', color="red")
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Gelir - Gider')
    ax.set_title(f'{year} Yılı Gelir Gider Tablosu')
    for label in ax.get_xticklabels():
        label.set_rotation(45)

    ax.grid(True)

    return fig


def yemek_populerlik():
    # Dictionary to store food counts
    food_counts = {}

    # Open the file and read each line
    with open("database/siparisler.txt", 'r') as file:
        for line in file:
            # Split the line by comma
            parts = line.strip().split(',')
            # Extract the food items
            foods = parts[3].split('-')
            # Update the counts for each food item
            for food in foods:
                food_counts[food] = food_counts.get(food, 0) + 1

    # Plotting the food counts
    foods = list(food_counts.keys())
    counts = list(food_counts.values())

    fig = plt.figure(figsize=(10, 6))
    plt.bar(foods, counts, width=0.5)
    plt.xlabel('Yemekler')
    plt.ylabel('Satilan Adet')
    plt.title('Yemek Populerlik Tablosu')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
