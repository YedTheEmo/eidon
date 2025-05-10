import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="MBTI Cognitive Function Analysis")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help", required=True)

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze MBTI cognitive functions")
    analyze_parser.add_argument("--type", required=True, help="The MBTI type (e.g., INFJ, INTJ)")
    analyze_parser.add_argument("--functions", nargs="+", choices=["ego", "subconscious", "unconscious", "superego"], help="Functions to output")
    analyze_parser.add_argument('--show-socionics', action='store_true', help='Show Socionics types in analysis output')
    analyze_parser.add_argument('--compare-to', help='Compare to another MBTI type for Socionics relation')

    # Infer command
    infer_parser = subparsers.add_parser("infer", help="Infer MBTI type from cognitive function stack")
    infer_parser.add_argument("--stack", nargs=4, required=True, help="Four-letter cognitive function stack (e.g., Ni Fe Ti Se)")

    return parser.parse_args()

