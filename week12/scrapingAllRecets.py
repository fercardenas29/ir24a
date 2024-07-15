import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random

# Lista de diferentes User-Agents para rotar
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
]

# Definir la función para realizar el scraping de Allrecipes
def scrape_allrecipes():
    base_url = 'https://www.allrecipes.com/recipes/'
    recipes = []

    def get_recipe_links(url):
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True) if '/recipe/' in a['href']]
    
    def get_all_pages_links(base_url):
        page_links = [base_url]
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        pagination = soup.find('nav', class_='category-page-list-related-nav')
        if pagination:
            page_numbers = pagination.find_all('a', class_='category-page-list-related-nav-next-button')
            last_page_number = int(page_numbers[-2].text.strip())
            for i in range(2, last_page_number + 1):
                page_links.append(f'{base_url}?page={i}')
        return page_links
    
    # Obtener enlaces a todas las páginas de listados de recetas
    all_page_links = get_all_pages_links(base_url)
    all_recipe_links = []

    # Obtener enlaces a recetas desde cada página de listados
    for page_link in all_page_links:
        print(f"Procesando página: {page_link}")
        all_recipe_links.extend(get_recipe_links(page_link))
    
    print(f"Encontrados {len(all_recipe_links)} enlaces de recetas")

    for link in all_recipe_links:
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            # Añadir un tiempo de espera aleatorio para evitar ser detectado como bot
            time.sleep(random.uniform(1, 3))
            
            # Obtener el contenido de la página de la receta
            response = requests.get(link, headers=headers)
            if response.status_code != 200:
                print(f"Error al acceder a {link}: Status code {response.status_code}")
                continue

            recipe_soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer el título de la receta desde la etiqueta <title>
            title_tag = recipe_soup.find('title')
            title = title_tag.text.strip().replace(' Recipe', '') if title_tag else 'No title'
            
            # Extraer la descripción de la receta desde el <p> con clase 'article-subheading'
            description_tag = recipe_soup.find('p', class_='article-subheading')
            description = description_tag.text.strip() if description_tag else 'No description'
            
            # Extraer los datos del script JSON
            script_tag = recipe_soup.find('script', type='application/ld+json')
            if script_tag:
                data = json.loads(script_tag.string)
                
                # Extraer los ingredientes y los pasos
                recipe = data[0] if isinstance(data, list) else data
                ingredients = recipe.get('recipeIngredient', [])
                steps = [step['text'] for step in recipe.get('recipeInstructions', []) if 'text' in step]
                
                # Almacenar los datos de la receta en la lista
                recipes.append({
                    'title': title,
                    'description': description,
                    'ingredients': ingredients,
                    'steps': steps
                })
            else:
                print(f"No se encontró script JSON en la receta {link}")
        except Exception as e:
            print(f"Error al procesar la receta en {link}: {e}")

    # Crear un DataFrame con los datos recopilados
    df = pd.DataFrame(recipes)
    return df

# Llamar a la función y mostrar los datos
df_recipes = scrape_allrecipes()
print(df_recipes.head())

# Guardar los datos en un archivo CSV
df_recipes.to_csv("allrecipes_data.csv", index=False)
