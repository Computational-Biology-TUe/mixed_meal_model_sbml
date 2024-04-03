"""Meal model."""

from pathlib import Path

from sbmlutils.factory import *
from sbmlutils.metadata import *
from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.examples.templates import terms_of_use

from mixed_meal_model_sbml import templates
from mixed_meal_model_sbml import annotations
from mixed_meal_model_sbml import MODEL_PATH

import roadrunner


class U(templates.U):
    """UnitsDefinitions."""

    pass


plasma = "Vext"
gut = "Vgut"

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
        port=True,
    ),
    # for now, we leave this compartment out
    # Compartment(
    #     gut,
    #     0,
    #     name="gut",
    #     sboTerm=SBO.PHYSICAL_COMPARTMENT,
    #     annotations=annotations.compartments["gut"],
    #     port=True,
    # ),
]

_m.species = [
    # Species(
    #     "met_ext",
    #     initialConcentration=0.0,
    #     name="metoprolol (plasma)",
    #     compartment=plasma,
    #     substanceUnit=U.mmole,
    #     hasOnlySubstanceUnits=False,
    #     sboTerm=SBO.SIMPLE_CHEMICAL,
    #     annotations=annotations.species["met"],
    #     port=True,
    # ),
    # Species("g_gut", gut, 0.0, annotations=annotations.species["glc"]),  # du[1] [unit=u"mg"],
    # Species("i_intestitial", gut, 0.0, annotations=annotations.species["ins"]),
    # # du[5] I_interstitial(t), [unit=u"μIU/ml"],
    # Species("tg_gut", gut, 0.0, annotations=annotations.species["tg"]),
    # # du[10]  TG_gut(t), [unit=u"mg"],
    # Species("tg_delay1", gut, 0.0, annotations=annotations.species["tg"]),  # du[11]
    # Species("tg_delay2", gut, 0.0, annotations=annotations.species["tg"]),  # du[12]


    Species("g_plasma", plasma, 0.0, name="g_plasma", annotations=annotations.species["glc"]),  # du[2] [unit=u"mmolGlucose/l"],
    Species("g_integral", plasma, 0.0, name="g_integral", annotations=annotations.species["glc"]),  # du[3]  G_int(t), [unit=u"(mmolGlucose*min)/l"],

    Species("i_plasma", plasma, 0.0, name="i_plasma", annotations=annotations.species["ins"]),  # du[4] I_plasma(t), [unit=u"μIU/ml"],
    Species("i_delay1", plasma, 0.0, name="i_delay1", annotations=annotations.species["ins"]),  # du[6]  I_delay_1(t), [unit=u"μIU/ml"],
    Species("i_delay2", plasma, 0.0, name="i_delay2", annotations=annotations.species["ins"]),  # du[7]  I_delay_2(t), [unit=u"μIU/ml"],
    Species("i_delay3", plasma, 0.0, name="i_delay3", annotations=annotations.species["ins"]),  # du[8]  I_delay_3(t), [unit=u"μIU/ml"],

    Species("nefa_plasma", plasma, 0.0, name="nefa_plasma", annotations=annotations.species["nefa"]),  # du[9] NEFA_plasma(t), [unit=u"mmolNEFA/l"],

    Species("tg_plasma", plasma, 0.0, name="tg_plasma", annotations=annotations.species["tg"]),  # du[13] TG_plasma(t), [unit=u"mmolTG/l"]
]

for s in _m.species:
    s.sboTerm = SBO.SIMPLE_CHEMICAL

_m.parameters = [
    # TODO: check sboterm
    # constants

    # from init matlab
    Parameter("f_G", 0.005551, name="f_G", sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER, unit=U.mg_per_l),
    Parameter("f_TG", 0.00113, name="f_TG", sboTerm=SBO.SBO_0000002, unit=U.mmole_per_ml),
    Parameter("f_I", 1.0, name="f_I", sboTerm=SBO.SBO_0000002, unit=U.to_mmole_per_l), #convert insulin from uIU/ml to mmol/l unit=U.to_mmole_per_l
    Parameter("tau_i", 31.0, name="tau_i", sboTerm=SBO.SBO_0000002, unit=U.min),
    Parameter("tau_d", 3.0, name="tau_d", sboTerm=SBO.SBO_0000002, unit=U.min),
    Parameter("G_threshold_pl", 9.0, name="G_threshold_pl", sboTerm=SBO.SBO_0000002, unit=U.dimensionless),
    Parameter("c1", 0.1, name="c1", sboTerm=SBO.SBO_0000002, unit=U.dimensionless),
    Parameter("V_G", 0.24285714285714285, name="V_G", sboTerm=SBO.SBO_0000002, unit=U.dimensionless), # TODO: change unit # [L/kg] volume of distribution for glucose
    Parameter("V_TG", 0.06, name="V_TG", sboTerm=SBO.SBO_0000002, unit=U.dimensionless),  # TODO: change unit # [L/kg]  volume of distribution of triglycerides (volume of blood)
    Parameter("t_integralwindow", 30, name="t_integralwindow", sboTerm=SBO.SBO_0000002, unit=U.dimensionless), # TODO: unit min?

    # from parameters matlab
    # glucose + insulin parameters
    Parameter("k1", 0.0105, name="K1", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k1 rate constant for glucose stomach emptying (fast)[1/min]
    Parameter("k2", 0.28, name="K2", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k2 rate constant for glucose appearence from gut [1/min]
    Parameter("k3", 6.07e-3, name="K3", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k3 rate constant for suppresstion of hepatic glucose release by change of plasma glucose [1/min]
    Parameter("k4", 2.35e-4, name="K4", sboTerm=SBO.SBO_0000002, unit=U.micro_mole_glucose_rate),  # k4 rate constant for suppression of hepatic glucose release by delayed (remote) insulin [μmolGlucose/(μIU*min)]
    Parameter("k5", 0.0424, name="K5", sboTerm=SBO.SBO_0000002, unit=U.micro_mole_glucose_rate),  # k5 rate constant for delayed insulin depedent uptake of glucose [μmolGlucose/(μIU*min)],
    Parameter("k6", 2.2975, name="K6", sboTerm=SBO.SBO_0000002, unit=U.micro_iu_insulin_rate),  # k6 rate constant for stimulation of insulin production by the change of plasma glucose concentration (beta cell funtion) [μIU/(min*μmolGlucose)],
    Parameter("k7", 1.15, name="K7", sboTerm=SBO.SBO_0000002, unit=U.micro_iu_insulin_rate),  # k7 rate constant for integral of glucose on insulin production (beta cell function) [μIU/(min*μmolGlucose)],
    Parameter("k8", 7.27, name="K8", sboTerm=SBO.SBO_0000002, unit=U.micro_iu_insulin_rate),  # k8 rate constant for the simulation of insulin production by the rate of change in plasma glucose concentration (beta cell function) [μIU/(min*μmolGlucose)],
    Parameter("k9", 3.83e-2, name="K9", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k9 rate constant for outflow of insulin from plasma to interstitial space [/min],
    Parameter("k10", 2.84e-1, name="K10", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k10 rate constant for degredation of insulin in remote compartment [/min],
    Parameter("sigma", 1.4, name="sigma", sboTerm=SBO.SBO_0000002, unit=U.dimensionless),  # sigma shape factor (appearance of meal)
    Parameter("Km", 13.2, name="Km", sboTerm=SBO.SBO_0000002, unit=U.mmole_glucose_per_l),  # Km michaelis-menten coefficient for glucose uptake [mmolGlucose/l],
    Parameter("G_b", 5.0, name="G_b", sboTerm=SBO.SBO_0000002, unit=U.mmole_glucose_per_l),  # G_b basal plasma glucose [mmolGlucose/l]
    Parameter("I_PL_b", 18, name="I_PL_b", sboTerm=SBO.SBO_0000002, unit=U.mmole_glucose_per_l), # I_PL_b basal plasma glucose [μIU/ml]
    Parameter("G_liv_b", 0.043, name="I_pl_b", sboTerm=SBO.SBO_0000002, unit=U.mmole_glucose_per_l_min),  # basal hepatic glucose release [mmolGlucose/(l*min)]

    # triglyceride + NEFA parameters
    Parameter("spill", 30.0, name="spill", sboTerm=SBO.SBO_0000002, unit=U.dimensionless),  # spill - fractional spillover of LPL derived NEFA
    Parameter("k11", 0.00045, name="K11", sboTerm=SBO.SBO_0000002, unit=U.lipolysis_coefficien_unit),  # k11 - rate coeficient LPL lipolysis sips/jelic models [(mmolNEFA*ml)/(μIU*mmolTG*min)]
    Parameter("ATL_max", 0.215, name="ATL_max", sboTerm=SBO.SBO_0000002, unit=U.mmole_nefa_per_l_min),  # ATL_max maximum rate of ATL lipolysis in adipose tissues [mmolNEFA / (l * min)],
    Parameter("K_ATL", 0.0385, name="K_ATL", sboTerm=SBO.SBO_0000002, unit=U.ml_sqr_per_micro_iu_sqr),  # K_ATL michealis menten coeficient for ATL lipolysis of store TG in adipose tissue [ml^2/μIU^2]
    Parameter("k12", 0.0713, name="k12", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k12 rate constanst for uptake of NEFA into tissues (currently insulin indenpendent) [/min]
    Parameter("tau_LPL", 208.88, name="tau_LPL", sboTerm=SBO.SBO_0000002, unit=U.min),  # tau_LPL time delay for insulin stimulation of LPL lipolysis [min]
    Parameter("k13", 0.0088, name="k13", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k13 - rate constant for stomach emptying TG(very slow) [/min]
    Parameter("k14", 0.0163, name="k14", sboTerm=SBO.SBO_0000002, unit=U.per_min),  # k14 - rate constant for rate of TG appearance from gut [/min]
    Parameter("k15", 1e-5, name="k15", sboTerm=SBO.SBO_0000002, unit=U.micromol_tg_per_min_microiu),  # k15 coefficient for inhibition of TG secretion from liver by insulin [μmolTG/(min*μIU)]
    Parameter("k16", 0.0119, name="k16", sboTerm=SBO.SBO_0000002, unit=U.mmole_tg_per_l_min),  # k16 basal secretion of TG from liver [mmolTG/(l*min)]

    # input parameters (for now, test values)
    # TODO: verify where M_G_gut comes from
    Parameter("M_G_gut", 0, name="M_G_gut", unit=U.mg),  # test value, intial mass of glucose in digestive tract
    Parameter("D_meal_G", 75000, name="D_meal_G", unit=U.mg),  # test value, meal glucose mass
    Parameter("G_PL", 5, name="G_PL", unit=U.mg),  # test value, fasting glucose
    Parameter("I_d1", 0, name="I_d1"),  # test value, insulin concentrtion in remote compartment
    Parameter("BW", 75, name="BW"),  # test value, kg subject_body_mass

    # gut products. TODO: move to gut compartment, add unit and sboterm
    Parameter("g_gut", 0.0, name="g_gut", annotations=annotations.species["glc"], constant=False),  # du[1] [unit=u"mg"],
    Parameter("i_intestitial", 0.0, name="i_intestitial", annotations=annotations.species["ins"], constant=False),  # du[5] I_interstitial(t), [unit=u"μIU/ml"],
    Parameter("tg_gut", 0.0, name="tg_gut", annotations=annotations.species["tg"], constant=False),  # du[10]  TG_gut(t), [unit=u"mg"],
    Parameter("tg_delay1", 0.0, name="tg_delay1", annotations=annotations.species["tg"], constant=False),  # du[11]
    Parameter("tg_delay2", 0.0, name="tg_delay2", annotations=annotations.species["tg"], constant=False),  # du[12]
]

# Assignment rules
_m.rules = [
    # TODO: which sboTerm?
    AssignmentRule("c2", name="c2", value="G_liv_b*(Km + G_b)/G_b-k5*f_I*G_liv_b"),  # c.c2 = c.G_liv_b.*(parameters(12) + parameters(13))./parameters(13) - parameters(5).*c.f_I.*parameters(15);
    AssignmentRule("c3", name="c3", value="k7*G_b/(f_I*tau_i*I_PL_b)*t_integralwindow"),  # c.c3 = parameters(7).*parameters(13)./(c.f_I*c.tau_i.*parameters(14)).*c.t_integralwindow;

    #  Appearance of glucose from meal
    AssignmentRule("G_meal", name="G_meal", value="sigma*(k1^sigma)*time^(sigma-1)* exp(-(k1*(time))^sigma)* D_meal_G"),  # appearance fo glucose from meal as a function of time

    # NOTE: M_G_gut is returned in the original model, but needs to be a species for simulating this. But it is in the gut compartment.
    # to be tackled when adding the gut compartment
    # AssignmentRule("M_G_gut", name="M_G_gut", value="G_meal - k2*M_G_gut"), # glucose mass in gut

    # plasma glucose
    AssignmentRule("G_liv", name="G_liv", value="G_liv_b - k4*f_I*I_d1 - k3*(G_PL-G_b)"),  # net glucose flux across liver
    AssignmentRule("G_gut", name="G_gut", value="k2*(f_G/(V_G*BW))*M_G_gut"),  # glucose concentration in gut

]

# k1     = parameters(1);  % rate constant for glucose stomach emptying (fast)[1/min]
# k2     = parameters(2);  % rate constant for glucose appearance from gut [1/min]
# k3     = parameters(3);  % rate constant for suppression of hepatic glucose release by change of plasma glucose [1/min]
# k4     = parameters(4);  % rate constant for suppression of hepatic glucose release by  delayed insulin (remote compartment) [1/min]
# k5     = parameters(5);  % rate constant for delayed insulin depedent uptake of glucose[1/min]
# k6     = parameters(6);  % rate constant for stimulation of insulin production by the change of plasma glucose concentration[1/min] (proportional)
# k7     = parameters(7);  % rate constant for integral of glucose on insulin production[1/min] (integral)
# k8     = parameters(8);  % rate constant for the simulation of insulin production by the rate of change in plasma glucose concentration [1/min] (derivative)
# k9     = parameters(9);  % rate constant for outflow of insulin from plasma to remote compartment[1/min]
# k10    = parameters(10); % rate constant for utilisation of insulin in remote compartment (degredation)
# sigma  = parameters(11); % shape factor (appearance of meal)[-]
# KM     = parameters(12); % michaelis-menten coefficient for glucose uptake[mmol/l]
# G_b    = parameters(13); % basal plasma glucose [mmol/l]
# I_PL_b = parameters(14); % basal plasma glucose [microU/ml]
# G_liv_b = parameters(15);%basal hepatic glucose release
#
# %triglyceride + NEFA parameters (new)
# spill   = parameters(16); %fractional spill over of LPL derived NEFA
# k11     = parameters(17); %rate constant for Lipoprotein lipase lipolysis of circulating triglyceride
# ATL_max = parameters(18); %Maximum rate of NEFA release from adipose tissue(ATL lipolysis)
# K_ATL   = parameters(19); %Michealis Menten coefficient for rate of NEFA release from adipose tissue(ATL lipolysis)
# k12     = parameters(20); %rate constant for NEFA uptake into tissues
# tau_LPL = parameters(21); %time delay for insulin stimulation of LPL lipolysis
# k13     = parameters(22); %rate constant for stomach emptying TG(slow)
# k14     = parameters(23); %rate constant for rate of TG appearance from gut
# k15     = parameters(24); %coefficient for inhibition of TG secretion from liver by insulin
# k16     = parameters(25); %basal rate of TG secretion from liver

# %fixed to values specified in parameter vector (expected fasting values)
# c.c2     = c.G_liv_b.*(parameters(12) + parameters(13))./parameters(13) - parameters(5).*c.f_I.*parameters(15);
# c.c3     = parameters(7).*parameters(13)./(c.f_I*c.tau_i.*parameters(14)).*c.t_integralwindow;

#     # parameters

#     Parameter("mG", 75000),  # mg meal_glucose_mass  # p[26]
#     Parameter("mTG", 60000),  # mg meal_tg_mass  # p[27]
#     Parameter("BW", 75),  # kg subject_body_mass  # p[28]
# ]

#
# # Assignment rules
# _m.rules = [
#     AssignmentRule("VG", "(260 / sqrt(BW / 70)) / 1000"),
#     AssignmentRule("VTG", "(70 / sqrt(BW / 70)) / 1000"),
# ]

# # ------------------------------------
# # glucose appearance from the meal
# du[1] = glucose_meal_appearance(p[11], p[1], t, mG, p[2], u[1])
# glucose_from_meal = meal_appearance(σ, k, t, M)
# intestinal_absorption = k2 * g_gut
# glucose_from_meal - intestinal_absorption
#
# # gamma function
# k = k1
# σ = sigma
# t = time
# M = mG
# meal_appearance(σ, k, t, M) = (k ^ σ) * t ^ (σ - 1) * exp(-1 * (k * t)) * M * (1 / gamma(σ))
#
#
# # ------------------------------------
# # glucose in the plasma
# du[2] = plasma_glucose_flux(VG, BW, fI, fG, c1, G_threshold_pl, p, u)
#
# # VG, BW, fI, fG, c1, G_threshold_pl, p, u
#
# distribution_volume_correction = 1 / (VG * BW)
# unit_conversion_glucose_insulin = 1 / fI
# unit_conversion_mg_to_mM = fG
# basal_production = p[15]
# glomerular_filtration_rate = c1
# renal_threshold = G_threshold_pl
#
# # Liver
# egp_inhibition_by_insulin = p[4] * u[5] * unit_conversion_glucose_insulin
# egp_inhibition_by_glucose = p[3] * (u[2] - p[13])
# G_liver = basal_production - egp_inhibition_by_insulin - egp_inhibition_by_glucose
#
# # Intestines (gut)
# glucose_appearance = p[2] * u[1]
# G_gut = glucose_appearance * distribution_volume_correction * unit_conversion_mg_to_mM
#
# # Insulin-independent glucose utilization (maintain steady-state)
# normalized_utilization_rate = ((p[12] + p[13]) * u[2]) / (p[13] * (p[12] + u[2]))
# G_iid = normalized_utilization_rate * basal_production
#
# # Insulin-dependent glucose utilization
# utilization_rate = p[5] * u[2] / (p[12] + u[2])
# G_idp = utilization_rate * u[5]
#
# # Renal excretion of excess glucose
# G_ren = glomerular_filtration_rate * distribution_volume_correction * (u[2] - renal_threshold) * (
#             u[2] > renal_threshold)
#
# G_liver + G_gut - G_iid - G_idp - G_ren
#
# # ------------------------------------
# # PID Integrator equation
# du[3] = u[2] - p[13]
#
# # ------------------------------------
# # fI, tau_i, tau_d,  # p, u, du
# # insulin in the plasma
# unit_conversion_glucose_insulin = 1 / fI
#
# # Pancreas
# proportional = p[6] * (u[2] - p[13])
# integral = (p[7] / tau_i) * (u[3] + p[13])
# derivative = (p[8] * tau_d) * du[2]
# I_pnc = unit_conversion_glucose_insulin * (proportional + integral + derivative)
#
# # Liver insulin degradation (maintain steady-state)
# basal_rate = unit_conversion_glucose_insulin * (p[7] / tau_i) * p[13]
# I_liv = basal_rate * (u[4] / p[14])
#
# # Transport to interstitial fluid
# I_int = p[9] * (u[4] - p[14])
#
# I_pnc - I_liv - I_int
#
# du[4] = plasma_insulin_flux(fI, tau_i, tau_d, p, u, du)
# # ------------------------------------
#
# # Insulin in the interstitial fluid
# appearance = p[9] * (u[4] - p[14])
# degradation = p[10] * u[5]
#
# appearance - degradation
# du[5] = interstitial_insulin_flux(p, u)
#
# # ------------------------------------
# # Insulin delays for NEFA_pl
# du[6] = 3 / p[21] * (u[4] - u[6])
# du[7] = 3 / p[21] * (u[6] - u[7])
# du[8] = 3 / p[21] * (u[7] - u[8])
#
# # ------------------------------------
# # plasma NEFA
# LPL_lipolysis = p[17] * u[13] * u[8]
# fractional_spillover = (1 / 100) * p[16] * (p[14] / u[6])
# spillover = 3 * fractional_spillover * LPL_lipolysis
# adipose_tg_lipolysis = p[18] / (1 + p[19] * u[6] ^ 2)
# tissue_uptake = p[20] * u[9]
# spillover + adipose_tg_lipolysis - tissue_uptake
# du[9] = plasma_nefa_flux(p, u)
#
# # ------------------------------------
# # Gut TG
#
# #   (k^σ)*t^(σ-1) * exp(-1*(k*t)) * M * (1/gamma(σ))
# du[10] = meal_appearance(p[11], p[22], t, mTG) - p[23] * u[10]
#
#
# du[11] = p[23] * (u[10] - u[11])
# du[12] = p[23] * (u[11] - u[12])
#
# # ------------------------------------
# # plasma TG
# distribution_volume_correction = 1 / (VTG * BW)
# unit_conversion_mg_to_mM = fTG
#
# # endogenous secretion of TG (in the form of VLDL)
# VLDL = p[25] - p[24] * (u[8] - p[14])
#
# # TG from the gut
# TG_gut = p[23] * distribution_volume_correction * unit_conversion_mg_to_mM * u[12]
#
# # LPL lipolysis
# LPL_lipolysis = p[17] * u[13] * u[8]
#
# VLDL + TG_gut - LPL_lipolysis
# du[13] = plasma_tg_flux(VTG, BW, fTG, p, u)
# # ------------------------------------
#
#
# _m.reactions = [
#     du[1] = glucose_meal_appearance(p[11], p[1], t, mG, p[2], u[1])
#
#     # glucose in the plasma
#     du[2] = plasma_glucose_flux(VG, BW, fI, fG, c1, G_threshold_pl, p, u)
#
#     # PID Integrator equation
#     du[3] = u[2] - p[13]
#
#     # insulin in the plasma
#     du[4] = plasma_insulin_flux(fI, tau_i, tau_d, p, u, du)
#
#     # Insulin in the interstitial fluid
#     du[5] = interstitial_insulin_flux(p, u)
#
#     # Insulin delays for NEFA_pl
#     du[6] = 3 / p[21] * (u[4] - u[6])
#     du[7] = 3 / p[21] * (u[6] - u[7])
#     du[8] = 3 / p[21] * (u[7] - u[8])
#
#     # plasma NEFA
#     du[9] = plasma_nefa_flux(p, u)
#
#     # Gut TG
#     du[10] = meal_appearance(p[11], p[22], t, mTG) - p[23] * u[10]
#     du[11] = p[23] * (u[10] - u[11])
#     du[12] = p[23] * (u[11] - u[12])
#
#     # plasma TG
#     du[13] = plasma_tg_flux(VTG, BW, fTG, p, u)
#
#     # Reaction(
#     #     "METEX",
#     #     name="metoprolol renal excretion",
#     #     equation="met_ext -> met_urine",
#     #     sboTerm=SBO.TRANSPORT_REACTION,
#     #     compartment="Vki",
#     #     pars=[
#     #         Parameter(
#     #             "METEX_k",
#     #             2.5,  # (7.5 + 60 + 10)/77.5
#     #             unit=U.per_min,
#     #             name="metoprolol urinary excretion (kidney)",
#     #             sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
#     #         ),
#     #     ],
#     #     formula=("f_renal_function * METEX_k * Vki * met_ext", U.mmole_per_min),
#     # )
# ]

meal_model = _m


def simulate(sbml_path: Path):
    import pandas as pd
    r: roadrunner.RoadRunner = roadrunner.RoadRunner(str(sbml_path))
    _s = r.simulate(start=0, end=10, steps=1000)
    r.plot(_s)
    s_out = pd.DataFrame(_s, columns=_s.colnames)
    print(s_out)


if __name__ == "__main__":
    result = create_model(
        filepath=MODEL_PATH, model=meal_model, validation_options=ValidationOptions(units_consistency=False, modeling_practice=False)
    )
    simulate(result.sbml_path)
    visualize_sbml(sbml_path=result.sbml_path, delete_session=True)
