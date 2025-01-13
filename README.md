# Magistrates of the Roman Republic

It is my belief that the first two volumes of T R S Broughton's *Magistrates of the Roman Republic* [did not have its copyright renewed and are therefore in the public domain](https://guides.library.cornell.edu/copyright/publicdomain). No such renewal appears in the Copyright Office register for the years where it would have had to have been renewed for it not to fall into the public domain. It does not appear that _MRR_ 3 is yet in the public domain. If its copyright resides with the author, it will expire 70 years after Broughton's death (ie 2063).

This project includes the images of scans of _MRR_ vols 1–2. The images for _MRR_ 1 are taken from [HathiTrust](https://babel.hathitrust.org/cgi/pt?id=mdp.39015009351001). The images for _MRR_ 2 were taken by a [CZUR Aura](https://shop.czur.com/products/aura) overhead scanner in black-and-white mode. The scans for both were then fed into an `unpaper` pipeline for cleaning, processing, etc. A not-insubstantial amount of work has been done to clean up the scans; the images in `raw` without suffixes such as `skip` are usually rescanned or cleaned-up versions of the original scans.

The processing code is publicly available so that other people comment on or perhaps learn from it. Solving the problems relating to inconsistent page sizing, aspect ratio adjustment, and bothersome scan borders was not altogether trivial.

After processing, the images were then bundled into a PDF (suffixed `unpaper`) and were fed into `ocrmypdf` (relying on `tesseract`). The OCR'd PDF (suffixed `ocr`) was then edited in Adobe Acrobat XI for renumbering by actual pages, removal of missed duplicate pages, image optimisation, and metadata inclusion. Since these steps were done in Acrobat, it is not possible to entirely reproduce the release PDFs entirely progrmamatically.

See `releases` for the final PDF versions.

## Supplements (1960 and 1986)

The 1960 supplement, which is also added to the end of some editions of _MRR_ 2, was superseded by the 1986 supplement. The 1986 supplement is referred to as _MRR_ 3. It contains everything in the original 1960 supplement that was not itself rejected in the intervening years as well as more besides, totalling 294 pages. Broughton wrote in _MRR_ 3 preface (June 1986):

> [In] the more than thirty years since the original publication and more than twenty years since the appearance of the Supplement of 1960 have seen the discovery of much new evidence and a vast accumulation of studies and reviews of considerably importance... The first question, whether to prepare a Second Supplement continuing the earlier one of 1960 or to incorporate the earlier one in the new one and thus create a single Supplement, was answered in favor of a single one, in the belief that it would make the work as a whole easier to consult. The decision finds some confirmation in the number of notes in the 1960 Supplement that were found to require additions or changes.

The 1960 supplement should not be consulted due to its supersession by _MRR_ 3. I have chosen to do two things: first, because it is still in copyright, _MRR_ 3 cannot be given here to complete the set; second, because the 1960 supplement is not altogether reliable in Broughton's own considered opinion, I have opted also not to investigate its copyright status, scan it, and present it here. If you need reference it, go to a library.

## Licencing

The GPL v2 licence in this repository applies *to the code*.

The input images for _MRR_ 1 created by Google rehosted here are already in the public domain; I release the input images for _MRR_ 2 also into the public domain. All PDFs derived from those images, as well as those released on the releases tab, I also release into the public domain.

## Thanks

My thanks to those at Google who digitised _MRR_ vol 1, those at CZUR who created such an easy-to-use scanner, the `unpaper` team for producing software which can fix up all the artefacts and errors that are rather unavoidable with even easy-to-use scanners, the `ocrmypdf` team for creating such an easy-to-use OCR endpoint, and those at `tesseract` for creating the OCR software itself that can read English and Greek.

Separately, I also thank the team at the [_Digital Prosopography of the Roman Republic_](https://romanrepublic.ac.uk) who have already digitised _MRR_ and put it into a searchable web database. Someone needed to do it and they did a brilliant job of it. The only quibble I have with their work is that they do not have pinpoint citations to the page numbers for each statement.
