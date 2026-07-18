import os
import requests
import json

SESSION = os.environ.get('LEETCODE_SESSION')
CSRF = os.environ.get('CSRF_TOKEN')

headers = {
    'Cookie': f'LEETCODE_SESSION={SESSION}; csrftoken={CSRF}',
    'x-csrftoken': CSRF,
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com'
}

def sync_leetcode():
    url = "https://leetcode.com/graphql"
    # Query ดึงข้อมูล 5 ข้อล่าสุดที่ผ่าน (เปลี่ยน YOUR_USERNAME เป็นชื่อผู้ใช้ LeetCode ของคุณด้วยครับ)
    query = """
    query {
      recentAcSubmissionList(username: "2KYGyCtezl", limit: 5) {
        id
        title
        titleSlug
      }
    }
    """
    
    response = requests.post(url, json={'query': query}, headers=headers)
    data = response.json()
    submissions = data.get('data', {}).get('recentAcSubmissionList', [])
    
    if not submissions:
        print("ไม่พบข้อมูล หรือ Session/Token หมดอายุ")
        return

    for sub in submissions:
        title = sub['title']
        slug = sub['titleSlug']
        
        # สร้างหมวดหมู่โฟลเดอร์ (เบื้องต้นจะสร้างโฟลเดอร์ชื่อ LeetCode/ตามด้วยชื่อโจทย์)
        # *หากต้องการแยกเป็น array, math ต้องใช้ GraphQL ดึง topicTags เพิ่มเติม*
        folder_path = f"LeetCode/{slug}"
        os.makedirs(folder_path, exist_ok=True)
        
        # สร้างไฟล์ README หรือไฟล์จำลองโค้ดเก็บไว้ในโฟลเดอร์
        file_path = f"{folder_path}/README.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nซิงค์ข้อมูลอัตโนมัติสำเร็จแล้ว!")
            
        print(f"สร้างโฟลเดอร์และบันทึกข้อ {title} สำเร็จ!")

if __name__ == "__main__":
    sync_leetcode()
