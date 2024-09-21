import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Помилка при завантаженні URL {url}: {e}")
        return None

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def map_function(word):
    return word.lower(), 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)
    
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    top_words = sorted_word_counts[:top_n]
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Топ {top_n} слів за частотою використання')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        word_counts = map_reduce(text)
        visualize_top_words(word_counts, top_n=10)
    else:
        print("Помилка: Не вдалося отримати текст.")
