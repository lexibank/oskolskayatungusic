from pathlib import Path
from clldutils.misc import slug
import pylexibank

SOURCES = {
    
    
    
}



# Helper functions
def get_subrow(language, header, row):
    """
    Returns a dictionary of values for just the given `language`
    from the given `row`
    """
    return dict(zip(
        [h[1] for h in header if h[0] == language],
        [row[i] for i, h in enumerate(header) if h[0] == language]
    ))


def get_best(row):
    """Selects the best form to use"""
    for k in ['IPA', 'Standard romanization', 'Basic orthography']:
        if row.get(k):
            return row[k]
    return ""


def get_source(s):
    if s in SOURCES:
        return SOURCES[s]
    elif s.split(":")[0] in SOURCES:
        return SOURCES[s.split(":")[0]]
    print("UNKNOWN SOURCE: %s" % s)
    return s



class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "oskolskayatungusic"

    # register custom data types here (or language_class, lexeme_class, cognate_class):
    #concept_class = Concept

    # define the way in which forms should be handled
    form_spec = pylexibank.FormSpec(
        first_form_only=True,
        brackets={"(": ")", "[": "]"},  # characters that function as brackets
        separators=";/,~",  # characters that split forms e.g. "a, b".
        missing_data=('?', '-', '='),  # characters that denote missing data.
        replacements=[("CASE", ""), ('...', ''), (" ", "_")],
        strip_inside_brackets=True   # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.
        to download a temporary TSV file and convert to persistent CSV:

        >>> with self.raw_dir.temp_download("http://www.example.com/e.tsv", "example.tsv") as data:
        ...     self.raw_dir.write_csv('template.csv', self.raw_dir.read_csv(data, delimiter='\t'))
        """
        self.raw_dir.xls2csv('Tungusic_dataset.xls')

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        A `pylexibank.cldf.LexibankWriter` instance is available as `args.writer`. Use the methods
        of this object to add data.
        """
        # add sources
        args.writer.add_sources()
        
        # load languages
        language_lookup = args.writer.add_languages(lookup_factory="Name")

        # load concepts
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="Name",
        )

        # load data
        data = self.raw_dir.read_csv('Tungusic_dataset.Vocabulary.csv', dicts=False)
        
        # sort out header -
        header, subhead = data.pop(0), data.pop(0)
        # fill head1 empty cells
        for i, value in enumerate(header):
            if not value:
                header[i] = header[i - 1]

        header = list(zip(header, subhead))
        # get language columns -
        languages = set([h[0] for h in header if h[0] != 'Meaning'])
        
        # iterate over rows - 
        concept = None
        for i, row in enumerate(data, 1):
            assert len(row) == len(header), 'something went wrong'
            # update concept if we have a value in row[0]
            # otherwise we are still in the previous concept
            concept = row[0] if row[0] else concept
            
            for language in languages:
                subrow = get_subrow(language, header, row)
                form = get_best(subrow)
                if form.strip():
                
                    lex = args.writer.add_forms_from_value(
                        Language_ID=language_lookup[language],
                        Parameter_ID=concepts[concept],
                        Value=form,
                        Comment=subrow["Comments"],
                        Source=get_source(subrow['References'])
                    )
                    
                    # add cognates - 
                    args.writer.add_cognate(
                        lexeme=lex[0],
                        Cognateset_ID="%s-%d" % (concepts[concept], i)
                    )


