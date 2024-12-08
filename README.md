
# GSERP API

## Overview

The GSERP API is an open-source project designed to perform search queries on Google and return organic search results. It leverages the `requests-ip-rotator` to handle IP rotation, ensuring that requests are made from different IP addresses to avoid being blocked by Google. The API is built using Python and provides a simple interface for querying and retrieving search results.

## Features

- **IP Rotation**: Utilizes `requests-ip-rotator` to rotate IP addresses for each request.
- **Customizable Search**: Allows specifying search parameters such as country, language, location, and fields to retrieve.
- **Field Selection**: Users can choose which fields to include in the search results, such as title, link, snippet, etc.
- **Error Handling**: Provides detailed error messages for invalid field selections and connection issues.

## Installation

```
pip install gserp-api
```

or from source:

```
git clone git@github.com:rushout09/gserp-api.git
cd gserp-api
python3 -m venv venv
source venv/bin/activate
pip install -r requriements.txt
```

## Usage


