def calculate_risk_score(age, income, driving_record, smoker, disease="None", dependents=0):
    score = 0

    # 1️⃣ Age factor
    if age < 25:
        score += 2
    elif age > 60:
        score += 3
    else:
        score += 1

    # 2️⃣ Income level factor (Annual income)
    if income < 300000:          # below ₹3L = financial stress
        score += 3
    elif income < 600000:        # ₹3–6L = moderate
        score += 2
    elif income < 1000000:       # ₹6–10L = stable middle
        score += 1
    else:                        # ₹10L+ = low financial risk
        score += 0

    # 3️⃣ Driving record
    if driving_record == "DUI":
        score += 3
    elif driving_record == "Major Violations":
        score += 2
    elif driving_record == "Minor Violations":
        score += 1

    # 4️⃣ Smoking
    if smoker == "Yes":
        score += 3

    # 5️⃣ Health conditions
    if disease != "None":
        if disease in ["Diabetes", "Hypertension", "Asthma"]:
            score += 2
        elif disease in ["Heart Disease", "Cancer"]:
            score += 3
        else:
            score += 1

    # 6️⃣ Dependents (financial load)
    if dependents >= 4:
        score += 2
    elif dependents >= 2:
        score += 1

    # 7️⃣ Risk interpretation
    if score <= 3:
        return "Low Risk"
    elif score <= 7:
        return "Medium Risk"
    else:
        return "High Risk"
    