import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id, github_repo_url):
    # 1. Read PEM file as-is (multi-line, DO NOT modify)
    with open("student_public.pem", "r") as f:
        pem_key = f.read()

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,  # NO .git
        "public_key": pem_key  # keep multi-line as-is
    }

    # 2. Send POST request
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        data = response.json()
    except Exception as e:
        print("Request failed:", e)
        return

    if data.get("status") != "success":
        print("API error:", data)
        return

    # 3. Save encrypted seed to file (DO NOT COMMIT)
    with open("encrypted_seed.txt", "w") as f:
        f.write(data["encrypted_seed"])

    print("Encrypted seed saved to encrypted_seed.txt")

# Run script
request_seed(
    student_id="23P31A0528",
    github_repo_url="https://github.com/koonisettimahesh/pki-2fa-project"
)
