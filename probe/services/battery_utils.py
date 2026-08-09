import pybamm

def get_pybamm_parameters(chemistry: str) -> pybamm.ParameterValues:
   chem_upper = chemistry.strip().upper()

   if any(x in chem_upper for x in ["NMC", "NCA", "LI-ION", "LITHIUM ION", "LITHIUM-ION"]):
       print("\n SUCCESS: Detected and loaded [ LITHIUM-ION (NMC) ] chemistry template via Chen2020 parameters.")
       return pybamm.ParameterValues("Chen2020")
       
   elif any(x in chem_upper for x in ["LFP", "LITHIUM IRON", "LI-FE", "LIFEPO4"]):
       print("\n SUCCESS: Detected and loaded [ LITHIUM IRON PHOSPHATE (LFP) ] chemistry template via Marquis2019 parameters.")
       return pybamm.ParameterValues("Marquis2019")
       
   else:
       print("\n WARNING: Unknown input. Falling back to default LFP parameter values.")
       return pybamm.ParameterValues("Marquis2019")

def verify_label_plausibility(category: str, nominal_capacity_mah: float) -> bool:
   if category == "18650" and nominal_capacity_mah > 3600:
       return False
   return True
