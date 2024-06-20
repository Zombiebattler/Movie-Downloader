from urllib.parse import urlparse
from tqdm import tqdm
from imdb import IMDb
import requests
import os

def startup():
    if not os.path.exists('./downloads'):
        os.mkdir('./downloads')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_format(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    file_extension = os.path.splitext(filename)[1]
    file_extension = file_extension.lstrip('.')
    return file_extension

def search(title):
    ia = IMDb()
    movies = ia.search_movie(title)
    print("\n")
    for i in range(min(5, len(movies))):
        print(f"{i + 1} - {movies[i]['title']} ({movies[i].get('year', 'N/A')})")

    inp = int(input("\nChoose a movie: "))
    if 1 <= inp <= min(5, len(movies)):
        selected_movie = movies[inp - 1]
        ia.update(selected_movie)
        movie_id = selected_movie.movieID

        print(f"\n🍿 {selected_movie['title']}:")
        print(f"   Rating: {selected_movie.get('rating', 'N/A')}")
        print(f"   Runtime: {selected_movie.get('runtimes', ['N/A'])[0]} min")
        print(f"   IMDb Link: https://www.imdb.com/title/tt{movie_id}/")

        data = {"name" : f"{selected_movie['title']}","id": f"tt{movie_id}","year" : f"{selected_movie['year']}",}
        return data
    else:
        print("Invalid selection. Please choose a number from the list.")
        return False


def download_video(url, filename):
    print("\n📥 Downloading video...\n")
    try:
        filename = f"./downloads/{filename}"
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, ascii=True) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    except Exception:
        print("\n❌ Video Download Failed \n")
        input()
    print("\n✅ Download complete!\n")
    input()

def main():
    print("\n╔════════════════════════════════════════════════════╗")
    print("║               🎥 Movie Downloader 🎥               ║")
    print("║                  By zombiebattler                  ║")
    print("║           https://github.com/Zombiebattler         ║")
    print("╚════════════════════════════════════════════════════╝\n")

    url = input("Enter movie URL: ")
    data = search(input("Search movie name: "))

    if data:
        download_video(url, (f"{data['name']} ({data['year']}) [imdbid-{data['id']}].{get_format(url)}"))
    else:
        print("Error: Movie not found.")

if __name__ == '__main__':
    try:
        startup()
        while True:
            main()
            input()
            clear()
    except Exception as e:
        print(f"Critical Error:\n{e}")
