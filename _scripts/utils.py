import pandas as pd
from urllib.parse import urlparse

safe_doi = lambda x: x.replace("/", "_")

def short_doi(full_doi):
    parsed_url = urlparse(full_doi)
    # If the DOI is a URL, get the path after 'doi.org/'
    if parsed_url.netloc == "doi.org":
        return parsed_url.path.lstrip("/")  # Remove the leading '/'
    return full_doi

def read_included_dois(doi_filename):
    df = pd.read_csv(doi_filename, names=['doi'])
    df['doi'] = df.doi.apply(short_doi)
    return df

def format_name(name):
    names = name.split(' ')
    return ' '.join([f'{n[0]}.' for n in names[:-1]] + names[-1:])

def format_authors(author_list: list[dict]):
    authors = [format_name(author['name']) for author in author_list]

    if not authors:
        return 'authors missing'
    elif len(authors) == 1:
        return authors[-1]
    return ', '.join(authors[:-1]) + ' & ' + authors[-1]

def get_date(metadata: dict):
    return metadata['publicationDate'] if metadata['publicationDate'] else f'{metadata['year']}-01-01'
