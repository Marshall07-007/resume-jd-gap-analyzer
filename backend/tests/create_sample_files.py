import os
import pymupdf
import docx

sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(sample_dir, exist_ok=True)

# 1. Generate sample PDF resume
pdf_path = os.path.join(sample_dir, "sample_resume_frontend.pdf")
doc = pymupdf.open()
page = doc.new_page()

pdf_text = """Alex Morgan
alex.morgan@example.com | (555) 234-5678 | github.com/alexmorgan | linkedin.com/in/alexmorgan

EDUCATION
Bachelor of Science in Computer Science, State University (2024)

TECHNICAL SKILLS
Languages: HTML5, CSS3, JavaScript (ES6+), Git
Frameworks: ReactJS, Tailwind CSS
Tools: VS Code, Git, GitHub

PROJECTS
Student Learning Portal
• Developed a responsive single-page student dashboard using HTML, CSS, and JavaScript.
• Integrated local storage persistence and dynamic DOM state management.
• Managed codebase version control using Git and published repository to GitHub.

Weather Forecasting App
• Built a weather forecast web application utilizing JavaScript and CSS Grid.
• Interfaced with open weather APIs and handled asynchronous fetch requests.
"""

page.insert_text((50, 50), pdf_text, fontsize=11)
doc.save(pdf_path)
doc.close()
print(f"Generated sample PDF at: {pdf_path}")

# 2. Generate sample DOCX resume
docx_path = os.path.join(sample_dir, "sample_resume_qa.docx")
doc_word = docx.Document()
doc_word.add_heading("Taylor Reed - QA Tester", level=0)
doc_word.add_paragraph("Email: taylor.reed@example.com | Phone: (555) 987-6543 | LinkedIn: linkedin.com/in/taylorreed")

doc_word.add_heading("EDUCATION", level=1)
doc_word.add_paragraph("B.Tech in Information Technology, Global Institute of Technology (2023)")

doc_word.add_heading("SKILLS", level=1)
doc_word.add_paragraph("Manual Testing, Test Cases, Bug Reporting, Postman, SQL, Git")

doc_word.add_heading("PROJECTS", level=1)
doc_word.add_paragraph("E-Commerce Web Application Testing Suite")
doc_word.add_paragraph("• Authored 60+ functional and boundary test cases for user authentication and checkout cart.")
doc_word.add_paragraph("• Logged and tracked critical defect lifecycles with structured reproduction steps.")
doc_word.add_paragraph("• Executed RESTful API test assertions using Postman.")

doc_word.save(docx_path)
print(f"Generated sample DOCX at: {docx_path}")
