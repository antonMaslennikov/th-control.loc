import requests

class WordPressAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def retrieve_all_publications(self):
        response = requests.get(f"{self.api_url}/wp-json/wp/v2/posts")
        if response.status_code == 200:
            publications = response.json()
            return publications
        else:
            print(f"Failed to retrieve publications. Error: {response.text}")
            return None

    def print_all_publications(self):
        publications = self.retrieve_all_publications()
        if publications is not None:
            print("All Publications:")
            for publication in publications:
                print(f"- {publication['title']['rendered']}")
