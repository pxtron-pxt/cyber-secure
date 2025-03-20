from enum import Enum
from typing import Dict

class RuleType(Enum):
    ALLOW = 1
    BLOCK = 2

class Firewall:
    def __init__(self) -> None:
        self.rules: Dict[str, RuleType] = {}

    def add_rule(self, ip: str, rule: RuleType) -> None:
        """Add or update a firewall rule for a specific IP"""
        self.rules[ip] = rule
        print(f"Rule {'updated' if ip in self.rules else 'added'}: {ip} - {rule.name}")

    def display_rules(self) -> None:
        """Display all current firewall rules"""
        if not self.rules:
            print("No rules found.")
            return
        
        print("\nFirewall Rules:")
        for ip, rule in self.rules.items():
            print(f"{ip:20} - {rule.name}")

    def check_ip(self, ip: str) -> None:
        """Check the status of a specific IP address"""
        rule = self.rules.get(ip)
        if rule:
            print(f"IP {ip} is {rule.name}ED")
        else:
            print(f"No rule found for IP: {ip}")

    def remove_rule(self, ip: str) -> None:
        """Remove a firewall rule for a specific IP"""
        if ip in self.rules:
            del self.rules[ip]
            print(f"Rule removed for IP: {ip}")
        else:
            print(f"No rule found for IP: {ip}")

def get_user_choice() -> int:
    """Get and validate user menu choice with error handling"""
    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            print("Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main_menu(firewall: Firewall) -> None:
    """Handle the main menu interaction"""
    menu = """
Firewall & Security Rules Manager
1. Add Rule
2. Display Rules
3. Check IP
4. Remove Rule
5. Exit
"""
    while True:
        print(menu)
        choice = get_user_choice()

        if choice == 5:
            print("Exiting program...")
            break

        try:
            if choice == 1:
                ip = input("Enter IP to add/update rule: ").strip()
                rule_input = input("Enter rule (1 = ALLOW, 2 = BLOCK): ").strip()
                if rule_input not in {'1', '2'}:
                    print("Invalid rule type. Please enter 1 or 2.")
                    continue
                rule = RuleType.ALLOW if rule_input == '1' else RuleType.BLOCK
                firewall.add_rule(ip, rule)

            elif choice == 2:
                firewall.display_rules()

            elif choice == 3:
                ip = input("Enter IP to check: ").strip()
                firewall.check_ip(ip)

            elif choice == 4:
                ip = input("Enter IP to remove rule: ").strip()
                firewall.remove_rule(ip)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    firewall = Firewall()
    main_menu(firewall)