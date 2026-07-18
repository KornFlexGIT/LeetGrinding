import os
import requests
import json

# ดึงค่า Secrets จาก GitHub Actions
SESSION = os.environ.get('LEETCODE_SESSION')
CSRF = os.environ.get('CSRF_TOKEN')

# ตั้งค่า Headers สำหรับการเรียก LeetCode API
headers = {
    'Cookie': f'LEETCODE_SESSION={SESSION}; csrftoken={CSRF}',
    'x-csrftoken': CSRF,
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com'
}

def get_recent_submissions():
    # นี่คือ GraphQL Query เบื้องต้นสำหรับดึงข้อมูลการส่งโค้ดล่าสุด
    url = "https://leetcode.com/graphql"
    query = """
    query {
      recentAcSubmissionList(username: "YOUR_LEETCODE_USERNAME", limit: 15) {
        id
        title
        titleSlug
      }
    }
    """
    # หมายเหตุ: ในการใช้งานจริง จะต้องมีการเขียน Query ดึงโค้ด (Code) และ Tag (เช่น Array)
    # เพิ่มเติมผ่าน API รายโจทย์เพื่อนำมาสร้างโฟลเดอร์
    
    response = requests.post(url, json={'query': query}, headers=headers)
    print("ดึงข้อมูลสำเร็จ!", response.json())
    # โค้ดส่วนจัดการโฟลเดอร์และสร้างไฟล์จะถูกเขียนต่อในบริเวณนี้
    # เช่น os.makedirs('LeetCode/array', exist_ok=True)

if __name__ == "__main__":
    get_recent_submissions()
