# Magistrates of the Roman Republic

This project includes the images of scans of _MRR_ vols 1–2 and the 1960 supplement.
* Images for _MRR_ 1 are from [HathiTrust](https://babel.hathitrust.org/cgi/pt?id=mdp.39015009351001). 
* Images for _MRR_ 2 were taken by a [CZUR Aura](https://shop.czur.com/products/aura) overhead scanner in black-and-white mode.
* Images for the _MRR Supplement_ (1960) are from [HathiTrust](https://babel.hathitrust.org/cgi/pt?id=mdp.39015009342562) as well.

All scans were fed into an `unpaper` pipeline for cleaning, processing, etc. A not-insubstantial amount of work has been done to clean up the scans; the images in `raw` without suffixes such as `skip` are usually rescanned or cleaned-up versions of the original scans.

The processing code is publicly available so that other people comment on or perhaps learn from it. Solving the problems relating to inconsistent page sizing, aspect ratio adjustment, and bothersome scan borders was not altogether trivial.

After processing, the images were then bundled into a PDF (suffixed `unpaper`) and were fed into `ocrmypdf` (relying on `tesseract`). The OCR'd PDF (suffixed `ocr`) was then edited in Adobe Acrobat for renumbering by actual pages, removal of missed duplicate pages, image optimisation, and metadata inclusion. Since these steps were done in Acrobat, it is not possible to entirely reproduce the release PDFs entirely programmatically.

See `releases` for the final PDF versions.

## Supplements (1960 and 1986)

The 1960 supplement, which is also added to the end of some editions of _MRR_ 2, was superseded by the 1986 supplement. The 1986 supplement is generally cited as "_MRR_ 3"; the 1960 supplement was cited as "MRR Suppl". It is essentially no longer cited, however, because the 1986 supplement entirely supersedes the 1960 supplement, including everything that was not itself rejected in the intervening years as well as more besides.

Broughton wrote in _MRR_ 3 preface (June 1986):

> [In] the more than thirty years since the original publication and more than twenty years since the appearance of the Supplement of 1960 have seen the discovery of much new evidence and a vast accumulation of studies and reviews of considerably importance... The first question, whether to prepare a Second Supplement continuing the earlier one of 1960 or to incorporate the earlier one in the new one and thus create a single Supplement, was answered in favor of a single one, in the belief that it would make the work as a whole easier to consult. The decision finds some confirmation in the number of notes in the 1960 Supplement that were found to require additions or changes.

The 1960 supplement should not be consulted due to its supersession by _MRR_ 3. 

I had initially decided not to present a copy of the 1960 supplement but after some prodding decided to do so regardless. It was pointed out that the [HathiTrust](https://babel.hathitrust.org/cgi/pt?id=mdp.39015009342562) scans are not searchable and that it would probably be preferable to present something rather than nothing.

## Copyright

It is my belief that the first two volumes of T R S Broughton's *Magistrates of the Roman Republic* [did not have its copyright renewed and are therefore in the public domain](https://guides.library.cornell.edu/copyright/publicdomain). No such renewal appears in the Copyright Office register for the years where it would have had to have been renewed for it not to fall into the public domain. I also believe the _MRR Supplement_ (1960) is in the public domain due to a lack of a copyright notice as required under then-in-force copyright law. 

It does not appear that _MRR_ 3 is yet in the public domain. If its copyright resides with the author, it will expire 70 years after Broughton's death (ie 2063).

## Licencing

The GPL v2 licence in this repository applies *to the code*.

The input images for _MRR_ 1 created by Google rehosted here are already in the public domain; I release the input images for _MRR_ 2 also into the public domain. All PDFs derived from those images, as well as those released on the releases tab, I also release into the public domain.

## Thanks

My thanks to those at Google who digitised _MRR_ vol 1, those at CZUR who created such an easy-to-use scanner, the `unpaper` team for producing software which can fix up all the artefacts and errors that are rather unavoidable with even easy-to-use scanners, the `ocrmypdf` team for creating such an easy-to-use OCR endpoint, and those at `tesseract` for creating the OCR software itself that can read English and Greek.

Separately, I also thank the team at the [_Digital Prosopography of the Roman Republic_](https://romanrepublic.ac.uk) who have already digitised _MRR_ and put it into a searchable web database. Someone needed to do it and they did a brilliant job of it. The only quibble I have with their work is that they do not have pinpoint citations to the page numbers for each statement.
