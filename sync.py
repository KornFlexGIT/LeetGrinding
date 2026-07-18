import os
import requests

# ดึงค่า Secret จาก GitHub Actions
SESSION = os.environ.get('LEETCODE_SESSION')
CSRF = os.environ.get('CSRF_TOKEN')
USERNAME = "2KYGyCtezl" # ID ของคุณ

headers = {
    'Cookie': f'LEETCODE_SESSION={SESSION}; csrftoken={CSRF}',
    'x-csrftoken': CSRF,
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com'
}

# แมปปิ้งนามสกุลไฟล์ให้ตรงกับภาษาที่ใช้เขียน
EXTENSIONS = {
    'cpp': '.cpp', 'python': '.py', 'python3': '.py', 'java': '.java',
    'javascript': '.js', 'c': '.c', 'csharp': '.cs', 'golang': '.go',
    'typescript': '.ts', 'sql': '.sql'
}

def fetch_graphql(query, variables):
    url = "https://leetcode.com/graphql"
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response.json()

def sync_leetcode():
    # 1. ดึงข้อมูลโจทย์ล่าสุดที่ทำผ่าน
    query_recent = """
    query($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: 15) {
        id
        title
        titleSlug
      }
    }
    """
    recent_data = fetch_graphql(query_recent, {"username": USERNAME, "limit": 15})
    submissions = recent_data.get('data', {}).get('recentAcSubmissionList', [])

    if not submissions:
        print("ไม่พบข้อมูลการส่งโค้ด หรือ Session อาจจะหมดอายุ")
        return

    for sub in submissions:
        sub_id = sub['id']
        title = sub['title']
        slug = sub['titleSlug']

        # 2. ดึงซอร์สโค้ดที่คุณเขียนผ่าน API
        query_code = """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
            lang { name }
          }
        }
        """
        code_data = fetch_graphql(query_code, {"submissionId": int(sub_id)})
        details = code_data.get('data', {}).get('submissionDetails')
        
        if not details:
            print(f"ดึงซอร์สโค้ดข้อ {title} ไม่สำเร็จ ข้ามไปก่อน...")
            continue
            
        source_code = details['code']
        lang_name = details['lang']['name']
        ext = EXTENSIONS.get(lang_name, '.txt') # หานามสกุลไฟล์

        # 3. ดึงหมวดหมู่ (Topic Tags) ของโจทย์ข้อนี้
        query_tag = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            topicTags { slug }
          }
        }
        """
        tag_data = fetch_graphql(query_tag, {"titleSlug": slug})
        tags = tag_data.get('data', {}).get('question', {}).get('topicTags', [])
        
        # เลือก Tag แรกมาตั้งเป็นชื่อโฟลเดอร์หลัก ถ้าไม่มีให้ใส่ uncategorized
        # เช่น 'array', 'hash-table', 'math'
        main_tag = tags[0]['slug'].replace('-', '_') if tags else 'uncategorized'

        # 4. สร้างโครงสร้างโฟลเดอร์และบันทึกโค้ด
        # จะได้โครงสร้างแบบ: LeetCode/array/two-sum/solution.cpp
        folder_path = f"LeetCode/{main_tag}/{slug}"
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = f"{folder_path}/solution{ext}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)
            
        print(f"✅ บันทึกข้อ '{title}' ลงในหมวดหมู่ [{main_tag}] เรียบร้อยแล้ว!")

if __name__ == "__main__":
    sync_leetcode()
