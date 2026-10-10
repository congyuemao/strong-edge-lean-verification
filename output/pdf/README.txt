PACKING20 PROOF MANUSCRIPT

Final deliverable: packing20_proof_manuscript.pdf
Language: English. Format: A4 mathematical manuscript. No author information.

The manuscript contains the complete mathematical argument, all five local
clique estimates, the private-neighbourhood count, the sharpness example,
references, and a correspondence with the audited Lean development.

The original Lean project and the audit evidence remain in their original
workspace directories and were not edited for this manuscript.

Files:
  packing20_manuscript.md    Editable manuscript source, using the small
                            layout directives parsed by build_manuscript.py.
  build_manuscript.py        PDF builder with embedded vector mathematics.
  check_manuscript.py        PDF and source-preservation checks.
  manuscript_build.json     Final PDF hash and typesetting information.
  manuscript_validation.json  Validation record for the delivered PDF.

To rebuild on Windows, install Python packages reportlab, matplotlib, Pillow,
pypdf, and pdfplumber, then run:
  python build_manuscript.py
  python check_manuscript.py

The builder uses Windows Times New Roman and Matplotlib STIX fonts.
It was exercised with Matplotlib 3.11.2. No TeX installation is needed.
Temporary renderings and downloaded build dependencies were removed after
visual inspection. The final PDF contains no rasterized formula images.
