Your birthday present
=====================

Sister Sara,

This is why I asked you to pick some favorite pieces of art. I wrote a little
computer program that took Van Gogh's Starry Night and Dali's The Persistence
of Memory

![](https://raw.githubusercontent.com/mccutchen/sara-birthday-gift/master/input/starrynight.gif)
![](https://raw.githubusercontent.com/mccutchen/sara-birthday-gift/master/input/dali.jpg)

… and turned them into these images:

![](https://raw.githubusercontent.com/mccutchen/sara-birthday-gift/master/gift/starry-night.png)
![](https://raw.githubusercontent.com/mccutchen/sara-birthday-gift/master/gift/persistence-of-memory.png)

I have no idea how they'll look when printed on canvas.  I hope they turned out
nicely, though!

Some technical details, if you're interested
--------------------------------------------

Every time you run the program, the output will be different. You give it an
input image and it builds a [Markov chain][markov-chain] based on the colors in
that image and uses that model to produce a different output image.

This is a horrible oversimplification, but the Markov chain basically lets me
take a color from the input image and ask what color is most likely to come
next.

So, given that, here's basically how the output image is generated:

 1. Figure out how many output colors we need (ie, the area of the output
    image, ie `width * height`)

 2. Pick a random starting color from the input image and use the Markov chain
    to generate the required number of output colors, where each subsequent
    color is statistically likely to follow the previous color.

 3. Pick a "focal point" for the output image, slightly offset from the center.
    Sort our output coordinates by their distance from this focal point. (This
    accounts for circular nature of the resulting image.)

 4. Sort the colors by their numeric value (this accounts for the transition
    from light to dark as we approach the focal point)

I hope that makes at least a little bit of sense.  Check out
[markovangelo.py][markovangelo], above, if you want to know what the code looks
like.

Also, I should note that this is a hideously inefficient way to remix an image,
but it started as a fun thought experiment and I think the results are
interesting.

And if you feel like experimenting with other images, this should be easy to
run on Akiko's new laptop.  I'd be happy to help with that, if you're
interested.

### Love,

### Brother Will


[markov-chain]: http://en.wikipedia.org/wiki/Markov_chain
[markovangelo]: https://github.com/mccutchen/sara-birthday-gift/blob/master/markovangelo.py
