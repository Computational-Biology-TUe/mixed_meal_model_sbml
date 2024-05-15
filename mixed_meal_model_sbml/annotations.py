from sbmlutils.metadata import BQB

species = {
    "glc": [
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
    "ins": [
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
    "nefa": [
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
    "tg": [
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
    "met": [ # TODO: change
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
}


compartments = {
    "plasma": [ # TODO: check and add(?)
        (BQB.IS, "ncit/C13356"),
    ],
    "gut": [  # TODO: change
        (BQB.IS, "chebi/CHEBI:6904"),
        (BQB.IS, "ncit/C61845"),
        (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
    ],
}
