import json
from urllib.parse import urlparse, parse_qs, unquote
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from requests_ip_rotator import ApiGateway

# Valid keys for search result fields
VALID_KEYS = {"title", "link", "displayed_link", "favicon", "snippet", "source"}

# Titles to be excluded from search results
invalid_titles = ["Description"]

def search(gateway: ApiGateway, query: str, *fields, country=None, lang="en", location=None, lang_restrict=None):
    """
    Perform a search query on Google and return the organic search results.
    """

    # Validate field inputs
    if "position" in fields:
        return (
            _format_json_output({"error": "The 'position' key is not a valid choice."}),
            None,
        )
    invalid_keys = set(fields) - VALID_KEYS
    if invalid_keys:
        return (
            _format_json_output({"error": f"Invalid keys: {', '.join(invalid_keys)}"}),
            None,
        )

    # Prepare headers and gateway for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4454.0 Safari/537.36"
    }

    session = requests.Session()
    session.mount("https://www.google.com", gateway)

    # Construct search URL
    url = f"https://www.google.com/search?q={query}"
    if country:
        url += f"&gl={country}"
    if lang:
        url += f"&hl={lang}"
    if lang_restrict:
        url += f"&lr={lang_restrict}"
    if location:
        url += f"&uule={location}"

    response = None

    # Attempt to get a valid response from Google
    try:
        while True:
            try:
                response = session.get(url, headers=headers)
                if response.status_code == 200:
                    print("Received a 200 OK response!")
                    break
                print("Status Code:", response.status_code, "Switching IP...")
            except requests.exceptions.Timeout:
                print("Request timed out. Switching IP...")
            except requests.ConnectionError:
                print("Connection error. Switching IP...")
            except Exception as error:
                print("An unexpected error occurred:", error, ". Switching IP...")

        if response.status_code != 200:
            return _format_json_output({"error": "Failed to retrieve web page."})

        soup = BeautifulSoup(response.text, "html.parser")

        # Check if search results are loaded
        if not soup.select_one("div#search"):
            return {"error": "Search results not loaded."}

        search_results = []

        # Determine which fields to fetch based on input
        fetch_all = not bool(fields)
        fetch_position = "position" in fields or fetch_all
        fetch_title = "title" in fields or fetch_all
        fetch_link = "link" in fields or fetch_all
        fetch_displayed_link = "displayed_link" in fields or fetch_all
        fetch_favicon = "favicon" in fields or fetch_all
        fetch_snippet = "snippet" in fields or fetch_all
        fetch_source = "source" in fields or fetch_all

        if (
            any(
                [
                    fetch_title,
                    fetch_link,
                    fetch_displayed_link,
                    fetch_favicon,
                    fetch_snippet,
                    fetch_source,
                ]
            )
            and "position" not in fields
        ):
            fetch_position = True

        position = 0
        for result in soup.select(".tF2Cxc"):
            result_dict = OrderedDict()

            if fetch_position:
                position += 1
                result_dict["position"] = position

            # Extract information based on fields to fetch
            if fetch_title:
                title_element = result.select_one("h3")
                if title_element:
                    result_dict["title"] = title_element.get_text()

            if fetch_link:
                link_element = result.select_one("a")
                if link_element and link_element.has_attr("href"):
                    result_dict["link"] = _clean_url(link_element["href"])

            if fetch_displayed_link:
                displayed_link_element = result.select_one(".TbwUpd.NJjxre")
                if displayed_link_element:
                    result_dict["displayed_link"] = displayed_link_element.get_text()

            if fetch_favicon:
                favicon_element = result.select_one(".TbwUpd.NJjxre img")
                if favicon_element:
                    result_dict["favicon"] = favicon_element["src"]

            if fetch_snippet:
                result_dict["snippet"] = _extract_snippet(result)

            if fetch_source:
                source_element = result.select_one("cite")
                if source_element:
                    result_dict["source"] = source_element.get_text()

            if result_dict.get("title") not in invalid_titles:
                search_results.append(result_dict)

        json_result = {"organic_results": search_results}

        return _format_json_output(json_result)

    except (ConnectionError, ValueError) as exc:
        error = {"error": str(exc)}
        return error

def _format_json_output(data):
    """
    Format data into a JSON string.
    """
    return json.dumps(data, indent=4, ensure_ascii=False)

def _clean_url(url):
    """
    Clean and extract the actual URL from the query string.
    """
    parsed = urlparse(url)
    url_qs = parse_qs(parsed.query)
    if "q" in url_qs:
        return unquote(url_qs["q"][0])
    elif "url" in url_qs:
        return unquote(url_qs["url"][0])
    return url

def _extract_snippet(result_item):
    """
    Extract snippet text from a search result item.
    """
    snippet_parts = result_item.select(
        ".VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf span"
    )
    if snippet_parts:
        return " ".join(part.get_text() for part in snippet_parts)
    return ""
