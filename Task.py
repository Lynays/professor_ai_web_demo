from agent import*

request_understand_task = Task(
    description = """
    Analyze the user's teaching request.
    Find the user's request in:
        {user_request}
    Extract:
    - Topic
    - Target Audience
    - Teaching Style
    - Depth
    - Special Requirements
    """,

    expected_output = """
    {
        "topic":"",
        "target_audience":"",
        "teaching_style":"",
        "depth":"",
        "special_requirements":[]
    }
    """,

    agent = Rqst_Understander
)
pdf_reader_task = Task(
    description = """
    Analyze the uploaded PDF located at:

    {pdf_path}
    Using the tool:PDFSearchTool
    Extract:
    - Core Concepts
    - Definitions
    - Formulas
    - Examples
    - Practices
    - Supplementary Materials
    """,

    expected_output = """
    {
        "core_concepts":[],
        "definitions":[],
        "formulas":[],
        "examples":[],
        "practices":[],
        "supplementary_materials":[]
    }
    """,

    agent = pdf_reader
)
dependency_analysis_task = Task(
    description = """
    Analyze prerequisite knowledge required to understand
    the concepts extracted from the PDF.

    Determine:
    - prerequisite concepts
    - missing foundations
    - recommended teaching order
    """,
    context = [pdf_reader_task],
    expected_output = """
    {
        "required_prerequisites":[],
        "must_explain_before_main_topic":[],
        "recommended_order":[]
    }
    """,

    agent = dependency_analyzer
)

outline_builder_task = Task(
    description = """
    Build a detailed teaching outline.

    Use:
    - user requirements
    - pdf analysis
    - prerequisite analysis

    Create a complete lesson plan.
    """,
    context = [pdf_reader_task,
               dependency_analysis_task,
               request_understand_task],
    expected_output = """
    {
        "lesson_flow":[
            {
                "title":"",
                "objective":"",
                "concepts":[]
            }
        ]
    }
    """,

    agent = outline_builder
)
outline_checker_task = Task(
    description = """
    Verify that the lesson outline:

    - Covers all important concepts
    - Has proper teaching order
    - Matches requested depth
    - Contains no major redundancy
    """,
    context = [outline_builder_task,pdf_reader_task],
    expected_output = """
    {
        "coverage_score":0,
        "ordering_ok":true,
        "depth_ok":true,
        "redundancy_found":false,
        "missing_topics":[],
        "repair_needed":true
    }
    """,

    agent = outline_checker
)
repair_task = Task(
    description = """
    Repair the lesson outline according to the checker report.
    IF repair_needed is false:
        Output the orignal outline unchanged
    IF repair_needed is true:
        Fix:
        - Missing concepts
        - Wrong order
        - Insufficient depth
        - Redundant sections
    """,
    context = [outline_builder_task,
               outline_checker_task],
    expected_output = """
    Revised lesson outline
    """,

    agent = repair_agent
)
lecturer_task = Task(
    description = f"""
    Deliver the lesson.

    IMPORTANT:
    The entire lesson MUST be written in CHINESE.
    Do NOT use any other language unless explicitly required.
    Requirements:

    - Explain step by step.
    - Use analogies.
    - Use examples.
    - Explain prerequisites first.
    - Do NOT skip intermediate reasoning.
    - Assume the student's level specified earlier.
    """,
    context = [repair_task,request_understand_task],
    expected_output = """
    Complete lecture notes in Markdown.

    Example:

    # Topic

    ## Intuition

    ## Definition

    ## Example

    ## Summary
    """,

    agent = lecturer
)
comprehension_check_task = Task(
    description = """
    Generate questions to evaluate understanding.

    Questions should test:
    - conceptual understanding
    - intuition
    - application
    """,
    context = [lecturer_task],
    expected_output = """
    {
        "questions":[
            {
                "question":"",
                "difficulty":"easy"
            }
        ]
    }
    """,

    agent = comprehension_checker
)
answer_evaluation_task = Task(
    description = """
    Evaluate the student's answers.

    Identify:
    - mastered concepts
    - misunderstood concepts
    - concepts needing review
    """,

    expected_output = """
    {
        "score":0,
        "mastered":[],
        "needs_review":[],
        "misunderstood":[]
    }
    """,

    agent = answer_evaluator
)
qa_task = Task(
    description = """
    Answer follow-up questions about the lesson.

    Use:
    - lecture content
    - PDF content
    - previous explanations

    Maintain consistency with earlier teaching.
    """,

    expected_output = """
    Detailed answer.
    """,

    agent = qa_agent
)