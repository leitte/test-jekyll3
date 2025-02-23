import pathlib
import pandas as pd
import requests
import time
import yaml
from urllib.parse import urlparse

doi_filename = '_data/dois.csv'
metadata_dir = pathlib.Path('_data/paper_metadata')
posts_dir = pathlib.Path('_posts')

metadata_dir.mkdir(exist_ok=True)
posts_dir.mkdir(exist_ok=True)

def get_short_doi(full_doi):
    parsed_url = urlparse(full_doi)
    # If the DOI is a URL, get the path after 'doi.org/'
    if parsed_url.netloc == "doi.org":
        return parsed_url.path.lstrip("/")  # Remove the leading '/'
    return full_doi

safe_doi = lambda x: x.replace("/", "_")

df = pd.read_csv(doi_filename, names=['doi'])
df['doi'] = df.doi.apply(get_short_doi)

def download_metadata(doi):
    params = {
        "fields": "referenceCount,citationCount,title,abstract,externalIds,year,publicationDate,authors,venue"
    }
    headers = {}

    r = requests.get(
        f'https://api.semanticscholar.org/graph/v1/paper/{doi}',
        headers=headers,
        params=params,
    )

    if r.status_code == 200:
        return r.json()
    return None

existing_metadata_files = {f.name for f in metadata_dir.glob("*.yml")}

# check for each doi if we have the metadata yet
for doi in df['doi']:
    doi_safe = safe_doi(doi)
    
    if not any(doi_safe.lower() in filename.lower() for filename in existing_metadata_files):
        metadata = download_metadata(doi)
        firstAuthor_lastName = metadata['authors'][0]['name'].split(' ')[-1]
        date = metadata['publicationDate'] if metadata['publicationDate'] else f'{metadata['year']}-01-01'

        metadata_filename = metadata_dir / f'{date}_{firstAuthor_lastName}_{doi_safe}.yml'
        with open(metadata_filename, 'w') as file:
            yaml.safe_dump(metadata, file)
        time.sleep(.1)

# delete metadata that is no longer on the doi list
current_dois = df['doi'].apply(safe_doi).apply(lambda x: x.lower())
for metadata_file in metadata_dir.glob("*.yml"):
    if not any(doi in metadata_file.name.lower() for doi in current_dois):
        metadata_file.unlink()  # Delete the file
