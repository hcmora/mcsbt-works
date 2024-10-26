###
# Code exercise to practice API requests, data management and plotting
###

import requests
import logging
import time
import matplotlib.pyplot as plt
from collections import Counter

logging.getLogger().setLevel(logging.INFO)

# Define an auxiliary function for the GET requests


def get_from_poke_api(endpoint: str = None, poke_id: str = None) -> dict:

    base_url = 'https://pokeapi.co/api/v2'
    url = base_url + '/' + endpoint + '/' + \
        poke_id if poke_id is not None else base_url + '/' + endpoint

    response = requests.get(url=url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        logging.warning('Could not obtain information from Pokemon API.')
        return None


# Get all the data necessary to work with. That is, get all the pokemon types available, and then get the pokemons from all those types
number_of_pokemons = 251
sleep_time = .5
pokemon_types_response = get_from_poke_api(endpoint='type')
pokemon_types = pokemon_types_response.get('results')
pokemon_with_types = {}

if pokemon_types is not None:
    for poke_type in pokemon_types:
        type_name = poke_type['name']
        pokemon_list = []
        # Get all the pokemons related to that type, and add all the pokemons associated with it to the dictionary
        # Add little sleep to give time between requests.
        time.sleep(sleep_time)
        pokemon_in_type_response = get_from_poke_api(
            endpoint='type', poke_id=type_name)
        pokemons = pokemon_in_type_response['pokemon']
        for pokemon in pokemons:
            id_value = pokemon['pokemon']['url'].rstrip('/').split('/')[-1]
            # Only check the first 251 pokemons, that is, until gen 2
            if int(id_value) <= number_of_pokemons:
                # Check if pokemon has been saved in the dictionary with a type. If not, add it directly, if it's already saved, add the secondary type
                if pokemon_with_types.get(pokemon['pokemon']['name']) is None:
                    pokemon_with_types[pokemon['pokemon']['name']] = type_name
                else:
                    pokemon_with_types[pokemon['pokemon']['name']
                                       ] = pokemon_with_types[pokemon['pokemon']['name']] + '-' + type_name
logging.info(f'The pokemon dictionary build is: {pokemon_with_types}')

# Count how much each value is repeated
value_counts = Counter(pokemon_with_types.values())
logging.info(f'Value counts is {value_counts}')

# Prepare the data for the pie chart
labels = [f"{value} ({count})" for value, count in value_counts.items()]
sizes = [count for count in value_counts.values()]

# # Plot the pie chart
# plt.figure(figsize=(8, 8))
# plt.pie(
#     sizes,
#     labels=labels,
#     autopct='%1.1f%%',  # display percentage
#     startangle=140
# )
# plt.title("Quantity of Pokemons by Type")
# plt.show()

# Plot a bar chart, using a color mapping appropiate for each type
sorted_counts = dict(
    sorted(value_counts.items(), key=lambda item: item[1], reverse=True))

type_colors = {
    'water': 'blue',
    'normal': 'gray',
    'fire': 'red',
    'electric': 'yellow',
    'normal-flying': 'lightgray',
    'poison': 'purple',
    'psychic': 'pink',
    'fighting': 'brown',
    'poison-grass': 'darkgreen',
    'ground': 'sienna',
    'ground-rock': 'sandybrown',
    'poison-bug': 'darkolivegreen',
    'grass': 'green',
    'fairy': 'lightpink',
    'flying-bug': 'lightgreen',
    'rock-water': 'teal',
    'bug': 'olive',
    'water-psychic': 'lightblue',
    'normal-fairy': 'lavender',
    'flying-fire': 'orangered',
    'flying-poison': 'violet',
    'flying-psychic': 'plum',
    'flying-grass': 'mediumseagreen',
    'poison-water': 'mediumorchid',
    'poison-ghost': 'indigo',
    'water-ice': 'deepskyblue',
    'grass-psychic': 'mediumspringgreen',
    'flying-water': 'skyblue',
    'flying-ice': 'lightsteelblue',
    'poison-ground': 'darkkhaki',
    'ground-water': 'cadetblue',
    'ground-ice': 'lightcyan',
    'bug-grass': 'darkseagreen',
    'bug-steel': 'darkslategray',
    'steel-electric': 'gold',
    'fire-dark': 'darkred',
    'water-electric': 'aquamarine',
    'water-fairy': 'powderblue',
    'psychic-ice': 'thistle',
    'dragon': 'purple',
    'normal-psychic': 'lightgray',
    'fighting-water': 'lightsalmon',
    'fighting-bug': 'darkorange',
    'flying-rock': 'lightcoral',
    'flying-electric': 'khaki',
    'flying-dragon': 'mediumpurple',
    'flying-fairy': 'mistyrose',
    'flying-dark': 'dimgray',
    'flying-ground': 'burlywood',
    'flying-steel': 'silver',
    'ground-steel': 'lightgray',
    'rock': 'darkgoldenrod',
    'rock-bug': 'darkolivegreen',
    'rock-fire': 'firebrick',
    'rock-dark': 'black',
    'ghost': 'purple',
    'water-dragon': 'royalblue',
    'psychic-fairy': 'orchid',
    'ice-dark': 'midnightblue',
    'dark': 'black'
}

colors = [type_colors.get(type_, "gray") for type_ in sorted_counts.keys()]

plt.figure(figsize=(12, 8))
plt.bar(sorted_counts.keys(), sorted_counts.values(), color=colors)
plt.xticks(rotation=90, ha="center")
plt.title("Counts of Pokemon Types (Ordered by Frequency)")
plt.xlabel("Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
