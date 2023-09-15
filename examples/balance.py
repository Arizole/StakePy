from StakePy import Stake

stake = Stake("API KEY", "USER AGENT", "CF CLEARANCE")

def get_available_balances():
    # Get Convertion Rate
    rate_data = {}
    convert_rate = stake.get_convert_rate()
    for rate in convert_rate["data"]["info"]["currencies"]:
        rate_data[rate["name"]] = rate["jpy"]
    
    # Get Available Balances
    balance = stake.get_balances()
    balance_data = {}
    for bl in balance["data"]["user"]["balances"]:
        if bl["available"]["amount"] == 0:
            continue
        balance_data[bl["available"]["currency"]] = {
            "raw": bl["available"]["amount"],
            "cal": bl["available"]["amount"] * rate_data[bl["available"]["currency"]]
        }
    
    # Show Balances
    for bl_data_name in balance_data.keys():
        bl_data = balance_data[bl_data_name]
        raw = bl_data["raw"]
        cal = bl_data["cal"]
        print(f"{bl_data_name}: {raw}({cal}JPY)")

if __name__ == "__main__":
    get_available_balances()