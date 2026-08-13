def identify_battery_type(chemistry: str) -> str | None:
    try:
        chem_upper = chemistry.strip().upper()
        
        if any(x in chem_upper for x in ["NMC", "NCA", "LI-ION", "LITHIUM ION", "LITHIUM-ION"]):
            print("\n SUCCESS: Logged as LITHIUM-ION")
            return "LITHIUM-ION"
            
        elif any(x in chem_upper for x in ["LFP", "LITHIUM IRON", "LI-FE", "LIFEPO4"]):
            print("\n SUCCESS: Logged as LITHIUM-IRON-PHOSPHATE")
            return "LFP"
            
        else:
            print("\n WARNING: Unknown input chemistry.")
            return None
            
    except (ValueError, AttributeError):
        print("\n ERROR: Invalid chemistry input type received.")
        return None

def verify_label_plausibility(category: str, nominal_capacity_mah: float) -> bool:
    if category == "18650" and nominal_capacity_mah > 3600:
        return False
    return True
