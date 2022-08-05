#!/bin/sh

curl -XPUT http://es:9200/movies -H 'Content-Type: application/json' -d'
{
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "scaled_float",
                "scaling_factor": "10"
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "genre": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {
                        "type": "keyword"
                    },
                    "full_name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "actors_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "writers_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {
                        "type": "keyword"
                    },
                    "full_name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {
                        "type": "keyword"
                    },
                    "full_name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "creation_date": {
                "type": "date"
            },
            "age_rating": {
                "type": "keyword"
            },
            "url": {
                "type": "keyword"
            },
            "type": {
                "type": "keyword"
            }
        }
    }
}'


curl -XPUT http://es:9200/genres -H 'Content-Type: application/json' -d'
{
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {
                "type": "keyword"
            },
            "name": {
                "type": "keyword"
            },
            "description": {
                "type": "text"
            },
            "popularity": {
                "type": "long"
            }
        }
    }
}'


curl -XPUT http://es:9200/persons -H 'Content-Type: application/json' -d'
{
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {
                "type": "keyword"
            },
            "full_name": {
                "type": "keyword"
            },
            "role": {
                "type": "text"
            },
            "film_ids": {
                "type": "keyword"
            }
        }
    }
}'

