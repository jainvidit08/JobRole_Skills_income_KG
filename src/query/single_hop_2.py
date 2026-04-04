from single_hop_1 import load_kg, single_hop_query
import os

def main():
    PKL_PATH = os.path.join('..', 'model', 'knowledge_graph.pkl')
    
    try:
        kg = load_kg(PKL_PATH)
        print("--- Knowledge Graph Recommendation System ---")
        print("Type 'exit' at any time to quit.\n")

        while True:
            print("\n--- Available Queries ---")
            print("1. Skills for a Category")
            print("2. Income for a Skill")
            print("3. Categories for an Education")
            print("4. Income for a Job Category")
            print("5. Income for an Experience Level")
            print("6. Income for an Education Level")
            
            choice = input("\nSelect an option (1-6): ").strip()

            if choice.lower() == 'exit':
                break

            # --- Logic for Options 1, 2, and 3 remains as before ---
            if choice == '1':
                cat = input("Enter Category (e.g., DevOps): ").strip()
                results = single_hop_query(kg, cat, "PART_OF", direction="in")
                print_results(results, f"Skills for {cat}")

            elif choice == '2':
                skill = input("Enter Skill (e.g., Python): ").strip()
                results = single_hop_query(kg, skill, "PAYS_DIRECT", direction="out")
                print_results(results, f"Income for {skill}")

            elif choice == '3':
                edu = input("Enter Education (e.g., Master): ").strip()
                results = single_hop_query(kg, edu, "QUALIFIES_FOR", direction="out")
                print_results(results, f"Categories for {edu}")

            # --- NEW: Job Category -> Income ---
            elif choice == '4':
                cat = input("Enter Category (e.g., UI/UX Design): ").strip()
                results = single_hop_query(kg, cat, "PAYS", direction="out")
                print_results(results, f"Income distribution for {cat}")

            # --- NEW: Experience Level -> Income ---
            elif choice == '5':
                exp = input("Enter Level (e.g., junior, mid, senior): ").strip()
                results = single_hop_query(kg, exp, "EARNS", direction="out")
                print_results(results, f"Income distribution for {exp} level")

            # --- NEW: Education -> Income ---
            elif choice == '6':
                edu = input("Enter Education (e.g., Master, Bachelor): ").strip()
                results = single_hop_query(kg, edu, "RESULT_IN", direction="out")
                print_results(results, f"Income distribution for {edu} level")

            else:
                print("Invalid choice. Please select 1-6.")

    except Exception as e:
        print(f"System Error: {e}")

def print_results(results, title):
    """Helper function to print formatted results."""
    if isinstance(results, list) and results:
        print(f"\n--- {title} ---")
        for item, weight in results:
            print(f"- {item} (Frequency: {weight})")
    else:
        print(f"\nNo data found.")

if __name__ == "__main__":
    main()