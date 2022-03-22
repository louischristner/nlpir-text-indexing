# Text indexing

Proximity between crime movies and thriller movies.
Can we use word distribution statistics on movie scripts to understand their proximity and differences?

## How to use

To retrieve movie scripts from a IMSDb page.
```sh
python sources/script_retriever.py imsdb_page_url folder_name
```

To process scripts and generate graphics.
```sh
python sources/graph_generator.py crime_movies thriller_movies
```

## Sources

https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt
