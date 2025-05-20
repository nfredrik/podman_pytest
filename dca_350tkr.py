import numpy as np
import matplotlib.pyplot as plt

def simulate_investment_lump_sum(amount, periods, annual_return, volatility):
    """
    Simulerar en engångsinvestering (lump sum) där hela beloppet investeras direkt
    och sedan växer med en genomsnittlig ränta (med viss volatilitet) under 'periods' månader.
    """
    # Räknar ut månatlig genomsnittlig avkastning baserat på den årliga
    monthly_return = (1 + annual_return) ** (1/12) - 1
    values = [amount]  # Investeringen vid tidpunkt 0
    balance = amount
    for _ in range(periods):
        # Simulera en månatlig avkastning med något spridning (volatilitet)
        r = np.random.normal(loc=monthly_return, scale=volatility)
        balance *= (1 + r)
        values.append(balance)
    return values

def simulate_investment_dca(total_amount, periods, annual_return, volatility):
    """
    Simulerar Dollar Cost Averaging (DCA) genom att dela upp 'total_amount' i lika stora,
    månatliga investeringar över 'periods' månader. Varje månad investeras en fast summa,
    och portföljen antar en viss avkastning (med volatilitet).
    """
    monthly_investment = total_amount / periods
    monthly_return = (1 + annual_return) ** (1/12) - 1
    values = []
    balance = 0.0
    for _ in range(periods):
        # Lägg till den månatliga investeringen
        balance += monthly_investment
        # Applicera avkastningen för månaden
        r = np.random.normal(loc=monthly_return, scale=volatility)
        balance *= (1 + r)
        values.append(balance)
    return values

# Inställningar för simuleringen
total_amount = 350000         # Totalt investeringsbelopp (kr)
periods = 12                  # Antal månader över vilka investeringen sprids ut
annual_return = 0.05          # Antagen årlig avkastning (5% exempelvis)
volatility = 0.05             # Månadsvolatilitet (kan justeras)

# Sätter en frö (seed) för återupprepbarhet i simuleringen
np.random.seed(42)

# Kör simuleringen
lump_sum_values = simulate_investment_lump_sum(total_amount, periods, annual_return, volatility)
dca_values = simulate_investment_dca(total_amount, periods, annual_return, volatility)

# Plotta resultaten
months_axis_lump = list(range(0, periods + 1))  # Från tid 0 till periodens slut
print(lump_sum_values)
months_axis_dca = list(range(1, periods + 1))    # DCA-värden för varje investeringsmånad

plt.figure(figsize=(10, 6))
plt.plot(months_axis_lump, lump_sum_values, label="Lump Sum", marker="o")
plt.plot(months_axis_dca, dca_values, label="DCA", marker="s")
plt.xlabel("Månader")
plt.ylabel("Portföljvärde (kr)")
plt.title("Simulering: Engångsinvestering vs. DCA")
plt.legend()
plt.grid(True)
plt.show()
