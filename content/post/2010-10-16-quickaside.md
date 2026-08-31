---
layout: post
title: "quick aside"
date: 2010-10-16T00:00:00
categories: Blog
author: Owen McManus
---

just a quick aside.

Before I put up my post on randomization in video games, I thought I should make a comment on the latest build of "<a href="../stuff/colorGame/WebPlayer.html" style="">colour game</a>" (working title).

The latest build of the game is up. I had previously, incrementally updated the graphics every few builds... in this build I ripped them out entirely. Every object in the game is represented by some primitive (sphere, cube, etc.).

I found that I couldn't even look at the game without wanting to change something about the visual state of that nonsense. I like working on the art side. I find modelling enjoyable, and photoshop can be downright relaxing, even under deadlines. Even thought the art wasn't even 20% of the way completed, I just couldn't stop thinking about it. It was definitely having an effect on how much thought and effort I put into the code and game play. The solution was simple. Remove art from the prototype. Any art and graphic design I do for the game is now on paper or modeled separately and not imported into the game. This also forced me to create a more clean and clear hierarchy structure for all my game assets that lets me swap out the primitives with finished models fairly trivially.  Good stuff.

I'm pretty sure that this is the way I will prefer to work moving forward. When I used to do vinyl vehicle wraps and decals we always used the nastiest magenta illustrator could muster as the stand in colour. If the area was part of the design that was supposed to be cut out, or just an area where the artwork wasn't complete, it would always be that terrible magenta. The reasoning was that if whoever was running the printer at the time saw that they would know not to print the file, because no client would ever want that colour on their vehicle. Valve uses a similar approach in level design by building everything out of orange boxes. If I could find something to use more hideous than a flat lit cube as my stand in prototyping object, I would.

I also spent the last month just stripping the game down to the nuts and rebuilding most of it from scratch. It really didn't take very long, since I work on this less than an hour a day most weeks. Less on other weeks. I had learned quite a lot building everything the first few times, so it was time to toss out all the, sprawling, old broken code and write some new, tidier, marginally less broken code.

Next post:

a thoroughly absorbing and delightful mess of pedantic nerdy bullshit.

<strong style="">Randomization</strong>
