---
title: Talks
permalink: /talks.html
layout: page
---

You can find more of [my talks at Speakerdeck](https://speakerdeck.com/u/aheusingfeld)

## Talks on this blog

{% for post in site.categories.talks %}
- [{{ post.title }}]({{ post.url | relative_url }}) ({{ post.date | date: "%Y-%m-%d" }})
{% endfor %}
