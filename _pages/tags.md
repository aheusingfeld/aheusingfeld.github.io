---
title: "Posts by Tag"
permalink: /tags/
layout: page
---

{% for tag in site.tags %}
## {{ tag[0] }}

{% for post in tag[1] %}
- [{{ post.title }}]({{ post.url | relative_url }}) ({{ post.date | date: "%Y-%m-%d" }})
{% endfor %}
{% endfor %}
