from sbmlutils.examples.templates import creators as template_creators
from sbmlutils.factory import Creator
from sbmlutils.factory import ModelUnits
from sbmlutils.factory import UnitDefinition
from sbmlutils.factory import Units

micro_mole_glucose_def = "180*μg"
micro_iu_insulin_def = "34.7*μg"
micro_mole_nefa_def = "213.32*μg"
micro_mole_tg_def = "176.12*μg"

nano_iu_insulin_def = "0.0.347*μg"

mmole_glucose_def = f"{micro_mole_glucose_def}*1000"
mmole_nefa_def = f"{micro_mole_nefa_def}*1000"
mmole_tg_def = f"{micro_mole_tg_def}*1000"


class U(Units):
    """UnitDefinitions."""
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("litre_per_min", "litre/min")
    lipolysis_coefficien_unit = UnitDefinition(
        "lipolysis_coefficien_unit",
        f"{mmole_nefa_def}*ml/({micro_iu_insulin_def}*{mmole_tg_def}*min)")  # (mmolNEFA*ml)/(μIU*mmolTG*min)
    m2 = UnitDefinition("m2", "meter^2")
    mg = UnitDefinition("mg")
    mg_per_l = UnitDefinition("mg_per_l", "mg/litre")
    min = UnitDefinition("min")
    mM = UnitDefinition("mM", "mmole/liter")
    micro_iu_insulin = UnitDefinition("micro_iu_insulin", micro_iu_insulin_def)
    micro_iu_insulin_per_ml = UnitDefinition("micro_iu_insulin_per_ml",
                                             f"{micro_iu_insulin_def}/ml")
    micro_iu_insulin_rate = UnitDefinition(
        "micro_iu_insulin_rate",
        f"{micro_iu_insulin_def}/({micro_mole_glucose_def}*min)")  # μIU/(min*μmolGlucose)
    micro_mole_glucose = UnitDefinition("micro_mole_glucose", micro_mole_glucose_def)
    micro_mole_glucose_per_ml = UnitDefinition("micro_mole_glucose_per_ml",
                                               f"{micro_mole_glucose_def}/ml")
    micro_mole_glucose_rate = UnitDefinition(
        "micro_mole_glucose_rate",
        f"{micro_mole_glucose_def}/({micro_iu_insulin_def}*min)")  # μmolGlucose/(μIU*min)
    micromol_tg_per_min_microiu = UnitDefinition(
        "micromol_tg_per_min_microiu",
        f"{micro_mole_tg_def}/(min*{micro_iu_insulin_def})")  # μmolTG/(min*μIU)
    ml_sqr_per_micro_iu_sqr = UnitDefinition("ml_sqr_per_micro_iu_sqr",
                                             f"ml^2/{micro_iu_insulin_def}^2")  # ml^2/μIU^2
    mmole = UnitDefinition("mmole")
    mmole_glucose = UnitDefinition("mmole_glucose", mmole_glucose_def)
    mmole_glucose_min = UnitDefinition("mmole_glucose_min",
                                       f"{mmole_glucose_def}*min")  # mmolGlucose/l
    mmole_glucose_per_l = UnitDefinition("mmole_glucose_per_l",
                                         f"{mmole_glucose_def}/liter")  # mmolGlucose/l
    mmole_glucose_per_l_min = UnitDefinition("mmole_glucose_per_l_min",
                                             f"({mmole_glucose_def}*min)/liter")  # (mmolGlucose*min)/l
    mmole_nefa = UnitDefinition("mmole_nefa",
                                      f"{mmole_nefa_def}")  # mmolNEFA/l
    mmole_nefa_per_l = UnitDefinition("mmole_nefa_per_l",
                                      f"{mmole_nefa_def}/(liter*min)")  # mmolNEFA/l
    mmole_nefa_per_l_min = UnitDefinition("mmole_nefa_per_l_min",
                                          f"{mmole_nefa_def}/(liter*min)")  # mmolNEFA/(l*min)
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_l_min = UnitDefinition("mmole_per_l_min", "mmole/liter/min")
    mmole_per_ml = UnitDefinition("mmole_per_ml", "mmole/ml")
    mmole_tg = UnitDefinition("mmole_tg",
                                    f"{mmole_tg_def}")  # mmolTG/l
    mmole_tg_per_l = UnitDefinition("mmole_tg_per_l",
                                    f"{mmole_tg_def}/(liter)")  # mmolTG/l
    mmole_tg_per_l_min = UnitDefinition("mmole_tg_per_l_min",
                                        f"{mmole_tg_def}/(liter*min)")  # mmolTG/(l*min)
    nano_iu_insulin = UnitDefinition("nano_iu_insulin",
                                             f"{nano_iu_insulin_def}")
    per_min = UnitDefinition("per_min", "1/min")
    to_mmole_per_l = UnitDefinition(
        "to_mmole_per_l",
        f"({micro_iu_insulin_def}/ml)*((mmole*min)/({micro_iu_insulin_def}*liter))")  # μUI/ml*((mmole*ml)/(μUI*liter))
    volume_distribution = UnitDefinition("volume_distribution",
                                        "1/kilogram^2")  # mmolTG/(l*min)


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)

creators = [
               Creator(
                   familyName="O'Donovan",
                   givenName="Shauna",
                   email="s.d.odonovan@tue.nl",
                   organization="Technical University Eindhoven",
               ),
           ] + template_creators
