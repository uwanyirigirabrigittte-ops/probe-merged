import pybamm


def get_pybamm_parameters(chemistry: str) -> pybamm.ParameterValues:
   chem_upper = chemistry.upper()
  
   if "NMC" in chem_upper:
       return pybamm.ParameterValues("Chen2020")
   elif "LFP" in chem_upper:
       return pybamm.ParameterValues("Marquis2019")
   else:
       return pybamm.ParameterValues("Marquis2019")
def verify_label_plausibility(category: str, nominal_capacity_mah: float) -> bool:
   if category == "18650" and nominal_capacity_mah > 3600:
       return False
   return True
