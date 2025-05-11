import sys
from core.functions import analyze_type, infer_mbti_from_stack
from core.bigfive import BigFiveProfile
from core.cbt import analyze_cbt_thought 
from utils import parse_arguments

def main():
    args = parse_arguments()

    if args.command == "analyze":
        if args.functions is None:
            args.functions = ["ego", "subconscious", "unconscious", "superego"]

        if args.type:
            analyze_type(
                args.type.upper(),
                args.functions,
                show_socionics=getattr(args, 'show_socionics', False),
                compare_to_type=args.compare_to.upper() if args.compare_to else None
            )

        if args.bigfive:
            try:
                if len(args.bigfive) != 5:
                    raise ValueError("Big Five input must have exactly 5 values.")
                o, c, e, a, n = args.bigfive
                mbti_type = args.type.upper() if args.type else None
                b5 = BigFiveProfile(o, c, e, a, n, mbti_type=mbti_type)
                b5.validate()
                print("\nBig Five Analysis:")
                print("\n".join(b5.get_report()))
            except ValueError as e:
                print(f"Error: {str(e)}")
                sys.exit(1)

        if args.cbt_thought:
            try:
                cbt_results = analyze_cbt_thought(args.cbt_thought)
                print("\nCBT Analysis:")
                if cbt_results['distortions']:
                    print("Detected cognitive distortions:")
                    for dist in cbt_results['distortions']:
                        print(f"- {dist['name']}: {dist['description']}")
                        print(f"  Suggested reframe: {dist['reframe']}")
                else:
                    print("No common cognitive distortions detected.")
            except Exception as e:
                print(f"Error during CBT analysis: {str(e)}")
                sys.exit(1)

    elif args.command == "infer":
        stack = [func.strip() for func in args.stack]
        try:
            result = infer_mbti_from_stack(stack)
            if result['exact_match']:
                print(f"MBTI Type: {result['type']}")
            else:
                print(f"Closest MBTI: {result['type']} (confidence: {result['confidence']}%)")
                print(f"Expected stack: {'-'.join(result['closest_stack'])}")
                print(f"Differences in positions: {', '.join(map(str, result['differences']))}")
        except ValueError as e:
            print(f"Error: {str(e)}")

    else:
        print("Invalid command. Use --help for more information.")

if __name__ == "__main__":
    main()

