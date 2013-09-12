StreamingUnzip
==============

Say you have some huge zip file full of csv files. Say it's so big that you want to
just start working on it without waiting for it to download. If they were just csv
files you would just pipe them in... but they're compressed and bunched up together.

Can you pipe them and unzip them? The open source unzip based on PKWARE's spec will
only unzip the first archive file. What do you do?!

StreamingUnzip allows you to stream the ZIP file and get at all of the entries within.
You do need to give it an end chunk of your zip archive (still smalled than
downloading the whole thing!), and then you just pipe in the file and get uncompressed
bytes out of stdout or your stream of choice.