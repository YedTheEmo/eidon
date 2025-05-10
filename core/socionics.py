"""
socionics.py

Exact Mathematical Socionics intertype relations via altered MBTI variables and P/J status,
covering all 16 types and 14 classical relations with directionality.

Authoritative, exception-free, and deterministic.
"""

from typing import List, Optional

# MBTI to Socionics type code mapping
MBTI_TO_SOCIONICS = {
    'ISTJ': 'LSI',
    'ISFJ': 'ESI',
    'INFJ': 'IEI',
    'INFP': 'EII',
    'ISTP': 'SLI',
    'ISFP': 'SEI',
    'INTP': 'LII',
    'ESTJ': 'LSE',
    'ESFJ': 'ESE',
    'ENFJ': 'EIE',
    'ENFP': 'IEE',
    'ESTP': 'SLE',
    'ESFP': 'SEE',
    'ENTP': 'ILE',
    'INTJ': 'ILI',
    'ENTJ': 'LIE',
}

def mbti_to_socionics(mbti: str) -> str:
    mbti = mbti.upper()
    soc = MBTI_TO_SOCIONICS.get(mbti)
    if not soc:
        raise ValueError(f"Unknown MBTI type: {mbti}")
    return soc

def get_altered_variables(mbti_a: str, mbti_b: str) -> List[int]:
    """
    Returns list of altered variable indices (1-based) between two MBTI types.
    Variables order: 1=E/I, 2=N/S, 3=T/F, 4=P/J
    """
    vars_a = mbti_a.upper()
    vars_b = mbti_b.upper()
    altered = []
    for i in range(4):
        if vars_a[i] != vars_b[i]:
            altered.append(i+1)
    return altered

def get_pj(mbti: str) -> str:
    """
    Returns 'p' or 'j' for Perceiving or Judging.
    """
    return mbti[3].lower()

def get_exact_relation(mbti_a: str, mbti_b: str) -> Optional[str]:
    """
    Determine exact socionics intertype relation based on altered variables and P/J of both types,
    with directionality for asymmetric relations.
    """
    altered = tuple(sorted(get_altered_variables(mbti_a, mbti_b)))
    pj_a = get_pj(mbti_a)
    pj_b = get_pj(mbti_b)

    # Identity
    if not altered:
        return "Identity"

    # Relations independent of P/J direction
    if altered == (1,):
        return "Contrary"
    if altered == (4,):
        return "Quasi-Identical"
    if altered == (2, 3):
        return "Super-Ego"
    if altered == (2, 3, 4):
        return "Activity"
    if altered == (1, 2, 3, 4):
        return "Conflict"
    if altered == (1, 4):
        return "Mirror"
    if altered == (1, 2, 3):
        return "Duality"

    # Relations depending on P/J and direction (A relative to B)
    if altered == (2,):
        return "Look-a-Like" if pj_a == 'p' else "Comparative"
    if altered == (3,):
        return "Comparative" if pj_a == 'p' else "Look-a-Like"
    if altered == (1, 2):
        return "Semi-Duality" if pj_a == 'p' else "Illusionary"
    if altered == (1, 3):
        return "Illusionary" if pj_a == 'p' else "Semi-Duality"

    # Supervisor / Supervisee (directional)
    if altered == (1, 2, 4):
        if pj_a == 'p' and pj_b == 'j':
            return "Supervisor"
        if pj_a == 'j' and pj_b == 'p':
            return "Supervisee"
    if altered == (1, 3, 4):
        if pj_a == 'j' and pj_b == 'p':
            return "Supervisor"
        if pj_a == 'p' and pj_b == 'j':
            return "Supervisee"

    # Benefactor / Beneficiary (directional)
    if altered == (2, 4):
        if pj_a == 'j' and pj_b == 'p':
            return "Benefactor"
        if pj_a == 'p' and pj_b == 'j':
            return "Beneficiary"
    if altered == (3, 4):
        if pj_a == 'p' and pj_b == 'j':
            return "Benefactor"
        if pj_a == 'j' and pj_b == 'p':
            return "Beneficiary"

    # If no match found
    return None

def get_intertype_relation(mbti_a: str, mbti_b: str) -> Optional[str]:
    """
    Public function to get socionics intertype relation between two MBTI types.
    Returns exact classical relation or None if invalid input or no relation.
    """
    try:
        # Validate MBTI types
        _ = mbti_to_socionics(mbti_a)
        _ = mbti_to_socionics(mbti_b)
    except ValueError:
        return None

    return get_exact_relation(mbti_a, mbti_b)

