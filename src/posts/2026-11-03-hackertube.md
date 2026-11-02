---
title: Hackertube , A Youtube make from what Hacker News Recommends
date: 2026-11-03
tags: technology, ai, llm
---

[HackerTube](https://hackertube.org/) is a small video site that Andrej Karpathy
shared on X as a "weekend hack". It looks like YouTube, but it has one rule: a video
is on the site only because people on Hacker News kept recommending it in comments.
There is no watch-time algorithm and no account to create.

I read about it from news and blog write-ups, because I could not open the original
post on X. Anything below that comes from those reports is marked as such, and numbers
may differ a little between sources.

## What it is

- About **6,454 videos**, from 2007 to 2026, sorted into roughly **150 topics**.
- The home page, **Longs** (long videos), **Categories** and **Playlists** are the
  main ways to browse.
- **Liked**, **History** and **Watch later** are stored in your own browser, so they
  do not sync between devices.
- Thumbnails are taken from a frame in the middle of each video, not from the
  creator's thumbnail.
- Videos play through YouTube's embedded player.

## How the list was made

According to the reports, the pipeline went like this:

1. Take every Hacker News comment from 2007 to 2026 (about 43 million) and look for
   YouTube links.
2. Keep a video only if several different people linked it, in several different
   months. Roughly 7,000 videos passed this filter.
3. Let Claude read each comment together with the story it was posted under, and label
   whether the commenter recommends the video, only cites it, jokes about it, or
   criticises it. That produced about 40,000 labelled comments.
4. Let Claude write a short card for each video: a summary and why Hacker News likes
   it.
5. Rank videos by how many *separate months* they were recommended, so a video that is
   recommended for years beats one that had a single spike.

Karpathy said that Claude Opus 5.5 led the work and that it took around two hours.
He did only the parts that need a human: a Google Cloud API key, a rented server and
a domain name.

## What I find interesting

**The signal is people, not an algorithm.** "Recommended by many different people over
many years" is a good proxy for quality. It tends to surface long talks and
explanations that are still worth watching years later.

**It shows what an AI agent can build quickly.** The hard part was not the website. It
was reading tens of thousands of comments and deciding which ones mean "watch this".
That is a text-classification job that used to need a lot of manual work.

**The data is shared.** The site offers a downloadable export (videos, labelled
comments, related videos and the topic list), written so that you can hand it to your
own agent and build a different version. The reports say it is licensed under
ODC-By 1.0, which means you must credit HackerTube if you use it.

## Caveats

- The summaries and labels were written by an AI. The site itself warns that a few may
  be wrong.
- The videos come from a fixed dataset. I could not find whether new videos will be
  added.
- Hacker News readers are mostly programmers, so the list leans towards programming
  and technology.
- Check the licence and YouTube's terms before building something on top of the data.

## Try it

Open [hackertube.org](https://hackertube.org/), pick a category you like and watch one
long talk. If you want to see how a project like this is built, the data export is the
best place to start.

## Sources

- [Karpathy launches HackerTube (Pasquale Pillitteri)](https://pasqualepillitteri.it/en/news/29352/karpathy-launches-hackertube-hacker-news-videos)
- [Karpathy's HackerTube: How Claude Built It in 2 Hours (CellCog)](https://cellcog.ai/blog/karpathy-hackertube/)
- [Karpathy HackerTube: 6,454 Videos Built With Claude in 2h (ExplainX)](https://explainx.ai/blog/karpathy-hackertube-claude-opus-5-5-6454-videos-hacker-news-built-in-two-hours-2026)
- [Andrej Karpathy launches HackerTube (Crypto Briefing)](https://cryptobriefing.com/andrej-karpathy-launches-hackertube/)
