# Header Image Generation — Session Handover Prompt

Copy everything below the line into a new Claude Code session.

---

## Context

I'm redesigning my Jekyll blog (Lagrange theme) on the `develop` branch in this worktree. The theme and layout work is done. What's left is generating header images for all 32 blog posts using **Gemini Nano Banana Pro** (`gemini-3-pro-image-preview`) via the `google-genai` Python SDK.

**The previous session's auto-generated images were rejected** — they had nothing to do with the article content and were the wrong format. This time we do it **one post at a time**: you draft the image prompt, I review and approve it, only then you send it to the API.

## Technical Setup

- **Model**: `gemini-3-pro-image-preview` (Gemini Nano Banana Pro)
- **SDK**: `google-genai` (already installed in venv at `/tmp/genai-venv/bin/python3`)
- **API key**: environment variable `GOOGLE_API_KEY` (I'll provide it when needed)
- **Image output**: save as PNG to `assets/img/<slug>.png`
- **Front matter**: each post already has `image: <slug>.png` — no need to update front matter
- **Aspect ratio**: Lagrange shows thumbnails with `margin-top: -11.5%; margin-bottom: -11.5%` crop, so images should be roughly **16:9** landscape
- **Blog color palette**: dark navy-slate `#2c3242`, warm brown `#8a7550`, warm beige `#d4c5a9`

## Image Style Goals

Each image should:
- Be **lively and evocative** — spark positive impression and curiosity in readers who only see the thumbnail
- Reflect the **actual content** of the article (not just the title)
- Work as a **visual teaser** that makes someone want to click and read
- Use a **clean, professional style** — no text, no words, no letters in the image
- Have a **muted but warm color palette** that harmonizes with the blog's color scheme
- Be **abstract/conceptual** or use **visual metaphors** rather than literal depictions
- Avoid generic stock-photo clichés (no handshakes, no puzzle pieces, no lightbulbs)

## Workflow for Each Post

1. **You** present the post title, summary, and your **draft prompt** for the image
2. **I** review the prompt, suggest changes or approve it
3. **Only after my approval**, you call the API and save the image
4. We move to the next post

## All 32 Posts (chronological)

### POST 1: `_posts/2009-04-22--letztlich-doch-hier.html`
- **Title**: ...letztlich doch hier
- **Lang**: DE
- **Image file**: `-letztlich-doch-hier.png`
- **Summary**: Inaugural blog post about choosing Blogger.com despite wanting to self-host. Reflects on convenience vs. data privacy, referencing Apple's 1984 commercial as a cautionary note about surveillance.

### POST 2: `_posts/2011-01-19-probleme-beim-login-ins-elster-eportal-mit-mac-os-x.html`
- **Title**: Probleme beim Login ins Elster ePortal mit Mac OS X
- **Lang**: DE
- **Image file**: `probleme-beim-login-ins-elster-eportal-mit-mac-os-x.png`
- **Summary**: Login problem with German tax filing portal (Elster ePortal) on Mac OS X — Java applet fails with 404 error. Solution: install Java for Mac OS X 10.6 Update 3.

### POST 3: `_posts/2011-02-10-umlaute-und-sonderzeichen-in-spring-roo.html`
- **Title**: Umlaute und Sonderzeichen in Spring Roo?
- **Lang**: DE
- **Image file**: `umlaute-und-sonderzeichen-in-spring-roo.png`
- **Summary**: Fixing broken German Umlauts and special characters in Spring Roo — three causes: JSP encoding, filter order in web.xml, and database connection string encoding.

### POST 4: `_posts/2011-02-13-broken-special-chars-in-spring-roo.html`
- **Title**: Broken special chars in Spring Roo internationalization?
- **Lang**: EN
- **Image file**: `broken-special-chars-in-spring-roo.png`
- **Summary**: English version of the previous post. Fixing broken special characters in Spring Roo covering JSP encoding, CharacterEncodingFilter, and DB connection encoding.

### POST 5: `_posts/2011-06-03-how-to-set-default-comment-security-level-in-atlassian-jira.html`
- **Title**: How to Set Default Comment Security Level in Atlassian JIRA
- **Lang**: EN
- **Image file**: `how-to-set-default-comment-security-level-in-atlassian-jira.png`
- **Summary**: JavaScript workaround for setting a default comment security level in JIRA 4.2+, using jQuery to programmatically control the dropdown.

### POST 6: `_posts/2011-06-05-praxistipps-zu-ftplicity.html`
- **Title**: Praxistipps zu ftplicity
- **Lang**: DE
- **Image file**: `praxistipps-zu-ftplicity.png`
- **Summary**: Practical tips for ftplicity (duplicity wrapper) for encrypted FTP backups on Linux — monitoring storage usage and understanding backup age/schedule parameters.

### POST 7: `_posts/2011-09-23-starting-photooapp-a-springroo-tutorial-application.html`
- **Title**: Starting PhotooApp - A SpringRoo tutorial application
- **Lang**: DE
- **Image file**: `starting-photooapp-a-springroo-tutorial-application.png`
- **Summary**: Introduces "PhotooApp", a server-based photo management demo built with SpringRoo 1.2.0.M1 using the Repository/DAO pattern. Lays out requirements and planned tutorial series.

### POST 8: `_posts/2011-09-25-springroo-entity-klassen-und-jpa-repositories-mit-springroo-erstellen.html`
- **Title**: SpringRoo - Entity-Klassen und JPA-Repositories mit SpringRoo erstellen
- **Lang**: DE
- **Image file**: `springroo-entity-klassen-und-jpa-repositories-mit-springroo-erstellen.png`
- **Summary**: Step-by-step tutorial on creating entity classes, JPA repositories, and services for the PhotooApp using SpringRoo shell commands, MySQL setup, and Maven/Jetty deployment.

### POST 9: `_posts/2011-10-01-iphone-wartezeit-f-r-rufumleitung-bei-abwesenheit-setzen.html`
- **Title**: iPhone - Wartezeit für Rufumleitung bei Abwesenheit setzen
- **Lang**: DE
- **Image file**: `iphone-wartezeit-f-r-rufumleitung-bei-abwesenheit-setzen.png`
- **Summary**: How to configure the call forwarding timeout on iPhone using GSM codes typed into the phone dialer, since this carrier-side setting isn't exposed in the UI.

### POST 10: `_posts/2011-10-24-springroo-howto-translate-java-exceptions-to-user-friendly-error-messages.html`
- **Title**: SpringRoo - Howto translate Java exceptions to user-friendly error messages
- **Lang**: EN
- **Image file**: `springroo-howto-translate-java-exceptions-to-user-friendly-error-messages.png`
- **Summary**: Tutorial on translating technical Java exceptions into user-friendly, internationalized error messages using a custom I18nMappingExceptionResolver in SpringRoo.

### POST 11: `_posts/2012-03-13-alternative-zu-google-vielleicht-duckduckgo.html`
- **Title**: Alternative zu Google? DuckDuckGo
- **Lang**: DE
- **Image file**: `alternative-zu-google-vielleicht-duckduckgo.png`
- **Summary**: Recommends DuckDuckGo as a privacy-respecting Google alternative. Explains setup in Firefox and features like "bangs" vs. Firefox Smart Keywords.

### POST 12: `_posts/2012-10-06-JavaOne.html`
- **Title**: Getting ready for JavaOne 2012
- **Lang**: EN
- **Image file**: `JavaOne.png`
- **Summary**: Author's first trip to the US and acceptance as speaker at Oracle JavaOne 2012 in San Francisco, presenting on Enterprise Application Integration patterns with Spring Integration.

### POST 13: `_posts/2012-10-09-JavaOne_Session-material-online.html`
- **Title**: JavaOne 2012 Session material is now available
- **Lang**: EN
- **Image file**: `JavaOne_Session-material-online.png`
- **Summary**: Oracle published recordings for all JavaOne 2012 sessions including the author's EAI patterns talk. Links to slides on GitHub and conference photos.

### POST 14: `_posts/2012-11-02-JBoss-Forge-in_IntelliJ.md`
- **Title**: JBoss Forge in IntelliJ IDEA
- **Lang**: EN
- **Image file**: `JBoss-Forge-in_IntelliJ.png`
- **Summary**: How to integrate JBoss Forge (CLI rapid-application-development shell) into IntelliJ IDEA as an External Tool, with specific Mac OS X configuration settings.

### POST 15: `_posts/2012-11-26-Productivity-for-Finder.md`
- **Title**: Enhancements for Mac OS X Finder.app
- **Lang**: EN
- **Image file**: `Productivity-for-Finder.png`
- **Summary**: Three AppleScripts for Mac OS X Finder: copy POSIX path to clipboard, open in TextWrangler, open in iTerm2. Each supports toolbar icon and drag-and-drop.

### POST 16: `_posts/2012-11-30-Ubuntu+Java-on-Nexus7.md`
- **Title**: Ubuntu and Java on Nexus7
- **Lang**: EN
- **Image file**: `Ubuntu+Java-on-Nexus7.png`
- **Summary**: Step-by-step guide for installing Ubuntu Linux and Oracle Java (JDK 7 with JavaFX) on a Google Nexus 7 tablet, covering bootloader unlock, SSH stabilization, and ARM library dependencies.

### POST 17: `_posts/2012-12-13-Glassfish4-on-Nexus7.md`
- **Title**: Glassfish 4 on Nexus7
- **Lang**: EN
- **Image file**: `Glassfish4-on-Nexus7.png`
- **Summary**: Running GlassFish 4 (Java EE app server) on the Nexus 7 tablet under Ubuntu. A WebSocket HTML5 game was deployed successfully despite limited RAM.

### POST 18: `_posts/2013-03-20-Mac-OS-X-for-java-developers.md`
- **Title**: Mac OS X setup tips & tricks
- **Lang**: EN
- **Image file**: `Mac-OS-X-for-java-developers.png`
- **Summary**: Comprehensive reference list of recommended Mac OS X apps, tools, and settings for a Java developer's workstation — system utilities, dev tools, productivity apps, QuickLook plugins, bash config.

### POST 19: `_posts/2013-04-21-collaborator-on-sonar-intellij-plugin.md`
- **Title**: Collaborator on Sonar IntelliJ Plugin
- **Lang**: EN
- **Image file**: `collaborator-on-sonar-intellij-plugin.png`
- **Summary**: Announces "Collaborator" status on the Sonar IntelliJ IDEA plugin. Describes SonarQube code analysis benefits and plans for feature parity with the Eclipse plugin.

### POST 20: `_posts/2013-04-21-speaking-at-javaforum-stuttgart.md`
- **Title**: I'm speaking at Java Forum Stuttgart 2013
- **Lang**: EN
- **Image file**: `speaking-at-javaforum-stuttgart.png`
- **Summary**: Announcement of speaking at Java Forum Stuttgart on July 4th, 2013, presenting "Enterprise Integration Patterns - Best Practices for application integration."

### POST 21: `_posts/2013-06-27-postfix-and-etc-hosts.md`
- **Title**: Postfix and /etc/hosts
- **Lang**: EN
- **Image file**: `postfix-and-etc-hosts.png`
- **Summary**: Configuring Postfix mail forwarding on a KVM host where DNS resolves the mail domain to localhost, creating a delivery loop. Fix: add VM IP to /etc/hosts and set smtp_host_lookup=native.

### POST 22: `_posts/2013-07-13-speaking-at-javaone2013.md`
- **Title**: Speaking at JavaOne 2013
- **Lang**: EN
- **Image file**: `speaking-at-javaone2013.png`
- **Summary**: Accepted to speak at JavaOne 2013 on "Enterprise Application Integration Patterns and Best Practices" (CON7969). Also highlights colleague's OpenHAB home automation talk.

### POST 23: `_posts/2013-08-06-getting-started-with-clojure.md`
- **Title**: Getting started with Clojure
- **Lang**: EN
- **Image file**: `getting-started-with-clojure.png`
- **Summary**: Beginner's guide to Clojure — Leiningen setup, IntelliJ plugins, learning via Clojure Koans, contributing to a real project. Key learnings about REPL, functional programming, Clojure syntax.

### POST 24: `_posts/2013-08-08-speaking-at-DOAG-SIG-Middleware.asciidoc`
- **Title**: DOAG SIG Middleware 2013: Enterprise Integration with GlassFish
- **Lang**: EN
- **Image file**: `speaking-at-DOAG-SIG-Middleware.png`
- **Summary**: Invited by DOAG (German Oracle Users Group) to present on "Enterprise Integration with GlassFish" at SIG Middleware in Duesseldorf.

### POST 25: `_posts/2013-09-10-First-steps-with-android.asciidoc`
- **Title**: First Steps with Android
- **Lang**: EN
- **Image file**: `First-steps-with-android.png`
- **Summary**: Experiences starting Android development — difficulties with Eclipse/Ant to Android Studio/Gradle transition, environment setup, JUnit version conflicts, and recommended testing libraries.

### POST 26: `_posts/2014-09-06-personal-reset.adoc`
- **Title**: Personal Reset
- **Lang**: EN
- **Image file**: `personal-reset.png`
- **Summary**: Reflective post about being spread too thin. Three corrective steps: write more short posts, reduce Twitter output and drop some projects, use DayOne journal for focus. Also preparing a JavaOne microservices talk.

### POST 27: `_posts/2014-10-08-innoq-company-culture.adoc`
- **Title**: Article on company culture at innoQ
- **Lang**: EN
- **Image file**: `innoq-company-culture.png`
- **Summary**: Links to an article the author wrote about company culture at innoQ on their company blog. Invites reader feedback on writing style and content.

### POST 28: `_posts/2015-01-31-migrate-owncloud.adoc`
- **Title**: Migrate Owncloud from PostgreSQL to MySQL
- **Lang**: EN
- **Image file**: `migrate-owncloud.png`
- **Summary**: Persistent Doctrine DBAL/PostgreSQL errors in ownCloud during file scanning. Solution: migrate to MySQL using ownCloud's built-in `db:convert-type` command.

### POST 29: `_posts/2015-05-08-per-request-debugging-with-log4j2.adoc`
- **Title**: Per request debugging with Log4j 2 filters
- **Lang**: EN
- **Image file**: `per-request-debugging-with-log4j2.png`
- **Summary**: Enable TRACE-level logging per HTTP request in production using Log4j 2's DynamicThresholdFilter. Uses a custom HTTP header extracted into ThreadContext for targeted debug logging without affecting system performance.

### POST 30: `_posts/2016-12-12-innovation-tokens-jaxenter.adoc`
- **Title**: Article on Innovation Tokens at jaxenter
- **Lang**: EN
- **Image file**: `innovation-tokens-jaxenter.png`
- **Summary**: Republication of a German article about "Innovation Tokens" on jaxenter.de — how Innovation Tokens help deal with technology overload and romanticism in IT decisions.

### POST 31: `_posts/2016-12-22-owncloud-updates-between-multiple-major-versions.adoc`
- **Title**: Owncloud 8 upgrade to 10: how to skip Major Versions
- **Lang**: EN
- **Image file**: `owncloud-updates-between-multiple-major-versions.png`
- **Summary**: Ubuntu upgrade accidentally deleted ownCloud PHP files and jumped from v8 to v10. Fix: downgrade to 8.2 using owncloud-files package, then step-by-step upgrade through 9.0 to stable.

### POST 32: `_posts/2023-10-01-why-small-experiments.md`
- **Title**: Why Small Experiments can help to overcome Innovator's Dilemma
- **Lang**: EN
- **Image file**: `why-small-experiments.png`
- **Summary**: Organizational management essay arguing "Small Experiments" (hypothesis-driven tests with tightly scoped questions) help manage uncertainty and enable innovation in larger organizations. Keeping scope small reduces costs, cognitive load, and risk while increasing trust.

## Python snippet for generating a single image

```python
import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

prompt = "YOUR APPROVED PROMPT HERE"

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

for part in response.parts:
    if part.inline_data is not None:
        img = part.as_image()
        img.save("assets/img/SLUG.png")
        print("Saved!")
        break
```

Run with: `GOOGLE_API_KEY=... /tmp/genai-venv/bin/python3 script.py`

## Let's start

Please begin with POST 1. Show me:
1. The post title and your summary
2. Your draft image generation prompt
3. Wait for my approval before calling the API
