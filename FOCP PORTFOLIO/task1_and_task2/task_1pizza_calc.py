# Beckett Pizza Plaza - 4-for-3 Assignment

def main():
    print("Beckett Pizza Plaza 4-for-3 Offer")
    print("=================================")

    # This is our list to store the 4 prices
    pizza_list = []
    
    # Loop until we have exactly 4 items in the list
    while len(pizza_list) < 4:
        try:
            # We use a temporary variable 'val' to check the user's input
            # Added .strip() to handle accidental spaces
            user_input = input(f"Enter The Price of Pizza #{len(pizza_list) + 1}: ").strip()
            val = float(user_input)
            
            if val > 0:
                pizza_list.append(val)
            else:
                print("Please enter a valid price!")
                
        except ValueError:
            print("Please enter a valid price!")

    # Math Logic
    total_before_discount = sum(pizza_list)
    cheapest_item = min(pizza_list)
    
    # Final price is the sum minus the free one
    final_bill = total_before_discount - cheapest_item
    
    # Percentage calculation
    # Changed to :.1f to provide a more accurate discount figure
    saving_percent = (cheapest_item / total_before_discount) * 100

    print(f"\nOrder Total is £{final_bill:.2f}, a fabulous discount of {saving_percent:.1f}%!")

if __name__ == "__main__":
    main()