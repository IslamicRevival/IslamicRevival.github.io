---
layout: home

title: Islamic Revival - AI crowdsourcing framework for knowledge sharing & archiving
titleTemplate: Islamic Revival - AI crowdsourcing framework for knowledge sharing & archiving

hero:
  name: Islamic Revival
  text: an AI framework for Islamic media 
  tagline: to build a long-lived repository to share, archive & search Islamic books, articles, documents, video summaries, etc. through a transparent and community-based contribution policy (similar to open source software) - we are a non-commercial, non-partisan, non-sectarian site. The framework is powered by some of the latest technologies including ChatGPT 3 (Da Vinci model & Natural Language Processing for summarizing texts and audio), JavaScript VueJS 3 fronten for speed, Python 3 backend for data wrangling, AI transcription via Google’s YouTube v3 APIs, Microsoft’s GitHub for code & security tools, that combined enable a highly mature and advanced content generation, curation, delivery, hosting and searching experience.
  #image:
   # src: /quill.svg
   # alt: Vite
  actions:
    - theme: brand
      text: Add/edit content
      link: /contributing/how-to-content.html
    - theme: alt
      text: Writing guide
      link: /contributing/writing-guide.html
    - theme: brand
      text: ⭐ Searchable summarized video transcripts
      link: /blogging_theology/What_is_Truth_with_Firas_Zahabi

features:
  - icon: 🔈
    title: Fiqh & Tafseer
    details: Summaries of Prof. Dr. Muhammad AL-Massari
    link: /massari/02_-_Establishing_an_Islamic_State__Is_it_an_Obligation_(Fardh)
  - icon: 📹
    title: Blogging Theology
    details: Summaries of Paul Williams
    link:  /blogging_theology/What_is_Truth_with_Firas_Zahabi
  - icon: 🔈
    title: Mohammed Hijab
    details: Summaries of Mohammed Hijab
    link: /hijab/Controversial_Questions_to_Prof.Jonathan_Brown_and_Dr._Shadee_ElMasri_(MH_Podcast__6)
  - icon: 🙌
    title: Sapience
    details: Summaries of Hamza Tzortzis
    link: /sapience/Divine_Commands__Why_Morality_Leads_to_God
  - icon: 📕
    title: books
    details: Free docs on Tawheed, Saqeefah & more!
    link: /files/pdfs
---
<script setup>
import { withBase } from 'vitepress'
</script>

<style>
.item {
  max-width: 20%;
}
.VPHero {
  margin: auto;
  align-content: center;
  float: right;
  width: 90%;
}

.actions {
  margin: auto;
  width: 95%;
  align-content: center;
  float: right;
}

.comments-container {
  margin: auto;
  width: 80%;
  align-content: center;
  float: center;
}

</style>
