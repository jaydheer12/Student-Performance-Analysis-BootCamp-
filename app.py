import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 16px;
        color: #666;
        margin-top: 5px;
    }
    
    .add-student-form {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        border: 2px dashed #667eea;
        margin-bottom: 25px;
    }
    
    .student-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 14px rgba(102, 126, 234, 0.2);
    }
    
    .success-button>button {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
    }
    
    .warning-button>button {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 25px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'students' not in st.session_state:
    st.session_state.students = []
    st.session_state.student_counter = 1

# Available names for random generation
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Susan', 'Richard', 'Jessica', 'Joseph', 'Sarah',
    'Thomas', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Margaret',
    'Anthony', 'Sandra', 'Mark', 'Ashley', 'Donald', 'Dorothy', 'Steven', 'Betty'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
    'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson'
]

# Header
st.markdown("""
<div class="header">
    <h1>🎓 Student Performance Dashboard</h1>
    <h3>Data Analytics Bootcamp - Student Management System</h3>
</div>
""", unsafe_allow_html=True)

# ===========================================
# MAIN CONTENT AREA - STUDENT ADDING SECTION
# ===========================================
st.markdown("## 👥 Add New Students")

# Create tabs for different ways to add students
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Add Single Student", 
    "🎲 Add Random Students", 
    "📊 Bulk Add Students", 
    "📁 Import from CSV"
])

# Tab 1: Add Single Student Form
with tab1:
    st.markdown('<div class="add-student-form">', unsafe_allow_html=True)
    st.markdown("### 📝 Add Single Student")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("Student Name", placeholder="Enter full name", key="single_name")
        
    with col2:
        student_id = st.text_input("Student ID (Optional)", placeholder="Leave blank for auto-generated")
    
    col3, col4 = st.columns(2)
    
    with col3:
        study_hours = st.slider(
            "Daily Study Hours",
            min_value=0.0,
            max_value=12.0,
            value=4.0,
            step=0.5,
            help="Hours spent studying per day"
        )
    
    with col4:
        final_score = st.slider(
            "Final Score (%)",
            min_value=0,
            max_value=100,
            value=75,
            step=1,
            help="Final exam score in percentage"
        )
    
    # Performance category based on score
    if final_score >= 85:
        performance = "Excellent 🌟"
        color = "#4CAF50"
    elif final_score >= 70:
        performance = "Good 👍"
        color = "#2196F3"
    elif final_score >= 50:
        performance = "Average 📊"
        color = "#FF9800"
    else:
        performance = "Needs Improvement 📈"
        color = "#F44336"
    
    # Display performance preview
    st.markdown(f"""
    <div style="background-color: {color}20; padding: 15px; border-radius: 10px; border-left: 4px solid {color}; margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>Performance Preview:</strong>
                <span style="color: {color}; font-weight: bold; margin-left: 10px;">{performance}</span>
            </div>
            <div>
                <strong>Predicted:</strong>
                <span style="margin-left: 10px;">{round(40 + 7 * study_hours, 1)}%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("➕ Add Student", type="primary", use_container_width=True):
            if student_name:
                # Generate ID if not provided
                if not student_id:
                    student_id = f"STU{st.session_state.student_counter:03d}"
                
                # Create student record
                new_student = {
                    'id': student_id,
                    'name': student_name,
                    'study_hours': study_hours,
                    'final_score': final_score,
                    'performance': performance,
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'manual'
                }
                
                # Add to session state
                st.session_state.students.append(new_student)
                st.session_state.student_counter += 1
                
                st.success(f"✅ Student '{student_name}' added successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Please enter a student name!")
    
    with col_btn2:
        if st.button("🔄 Reset Form", type="secondary", use_container_width=True):
            st.rerun()
    
    with col_btn3:
        if st.button("🎲 Generate Random Student", type="secondary", use_container_width=True):
            # Auto-fill form with random data
            random_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            random_hours = round(random.uniform(1, 10), 1)
            random_score = round(random.uniform(50, 100), 1)
            
            # Update form values using session state
            st.session_state.single_name = random_name
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Add Random Students
with tab2:
    st.markdown('<div class="add-student-form">', unsafe_allow_html=True)
    st.markdown("### 🎲 Generate Random Students")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Random generation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_students = st.number_input(
            "Number of Students",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            help="How many random students to generate"
        )
    
    with col2:
        score_range = st.slider(
            "Score Range",
            min_value=0,
            max_value=100,
            value=(50, 90),
            help="Range for random scores"
        )
    
    with col3:
        hours_range = st.slider(
            "Study Hours Range",
            min_value=0.0,
            max_value=12.0,
            value=(2.0, 8.0),
            step=0.5,
            help="Range for random study hours"
        )
    
    # Preview of what will be generated
    st.markdown("#### Preview of Random Generation:")
    preview_cols = st.columns(3)
    
    with preview_cols[0]:
        st.metric("Students to Add", num_students)
    
    with preview_cols[1]:
        st.metric("Avg Score", f"{(score_range[0] + score_range[1]) / 2:.0f}%")
    
    with preview_cols[2]:
        st.metric("Avg Hours", f"{(hours_range[0] + hours_range[1]) / 2:.1f}")
    
    # Generate button
    col_gen1, col_gen2 = st.columns([1, 3])
    
    with col_gen1:
        if st.button("🎲 Generate Students", type="primary", use_container_width=True):
            with st.spinner(f"Generating {num_students} random students..."):
                added_count = 0
                
                for i in range(num_students):
                    # Generate random name
                    first_name = random.choice(FIRST_NAMES)
                    last_name = random.choice(LAST_NAMES)
                    full_name = f"{first_name} {last_name}"
                    
                    # Generate random data within ranges
                    hours = round(random.uniform(hours_range[0], hours_range[1]), 1)
                    score = round(random.uniform(score_range[0], score_range[1]), 1)
                    
                    # Determine performance
                    if score >= 85:
                        performance = "Excellent 🌟"
                    elif score >= 70:
                        performance = "Good 👍"
                    elif score >= 50:
                        performance = "Average 📊"
                    else:
                        performance = "Needs Improvement 📈"
                    
                    # Create student ID
                    student_id = f"STU{st.session_state.student_counter:03d}"
                    
                    # Create student record
                    new_student = {
                        'id': student_id,
                        'name': full_name,
                        'study_hours': hours,
                        'final_score': score,
                        'performance': performance,
                        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'type': 'random'
                    }
                    
                    # Add to session state
                    st.session_state.students.append(new_student)
                    st.session_state.student_counter += 1
                    added_count += 1
                
                st.success(f"✅ Successfully generated {added_count} random students!")
                st.balloons()
                st.rerun()
    
    with col_gen2:
        if st.button("✨ Generate High Performers", type="secondary", use_container_width=True):
            # Generate 3 high-performing students
            for i in range(3):
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                student_id = f"STU{st.session_state.student_counter:03d}"
                
                new_student = {
                    'id': student_id,
                    'name': name,
                    'study_hours': round(random.uniform(6, 10), 1),
                    'final_score': round(random.uniform(85, 98), 1),
                    'performance': "Excellent 🌟",
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'high_performer'
                }
                
                st.session_state.students.append(new_student)
                st.session_state.student_counter += 1
            
            st.success("✅ Generated 3 high-performing students!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Bulk Add Students
with tab3:
    st.markdown('<div class="add-student-form">', unsafe_allow_html=True)
    st.markdown("### 📊 Bulk Add Students")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Quick Add Options:** Add multiple students with predefined characteristics.
    """)
    
    # Bulk add options in columns
    col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
    
    with col_bulk1:
        if st.button("📚 Add 5 Average Students", use_container_width=True):
            for i in range(5):
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                student_id = f"STU{st.session_state.student_counter:03d}"
                
                new_student = {
                    'id': student_id,
                    'name': name,
                    'study_hours': round(random.uniform(3, 6), 1),
                    'final_score': round(random.uniform(60, 80), 1),
                    'performance': "Average 📊",
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'bulk_average'
                }
                
                st.session_state.students.append(new_student)
                st.session_state.student_counter += 1
            
            st.success("✅ Added 5 average students!")
            st.rerun()
    
    with col_bulk2:
        if st.button("🌟 Add 3 Top Students", use_container_width=True):
            for i in range(3):
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                student_id = f"STU{st.session_state.student_counter:03d}"
                
                new_student = {
                    'id': student_id,
                    'name': name,
                    'study_hours': round(random.uniform(7, 10), 1),
                    'final_score': round(random.uniform(90, 100), 1),
                    'performance': "Excellent 🌟",
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'bulk_top'
                }
                
                st.session_state.students.append(new_student)
                st.session_state.student_counter += 1
            
            st.success("✅ Added 3 top-performing students!")
            st.rerun()
    
    with col_bulk3:
        if st.button("📈 Add 4 Improving Students", use_container_width=True):
            for i in range(4):
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                student_id = f"STU{st.session_state.student_counter:03d}"
                
                new_student = {
                    'id': student_id,
                    'name': name,
                    'study_hours': round(random.uniform(4, 8), 1),
                    'final_score': round(random.uniform(55, 75), 1),
                    'performance': "Good 👍",
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'bulk_improving'
                }
                
                st.session_state.students.append(new_student)
                st.session_state.student_counter += 1
            
            st.success("✅ Added 4 improving students!")
            st.rerun()
    
    # Manual bulk entry
    st.markdown("---")
    st.markdown("#### Or enter multiple students manually:")
    
    manual_input = st.text_area(
        "Enter student data (one per line, format: Name, Hours, Score)",
        placeholder="John Doe, 4.5, 85\nJane Smith, 6.0, 92\n...",
        height=100
    )
    
    if st.button("📥 Import from Text", type="secondary"):
        if manual_input:
            lines = manual_input.strip().split('\n')
            imported_count = 0
            
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 3:
                    try:
                        name = parts[0]
                        hours = float(parts[1])
                        score = float(parts[2])
                        
                        # Determine performance
                        if score >= 85:
                            performance = "Excellent 🌟"
                        elif score >= 70:
                            performance = "Good 👍"
                        elif score >= 50:
                            performance = "Average 📊"
                        else:
                            performance = "Needs Improvement 📈"
                        
                        student_id = f"STU{st.session_state.student_counter:03d}"
                        
                        new_student = {
                            'id': student_id,
                            'name': name,
                            'study_hours': hours,
                            'final_score': score,
                            'performance': performance,
                            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'manual_bulk'
                        }
                        
                        st.session_state.students.append(new_student)
                        st.session_state.student_counter += 1
                        imported_count += 1
                        
                    except ValueError:
                        st.warning(f"Could not parse line: {line}")
            
            st.success(f"✅ Imported {imported_count} students from text!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Import from CSV
with tab4:
    st.markdown('<div class="add-student-form">', unsafe_allow_html=True)
    st.markdown("### 📁 Import from CSV/Excel")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload file with columns: Name, StudyHours, Score"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df_uploaded = pd.read_csv(uploaded_file)
            else:
                df_uploaded = pd.read_excel(uploaded_file)
            
            # Show preview
            st.markdown("#### File Preview:")
            st.dataframe(df_uploaded.head(), use_container_width=True)
            
            # Column mapping
            st.markdown("#### Map Columns:")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                name_col = st.selectbox(
                    "Name Column",
                    options=df_uploaded.columns.tolist(),
                    index=0 if 'Name' in df_uploaded.columns else 0
                )
            
            with col2:
                hours_col = st.selectbox(
                    "Study Hours Column",
                    options=df_uploaded.columns.tolist(),
                    index=1 if len(df_uploaded.columns) > 1 else 0
                )
            
            with col3:
                score_col = st.selectbox(
                    "Score Column",
                    options=df_uploaded.columns.tolist(),
                    index=2 if len(df_uploaded.columns) > 2 else 0
                )
            
            # Import button
            if st.button("📥 Import from File", type="primary"):
                imported_count = 0
                
                for _, row in df_uploaded.iterrows():
                    try:
                        name = str(row[name_col])
                        hours = float(row[hours_col])
                        score = float(row[score_col])
                        
                        # Determine performance
                        if score >= 85:
                            performance = "Excellent 🌟"
                        elif score >= 70:
                            performance = "Good 👍"
                        elif score >= 50:
                            performance = "Average 📊"
                        else:
                            performance = "Needs Improvement 📈"
                        
                        student_id = f"STU{st.session_state.student_counter:03d}"
                        
                        new_student = {
                            'id': student_id,
                            'name': name,
                            'study_hours': hours,
                            'final_score': score,
                            'performance': performance,
                            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'file_import'
                        }
                        
                        st.session_state.students.append(new_student)
                        st.session_state.student_counter += 1
                        imported_count += 1
                        
                    except (ValueError, KeyError):
                        continue
                
                st.success(f"✅ Successfully imported {imported_count} students from file!")
                st.balloons()
                st.rerun()
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # Download template
    st.markdown("---")
    st.markdown("#### 📋 Download Template")
    
    template_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'StudyHours': [4.5, 6.0, 3.5],
        'Score': [85, 92, 68]
    }
    
    template_df = pd.DataFrame(template_data)
    
    csv_template = template_df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV Template",
        data=csv_template,
        file_name="student_data_template.csv",
        mime="text/csv"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================
# STUDENT DISPLAY SECTION
# ===========================================
st.markdown("## 📊 Student Overview")

if st.session_state.students:
    # Convert to DataFrame
    students_df = pd.DataFrame(st.session_state.students)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(students_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_students}</div>
            <div class="metric-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_hours = students_df['study_hours'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_hours:.1f}</div>
            <div class="metric-label">Avg Study Hours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_score = students_df['final_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_score:.1f}%</div>
            <div class="metric-label">Avg Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if total_students > 1:
            correlation = np.corrcoef(students_df['study_hours'], students_df['final_score'])[0, 1]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{correlation:.3f}</div>
                <div class="metric-label">Correlation</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">-</div>
                <div class="metric-label">Correlation</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display student cards in an expandable section
    with st.expander(f"👁️ View All Students ({total_students})", expanded=True):
        # Filter options
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            filter_performance = st.selectbox(
                "Filter by Performance",
                options=["All", "Excellent 🌟", "Good 👍", "Average 📊", "Needs Improvement 📈"]
            )
        
        with col_filter2:
            sort_by = st.selectbox(
                "Sort by",
                options=["Name", "Study Hours", "Final Score", "Recently Added"]
            )
        
        with col_filter3:
            if st.button("🗑️ Clear All Students", type="secondary", use_container_width=True):
                st.session_state.students = []
                st.session_state.student_counter = 1
                st.success("All students cleared!")
                st.rerun()
        
        # Apply filters
        filtered_df = students_df.copy()
        
        if filter_performance != "All":
            filtered_df = filtered_df[filtered_df['performance'] == filter_performance]
        
        # Apply sorting
        if sort_by == "Name":
            filtered_df = filtered_df.sort_values('name')
        elif sort_by == "Study Hours":
            filtered_df = filtered_df.sort_values('study_hours', ascending=False)
        elif sort_by == "Final Score":
            filtered_df = filtered_df.sort_values('final_score', ascending=False)
        elif sort_by == "Recently Added":
            filtered_df = filtered_df.sort_values('added_date', ascending=False)
        
        # Display student cards
        for _, student in filtered_df.iterrows():
            # Determine card color based on performance
            if "Excellent" in student['performance']:
                border_color = "#4CAF50"
                bg_color = "#4CAF5020"
            elif "Good" in student['performance']:
                border_color = "#2196F3"
                bg_color = "#2196F320"
            elif "Average" in student['performance']:
                border_color = "#FF9800"
                bg_color = "#FF980020"
            else:
                border_color = "#F44336"
                bg_color = "#F4433620"
            
            st.markdown(f"""
            <div class="student-card" style="border-left-color: {border_color}; background-color: {bg_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #333;">{student['name']}</h4>
                        <p style="margin: 5px 0; color: #666; font-size: 14px;">ID: {student['id']} | Added: {student['added_date']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background-color: {border_color}40; padding: 4px 12px; border-radius: 15px; font-size: 12px;">
                            {student['performance']}
                        </span>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div>
                        <strong>Study Hours:</strong> {student['study_hours']} hrs/day
                    </div>
                    <div>
                        <strong>Final Score:</strong> {student['final_score']}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Visualization
    st.markdown("## 📈 Performance Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Scatter plot
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        scatter = ax1.scatter(
            students_df['study_hours'], 
            students_df['final_score'],
            c=students_df['final_score'],
            cmap='viridis',
            s=100,
            alpha=0.7
        )
        
        # Add trend line
        if total_students > 1:
            z = np.polyfit(students_df['study_hours'], students_df['final_score'], 1)
            p = np.poly1d(z)
            ax1.plot(students_df['study_hours'], p(students_df['study_hours']), "r--", alpha=0.8)
        
        ax1.set_xlabel('Study Hours (per day)')
        ax1.set_ylabel('Final Score (%)')
        ax1.set_title('Study Hours vs. Final Score')
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Final Score (%)')
        st.pyplot(fig1)
    
    with viz_col2:
        # Performance distribution
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        
        # Count performance categories
        perf_counts = students_df['performance'].value_counts()
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
        
        bars = ax2.bar(perf_counts.index, perf_counts.values, color=colors[:len(perf_counts)])
        ax2.set_xlabel('Performance Category')
        ax2.set_ylabel('Number of Students')
        ax2.set_title('Student Performance Distribution')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add count labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        st.pyplot(fig2)
    
    # Export data
    st.markdown("---")
    st.markdown("### 📤 Export Data")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        # Convert to CSV
        csv_data = students_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"student_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_export2:
        # Show data table
        if st.button("📋 View Data Table", use_container_width=True):
            st.dataframe(
                students_df[['id', 'name', 'study_hours', 'final_score', 'performance', 'added_date']],
                use_container_width=True,
                height=400
            )

else:
    # Empty state
    st.markdown("""
    <div style="text-align: center; padding: 50px; background-color: #f8f9fa; border-radius: 15px;">
        <h3 style="color: #667eea;">📭 No Students Added Yet!</h3>
        <p style="font-size: 16px; color: #666; margin: 20px 0;">
            Use the tabs above to add students to your dashboard.
        </p>
        <div style="margin-top: 30px;">
            <p>Choose from these options:</p>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                <div style="text-align: center;">
                    <div style="font-size: 24px;">📝</div>
                    <div><strong>Add Single</strong></div>
                    <div style="font-size: 12px;">Detailed entry</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px;">🎲</div>
                    <div><strong>Random</strong></div>
                    <div style="font-size: 12px;">Quick generation</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px;">📊</div>
                    <div><strong>Bulk Add</strong></div>
                    <div style="font-size: 12px;">Multiple at once</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px;">📁</div>
                    <div><strong>Import</strong></div>
                    <div style="font-size: 12px;">From files</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🎓 <strong>Student Performance Dashboard</strong> | Data Analytics Bootcamp</p>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Students: {len(st.session_state.students)}</p>
</div>
""")