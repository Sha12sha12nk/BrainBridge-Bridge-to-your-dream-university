from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import base64
import os

# Set page config
st.set_page_config(
    page_title="BrainBridge: Bridge to Your Dream University",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Load datasets 

@st.cache_data
def load_data():
    universities = pd.read_csv('data/universities.csv')
    departments = pd.read_csv('data/departments.csv')
    courses = pd.read_csv('data/courses.csv')
    return universities, departments, courses

universities, departments, courses = load_data()

# Background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string.decode()});
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('images/background.jpg')

# Sidebar menu
with st.sidebar:
    menu_option = option_menu(
        menu_title="🎓 University Navigator",
        options=[
            "Home", "University Finder", "Department Explorer", "Course Recommender", 
            "Scholarship Finder", "Career Pathways", "Compare Universities", 
            "Favorites", "Events & Webinars", "Help / FAQ", "Admin Dashboard"
        ],
        icons=[
            "house", "search", "book", "bullseye", 
            "cash-coin", "briefcase", "layers", 
            "heart", "calendar-event", "question-circle", "gear"
        ],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "10px"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#f5f5f5"
            },
            "nav-link-selected": {
                "background-color": "#FF4B4B",
                "color": "white",
                "border-radius": "8px"
            },
        }
    )

# ---------------- HOME ----------------
if menu_option == "Home":
    st.title("BrainBridge: Bridge to Your Dream University")
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px;">
        Explore top universities, departments, and courses tailored to your 12th grade subjects and interests.
    </div>
    """, unsafe_allow_html=True)
    st.image("https://static.vecteezy.com/system/resources/previews/002/294/181/large_2x/welcome-to-university-web-banner-design-free-vector.jpg", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🏫 University Finder")
        st.write("Find the perfect university based on your profile")
    with col2:
        st.subheader("📚 Department Explorer")
        st.write("Explore departments across different schools")
    with col3:
        st.subheader("🎯 Course Recommender")
        st.write("Get personalized course recommendations")

# ---------------- UNIVERSITY FINDER ----------------
elif menu_option == "University Finder":
    st.title("🏫 Find Your Ideal University")

    col1, col2 = st.columns(2)
    with col1:
        subjects = st.multiselect(
            "12th Grade Subjects",
            ["Physics", "Chemistry", "Maths", "Biology", "Commerce", "Arts", "Computer Science"],
            
        )
    with col2:
        interests = st.multiselect(
            "Areas of Interest",
            ["Engineering", "Medicine", "Management", "Law", "Design", "Fashion", "Arts", "Sports"],
            
        )

    if st.button("🔍 Find Universities"):
        if not subjects or not interests:
            st.warning("Please select at least one subject and one interest")
        else:
            def subjects_match(required, selected):
                required_list = [s.strip().lower() for s in required.split(',')]
                selected_list = [s.strip().lower() for s in selected]
                return all(sub in required_list for sub in selected_list)

            matched_depts = departments[
                departments['required_subjects'].apply(lambda x: subjects_match(x, subjects))
            ]

            matched_universities = universities[
                (universities['university_id'].isin(matched_depts['university_id'])) &
                (universities['specialization'].str.lower().isin([i.lower() for i in interests]))
            ].sort_values('ranking')

            if matched_universities.empty:
                st.info("No universities found matching your criteria.")
            else:
                st.success(f"🎉 Found {len(matched_universities)} universities matching your profile.")

                for _, uni in matched_universities.iterrows():
                    with st.expander(f"🏛️ {uni['university_name']} - {uni['location']} | Rank: #{uni['ranking']}"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            if os.path.exists(uni['image_path']):
                                try:
                                    st.image('https://c8.alamy.com/comp/2F4PAHR/university-building-with-the-street-school-modern-concept-vector-illustration-2F4PAHR.jpg', width=200)
                                except Exception:
                                    st.warning("❌ Error loading image.")
                            else:
                                st.warning("📁 Image file not found.")
                        with col2:
                            st.markdown(f"""
                            **Specialization:** {uni['specialization']}  
                            **Location:** {uni['location']}  
                            **Ranking:** {uni['ranking']}
                            """)

                        uni_depts = matched_depts[matched_depts['university_id'] == uni['university_id']]
                        st.write("### Departments matching your profile")
                        cols = st.columns(3)
                        for i, (_, dept) in enumerate(uni_depts.iterrows()):
                            with cols[i % 3]:
                                if os.path.exists(dept['image_path']):
                                    try:
                                        st.image(dept['image_path'], width=150)
                                    except Exception:
                                        st.warning("❌ Failed to display department image.")
                                else:
                                    st.warning("📁 Department image not found.")
                                st.write(f"**{dept['department_name']}**")
                                st.write(f"*{dept['school_name']}*")
                                st.write(f"Required: {dept['required_subjects']}")

# ---------------- DEPARTMENT EXPLORER ----------------
elif menu_option == "Department Explorer":
    st.title("📚 Explore Top Departments")
    selected_school = st.selectbox("Select School", ["All Schools"] + list(departments['school_name'].unique()))
    filtered_depts = departments if selected_school == "All Schools" else departments[departments['school_name'] == selected_school]

    cols = st.columns(3)
    for i, (_, dept) in enumerate(filtered_depts.iterrows()):
        with cols[i % 3]:
            if os.path.exists(dept['image_path']):
                st.image(dept['image_path'], use_container_width=True)
            else:
                st.warning("📁 Image not found.")
            st.subheader(dept['department_name'])
            uni_name = universities[universities['university_id'] == dept['university_id']]['university_name'].values[0]
            st.write(f"**University:** {uni_name}")
            st.write(f"**Required Subjects:** {dept['required_subjects']}")
            dept_courses = courses[courses['department_id'] == dept['department_id']]
            if not dept_courses.empty:
                st.write("**Courses Offered:**")
                for _, course in dept_courses.iterrows():
                    st.write(f"- {course['course_title']} ({course['level']})")

# ---------------- COURSE RECOMMENDER ----------------
elif menu_option == "Course Recommender":
    st.title("🎯 Course Recommendation")
    with st.form("course_recommendation_form"):
        course_title = st.selectbox("Enter Course Title", courses['course_title'].unique())
        col1, col2 = st.columns(2)
        with col1:
            subject_filter = st.selectbox("Filter by Subject", ["All Subjects"] + list(courses['subject'].unique()))
        with col2:
            level_filter = st.selectbox("Filter by Level", ["All Levels", "Undergraduate", "Postgraduate"])
        num_recommendations = st.slider("Number of Recommendations", 1, 20, 7)
        submitted = st.form_submit_button("Recommend")

    if submitted:
        selected_course = courses[courses['course_title'] == course_title].iloc[0]
        similar_courses = courses[
            (courses['subject'] == selected_course['subject']) & 
            (courses['course_id'] != selected_course['course_id'])
        ]
        if subject_filter != "All Subjects":
            similar_courses = similar_courses[similar_courses['subject'] == subject_filter]
        if level_filter != "All Levels":
            similar_courses = similar_courses[similar_courses['level'] == level_filter]
        similar_courses = similar_courses.head(num_recommendations)
        for _, course in similar_courses.iterrows():
            dept = departments[departments['department_id'] == course['department_id']].iloc[0]
            uni = universities[universities['university_id'] == dept['university_id']].iloc[0]
            with st.expander(course['course_title']):
                col1, col2 = st.columns([1, 3])
                with col1:
                    if os.path.exists(dept['image_path']):
                        st.image(dept['image_path'], width=150)
                with col2:
                    st.write(f"**University:** {uni['university_name']}")
                    st.write(f"**Department:** {dept['department_name']}")
                    st.write(f"**Level:** {course['level']}")
                    st.write(f"**Price:** ₹{course['price']}")
                    st.write(f"**Popularity:** {course['num_subscribers']} students")

# ---------------- NEW TABS ----------------
elif menu_option == "Scholarship Finder":
    st.header("🎓 Find Scholarships Based on Your Preferences")

    # Load scholarships dataset
    try:
        scholarships = pd.read_csv("data/scholarships.csv")
    except FileNotFoundError:
        st.error("❌ scholarships.csv file not found in data folder!")
        st.stop()

    # Drop rows with missing essential data
    scholarships = scholarships.dropna(subset=["scholarship_name", "country", "eligibility"])

    # Filters
    country = st.selectbox("Select Country", scholarships['country'].dropna().unique())
    level = st.selectbox("Select Study Level", scholarships['level'].dropna().unique())
    field = st.selectbox("Select Field of Study", scholarships['field'].dropna().unique())

    # Apply filters
    results = scholarships[
        (scholarships['country'] == country) &
        (scholarships['level'] == level) &
        (scholarships['field'] == field)
    ]

    st.subheader(f"🎯 Found {len(results)} Scholarships:")

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            ### 🏅 {row['scholarship_name']}
            - 🌍 **Country**: {row['country']}
            - 🎓 **Level**: {row['level']}
            - 🧪 **Field**: {row['field']}
            - ✅ **Eligibility**: {row['eligibility']}
            - 💰 **Amount**: {row.get('amount', 'N/A')}
            - 🔗 [More Info]({row.get('link', '#')})
            """)
    else:
        st.warning("😕 No scholarships found for the selected filters.")



elif menu_option == "Career Pathways":
    st.title("🧭 Career Pathways")
    st.write("Select a subject or course to explore possible career paths.")

    selected_subject = st.selectbox("Choose a Subject", ["Engineering", "Medicine", "Law", "Commerce", "Arts"])
    career_map = {
    "Engineering": [
        "Software Developer", "Data Scientist", "Civil Engineer", "Product Manager", "AI Engineer",
        "Mechanical Engineer", "Electrical Engineer", "DevOps Engineer", "Robotics Specialist", "Cybersecurity Analyst"
    ],
    "Medicine": [
        "Doctor", "Surgeon", "Medical Researcher", "Healthcare Admin", "Dentist",
        "Veterinarian", "Physiotherapist", "Psychiatrist", "Pharmacist", "Radiologist"
    ],
    "Law": [
        "Lawyer", "Judge", "Legal Advisor", "Corporate Counsel", "Public Prosecutor",
        "Legal Journalist", "Human Rights Advocate", "Notary", "Legal Analyst", "Compliance Officer"
    ],
    "Commerce": [
        "Chartered Accountant", "Investment Banker", "Auditor", "Economist", "Financial Analyst",
        "Tax Consultant", "Stock Broker", "Actuary", "Business Analyst", "Cost Accountant"
    ],
    "Arts": [
        "Journalist", "Graphic Designer", "Writer", "Professor", "Social Media Manager",
        "Filmmaker", "Theatre Artist", "Historian", "Animator", "UX/UI Designer"
    ],
    "Science": [
        "Physicist", "Chemist", "Biotechnologist", "Research Scientist", "Lab Technician",
        "Astronomer", "Environmental Scientist", "Mathematician", "Oceanographer", "Geologist"
    ],
    "Management": [
        "Business Consultant", "HR Manager", "Marketing Manager", "Operations Manager", "Project Manager",
        "Entrepreneur", "Product Manager", "Brand Strategist", "Sales Head", "Supply Chain Analyst"
    ],
    "Design": [
        "UX Designer", "Interior Designer", "Fashion Designer", "Product Designer", "Game Designer",
        "Industrial Designer", "UI Designer", "Motion Graphic Artist", "Visual Designer", "Art Director"
    ],
    "IT & Computers": [
        "Software Engineer", "Web Developer", "Cloud Architect", "IT Support Specialist", "Blockchain Developer",
        "AI/ML Engineer", "Full Stack Developer", "System Analyst", "Game Developer", "Tech Lead"
    ]
}


    if selected_subject:
        st.write("### Suggested Careers:")
        for career in career_map[selected_subject]:
            st.success(f"✅ {career}")


elif menu_option == "Compare Universities":
    st.title("📊 Compare Universities")

    uni_names = universities['university_name'].unique()
    uni1 = st.selectbox("Select First University", uni_names)
    uni2 = st.selectbox("Select Second University", uni_names, index=1 if len(uni_names) > 1 else 0)

    if uni1 != uni2:
        u1 = universities[universities['university_name'] == uni1].iloc[0]
        u2 = universities[universities['university_name'] == uni2].iloc[0]

        st.write("### 📌 Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(uni1)
            st.write(f"**Location:** {u1['location']}")
            st.write(f"**Specialization:** {u1['specialization']}")
            st.write(f"**Ranking:** #{u1['ranking']}")
        
        with col2:
            st.subheader(uni2)
            st.write(f"**Location:** {u2['location']}")
            st.write(f"**Specialization:** {u2['specialization']}")
            st.write(f"**Ranking:** #{u2['ranking']}")
    else:
        st.warning("Please select two different universities.")


elif menu_option == "Favorites":
    st.title("❤️ Your Favorite Universities & Courses")

    st.info("🔐 Login system required for saving favorites. Currently, here are popular options:")
    popular_favorites = [
        "IIT Bombay – Computer Science",
        "Harvard University – Economics",
        "IIM Ahmedabad – MBA",
        "NID Ahmedabad – Product Design"
    ]
    for item in popular_favorites:
        st.write(f"⭐ {item}")


elif menu_option == "Events & Webinars":
    st.title("📅 Upcoming Events & Webinars")
    st.write("Stay updated with the latest university events and sessions.")


    events = [
        {"title": "MIT Admissions Webinar", "date": "June 15, 2025", "link": "https://calendar.mit.edu/"},
        {"title": "Study in UK Fair", "date": "July 1, 2025", "link": "https://study-uk.britishcouncil.org"},
        {"title": "Ask Me Anything – IIM Alumni", "date": "July 10, 2025", "link": "https://www.iima.ac.in/the-institute/events"}
    ]

    for event in events:
        with st.expander(f"📌 {event['title']} – {event['date']}"):
            st.markdown(f"[🔗 Join or Register Here]({event['link']})")


elif menu_option == "Help / FAQ":
    st.title("❓ Help / Frequently Asked Questions")
    st.write("Here you'll find guides, tips, and support for using this app effectively.")
    st.markdown("""
    - **Q:** How does the recommendation engine work?  
      **A:** Based on your subject choices and interests, it filters matching departments and universities.
    
    - **Q:** Can I save my preferences?  
      **A:** This feature will be available soon under **Favorites**.
    
    - **Q:** What data is this app using?  
      **A:** It's based on a curated CSV dataset of universities, departments, and courses.
    """)

# ---------------- ADMIN ----------------
elif menu_option == "Admin Dashboard":
    st.title("⚙️ Admin Dashboard")
    tab1, tab2, tab3 = st.tabs(["Universities", "Departments", "Courses"])
    with tab1:
        st.subheader("Manage Universities")
        st.dataframe(universities)
    with tab2:
        st.subheader("Manage Departments")
        st.dataframe(departments)
    with tab3:
        st.subheader("Manage Courses")
        st.dataframe(courses)
