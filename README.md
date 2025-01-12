# Magistrates of the Roman Republic

It is my belief that the first two volumes of T R S Broughton's *Magistrates of the Roman Republic* did not have its copyright renewed. No such renewal appears in the Copyright Office register for the years where it would have had to have been renewed for it not to fall into the public domain.

This project includes the images of scans of MRR vols 1–2. The images for MRR 1 are taken from HathiTrust. The images for MRR 2 were taken by a CZUR Aura overhead scanner in black-and-white mode. The scans for both were then fed into an `unpaper` pipeline for cleaning, processing, etc. A not-insubstantial amount of work has been done to clean up the scans; the images in `raw` without suffixes such as `skip` are usually rescanned or cleaned-up versions of the original scans.

The processing code is publicly available.

After processing, the images were then bunbled into a PDF (suffixed `unpaper`) and were fed into `ocrmypdf` (relying on `tesseract`). The OCR'd PDF (suffixed `ocr`) was then edited in Adobe Acrobat XI for renumbering by actual pages, image optimisation, and metadata inclusion.

See `releases` for the final PDF versions.
