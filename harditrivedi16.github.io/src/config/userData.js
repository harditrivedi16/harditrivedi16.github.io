let userData = {
  firstName: "Hardi",
  lastName: "Trivedi",
  headline:
    "Software Engineer | ML Engineer | AI Researcher",
  icons: [
    {
      id: 0,
      image: "fa-github",
      url: "https://github.com/",
      handle: "harditrivedi16",
      style: "socialicons",
    },
    
    {
      id: 1,
      image: "fa-facebook",
      url: "https://www.facebook.com/",
      handle: "",
      style: "socialicons",
    },
    {
      id: 2,
      image: "fa-instagram",
      url: "https://www.instagram.com/",
      handle: "",
      style: "socialicons",
    },
    {
      id: 3,
      image: "fa-linkedin",
      url: "https://linkedin.com/in/",
      handle: "harditrivedi",
      style: "socialicons",
    },
    
    {
      id: 4,
      image: "fa-twitter",
      url: "https://www.twitter.com/",
      handle: "",
      style: "socialicons",
    },
    {
      id: 5,
      image: "fa-medium",
      url: "https://www.medium.com/",
      handle: "",
      style: "socialicons",
    },
  ],
  instaLink: "https://linkedin.com/in/harditrivedi/",
  instagramId: "nachiket_trivedi",
  instaQuerry: "/?__a=1",

  myDescription: [
    `I’m Hardi Trivedi, a Software Engineer with nearly 3 years of experience across industry and AI research, and a Master’s 
     in CS(AI). I bring strengths of a software engineer with domain expertise in machine learning, skilled in building scalable 
     full-stack systems and developing intelligent models that solve real-world problems.

     Currently at Learn2AI, I design GenAI applications for ed-tech, working on user-facing tools, APIs, and data pipelines while 
     mentoring interns and leading deployments. Previously, I built a React-based portfolio management platform at Lotus 
     Infosystems used by 300+ users, and a healthcare prediction tool at Sahyog that supported clinics during COVID-19

     I also have significant research experience focused on advancing NLP for practical impact. I have published two 
     IEEE papers—one on localizing LLMs for low-resource languages, and another introducing a novel retrieval method that won 
     Best Paper at CAI 2025.

     I’m skilled in Software development (React, Node.js, Java, Python), scalable ML pipelines, and integrating Gen AI into
      practical applications. Because of my background in SDE, MLE, and AI research, I can bring strong AI insights to an SDE team,
       and I’m seeking extremely exciting roles where I can contribute at a much bigger scale!`,
  ],
  gitHubLink: "https://api.github.com/users/",
  githubId: "harditrivedi16",
  gitHubQuerry: "/repos?sort=updated&direction=desc",
  repos: [
    "Educational-Gen-AI-Agent",
    "Time-Aware-Retrieval-Augmented-Language-Model",
    "OpenAI_MERN_ImageGenerator_App ",
    "AI-powered-Portfolio-Maker",
    "Text-Concise-AI",
    "LLM-Based-Localization-in-the-Context-of-Low-Resource-Languages",
    "Knowledge-Retrieval-Interface",
    "Image-Classification--258",
    "Fever-based-Automated-fact-Checking",
  ],
  projectDesc: {
    "Educational-Gen-AI-Agent": [
      "An end-to-end Generative AI Agent Chatbot designed for interactive educational content delivery.", 
      "The system combines a JavaScript-based frontend with MCP and LangGraph-powered agentic workflows, offering a responsive user experience.",
      
    ],
    "OpenAI_MERN_ImageGenerator_App ":[
      "Constructed a React & Node app for rendering AI-generated images from prompts.",
      "Used OpenAI's DALLE API for real-time image generation and S3 to store and manage 1,000+ images from various prompts.",
    ],

    "AI-powered-Portfolio-Maker":[
      "Developed a React and Node.js web application with interactive UI components for creating customised portfolios in under 10 minutes",
      "Engineered backend automation for portfolio generation and export, evolving personal project into a full-stack frontend-focused application.",

    ],
    "Time-Aware-Retrieval-Augmented-Language-Model": [
      "TempRALM-a temporally aware retrieval-augmented language model which considers both the semantic and temporal relevance of retrieved documents",
      "This paper was presented at the 'IEEE Conference on Artificial Intelligence, 2025' and was also awarded the Best Paper Award.",
    ],
    "AI-powered-Portfolio-Make": [
      "Developed a React and Node.js web application with interactive UI components for creating customised portfolios in under 10 minutes.",
      "Engineered an AI-driven system that parses resumes and automatically generates and deploys live portfolios.",
    ],
    "Text-Concise-AI": [
      "Fine-tuned the Pegasus model for text summarization task built an end-to-end pipeline that includes data ingestion, validation, transformation, model training, and evaluation",
      " The model achieved a ROUGE score of 0.4,was deployed on an AWS EC2 instance and leveraged a  (CI/CD) pipeline to ensure deployment.",
    ],
    "LLM-Based-Localization-in-the-Context-of-Low-Resource-Languages": [
      "Evaluate the mBART models for low-resource Indian languages, including Hindi and Gujarati, and explore a sample Human Resources use case",
      "We focus on neural machine translation based on transfer learning, multilingual meta-learning, and zero-shot approaches",
    ],
    "Knowledge-Retrieval-Interface": [
      "Developed a non-root approach for dynamic malware detection in Android and wrote a research paper based on it.",
      "Became the youngest author to get the paper accepted at the reputed ICISS 2017, and received an IEEE award for the same.",
    ],
    "Image-Classification--258": [
      "Classified Images with Wildfire, by extractring frames from Youtube Videos",
      "Compared the performance of VGG-16 to ResNET",
    ],
    "Fever-based-Automated-fact-Checking": [
      "Applied ATLAS framework for FEVER-based fact-checking and question-answering tasks, specifically focusing on the 'Speed and Language Processing' textbook",
      "By leveraging a distributed computing , we utilized ATLAS's few-shot learning capabilities, which notably reduced the training time by 50%",
    ],
    
  },
  
  projectDates: {
    "Educational-Gen-AI-Agent":"2025",
    "Time-Aware-Retrieval-Augmented-Language-Model":" 2025",
    "OpenAI_MERN_ImageGenerator_App ":"2025",
    "AI-powered-Portfolio-Maker":" 2025",
    "Text-Concise-AI":" 2024",
    "LLM-Based-Localization-in-the-Context-of-Low-Resource-Languages":"2024",
    "Knowledge-Retrieval-Interface":"2024",
    "Image-Classification--258":"2024",
    "Fever-based-Automated-fact-Checking":" 2023",
  },
  
  experience: [
    [
      "Software Engineer (Gen AI Applications)",
      "Learn2AI.",
      " Jan 2025 - Current ",
      "Remote",
      [
        "Developed a responsive ed-tech web application with React and Tailwind, enabling seamless access to multimedia course content and interactive learning modules.",
        "Integrated REST APIs with frontend components and architected modular backend services in C++ and Python on GCP with CI/CD pipelines, supporting ~50 queries per minute.",
        "Implemented semantic search and summarisation features using Spark and GPT-4, improving content discovery and learner engagement.",
        "Authored documentation while mentoring 10 interns on frontend integration, API usage, and SWE best practices.",
      ],
    ],
    [
      "Applied Researcher",
      "San Jose State University",
      "Aug 2023 - May 2025",
      "San Jose, CA",
      [
        "Invented a novel retrieval algorithm for time-sensitive information and an automated dataset curation technique.",
        "Improved retrieval accuracy by 74% over baseline and 32% over a commercial RAG system.",
        
      ],
      [
        "Built a GenAI agent for Gujarati and Hindi, enhancing translation quality by 5–6% (BLEU).",
        "Achieved 93% response accuracy in HR domain case-study trials using a React + REST API integration with the agent.",
        
      ]
    ],
    [
      "Software Development Engineer",
      "Lotus Infosystems",
      "May 2021 - August 2022",
      " India",
      [
        "Built an interactive data visualisation dashboard in React and JavaScript, with CSS3, for real-time portfolio tracking and predictive insights.",
        "Designed intuitive and interactive UI components such as chart visualisations, filter panels, and accessibility features, significantly improving usability and engagement for 300+ active users.",
        "Connected the React frontend with a backend built in Java Lambdas and PostgreSQL through REST APIs, implementing state management (Redux) and lazy loading for dynamic and responsive data updates.",
        "Deployed services via CI/CD pipelines, maintaining 99% uptime and reducing dashboard data load latency by ~250ms, ensuring smooth and reliable user interactions.",
        
      ],
    ],
    [
      "Software Engineer",
      "Sahyog, Centre for Promoting Health",
      "Nov 2020 - May 2021",
      "India",
      [
        "Developed a React-based frontend for a COVID-19 prediction system, enabling intuitive interaction with patient data and predictions.",
        "Connected the frontend with a Flask backend consisting of a fine-tuned VGG16 model, providing the beta system to 10 clinics and improving patient consultation efficiency by ~30%. ",
      ],
    ],
  ],
  education: [
    [
      "Master of Science",
      "Artificial Intelligence",
      "San Jose State University",
      "Aug 2022",
      "AUG 2024",
      "San Jose, CA",
      
      [
        "Graduate Research Assistant in the domain of Machine Learning and NLP.",
        "Working with Professor Jorjeta Jetcheva for domain Large Language Models.",
        "Managed the Machine Learning coursework for the Summer Tech Academy, an initiative designed for California high school students. This ambitious program was funded by a $2.5M National Science Foundation grant, aiming to provide hands-on Computer Science education to underrepresented communities.",
      ],
      [
        "Machine Learning",
        "Enterprise Distributed Systems",
        "Natural Language Processing",
        "Data Mining",
        "Recommendation Systems and Web Mining",
        "Reinforcement Learning",
        "Maths for Artificial Intelligence",
        "Deep Learning",
      ],
    ],
    [
      "Bachelor of Technology",
      "Information and Communication Technology",
      "Ahmedabad University",
      "Aug 2017",
      "May 2021",
      " India",
      
      [
        "Led a 30+ member programming club for 1.5 years, organizing coding workshops, hackathons, and mentorship programs to foster a strong tech community among students.",
        
      ],
      
      [
        "Big Data Engineering",
        "Software Engineering",
        "Software Project Management",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Neural Networks",
        "Theory of Computation",
        "Logic for Computer Science",
      ],
      
    ],
  ],
  skills: [
    "Python",
    "C++",
    "Java",
    "R",
    "JavaScript",
    "TypeScript",
    "GoLang",
    "Scikit-Learn",
    "Pytorch",
    "Transformers(LLMs)",
    "Langchain",
    "LangGraph",
    "FAISS",
    "Vector DBs",
    "RAG",
    "React",
    "NodeJS",
    "Flask",
    "RestAPI",
    "FastAPI",
    "Spark",
    "Git",
    "SpringBoot",
    "SQL",
    "MySQL",
    "PostgresSQL",
    "MongoDB",
    "AWS",
    "Azure",
    "GCP",
    "CI/CD Pipeline",
  ],
};

export default userData;
