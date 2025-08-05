# catalog/views.py
from django.shortcuts import render
from pymongo import MongoClient

def index(request):
    client = MongoClient("mongodb://root:example@host.docker.internal:27018/")
    db = client.big_data_project
    collection = db.spaceflight_news

    articles = list(collection.find({}, {
        "_id": 0,
        "title": 1,
        "summary": 1,
        "url": 1,
        "image_url": 1,
        "news_site": 1,
        "published_at": 1,
    }).limit(20))

    return render(request, 'catalog/index.html', {"articles": articles})

def about(request):
    return render(request, 'catalog/about.html')

import re

def search(request):
    query = request.GET.get('q', '')

    articles = []
    if query:
        client = MongoClient("mongodb://root:example@host.docker.internal:27018/")
        db = client.big_data_project
        collection = db.spaceflight_news

        regex = re.compile(re.escape(query), re.IGNORECASE)
        articles = list(collection.find({"title": {"$regex": regex}}))

    context = {
        "query": query,
        "articles": articles,
        "not_found": query and not articles
    }

    return render(request, 'catalog/search.html', context)

def publishers(request):
    client = MongoClient("mongodb://root:example@host.docker.internal:27018/")
    db = client.big_data_project
    collection = db.spaceflight_news

    # Agrupar artículos por news_site
    pipeline = [
        {"$group": {
            "_id": "$news_site",
            "articles": {"$push": "$$ROOT"},
            "count": {"$sum": 1}
        }},
        {"$match": {"count": {"$gte": 3}}}
    ]

    grouped_data = list(collection.aggregate(pipeline))

    # Limitar a 5 artículos por sitio
    publishers_articles = []
    for entry in grouped_data:
        site = entry["_id"]
        articles = entry["articles"][:5]  # máximo 5
        publishers_articles.append({
            "site": site,
            "articles": articles
        })

    return render(request, 'catalog/publishers.html', {
        "publishers_articles": publishers_articles
    })


import pandas as pd
import plotly.express as px
from django.utils.safestring import mark_safe
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils.safestring import mark_safe

def dashboard(request):
    client = MongoClient("mongodb://root:example@mongo:27017/")
    db = client.big_data_project
    collection = db.spaceflight_news
    data = list(collection.find())
    df = pd.DataFrame(data)

    # Limpiar fechas
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    df = df.dropna(subset=['published_at'])

    # KPI
    total_articles = len(df)
    site_count = df['news_site'].nunique() if 'news_site' in df.columns else 0

    # Word Cloud
    wordcloud_html = ""
    if 'title' in df.columns and not df['title'].dropna().empty:
        text = " ".join(df['title'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        wordcloud_html = f"<img src='data:image/png;base64,{image_base64}' class='img-fluid'/>"

    # Pie Chart of News Sites
    pie_chart = ""
    if 'news_site' in df.columns and not df['news_site'].dropna().empty:
        site_counts = df['news_site'].value_counts()
        fig_pie = px.pie(values=site_counts.values, names=site_counts.index, title="Articles Distribution by News Site")
        pie_chart = fig_pie.to_html(full_html=False)

    # Time Series Chart
    time_series_html = ""
    if 'published_at' in df.columns and not df['published_at'].dropna().empty:
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
        published_counts = df.groupby(df['published_at'].dt.date).size()
        fig_time = px.line(x=published_counts.index, y=published_counts.values, labels={'x': 'Date', 'y': 'Articles'}, title='Articles Over Time')
        time_series_html = fig_time.to_html(full_html=False)

    # Summary Table
    summary_table = None
    if {'title', 'summary', 'url'}.issubset(df.columns):
        df_table = df[['title', 'summary', 'url']].dropna(subset=['title', 'summary', 'url'])
        summary_table = df_table.to_dict('records')

    return render(request, 'catalog/dashboard.html', {
        'total_articles': total_articles,
        'site_count': site_count,
        'wordcloud': mark_safe(wordcloud_html),
        'pie_chart': mark_safe(pie_chart),
        'time_chart': mark_safe(time_series_html),
        'summary_table': summary_table
    })
