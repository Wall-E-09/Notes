from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

class FuelComposition:
    def __init__(
        self,
        HP: float = 3.7,
        CP: float = 50.6,
        SP: float = 4.0,
        NP: float = 1.1,
        OP: float = 8.0,
        WP: float = 13.0,
        AP: float = 19.6
    ):
        self.HP = HP
        self.CP = CP
        self.SP = SP
        self.NP = NP
        self.OP = OP
        self.WP = WP
        self.AP = AP

def calculate_factors(WP, AP):
    KRS = 100 / (100 - WP)  # Коефіцієнт переходу до сухої маси
    KRG = 100 / (100 - WP - AP)  # Коефіцієнт переходу до горючої маси
    return KRS, KRG

def calculate_mass(components, factor):
    return {key: round(value * factor, 2) for key, value in components.items()}

def calculate_heat(CP, HP, OP, SP, WP):
    return round(339 * CP + 1030 * HP - 108.8 * (OP - SP) - 25 * WP, 4)

@app.route("/calculate", methods=["POST"])
def calculate_fuel():
    data = request.get_json()
    fuel = FuelComposition(**data)
    factors = calculate_factors(fuel.WP, fuel.AP)
    dry_mass = calculate_mass(vars(fuel), factors[0])
    combustible_mass = calculate_mass(vars(fuel), factors[1])
    heat_value = calculate_heat(fuel.CP, fuel.HP, fuel.OP, fuel.SP, fuel.WP)
    return jsonify({
        "dry_mass": dry_mass,
        "combustible_mass": combustible_mass,
        "heat_value": heat_value
    })

if __name__ == "__main__":
    app.run(debug=True)
