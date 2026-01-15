import requests
import json
import matplotlib.pyplot as plt

URL = "http://live-test-scores.herokuapp.com/scores/"

students = []
scores = []

response = requests.get(URL, stream=True)

for line in response.iter_lines():
    if line:
        decoded = line.decode("utf-8")
        if decoded.startswith("data:"):
            record = json.loads(decoded.replace("data: ", ""))
            students.append(record["studentId"])
            scores.append(record["score"])

        if len(scores) == 10:
            break

# Convert to percentage scale
scores = [round(score * 100, 1) for score in scores]

# Sort by score
sorted_data = sorted(zip(students, scores), key=lambda x: x[1])
students, scores = zip(*sorted_data)

average_score = round(sum(scores) / len(scores), 1)
print("Average Score:", average_score)

# Color logic
colors = []
for score in scores:
    if score >= 75:
        colors.append("green")
    elif score >= 60:
        colors.append("orange")
    else:
        colors.append("red")

plt.bar(students, scores, color=colors)

plt.axhline(
    average_score,
    linestyle='--',
    label=f"Average Score: {average_score}"
)

plt.legend()


# Value labels
for i, score in enumerate(scores):
    plt.text(i, score, f"{score}", ha="center", va="bottom", fontsize=8)

plt.title("Student Test Scores (Scaled to 100)")
plt.xlabel("Students (sorted by score)")
plt.ylabel("Score (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("student_scores.png", dpi=300, bbox_inches="tight")
plt.show()
