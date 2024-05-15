"""Meal model."""

from pathlib import Path
import roadrunner
from sbmlutils.examples.templates import terms_of_use
from sbmlutils.factory import AssignmentRule
from sbmlutils.factory import Compartment
from sbmlutils.factory import Function
from sbmlutils.factory import Model
from sbmlutils.factory import Parameter
from sbmlutils.factory import RateRule
from sbmlutils.factory import Species
from sbmlutils.factory import ValidationOptions
from sbmlutils.factory import create_model
from sbmlutils.metadata import SBO
from mixed_meal_model_sbml import MODEL_PATH
from mixed_meal_model_sbml import annotations
from mixed_meal_model_sbml import templates


class U(templates.U):
    """UnitsDefinitions."""

    pass


plasma = "plasma"
gut = "gut"

_m = Model(
    "meal_model",
    name="Meal model",
    notes="""
    # Meal model
    """
          + terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
)

_m.compartments = [
    Compartment(
        plasma,
        4,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma"],
        unit=U.liter,
        constant=True,
        # port=True,
    ),
    # for now, we leave this compartment out
    Compartment(
        gut,
        4,
        name="gut",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["gut"],
        port=True,
    ),
]

_m.species = [
    Species("g_gut",
            gut,
            initialAmount=0.0,
            boundaryCondition=False,
            name="g_gut",
            annotations=annotations.species["glc"],
            substanceUnit=U.mg),  # du[1] [unit=u"mg"],

    Species("g_plasma",
            plasma,
            initialConcentration=5,
            boundaryCondition=False,
            name="g_plasma",
            annotations=annotations.species["glc"],
            substanceUnit=U.mmole_glucose),  # du[2] [unit=u"mmolGlucose/l"]

    Species("g_integral",
            plasma,
            initialConcentration=0.0,
            boundaryCondition=False,
            name="g_integral",
            annotations=annotations.species["glc"],
            substanceUnit=U.mmole_glucose_min),  # du[3]  G_int(t), [unit=u"(mmolGlucose*min)/l"],

    Species("I_PL",
            plasma,
            initialConcentration=18,
            boundaryCondition=False,
            name="i_plasma",
            annotations=annotations.species["ins"],
            substanceUnit=U.nano_iu_insulin), # du[4] I_plasma(t), [unit=u"μIU/ml"],

    Species("i_intestitial",
            gut,
            initialConcentration=0.0,
            boundaryCondition=False,
            name="i_intestitial",
            annotations=annotations.species["ins"],
            substanceUnit=U.nano_iu_insulin), # du[5] I_interstitial(t), [unit=u"μIU/ml"],

    Species("i_delay1",
            plasma,
            initialConcentration=18,
            boundaryCondition=False,
            name="i_delay1",
            annotations=annotations.species["ins"],
            substanceUnit=U.nano_iu_insulin), # du[6]  I_delay_1(t), [unit=u"μIU/ml"],

    Species("i_delay2",
            plasma,
            initialConcentration=18,
            boundaryCondition=False,
            name="i_delay2",
            annotations=annotations.species["ins"],
            substanceUnit=U.nano_iu_insulin), # du[7]  I_delay_2(t), [unit=u"μIU/ml"],

    Species("i_delay3",
            plasma,
            initialConcentration=18,
            boundaryCondition=False,
            name="i_delay3",
            annotations=annotations.species["ins"],
            substanceUnit=U.nano_iu_insulin), # du[8]  I_delay_3(t), [unit=u"μIU/ml"],

    Species("nefa_plasma",
            plasma,
            initialConcentration=0.33,
            boundaryCondition=False,
            name="nefa_plasma",
            annotations=annotations.species["nefa"],
            substanceUnit=U.mmole_nefa),  # du[9] NEFA_plasma(t), [unit=u"mmolNEFA/l"],

    Species("tg_gut",
            gut, initialAmount=0.0,
            boundaryCondition=False,
            name="tg_gut",
            annotations=annotations.species["tg"],
            substanceUnit=U.mg),  # du[10]  TG_gut(t), [unit=u"mg"],

    Species("tg_delay1",
            gut,
            initialConcentration=0.0,
            boundaryCondition=False,
            name="tg_delay1",
            annotations=annotations.species["tg"]),  # du[11]

    Species("tg_delay2",
            gut,
            initialConcentration=0.0,
            boundaryCondition=False,
            name="tg_delay2",
            annotations=annotations.species["tg"]),  # du[12]

    Species("tg_plasma",
            plasma,
            initialConcentration=1.3,
            boundaryCondition=False,
            name="tg_plasma",
            annotations=annotations.species["tg"],
            substanceUnit=U.mmole_tg), # du[13] TG_plasma(t), [unit=u"mmolTG/l"]
]

for s in _m.species:
    s.sboTerm = SBO.SIMPLE_CHEMICAL

_m.parameters = [
    # TODO: check sboterm
    # constants

    # model input
    Parameter("fG", 0.005551, name="f_G", unit=U.mg_per_l),
    Parameter("fTG", 0.00113, name="f_TG", unit=U.mmole_per_ml),
    Parameter("fI", 1.0, name="f_I", unit=U.to_mmole_per_l),
    # convert insulin from uIU/ml to mmol/l unit=U.to_mmole_per_l
    Parameter("tau_i", 31.0, name="tau_i", unit=U.min),
    Parameter("tau_d", 3.0, name="tau_d", unit=U.min),
    Parameter("G_threshold_pl", 9.0, name="G_th_PL", unit=U.dimensionless),
    Parameter("c1", 0.1, name="c1", unit=U.dimensionless),

    # from parameters vector
    # k1 rate constant for glucose stomach emptying (fast)[1/min]
    Parameter("k1", 0.0105, name="K1", unit=U.per_min),

    # k2 rate constant for glucose appearence from gut [1/min]
    Parameter("k2", 0.28, name="K2", unit=U.per_min),

    # k3 rate constant for suppresstion of hepatic glucose release by change of plasma glucose [1/min]
    Parameter("k3", 6.07e-3, name="K3", unit=U.per_min),

    # k4 rate constant for suppression of hepatic glucose release by delayed (remote) insulin [μmolGlucose/(μIU*min)]
    Parameter("k4", 2.35e-4, name="K4", unit=U.micro_mole_glucose_rate),

    # k5 rate constant for delayed insulin depedent uptake of glucose [μmolGlucose/(μIU*min)],
    Parameter("k5", 0.0424, name="K5", unit=U.micro_mole_glucose_rate),

    # k6 rate constant for stimulation of insulin production by the change of
    # plasma glucose concentration (beta cell funtion) [μIU/(min*μmolGlucose)],
    Parameter("k6", 2.2975, name="K6", unit=U.micro_iu_insulin_rate),

    # k7 rate constant for integral of glucose on insulin production (beta cell function) [μIU/(min*μmolGlucose)],
    Parameter("k7", 1.15, name="K7", unit=U.micro_iu_insulin_rate),

    # k8 rate constant for the simulation of insulin production by the rate of
    # change in plasma glucose concentration (beta cell function) [μIU/(min*μmolGlucose)],
    Parameter("k8", 7.27, name="K8", unit=U.micro_iu_insulin_rate),

    # k9 rate constant for outflow of insulin from plasma to interstitial space [/min],
    Parameter("k9", 3.83e-2, name="K9", unit=U.per_min),

    # k10 rate constant for degredation of insulin in remote compartment [/min],
    Parameter("k10", 2.84e-1, name="K10", unit=U.per_min),

    # gamma(sigma)
    Parameter("sigma", 1.4, name="sigma", unit=U.dimensionless),

    # sigma shape factor (appearance of meal).
    Parameter("gamma_sigma", 0.8872638175030753, name="gamma_sigma", unit=U.dimensionless),

    # KM michaelis-menten coefficient for glucose uptake [mmolGlucose/l],
    Parameter("Km", 13.2, name="KM", unit=U.mmole_glucose_per_l),

    # G_b basal plasma glucose [mmolGlucose/l]
    Parameter("G_b", 5, name="G_b", unit=U.mmole_glucose_per_l),

    # I_PL_b basal plasma glucose [μIU/ml]
    Parameter("I_pl_b", 18, name="I_PL_b", unit=U.mmole_glucose_per_l),

    # basal hepatic glucose release [mmolGlucose/(l*min)]
    Parameter("G_liv_b", 0.043, name="I_pl_b", unit=U.mmole_glucose_per_l_min),

    # triglyceride + NEFA parameters

    # spill - fractional spillover of LPL derived NEFA
    Parameter("spill", 30.0, name="spill", unit=U.dimensionless),

    # k11 - rate coeficient LPL lipolysis sips/jelic models [(mmolNEFA*ml)/(μIU*mmolTG*min)]
    Parameter("k11", 0.00045, name="K11", unit=U.lipolysis_coefficien_unit),

    # ATL_max maximum rate of ATL lipolysis in adipose tissues [mmolNEFA / (l * min)],
    Parameter("ATL_max", 0.215, name="ATL_max", unit=U.mmole_nefa_per_l_min),

    # K_ATL michealis menten coeficient for ATL lipolysis of store TG in adipose tissue [ml^2/μIU^2]
    Parameter("K_ATL", 0.0385, name="K_ATL", unit=U.ml_sqr_per_micro_iu_sqr),

    # k12 rate constanst for uptake of NEFA into tissues (currently insulin indenpendent) [/min]
    Parameter("k12", 0.0713, name="k12", unit=U.per_min),

    # tau_LPL time delay for insulin stimulation of LPL lipolysis [min]
    Parameter("tau_LPL", 208.88, name="tau_LPL", unit=U.min),

    # k13 - rate constant for stomach emptying TG(very slow) [/min]
    Parameter("k13", 0.0088, name="k13", unit=U.per_min),

    # k14 - rate constant for rate of TG appearance from gut [/min]
    Parameter("k14", 0.0163, name="k14", unit=U.per_min),

    # k15 coefficient for inhibition of TG secretion from liver by insulin [μmolTG/(min*μIU)]
    Parameter("k15", 1e-5, name="k15", unit=U.micromol_tg_per_min_microiu),

    # k16 basal secretion of TG from liver [mmolTG/(l*min)]
    Parameter("k16", 0.0119, name="k16", unit=U.mmole_tg_per_l_min),

    # input parameters (for now, test values)
    Parameter("fasting_glucose", 5, name="fasting_glucose", unit=U.mmole),
    Parameter("fasting_insulin", 18, name="fasting_insulin", unit=U.micro_iu_insulin_per_ml),
    Parameter("fasting_TG", 1.3, name="fasting_TG", unit=U.mmole),
    Parameter("fasting_NEFA", 0.33, name="fasting_NEFA", unit=U.mmole),

    Parameter("mG", 75000, name="meals_glucose_mass", unit=U.mg),
    Parameter("mTG", 60000, name="meals_tg_mass", unit=U.mg),
    Parameter("BW", 84.2, name="subject_body_mass", unit=U.kilogram),

]

for parameter in _m.parameters:
    parameter.sboTerm = SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER

# Assignment rules
_m.rules = [

    # custom functions
    # return 1 if the first argument is bigger than the second, 0 otherwise
    Function("thresholding", name="thresholding", value="lambda(x,y, piecewise(1,gt(x,y),0))"),

    AssignmentRule("VG", name="VG", value="(260/sqrt(BW/70))/1000", unit=U.volume_distribution),
    AssignmentRule("VTG", name="VTG", value="(70/sqrt(BW/70))/1000", unit=U.volume_distribution),

    # equations

    # -------
    # # glucose appearance from the meal
    # du[1] = glucose_meal_appearance(p[11], p[1], t, mG, p[2], u[1])
    # glucose_from_meal = meal_appearance(σ, k, t, M)
    # intestinal_absorption = k2 * g_gut
    # glucose_from_meal - intestinal_absorption
    AssignmentRule("G_meal",
                   name="glucose_from_meal",
                   value="(k1^sigma)*time^(sigma-1) * exp(-1*(k1*time)) * mG * (1/gamma_sigma)"),
    # equations
    AssignmentRule("intestinal_absorption",  # TODO: check name
                   name="intestinal_absorption",
                   value="k2*g_gut"),

    RateRule("g_gut",
             name="glucose_from_meal",
             value="G_meal-intestinal_absorption"),

    # # ------------------------------------
    # # glucose in the plasma
    # du[2] = plasma_glucose_flux(VG, BW, fI, fG, c1, G_threshold_pl, p, u)

    AssignmentRule("distribution_volume_correction",
                   name="distribution_volume_correction",
                   value="1/(VG*BW)"),

    AssignmentRule("unit_conversion_glucose_insulin",
                   name="unit_conversion_glucose_insulin",
                   value="1/fI"),

    # # Liver
    AssignmentRule("egp_inhibition_by_insulin",
                   name="egp_inhibition_by_insulin",
                   value="k4*i_intestitial*unit_conversion_glucose_insulin"),

    AssignmentRule("egp_inhibition_by_glucose",
                   name="egp_inhibition_by_glucose",
                   value="k3*(g_plasma-G_b)"),

    AssignmentRule("G_liver",
                   name="G_liver",
                   value="G_liv_b-egp_inhibition_by_insulin-egp_inhibition_by_glucose"),

    # # Intestines (gut)
    AssignmentRule("glucose_appearance",
                   name="glucose_appearance",
                   value="k2*g_gut"),

    AssignmentRule("G_gut",
                   name="G_gut",
                   value="glucose_appearance*distribution_volume_correction*fG"),

    # # Insulin-independent glucose utilization (maintain steady-state)
    AssignmentRule("normalized_utilization_rate",
                   name="normalized_utilization_rate",
                   value="((Km+G_b)*g_plasma)/(G_b*(Km+g_plasma))"),

    AssignmentRule("G_iid",
                   name="Insulin-independent glucose utilization",
                   value=" normalized_utilization_rate*G_liv_b"),

    # # Insulin-dependent glucose utilization
    AssignmentRule("utilization_rate",
                   name="utilization_rate",
                   value="k5*g_plasma/(Km+g_plasma)"),

    AssignmentRule("G_idp",
                   name="G_idp",
                   value="utilization_rate*i_intestitial"),

    # # Renal excretion of excess glucose
    AssignmentRule("G_ren",
                   name="G_ren",
                   value="c1*distribution_volume_correction*(g_plasma-G_threshold_pl)*thresholding(g_plasma,G_threshold_pl)"),

    RateRule("g_plasma", name="plasma_glucose_flux", value="G_liver+G_gut-G_iid-G_idp-G_ren"),

    # # ------------------------------------
    # # PID Integrator equation
    # du[3] = u[2] - p[13]
    RateRule("g_integral", name="g_integral", value="g_plasma-G_b"),

    # # ------------------------------------
    # insulin in the plasma
    # du[4] = plasma_insulin_flux(fI, tau_i, tau_d, p, u, du)

    AssignmentRule("I_proportional",
                   name="I_proportional",
                   value="k6* (g_plasma-G_b)"),

    AssignmentRule("I_integral",
                   name="I_integral",
                   value="(k7/tau_i)*(g_integral+G_b)"),

    # AssignmentRule("I_derivative",
    #                name="I_derivative",
    #                value="(k8*tau_d)*rateOf(g_plasma)"),

    AssignmentRule("I_pnc",
                   name="I_pnc",
                   value="(I_proportional+I_integral)/fI"),

    # # Pancreas

    AssignmentRule("basal_rate",
                   name="basal_rate",
                   value="((k7/tau_i)*G_b)/fI"),

    AssignmentRule("I_liv",
                   name="I_liv",
                   value="basal_rate*(I_PL/I_pl_b)"),

    # # Transport to interstitial fluid

    AssignmentRule("I_int",
                   name="I_int",
                   value="k9*(I_PL-I_pl_b)"),

    RateRule("I_PL",
             name="plasma_insulin_flux",
             value="I_pnc - I_liv - I_int"),

    # # ------------------------------------

    # # Insulin in the interstitial fluid
    # du[5] = interstitial_insulin_flux(p, u)

    AssignmentRule("degradation",
                   name="Insulin degradation",
                   value="k10*i_intestitial"),

    RateRule("i_intestitial",
             name="interstitial_insulin_flux",
             value="I_int-degradation"),

    # # ------------------------------------
    # # Insulin delays for NEFA_pl
    RateRule("i_delay1",
             name="i_delay1",
             value="3/tau_LPL*(I_PL-i_delay1)"),

    RateRule("i_delay2",
             name="i_delay2",
             value="3/tau_LPL*(i_delay1-i_delay2)"),

    RateRule("i_delay3",
             name="i_delay3",
             value="3/tau_LPL*(i_delay2-i_delay3)"),

    # # ------------------------------------
    # # plasma NEFA
    # du[9] = plasma_nefa_flux(p, u)

    # # LPL lipolysis
    AssignmentRule("LPL_lipolysis",
                   name="LPL_lipolysis",
                   value="k11*tg_plasma*i_delay3"),

    AssignmentRule("fractional_spillover",
                   name="fractional_spillover",
                   value="(1/100)*spill*(I_pl_b/i_delay1)"),

    AssignmentRule("spillover",
                   name="spillover",
                   value="3*fractional_spillover*LPL_lipolysis"),

    AssignmentRule("adipose_tg_lipolysis",
                   name="adipose_tg_lipolysis",
                   value="ATL_max/(1+K_ATL*i_delay1^2)"),

    AssignmentRule("tissue_uptake",
                   name="tissue_uptake",
                   value="k12*nefa_plasma",
                   unit=U.mmole_nefa_per_l_min),

    RateRule("nefa_plasma",
             name="plasma_nefa_flux",
             value="spillover+adipose_tg_lipolysis-tissue_uptake"),

    # # ------------------------------------
    # # Gut TG
    # du[10] = meal_appearance(sigma, k13, t, mTG) - p[23] * u[10]
    # (k13^sigma)*t^(sigma-1) * exp(-1*(k13*t)) * mTG * (1/gamma(sigma))
    RateRule("tg_gut",
             name="glucose_from_meal",
             value="(k13^sigma)*time^(sigma-1)*exp(-1*(k13*time))*mTG*(1/gamma_sigma)-k14*tg_gut"),

    # du[11] = p[23] * (u[10] - u[11])
    RateRule("tg_delay1",
             name="tg_delay1",
             value="k14*(tg_gut-tg_delay1)"),

    # du[12] = p[23] * (u[11] - u[12])
    RateRule("tg_delay2",
             name="tg_delay2",
             value="k14*(tg_delay1-tg_delay2)"),

    # # ------------------------------------
    # # plasma TG
    # du[13] = plasma_tg_flux(VTG, BW, fTG, p, u)
    AssignmentRule("distribution_volume_correction_tg",
                   name="distribution_volume_correction_tg",
                   value="1/(VTG*BW)"),
    # unit_conversion_mg_to_mM = fTG

    # # endogenous secretion of TG (in the form of VLDL)
    AssignmentRule("VLDL",
                   name="endogenous secretion of TG",
                   value="k16-k15*(i_delay3-I_pl_b)"),

    # # TG from the gut
    AssignmentRule("TG_gut",
                   name="TG from the gut",
                   value="k14*distribution_volume_correction_tg*fTG*tg_delay2"),

    RateRule("tg_plasma",
             name="plasma_tg_flux",
             value="VLDL+TG_gut-LPL_lipolysis"),

]


meal_model = _m


def simulate(sbml_path: Path):
    """Run the simulation of the model.

    Args:
        sbml_path: path to the sbml file containing the model

    Returns:
        dataframe containing the simulation results

    """
    import pandas as pd
    r: roadrunner.RoadRunner = roadrunner.RoadRunner(str(sbml_path))
    _s = r.simulate(start=0, end=500, steps=500)
    s_out = pd.DataFrame(_s, columns=_s.colnames)
    s_out.to_pickle("test_res.pkl")

    return s_out


if __name__ == "__main__":
    result = create_model(
        filepath=MODEL_PATH, model=meal_model,
        validation_options=ValidationOptions(units_consistency=True, modeling_practice=False)
    )
    simulate(result.sbml_path)
    # visualize_sbml(sbml_path=result.sbml_path, delete_session=True)
