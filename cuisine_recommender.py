# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:19:25 2023

@author: Stella Massa Rebolledo

"""


import pandas as pd
import json
import apyori


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

'''   --------------    Loading And Analysis of the Data   --------------   '''
path='E:/Study_Repository\Centennial College\Fall 2023\COMP 262 - NLP\Assignment #3/recipes.json'
f = open(path)
 
# returns JSON object as a dictionary
data = json.load(f)

df = pd.DataFrame(data)

# # Exploration
df.head(5)
df.info()
df.shape

# Total number of instances
df['id'].nunique()   # 39774 unique values, one for every combination of ingredients


# Total number of distinct cuisines
df['cuisine'].nunique()  #20 types of cuisines


# Table for Cuisine Type and number of recipes per type
recipes_per_cuisine = df['cuisine'].value_counts().rename('Counts').rename_axis('Cuisine').reset_index()

print (recipes_per_cuisine)

# id is a column that won't bring any benefit, so drop it
df.drop(labels='id', axis=1, inplace=True)



'''   --------------    Recipes   --------------   '''
cuisine_types = list(recipes_per_cuisine['Cuisine'])

while True: 
    user_inpt = input("What kind of cuisine you are interested in today?")
    
    if user_inpt.lower()=='exit':
        break

    if user_inpt in cuisine_types:
        ingredients_lst = list(df[df['cuisine']==user_inpt]['ingredients'])
        num_recipes = recipes_per_cuisine[recipes_per_cuisine['Cuisine']==user_inpt]['Counts'].values[0]
        support = 100/num_recipes
        confidence = 0.5    
        
        Rules = list(apyori.apriori(ingredients_lst, min_support=support, confidence=confidence))
        
        sorted_rules = sorted(Rules, key=(lambda relation_record: relation_record[1]), reverse=True)
        print("Top Ingredients: ", list(sorted_rules[0][0]))
           
        test=[]
        rl_id = []
        
        for idx,relation_record in enumerate(Rules):
            for elem in relation_record[2]:
                if elem[3]>2.0:
                    test.append(elem)
                    rl_id.append(idx)
                        
        data = {'Rule_id': rl_id, 'Rule Element': test}
        df_rules = pd.DataFrame(data)
        
        w = df_rules.groupby('Rule_id')
        #print(w.first())
        if not w.groups:
            print("No rules with lift > 2 found.")
            print("\n\n")
            
        else: 
            for indx, rule in w:
                print(f'Top-five combination ingredients with lift > 2.0 for Rule {indx}: ')
                print ('-------------------------------------')
                print(rule.iloc[:5, 1:2])
                print("\n\n")
        
               
    else:
        print(f'Please enter a different type of cuisine, we do not have recommendations for {user_inpt} food')
        print ('\n\n')
 