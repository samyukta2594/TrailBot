from pathlib import Path
def test():
            try:
                from googlesearch import search
            except ImportError:
                print("No module named 'google' found")
            # to search
            query = "Steven Creek Canyon"

            for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                print(j)

