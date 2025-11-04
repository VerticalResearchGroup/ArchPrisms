Download the HTML file from acm.org for the conference (if the conference uses sessions, you might have to go and manually expand all the sessions). Use save whole page option and call this file conf.html

TOPDIR=directory with archprisms is installed


>python3 createpaperdirs.py ~/VM-Shared/acm-micro-2024.htm $TOPDIR/confname

Directory $TOPDIR/confname will be created. And each paper will get it's own directory, with url, title, abstract, pdf link in files inside respective directory.

Create a tmp directory; /tmp/confname


>python3 getallpdfs.py /tmp/confname $TOPDIR/confname

You may need to baby-sit the Selenium headless browser
At the end of this step, you'll find each paper directory will have PDFs of the paper.


>GOOGLE_API_KEY=<key> python3 generate-reviews.py $TOPDIR/prompts $TOPDIR/confname
This will run for an hour or so, depending on number of papers and create the 3 reviews for ecah paper.


