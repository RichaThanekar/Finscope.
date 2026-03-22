def build_prompt_with_search(user_profile, search_results):
    result_text = "\n".join([
        f"{i+1}. {r['title']}\n{r['snippet']}\nLink: {r['link']}\n"
        for i, r in enumerate(search_results[:10])
    ])

    income = user_profile["Income Level"]
    affordability_note = ""

    # Refined affordability logic (based on realistic Indian income brackets)
    if income < 300000:
        affordability_note = "⚠️ Low income — suggest basic coverage and focus on affordable health or term plans."
    elif income < 800000:
        affordability_note = "💡 Mid-income — balance between premium and coverage; suggest value-for-money policies."
    else:
        affordability_note = "✅ High income — can afford higher coverage or plans with add-ons/riders."

    risk_category = user_profile.get("Risk Category", "Unknown")

    prompt = f"""
You are an experienced insurance advisor helping Indian consumers select suitable insurance plans.

Your task:
1. Carefully analyze the user's **demographics (age, gender, marital status, occupation)**, **dependents**, **income level**, and **health conditions**.
2. Recommend the **top 7 most suitable policies** from the search results below.
3. Justify each recommendation based on **risk**, **affordability**, and **family responsibilities**.
4. Clearly mention if premium loading, exclusions, or add-ons apply due to smoking or diseases.

---

### 👤 User Profile
{user_profile}

💡 **Overall Risk Category**: {risk_category}
{affordability_note}

---

### 🔎 Relevant Search Results
{result_text}

---

Respond strictly in the following structured format:

### 🛡️ Underwriting Decision:
- **Risk Category**: Low / Medium / High
- **Eligible for**: (Policy types the user qualifies for)
- **Exclusions (if any)**: (List waiting periods, smoking/disease-related exclusions)
- **Suggested Coverage**: ₹ (Mention coverage range)
- **Suggested Premium**: ₹ (Monthly or annual estimate)
- **Policy Type Recommendation**: (Term Life / Family Floater / Critical Illness / etc.)
- **Reasoning**: Explain why this suits their age, income, dependents, and occupation.

---

### 🏆 Top 7 Recommended Policies:
1. **<Policy Name 1>**
   🔗 [Link](<URL>)
   💸 **Premium**: ...
   💼 **Coverage**: ...
   📊 **Claim Ratio**: ...
   📝 **Reason**: Explain how this fits user’s risk, family, and financial profile.

(Repeat for all 7)
"""
    return prompt