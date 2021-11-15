
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


# "We ran a Bayesian phylogenetic analysis, using the software BEAST 2.4.7
# (Bouckaert et al. 2014), from wordlists consisting of 254 cognate-coded basic
# vocabulary items for 21 Tungusic doculects...."
def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 21


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 46


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 254
