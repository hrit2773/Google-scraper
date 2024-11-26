import requests
from bs4 import BeautifulSoup

from flask import Flask, flash,render_template,request

app= Flask(__name__)

def google_search(query, num_results=10):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    params = {
        "q": query,
        "num": num_results
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []

    for result in soup.select('.tF2Cxc'):
        title_element = result.select_one('h3')
        link_element = result.select_one('a')
        description_element = result.select_one('.VwiC3b')

        if title_element and link_element and description_element:
            results.append({
                "title": title_element.get_text(),
                "link": link_element['href'],
                "description": description_element.get_text()
            })
    
    return results


@app.route('/', methods=['GET','POST'])
def index():
    query = request.args.get('q', '')  
    page = int(request.args.get('page', 1))
    per_page = 10 

    results = google_search(query,num_results=100)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    total_pages = -(-len(results) // per_page)

    return render_template(
        'search_page.html',
        query=query,
        results=paginated_results,
        page=page,
        total_pages=total_pages
    )

if __name__=='__main__':
    app.run(debug=True)