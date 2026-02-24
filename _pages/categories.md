---
title: "Posts by Category"
permalink: /categories/
layout: page
---

{% for category in site.categories %}
## {{ category[0] | capitalize }}

{% for post in category[1] %}
- [{{ post.title }}]({{ post.url | relative_url }}) ({{ post.date | date: "%Y-%m-%d" }})
{% endfor %}
{% endfor %}
