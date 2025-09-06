from typing import Dict, List
#from app.models import UserData
from app.models import UserData, ExperienceItem, EducationItem
def to_frontend_userdata(user: UserData) -> Dict:
    icons = [
        {"id": 0, "image": "fa-github",    "url": "https://github.com/",        "handle": user.github or "",   "style": "socialicons"},
        {"id": 1, "image": "fa-facebook",  "url": "https://www.facebook.com/",  "handle": user.facebook or "", "style": "socialicons"},
        {"id": 2, "image": "fa-instagram", "url": "https://www.instagram.com/", "handle": user.instagram or "", "style": "socialicons"},
        {"id": 3, "image": "fa-linkedin",  "url": "https://linkedin.com/in/",   "handle": user.linkedin or "", "style": "socialicons"},
        {"id": 4, "image": "fa-twitter",   "url": "https://www.twitter.com/",   "handle": user.twitter or "",  "style": "socialicons"},
        {"id": 5, "image": "fa-medium",    "url": "https://www.medium.com/",    "handle": user.medium or "",   "style": "socialicons"},
    ]

    my_desc = [user.about] if user.about else []

    # fallbacks your frontend expects
    repos = user.repo_names or []
    projectDesc = user.project_desc or {}
    projectDates = user.project_dates or {}

    exp_legacy: List = []
    for e in user.experience:
        entry = [e.title, e.company, e.date_range, e.location, e.bullets]
        if e.more_bullets:
            entry.append(e.more_bullets)
        exp_legacy.append(entry)

    edu_legacy: List = []
    for ed in user.education:
        edu_legacy.append([
            ed.degree, ed.field, ed.institution, ed.start_date, ed.end_date,
            ed.location, ed.details, ed.courses
        ])

    return {
        "firstName": user.firstName,
        "lastName":  user.lastName,
        "headline":  user.headline,
        "icons":     icons,

        "instaLink":   user.insta_link or "",
        "instagramId": user.instagram or "",
        "instaQuerry": "/?__a=1",

        "myDescription": my_desc,

        "gitHubLink":   "https://api.github.com/users/",
        "githubId":     user.github or "",
        "gitHubQuerry": "/repos?sort=updated&direction=desc",

        "repos":        repos,
        "projectDesc":  projectDesc,
        "projectDates": projectDates,

        "experience":   exp_legacy,
        "education":    edu_legacy,
        "skills":       user.skills or [],
    }
def from_frontend_userdata(data: Dict) -> UserData:
    # pull socials from icons and githubId
    handles = {"github":"", "facebook":"", "instagram":"", "linkedin":"", "twitter":"", "medium":""}
    for icon in data.get("icons", []):
        img = (icon.get("image") or "").replace("fa-", "")
        h   = icon.get("handle") or ""
        if img in handles:
            handles[img] = h

    # experience nested arrays → objects
    exp_objs = []
    for row in data.get("experience", []):
        # row = [title, company, date_range, location, bullets, (optional) more_bullets]
        title      = row[0] if len(row) > 0 else ""
        company    = row[1] if len(row) > 1 else ""
        date_range = row[2] if len(row) > 2 else ""
        location   = row[3] if len(row) > 3 else ""
        bullets    = row[4] if len(row) > 4 else []
        more       = row[5] if len(row) > 5 else []
        exp_objs.append(ExperienceItem(
            title=title, company=company, date_range=date_range, location=location,
            bullets=bullets or [], more_bullets=more or []
        ))

    # education nested arrays → objects
    edu_objs = []
    for row in data.get("education", []):
        # [degree, field, institution, start_date, end_date, location, details[], courses[]]
        degree     = row[0] if len(row) > 0 else ""
        field      = row[1] if len(row) > 1 else ""
        institution= row[2] if len(row) > 2 else ""
        start_date = row[3] if len(row) > 3 else ""
        end_date   = row[4] if len(row) > 4 else ""
        location   = row[5] if len(row) > 5 else ""
        details    = row[6] if len(row) > 6 else []
        courses    = row[7] if len(row) > 7 else []
        edu_objs.append(EducationItem(
            degree=degree, field=field, institution=institution,
            start_date=start_date, end_date=end_date, location=location,
            details=details or [], courses=courses or []
        ))

    about = ""
    md = data.get("myDescription")
    if isinstance(md, list) and md:
        about = md[0] or ""

    return UserData(
        firstName=data.get("firstName",""),
        lastName=data.get("lastName",""),
        headline=data.get("headline",""),
        about=about,

        github=data.get("githubId","") or handles["github"],
        facebook=handles["facebook"],
        instagram=data.get("instagramId","") or handles["instagram"],
        linkedin=handles["linkedin"],
        twitter=handles["twitter"],
        medium=handles["medium"],

        insta_link=data.get("instaLink",""),
        education=edu_objs,
        experience=exp_objs,
        skills=data.get("skills",[]) or [],
        repo_names=data.get("repos",[]) or [],
        project_desc=data.get("projectDesc",{}) or {},
        project_dates=data.get("projectDates",{}) or {},
        raw_resume_text=""
    )