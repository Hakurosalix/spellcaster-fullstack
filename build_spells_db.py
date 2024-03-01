import requests
import json
import pandas as pd
import markdown
import sqlite3

def convert_spell_data(url_end, keys_to_keep):
    spell = json.loads(requests.get(f'{url}{url_end}').text)
    spell_filtered = {}
    for key,value in keys_to_keep.items():
        spell_filtered[key] = spell[value]
    spell_filtered['Classes']=[i['name'] for i in spell['classes']]
    spell_filtered['School'] = spell['school']['name']
    spell_filtered['Classes'] = ", ".join(spell_filtered['Classes'])
    spell_filtered['Components'] = ", ".join(spell_filtered['Components'])
    spell_filtered['Description'] = markdown.markdown("\n".join(spell_filtered['Description']))
    return list(spell_filtered.values())

url = 'https://www.dnd5eapi.co'
spells = requests.get('https://www.dnd5eapi.co/api/spells')

spells_list = json.loads(spells.text)
spells_list = spells_list['results']

keys_to_keep = {'Name':'name', 'Spell_Level':'level', 'Concentration':'concentration', 'Ritual':'ritual', 'Range':'range' , 'Components':'components','Duration':'duration','Casting Time':'casting_time', 'Classes':'classes', 'School':'school','Description':'desc'} 
spellsdf = pd.DataFrame(columns= list(keys_to_keep.keys()))

for spell in spells_list:
    spellsdf.loc[len(spellsdf)] = convert_spell_data(spell['url'], keys_to_keep)

db_file = 'spellcaster.db'

conn = sqlite3.connect(db_file)
spellsdf.to_sql('spell_info',conn, index=False, if_exists='replace')

conn.close()






