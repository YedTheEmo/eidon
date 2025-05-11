import json
import os

class BigFiveNorms:
    _norms = None

    @classmethod
    def load_norms(cls, filepath=None):
        if cls._norms is None:
            if filepath is None:
                filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'mbti_bigfive_norms.json')
            try:
                with open(filepath, 'r') as f:
                    cls._norms = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Normative data file not found at {filepath}. Using empty norms.")
                cls._norms = {}
            except json.JSONDecodeError:
                print(f"Warning: Normative data file at {filepath} is invalid JSON. Using empty norms.")
                cls._norms = {}
        return cls._norms

    @classmethod 
    def get_type_norms(cls, mbti_type):
        norms = cls.load_norms()
        return norms.get(mbti_type.upper(), None)


class BigFiveProfile:
    # General population norms (mean ± SD) - placeholder values
    POPULATION_NORMS = {
        'openness': {'mean': 50.0, 'sd': 10.0},
        'conscientiousness': {'mean': 50.0, 'sd': 10.0},
        'extraversion': {'mean': 50.0, 'sd': 10.0},
        'agreeableness': {'mean': 50.0, 'sd': 10.0},
        'neuroticism': {'mean': 50.0, 'sd': 10.0}
    }

    def __init__(self, openness, conscientiousness, extraversion, agreeableness, neuroticism, mbti_type=None):
        self.traits = {
            'openness': openness,
            'conscientiousness': conscientiousness,
            'extraversion': extraversion,
            'agreeableness': agreeableness,
            'neuroticism': neuroticism
        }
        self.mbti_type = mbti_type.upper() if mbti_type else None

    def validate(self):
        for trait, value in self.traits.items():
            if not 0 <= value <= 100:
                raise ValueError(f"Invalid {trait} value: {value}. Must be between 0 and 100.")

    def get_report(self):
        report = []
        if self.mbti_type:
            type_norms = BigFiveNorms.get_type_norms(self.mbti_type)
            if type_norms:
                report.append(f"Using MBTI type-specific norms for {self.mbti_type}:")
                for trait, value in self.traits.items():
                    norm = type_norms.get(trait)
                    if norm is not None:
                        deviation = value - norm
                        report.append(f"{trait.title()}: {value:.1f} (Type norm: {norm}, Deviation: {deviation:+.1f})")
                    else:
                        report.append(f"{trait.title()}: {value:.1f} (No norm available)")
                return report

        # Fallback: Use population norms with percentiles
        report.append("Using general population norms:")
        for trait, value in self.traits.items():
            norm = self.POPULATION_NORMS[trait]['mean']
            sd = self.POPULATION_NORMS[trait]['sd']
            deviation = value - norm
            z = deviation / sd if sd > 0 else 0
            # Rough percentile approximation (normal distribution)
            percentile = int(50 + (z * 34))
            percentile = max(1, min(99, percentile))
            report.append(f"{trait.title()}: {value:.1f} (Norm: {norm}, Deviation: {deviation:+.1f}, Approx. percentile: {percentile}%)")
        return report
