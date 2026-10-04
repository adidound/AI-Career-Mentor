import pandas as pd

from services.skill_normalizer import normalize_skill


ROLES_PATH = "data/it_roles_clean.csv"
ROLE_SKILLS_PATH = "data/role_skill_profiles.csv"
OUTPUT_PATH = "data/role_family_mapping.csv"


# --------------------------------------------------
# ROLE FAMILY RULES
# --------------------------------------------------

FAMILY_RULES = {

    "AI / Machine Learning": {
        "title_keywords": [
            "artificial intelligence",
            "machine learning",
            "ai researcher",
            "ai engineer",
            "ai architect",
            "deep learning",
            "natural language processing",
            "nlp",
        ],
        "skills": {
            "machine learning",
            "deep learning",
            "machine learning algorithms",
            "neural networks",
            "natural language processing",
            "computer vision",
            "data science",
            "tensorflow",
            "pytorch",
            "keras",
            "ai architecture",
            "ai/ml architecture",
            "ai/ml algorithms",
        },
    },

    "Data / Analytics": {
        "title_keywords": [
            "data analyst",
            "data scientist",
            "data engineer",
            "data architect",
            "data modeler",
            "data quality",
            "data warehouse",
            "big data",
            "business intelligence",
            "power bi",
        ],
        "skills": {
            "data analysis",
            "data science",
            "data modeling",
            "data mining",
            "data visualization",
            "data processing",
            "data warehousing",
            "data engineering",
            "data pipelines",
            "data cleansing",
            "data quality tools",
            "machine learning",
            "statistics",
            "statistical analysis",
            "statistical modeling",
            "hadoop",
            "spark",
            "power bi",
            "tableau",
            "etl",
        },
    },

    "Software Engineering": {
        "title_keywords": [
            "software engineer",
            "software developer",
            "software architect",
            "software development",
            "developer",
            "programmer",
            "coder",
            "application engineer",
            "application developer",
            "application designer",
            "full stack",
            "back end",
            "backend",
            "front end",
            "frontend",
            "java developer",
            "python developer",
            "c# developer",
            "php developer",
            "javascript developer",
            "ruby on rails",
        ],
        "skills": {
            "software development",
            "software design",
            "software architecture",
            "application development",
            "application design",
            "programming",
            "programming languages",
            "data structures",
            "algorithms",
            "git",
            "java",
            "python",
            "c",
            "c++",
            "c#",
            "javascript",
            "typescript",
            "php",
            "ruby",
        },
    },

    "Web Development": {
        "title_keywords": [
            "web developer",
            "web engineer",
            "web designer",
            "webmaster",
            "web producer",
            "front end",
            "frontend",
            "back end",
            "backend",
            "full stack",
            "wordpress",
        ],
        "skills": {
            "html",
            "css",
            "javascript",
            "web development",
            "web design",
            "responsive design",
            "wordpress",
            "react",
            "angular",
            "angularjs",
            "vue.js",
            "web api",
        },
    },

    "Cloud / Infrastructure": {
        "title_keywords": [
            "cloud",
            "infrastructure",
            "aws solutions architect",
            "azure",
            "gcp",
            "terraform",
            "kubernetes",
            "docker",
            "linux administrator",
        ],
        "skills": {
            "aws",
            "azure",
            "gcp",
            "cloud computing",
            "cloud architecture",
            "cloud networking",
            "cloud platforms",
            "cloud services",
            "docker",
            "kubernetes",
            "terraform",
            "linux",
            "virtualization",
            "infrastructure management",
            "infrastructure as code",
        },
    },

    "DevOps / SRE": {
        "title_keywords": [
            "devops",
            "devsecops",
            "site reliability",
            "sre",
            "build and release",
            "automation specialist",
            "release manager",
            "release engineer",
            "jenkins",
            "ansible",
            "puppet",
            "chef",
            "terraform",
            "platform engineer",
        ],
        "skills": {
            "devops",
            "devops practices",
            "devsecops",
            "ci/cd",
            "ci/cd pipelines",
            "jenkins",
            "github actions",
            "gitlab ci",
            "build automation",
            "deployment automation",
            "release management",
            "artifact repository",
            "ansible",
            "puppet",
            "chef",
            "terraform",
            "sre",
            "system reliability",
        },
    },

    "Cybersecurity": {
        "title_keywords": [
            "security",
            "cybersecurity",
            "cyber security",
            "infosec",
            "penetration tester",
            "forensic",
            "security analyst",
            "security engineer",
            "security specialist",
            "security consultant",
            "security administrator",
            "security manager",
        ],
        "skills": {
            "cybersecurity",
            "penetration testing",
            "ethical hacking",
            "digital forensics",
            "application security",
            "cloud security",
            "network security",
            "vulnerability assessment",
            "vulnerability management",
            "vulnerability scanning",
            "security analysis",
            "security auditing",
            "security management",
            "security policies",
            "security protocols",
            "secure coding",
            "cryptography",
            "encryption",
            "incident response",
            "threat analysis",
            "threat detection",
        },
    },

    "Networking": {
        "title_keywords": [
            "network",
            "networking",
            "network engineer",
            "network architect",
            "network analyst",
            "network operations",
            "network infrastructure",
        ],
        "skills": {
            "networking",
            "network security",
            "network operations",
            "network monitoring",
            "routing",
            "tcp/ip",
            "firewalls",
            "firewall management",
            "vpn",
            "cisco",
        },
    },

    "Database": {
        "title_keywords": [
            "database",
            "sql developer",
            "oracle developer",
            "oracle sql",
            "database administrator",
            "database analyst",
            "database architect",
        ],
        "skills": {
            "sql",
            "sql server",
            "t-sql",
            "pl/sql",
            "mysql",
            "postgresql",
            "oracle",
            "oracle database",
            "mongodb",
            "nosql",
            "database management",
            "database design",
            "database development",
            "databases",
        },
    },

    "Mobile Development": {
        "title_keywords": [
            "android",
            "ios",
            "mobile",
            "mobile app",
            "mobile application",
        ],
        "skills": {
            "android sdk",
            "android studio",
            "ios",
            "ios sdk",
            "mobile app development",
            "mobile development",
            "mobile security",
            "react native",
            "flutter",
            "xcode",
        },
    },

    "Testing / QA": {
        "title_keywords": [
            "qa engineer",
            "quality assurance",
            "software quality assurance",
            "selenium engineer",
            "pytest engineer",
            "junit engineer",
            "coverage.py engineer",
            "jacoco engineer",
        ],
        "skills": {
            "testing",
            "unit testing",
            "test automation",
            "automation testing",
            "agile testing",
            "accessibility testing",
            "performance testing",
            "code coverage",
            "quality assurance",
            "qa processes",
            "selenium",
            "pytest",
            "junit",
            "testng",
            "coverage.py",
            "jacoco",
            "test execution",
            "test planning",
            "testing frameworks",
            "static code analysis",
        },
    },
    
    "UI / UX": {
        "title_keywords": [
            "ui designer",
            "ux designer",
            "ux/ui",
            "ui/ux",
            "interaction designer",
            "information architect",
            "accessibility specialist",
        ],
        "skills": {
            "figma",
            "ui design",
            "ui/ux",
            "ui/ux design",
            "interaction design",
            "information architecture",
            "wireframing",
            "prototyping",
            "responsive design",
            "usability testing",
        },
    },

    "Animation / Multimedia": {
        "title_keywords": [
            "animator",
            "animation",
            "artist",
            "compositor",
            "motion graphics",
            "vfx",
            "visual effects",
            "storyboard",
            "multimedia",
        ],
        "skills": {
            "2d animation",
            "3d animation",
            "3d modeling",
            "animation direction",
            "animation software",
            "character design",
            "cinematography",
            "blender",
            "maya",
            "motion graphics",
            "storyboarding",
            "video production",
            "visual effects",
        },
    },

    "Hardware / Embedded": {
        "title_keywords": [
            "hardware",
            "embedded",
            "firmware",
            "circuit",
            "cnc",
        ],
        "skills": {
            "hardware management",
            "hardware/software",
            "circuit design",
            "control systems",
            "cnc programming",
            "rtos",
        },
    },

    "Robotics": {
        "title_keywords": [
            "robotics",
            "robot",
        ],
        "skills": {
            "robotics",
            "ros",
            "rtos",
            "control systems",
        },
    },

    "Enterprise / Business Systems": {
        "title_keywords": [
            "erp",
            "salesforce",
            "sap",
            "confluence engineer",
            "tfs engineer",
            "sharepoint",
            "microsoft dynamics",
            "business systems",
        ],
        "skills": {
            "erp systems",
            "salesforce",
            "sharepoint",
            "microsoft dynamics",
            "sap modules",
            "business systems",
            "crm",
            "customer relationship management",
        },
    },

    "IT Operations": {
        "title_keywords": [
            "it support",
            "help desk",
            "systems administrator",
            "system administrator",
            "operations engineer",
            "it auditor",
            "support engineer",
            "it technician",
            "it administrator",
            "technical operations",
        ],
        "skills": {
            "system administration",
            "systems administration",
            "it support",
            "technical support",
            "troubleshooting",
            "incident management",
            "infrastructure management",
            "windows server",
            "linux administration",
        },
    },

    "Project / Product Management": {
        "title_keywords": [
            "project manager",
            "program manager",
            "product manager",
            "technical product manager",
            "chief technology officer (cto)",
            "digital transformation consultant",
            "iteration manager",
            "technology adoption manager",
            "program management",
            "portfolio manager",
            "project management",
        ],
        "skills": {
            "project management",
            "program management",
            "product management",
            "portfolio management",
            "planning",
            "roadmap planning",
            "stakeholder management",
            "requirements gathering",
        },
    },

    "Research": {
        "title_keywords": [
            "research",
            "scientist",
        ],
        "skills": {
            "research methods",
            "research methodologies",
            "research management",
            "statistical analysis",
            "statistical modeling",
            "scientific writing",
        },
    },

    "Marketing / SEO": {
        "title_keywords": [
            "seo",
            "search engine optimization",
            "marketing",
        ],
        "skills": {
            "seo",
            "seo strategy",
            "keyword research",
            "link building",
            "off-page optimization",
            "on-page optimization",
            "web analytics tools",
            "content marketing",
        },
    },

    "Finance / Business": {
        "title_keywords": [
            "finance",
            "financial",
            "sales",
            "account manager",
            "technical account",
        ],
        "skills": {
            "financial analysis",
            "budgeting",
            "investment management",
            "sales",
            "sales leadership",
            "sales strategy",
            "technical sales",
            "account management",
        },
    },

    "GIS / Geospatial": {
        "title_keywords": [
            "gis",
            "geographic information",
            "geospatial",
        ],
        "skills": {
            "gis software",
            "cartography",
            "spatial analysis",
        },
    },

    "Game Development": {
        "title_keywords": [
            "game",
            "unity",
            "unreal",
        ],
        "skills": {
            "game engines",
            "game development",
            "game design",
            "unity",
            "unity3d engine",
            "unreal engine",
        },
    },

    "API / Integration": {
        "title_keywords": [
            "api",
            "integration",
            "mulesoft",
            "micro services",
            "microservices",
        ],
        "skills": {
            "api design",
            "api development",
            "rest apis",
            "restful apis",
            "restful services",
            "web api",
            "integration",
            "systems integration",
            "service discovery",
            "service mesh",
            "microservices",
        },
    },
}


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

roles_df = pd.read_csv(
    ROLES_PATH,
    encoding="cp1252"
)

profiles_df = pd.read_csv(
    ROLE_SKILLS_PATH
)


# --------------------------------------------------
# PREPARE ROLE SKILLS
# --------------------------------------------------

role_skills = (
    profiles_df
    .groupby("normalized_title")["canonical_skill"]
    .apply(set)
    .to_dict()
)


# --------------------------------------------------
# CLASSIFY ROLE
# --------------------------------------------------

def classify_role(role_title, skills):

    title = str(role_title).strip().lower()

    normalized_skills = {
        normalize_skill(skill)
        for skill in skills
        if normalize_skill(skill)
    }

    scores = {}

    for family, rules in FAMILY_RULES.items():

        score = 0

        # Title evidence is stronger.
        for keyword in rules["title_keywords"]:
            if keyword in title:
                score += 3

        # Skill evidence provides supporting evidence.
        skill_matches = normalized_skills.intersection(
            rules["skills"]
        )

        score += len(skill_matches)

        if score > 0:
            scores[family] = score

    if not scores:
        return ["Unclassified"]

    max_score = max(scores.values())

    # Keep families with strong evidence.
    selected = [
        family
        for family, score in scores.items()
        if score >= max_score * 0.6
    ]

    return sorted(
        selected,
        key=lambda family: scores[family],
        reverse=True
    )


# --------------------------------------------------
# BUILD MAPPING
# --------------------------------------------------

records = []

for role in roles_df["normalized_title"].dropna().unique():

    skills = role_skills.get(role, set())

    families = classify_role(
        role,
        skills
    )

    for family in families:

        records.append({
            "normalized_title": role,
            "role_family": family,
        })


result = pd.DataFrame(records)


result = result.drop_duplicates(
    subset=[
        "normalized_title",
        "role_family"
    ]
)


result = result.sort_values(
    [
        "normalized_title",
        "role_family"
    ]
)


result.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("=" * 60)
print("ROLE FAMILY CLASSIFICATION")
print("=" * 60)

print(
    f"Total normalized roles : "
    f"{roles_df['normalized_title'].nunique()}"
)

print(
    f"Role-family mappings   : "
    f"{len(result)}"
)

print(
    f"Families used          : "
    f"{result['role_family'].nunique()}"
)

print()
print("Role family counts:")
print(
    result["role_family"]
    .value_counts()
    .to_string()
)

print()
print(f"Saved to: {OUTPUT_PATH}")