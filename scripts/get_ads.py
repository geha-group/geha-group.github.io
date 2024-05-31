import ads
import os
import yaml
import glob
import numpy as np
import re
import bibtexparser

# get current year
from datetime import date

today = date.today()
year = today.year

journal_names = {
    r"\\aj": ["AJ", "Astronomical Journal"],
    r"\\actaa": ["Acta Astron.", "Acta Astronomica"],
    r"\\araa": ["ARA\&A", "Annual Review of Astron and Astrophys"],
    r"\\apj": ["ApJ", "Astrophysical Journal"],
    r"\\apjl": ["ApJ", "Astrophysical Journal, Letters"],
    r"\\apjs": ["ApJS", "Astrophysical Journal, Supplement"],
    r"\\ao": ["Appl.~Opt.", "Applied Optics"],
    r"\\apss": ["Ap\&SS", "Astrophysics and Space Science"],
    r"\\aap": ["A\&A", "Astronomy and Astrophysics"],
    r"\\aapr": ["A\&A~Rev.", "Astronomy and Astrophysics Reviews"],
    r"\\aaps": ["A\&AS", "Astronomy and Astrophysics, Supplement"],
    r"\\azh": ["AZh", "Astronomicheskii Zhurnal"],
    r"\\baas": ["BAAS", "Bulletin of the AAS"],
    r"\\bac": [
        "Bull. astr. Inst. Czechosl.",
        "Bulletin of the Astronomical Institutes of Czechoslovakia ",
    ],
    r"\\caa": ["Chinese Astron. Astrophys.", "Chinese Astronomy and Astrophysics"],
    r"\\cjaa": [
        "Chinese J. Astron. Astrophys.",
        "Chinese Journal of Astronomy and Astrophysics",
    ],
    r"\\icarus": ["Icarus", "Icarus"],
    r"\\jcap": [
        "J. Cosmology Astropart. Phys.",
        "Journal of Cosmology and Astroparticle Physics",
    ],
    r"\\jrasc": ["JRASC", "Journal of the RAS of Canada"],
    r"\\memras": ["MmRAS", "Memoirs of the RAS"],
    r"\\mnras": ["MNRAS", "Monthly Notices of the RAS"],
    r"\\na": ["New A", "New Astronomy"],
    r"\\nar": ["New A Rev.", "New Astronomy Review"],
    r"\\pra": ["Phys.~Rev.~A", "Physical Review A: General Physics"],
    r"\\prb": ["Phys.~Rev.~B", "Physical Review B: Solid State"],
    r"\\prc": ["Phys.~Rev.~C", "Physical Review C"],
    r"\\prd": ["Phys.~Rev.~D", "Physical Review D"],
    r"\\pre": ["Phys.~Rev.~E", "Physical Review E"],
    r"\\prl": ["Phys.~Rev.~Lett.", "Physical Review Letters"],
    r"\\pasa": ["PASA", "Publications of the Astron. Soc. of Australia"],
    r"\\pasp": ["PASP", "Publications of the ASP"],
    r"\\pasj": ["PASJ", "Publications of the ASJ"],
    r"\\rmxaa": [
        "Rev. Mexicana Astron. Astrofis.",
        "Revista Mexicana de Astronomia y Astrofisica",
    ],
    r"\\qjras": ["QJRAS", "Quarterly Journal of the RAS"],
    r"\\skytel": ["S\&T", "Sky and Telescope"],
    r"\\solphys": ["Sol.~Phys.", "Solar Physics"],
    r"\\sovast": ["Soviet~Ast.", "Soviet Astronomy"],
    r"\\ssr": ["Space~Sci.~Rev.", "Space Science Reviews"],
    r"\\zap": ["ZAp", "Zeitschrift fuer Astrophysik"],
    r"\\nat": ["Nature", "Nature"],
    r"\\iaucirc": ["IAU~Circ.", "IAU Cirulars"],
    r"\\aplett": ["Astrophys.~Lett.", "Astrophysics Letters"],
    r"\\apspr": ["Astrophys.~Space~Phys.~Res.", "Astrophysics Space Physics Research"],
    r"\\bain": [
        "Bull.~Astron.~Inst.~Netherlands",
        "Bulletin Astronomical Institute of the Netherlands",
    ],
    r"\\fcp": ["Fund.~Cosmic~Phys.", "Fundamental Cosmic Physics"],
    r"\\gca": ["Geochim.~Cosmochim.~Acta", "Geochimica Cosmochimica Acta"],
    r"\\grl": ["Geophys.~Res.~Lett.", "Geophysics Research Letters"],
    r"\\jcp": ["J.~Chem.~Phys.", "Journal of Chemical Physics"],
    r"\\jgr": ["J.~Geophys.~Res.", "Journal of Geophysics Research"],
    r"\\jqsrt": [
        "J.~Quant.~Spec.~Radiat.~Transf.",
        "Journal of Quantitiative Spectroscopy and Radiative Transfer",
    ],
    r"\\memsai": ["Mem.~Soc.~Astron.~Italiana", "Mem. Societa Astronomica Italiana"],
    r"\\nphysa": ["Nucl.~Phys.~A", "Nuclear Physics A"],
    r"\\physrep": ["Phys.~Rep.", "Physics Reports"],
    r"\\physscr": ["Phys.~Scr", "Physica Scripta"],
    r"\\planss": ["Planet.~Space~Sci.", "Planetary Space Science"],
    r"\\procspie": ["Proc.~SPIE", "Proceedings of the SPIE"],
    r"\\scpm": [
        "Sci.~China~Phys.~Mech.",
        "Science China Physics, Mechanics, and Astronomy",
    ],
}


def replace_abbreviations(bib_entry):
    for abbrev, full_name in journal_names.items():
        abbrev_formatted = r"{" + abbrev + r"}"
        bib_entry = re.sub(abbrev_formatted, r"{" + full_name[1] + r"}", bib_entry)
    return bib_entry


def make_bib(authors, outfile="scripts/most_recent_all.bib"):
    processed_bibcodes = set()
    with open(outfile, "w+") as out:
        for author in authors:
            try:
                # Search for papers by the author, sorted by publication date (most recent first)
                # First author papers

                papers = list(
                    ads.SearchQuery(
                        q=f'author:"^{author}" AND author:"Geha, Marla" doctype:(article or eprint) year:({year-2}-{year})',
                        fl=[
                            "citation_count",
                            "abbr",
                            "bibcode",
                        ],
                        sort="date desc",  # Sort by publication date in descending order
                    )
                )
                if author != "Geha, Marla":
                    # nth author papers
                    papers2 = list(
                        ads.SearchQuery(
                            q=f'author:"{author}"AND author:"Geha, Marla"doctype:(article or eprint) year: {year-2}-{year}',
                            fl=[
                                "citation_count",
                                "abbr",
                                "bibcode",
                            ],
                            sort="date desc",  # Sort by publication date in descending order
                        )
                    )
                    author_last_name = extract_last_name(author)
                    specific_author_last_name = "Geha"
                    papers2 = [
                        paper
                        for paper in papers2
                        if any(
                            extract_last_name(a) == author_last_name
                            for a in paper.author[:9]
                        )
                        and any(
                            extract_last_name(a) == specific_author_last_name
                            for a in paper.author[:9]
                        )
                    ]
                    all_papers = papers + papers2
                else:
                    all_papers = papers

                unique_papers = {paper.bibcode: paper for paper in all_papers}.values()

                # # Get the most recent papers (up to the first 3) that haven't been processed yet
                most_recent_papers = [
                    paper
                    for paper in unique_papers
                    if paper.bibcode not in processed_bibcodes
                ][:3]

                bibcodes = [paper.bibcode for paper in most_recent_papers]

                # Mark these bibcodes as processed
                processed_bibcodes.update(bibcodes)

                # Export the BibTeX entries for the most recent papers
                if bibcodes:
                    bibquery = ads.ExportQuery(bibcodes)
                    bibs = bibquery.execute()
                    bibs = replace_abbreviations(bibs)
                    out.write(bibs)
            except Exception as e:
                print(f"An error occurred for author {author}: {e}")


def extract_names_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Find the YAML front matter
    front_matter = []
    in_front_matter = False
    for line in lines:
        if line.strip() == "---":
            if not in_front_matter:
                in_front_matter = True
                continue
            else:
                break
        if in_front_matter:
            front_matter.append(line)
            # print(line)

    # Parse the YAML front matter
    front_matter_str = "".join(front_matter)
    data = yaml.safe_load(front_matter_str)
    return data.get("title")  # Assuming 'name' is the key for names


def get_names_from_collections(collection_path):
    names = []
    print(collection_path)
    # Iterate over all Markdown files in the collection
    for file_path in glob.glob(os.path.join(collection_path, "*.md")):
        name = extract_names_from_file(file_path)
        if name:
            names.append(name)
    return names


# Function to extract the last name from "Last name, First name" or "{Last name}, First name" format
def extract_last_name(full_name):
    return full_name.split(",")[0].strip("{}").strip()


# Function to highlight the author name with <strong> tags
def highlight_author_name(authors, target_last_name):
    highlighted_authors = []
    for author in authors:
        last_name = extract_last_name(author)
        if last_name == target_last_name:
            highlighted_authors.append(f"<strong>{author.strip()}</strong>")
        else:
            highlighted_authors.append(author)
    return highlighted_authors


# Function to modify the author names in a single BibTeX entry
def modify_single_bibtex_entry(entry, target_full_name):
    # Extract the last name of the target author
    target_last_name = extract_last_name(target_full_name)

    # Corrected regex pattern to capture the entire author field string
    pattern = re.compile(r"author\s*=\s*\{(.*?)\},\n", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(entry)

    # Process the matches if found
    if matches:
        author_field = matches[0]

        # Split the authors correctly considering nested braces
        authors = re.split(r"\s+and\s+", author_field)

        # Highlight the target author
        highlighted_authors = highlight_author_name(authors, target_last_name)

        highlighted_authors_str = " and ".join(highlighted_authors)
        # Replace the entire author field with the new, properly formatted authors
        new_author_field = f"author = {{{highlighted_authors_str}}},\n"
        entry = entry.replace(f"author = {{{matches[0]}}},\n", new_author_field, 1)

    return entry


# Function to modify the author names in all BibTeX entries
def modify_bibtex_author_names(bibs_content, target_full_name):
    # Split the content into individual entries
    entries = re.split(r"\n@", bibs_content)

    # Process each entry
    modified_entries = []
    for i in range(len(entries)):
        if i > 0:
            entries[i] = "@" + entries[i]  # Add back the '@' symbol removed by split
        modified_entry = modify_single_bibtex_entry(entries[i], target_full_name)
        modified_entries.append(modified_entry)

    # Join the modified entries back into a single string
    modified_bibs_content = "\n".join(modified_entries)

    return modified_bibs_content


# Function to add a custom field to the BibTeX entry if any author is 4th or later
def add_custom_field_for_additional_authors(entry, author_list):
    if "author" in entry:
        authors = [a.strip() for a in entry["author"].split(" and ")]
        additional_authors = []
        for index, author in enumerate(authors):
            last_name = extract_last_name(author)
            if last_name in [extract_last_name(a) for a in author_list] and index >= 5:
                additional_authors.append(author)
        if additional_authors:
            entry["additional_authors"] = (
                "{Includes " + ", ".join(additional_authors) + "}"
            )


# Function to process the BibTeX file
def process_bibtex_file(bib_file_path, output_file_path, author_list):
    with open(bib_file_path, "r") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for entry in bib_database.entries:
        add_custom_field_for_additional_authors(entry, author_list)

    # Manually construct the BibTeX entries to ensure the order
    with open(output_file_path, "w") as bibtex_file:
        for entry in bib_database.entries:
            bibtex_file.write("@" + entry["ENTRYTYPE"] + "{" + entry["ID"] + ",\n")
            # Write the author field first if it exists
            if "author" in entry:
                bibtex_file.write(f'  author = {{{entry["author"]}}},\n')
            # Write all other fields except additional_authors and author
            for field in entry:
                if field not in ["ENTRYTYPE", "ID", "author", "additional_authors"]:
                    bibtex_file.write(f"  {field} = {{{entry[field]}}},\n")
            # Write the additional_authors field at the end if it exists
            if "additional_authors" in entry:
                bibtex_file.write(
                    f'  additional_authors = {{{entry["additional_authors"]}}},\n'
                )
            bibtex_file.write("}\n\n")


def main():
    collections = ["_pi", "_postdocs", "_grads", "_undergrads"]
    names = np.concatenate(
        [get_names_from_collections(folder) for folder in collections]
    )
    names = [name.split(" ") for name in names]
    names = [name[-1] + ", " + name[0] for name in names]
    sorted_names = sorted(names)
    make_bib(sorted_names, outfile="scripts/most_recent_all.bib")
    process_bibtex_file(
        "scripts/most_recent_all.bib", "scripts/most_recent_all.bib", names
    )

    with open("scripts/most_recent_all.bib", "r") as file:
        bibs_content = file.read()

    for name in names:
        bibs_content = modify_bibtex_author_names(bibs_content, name)

    with open("scripts/most_recent_all.bib", "w") as file:
        file.write(bibs_content)


if __name__ == "__main__":
    main()
