
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


# 5483 words
def test_forms(cldf_dataset, cldf_logger):
    assert len()[f for f in cldf_dataset['FormTable']]) == 5483


# "We detected only 17 borrowed forms in our dataset..."
def test_loans(cldf_dataset, cldf_logger):
    loans = set(
        (f['Language_ID'], f['Parameter_ID']) for f in cldf_dataset['FormTable'] if f['Loan']
    )
    loans = [f for f in cldf_dataset['FormTable'] if f['Loan']]
    for f in loans:
        print(f['ID'], f['Value'])
    assert len(loans) == 17


# "We ran a Bayesian phylogenetic analysis, using the software BEAST 2.4.7
# (Bouckaert et al. 2014), from wordlists consisting of 254 cognate-coded basic
# vocabulary items for 21 Tungusic doculects...."
def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 21


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 46


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 254


# "After excluding clear loanwords, our dataset included 1110 cognacy classes
# for 254 basic vocabulary meanings. See online Appendix 7 for the full list."
def test_cognates(cldf_dataset, cldf_logger):
    cogsets = {c['Cognateset_ID'] for c in cldf_dataset['CognateTable']}
    assert len(cogsets) == 1110