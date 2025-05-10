from core.socionics import * 

VALID_FUNCTIONS = {'Ni', 'Ne', 'Fi', 'Fe', 'Ti', 'Te', 'Si', 'Se'}

VALID_STACKS = {
    'ISTJ': ['Si', 'Te', 'Fi', 'Ne'],
    'ISFJ': ['Si', 'Fe', 'Ti', 'Ne'],
    'INFJ': ['Ni', 'Fe', 'Ti', 'Se'],
    'INTJ': ['Ni', 'Te', 'Fi', 'Se'],
    'ISTP': ['Ti', 'Se', 'Ni', 'Fe'],
    'ISFP': ['Fi', 'Se', 'Ni', 'Te'],
    'INFP': ['Fi', 'Ne', 'Si', 'Te'],
    'INTP': ['Ti', 'Ne', 'Si', 'Fe'],
    'ESTP': ['Se', 'Ti', 'Fe', 'Ni'],
    'ESFP': ['Se', 'Fi', 'Te', 'Ni'],
    'ENFP': ['Ne', 'Fi', 'Te', 'Si'],
    'ENTP': ['Ne', 'Ti', 'Fe', 'Si'],
    'ESTJ': ['Te', 'Si', 'Ne', 'Fi'],
    'ESFJ': ['Fe', 'Si', 'Ne', 'Ti'],
    'ENFJ': ['Fe', 'Ni', 'Se', 'Ti'],
    'ENTJ': ['Te', 'Ni', 'Se', 'Fi'],
}

def infer_mbti_from_stack(stack):
    # Validate input
    if len(stack) != 4:
        raise ValueError(f"Stack must have 4 functions (got {len(stack)})")
    
    stack = [func.capitalize() for func in stack]
    for func in stack:
        if func not in VALID_FUNCTIONS:
            raise ValueError(f"Invalid function: {func}")

    # Check exact match
    for mbti, valid_stack in VALID_STACKS.items():
        if stack == valid_stack:
            return {
                'type': mbti,
                'exact_match': True,
                'confidence': 100.0,
                'closest_stack': valid_stack,
                'differences': []
            }

    # Find closest match using weighted position scoring
    max_score = -1
    closest_type = None
    closest_stack = None

    for mbti, valid_stack in VALID_STACKS.items():
        score = sum((4 - i) for i in range(4) if stack[i] == valid_stack[i])
        if score > max_score or (score == max_score and stack[0] == valid_stack[0]):
            max_score = score
            closest_type = mbti
            closest_stack = valid_stack

    # Calculate confidence (max possible score = 4+3+2+1 = 10)
    confidence = (max_score / 10) * 100

    # Identify differing positions
    differences = [i+1 for i in range(4) if stack[i] != closest_stack[i]]

    return {
        'type': closest_type,
        'exact_match': False,
        'confidence': round(confidence, 1),
        'closest_stack': closest_stack,
        'differences': differences
    }

def opposite_jp(jp):
    return 'F' if jp == 'T' else 'T'

def opposite_ns(ns):
    return 'S' if ns == 'N' else 'N'

def derive_cognitive_stack(mbti_type):
    attitude = mbti_type[0]  # I or E
    perception = mbti_type[1]  # N or S
    judgment = mbti_type[2]    # T or F
    lifestyle = mbti_type[3]   # J or P

    is_introvert = attitude == 'I'
    is_judging = lifestyle == 'J'

    # Function pairs: (extraverted, introverted)
    perceiving_funcs = {'N': ('Ne', 'Ni'), 'S': ('Se', 'Si')}
    judging_funcs = {'T': ('Te', 'Ti'), 'F': ('Fe', 'Fi')}

    # Determine dominant and auxiliary functions
    if is_introvert:
        if is_judging:
            # Dominant: introverted perceiving, Auxiliary: extraverted judging
            dom = perceiving_funcs[perception][1]  # Ni or Si
            aux = judging_funcs[judgment][0]       # Te or Fe
        else:
            # Dominant: introverted judging, Auxiliary: extraverted perceiving
            dom = judging_funcs[judgment][1]       # Ti or Fi
            aux = perceiving_funcs[perception][0]  # Ne or Se
    else:
        if is_judging:
            # Dominant: extraverted judging, Auxiliary: introverted perceiving
            dom = judging_funcs[judgment][0]       # Te or Fe
            aux = perceiving_funcs[perception][1]  # Ni or Si
        else:
            # Dominant: extraverted perceiving, Auxiliary: introverted judging
            dom = perceiving_funcs[perception][0]  # Ne or Se
            aux = judging_funcs[judgment][1]       # Ti or Fi

    # Determine tertiary function: opposite perceiving/judging of auxiliary, flipped attitude
    # If auxiliary is perceiving (Ne, Ni, Se, Si), tertiary is judging (Te, Ti, Fe, Fi)
    # If auxiliary is judging (Te, Ti, Fe, Fi), tertiary is perceiving (Ne, Ni, Se, Si)

    # Helper to get opposite judging/ perceiving letter
    def opposite_jp(jp):
        return 'F' if jp == 'T' else 'T'

    def opposite_ns(ns):
        return 'S' if ns == 'N' else 'N'

    # Auxiliary function type and attitude
    aux_type = aux[0]  # N, S, T, or F
    aux_attitude = aux[1]  # 'e' or 'i'

    dom_type = dom[0]      # e.g. 'N' in 'Ni'
    dom_attitude = dom[1]  # e.g. 'i' in 'Ni'

    # For tertiary:
    if aux_type in ('N', 'S'):
        # Auxiliary is perceiving, tertiary is perceiving with opposite perception letter and opposite attitude
        tertiary_perception = opposite_ns(aux_type)
        tertiary_funcs = perceiving_funcs[tertiary_perception]
        tertiary = tertiary_funcs[1] if aux_attitude == 'e' else tertiary_funcs[0]
    else:
        # Auxiliary is judging, tertiary is judging with opposite judgment letter and opposite attitude
        tertiary_judgment = opposite_jp(aux_type)
        tertiary_funcs = judging_funcs[tertiary_judgment]
        tertiary = tertiary_funcs[1] if aux_attitude == 'e' else tertiary_funcs[0]

    # Inferior function: opposite J/P and opposite attitude of dominant
    if dom_type in ('N', 'S'):
        inferior_perception = opposite_ns(dom_type)
        inferior_funcs = perceiving_funcs[inferior_perception]
        inferior = inferior_funcs[1] if dom_attitude == 'e' else inferior_funcs[0]
    else:
        inferior_judgment = opposite_jp(dom_type)
        inferior_funcs = judging_funcs[inferior_judgment]
        inferior = inferior_funcs[1] if dom_attitude == 'e' else inferior_funcs[0]


    return [dom, aux, tertiary, inferior]

def flip_letter(ch):
    return {
        'I': 'E', 'E': 'I',
        'J': 'P', 'P': 'J',
        'F': 'T', 'T': 'F',
        'N': 'S', 'S': 'N'
    }.get(ch, ch)

def infer_shadow_type(mbti, mode):
    """Returns MBTI type representing shadow (subconscious, unconscious, superego)"""
    if mode == 'subconscious':
        # Flip all four letters (I/E, N/S, T/F, J/P)
        shadow = ''.join([flip_letter(c) for c in mbti])
    elif mode == 'unconscious':
        # Flip first (I/E) and last (J/P) letters only
        shadow = flip_letter(mbti[0]) + mbti[1] + mbti[2] + flip_letter(mbti[3])
    elif mode == 'superego':
        # Flip middle two letters (N/S and T/F) only
        shadow = mbti[0] + flip_letter(mbti[1]) + flip_letter(mbti[2]) + mbti[3]
    else:
        raise ValueError("Unknown shadow mode")
    return shadow

def get_function_roles(mbti_type):
    ego = derive_cognitive_stack(mbti_type)
    subconscious = derive_cognitive_stack(infer_shadow_type(mbti_type, 'subconscious'))
    unconscious = derive_cognitive_stack(infer_shadow_type(mbti_type, 'unconscious'))
    superego = derive_cognitive_stack(infer_shadow_type(mbti_type, 'superego'))
    return {
        'ego': ego,
        'subconscious': subconscious,
        'unconscious': unconscious,
        'superego': superego
    }

def analyze_type(mbti_type, functions, show_socionics=False, compare_to_type=None):
    roles = get_function_roles(mbti_type)  # Assuming this function exists and returns stacks per role

    if show_socionics:
        print(f"Analysis for {mbti_type} (MBTI):")
    else:
        print(f"Analysis for {mbti_type}:")

    for role in functions:
        if role in roles:
            stack = roles[role]
            inferred = infer_mbti_from_stack(stack)['type']  # get just MBTI string
            stack_str = '-'.join(stack)
            if show_socionics:
                print(f"{role.capitalize()}: {stack_str}  (MBTI: {inferred})")
            else:
                print(f"{role.capitalize()}: {stack_str}  (MBTI: {inferred})")

    # Show Socionics intertype relation if requested
    if show_socionics and compare_to_type:
        relation = get_intertype_relation(mbti_type.upper(), compare_to_type.upper())
        print(f"\nSocionics Relation between {mbti_type.upper()} and {compare_to_type.upper()}: {relation}")
