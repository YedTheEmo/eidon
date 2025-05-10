from core.functions import analyze_type, infer_mbti_from_stack
from utils import parse_arguments

def main():
    args = parse_arguments()

    if args.command == "analyze":
        if args.functions is None:
            args.functions = ["ego", "subconscious", "unconscious", "superego"]
        analyze_type(
            args.type.upper(),
            args.functions,
            show_socionics=getattr(args, 'show_socionics', False),
            compare_to_type=args.compare_to.upper() if args.compare_to else None
        )

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

