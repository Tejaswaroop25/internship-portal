from backend.models.internship import Internship

class RecommendationService:
    @staticmethod
    def parse_skills(skills_str):
        """Parse comma-separated skill strings into a clean set of normalized skills."""
        if not skills_str:
            return set()
        return {skill.strip().lower() for skill in skills_str.split(',') if skill.strip()}

    @classmethod
    def calculate_match(cls, student_skills_str, internship_requirements_str):
        """
        Calculate matching percentage and detailed skills comparison.
        Returns a dict:
        - match_score: int (0 to 100)
        - matched_skills: list
        - missing_skills: list
        - category: string ('Excellent Match', 'Good Match', 'Partial Match', 'Low Match')
        """
        student_skills = cls.parse_skills(student_skills_str)
        internship_reqs = cls.parse_skills(internship_requirements_str)

        if not internship_reqs:
            # If no specific requirements, it's a general match
            return {
                'match_score': 100 if student_skills else 50,
                'matched_skills': list(student_skills),
                'missing_skills': [],
                'category': 'Excellent Match' if student_skills else 'Good Match'
            }

        # Calculate matching sets
        matched_set = student_skills.intersection(internship_reqs)
        missing_set = internship_reqs.difference(student_skills)

        match_score = int((len(matched_set) / len(internship_reqs)) * 100)

        # Match category mapping
        if match_score >= 80:
            category = 'Excellent Match'
        elif match_score >= 50:
            category = 'Good Match'
        elif match_score >= 20:
            category = 'Partial Match'
        else:
            category = 'Low Match'

        # Match skill names back to original casing from requirements if possible
        original_reqs = [s.strip() for s in internship_requirements_str.split(',') if s.strip()]
        matched_skills = []
        missing_skills = []

        for req in original_reqs:
            if req.lower() in matched_set:
                matched_skills.append(req)
            else:
                missing_skills.append(req)

        return {
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'category': category
        }

    @classmethod
    def get_recommendations(cls, student):
        """
        Get all internships with calculated match details, sorted by compatibility.
        """
        if student.role != 'student':
            return []

        all_internships = Internship.query.all()
        recommendations = []

        for internship in all_internships:
            match_details = cls.calculate_match(student.skills, internship.requirements)
            
            # Additional detail for UI styling class
            score = match_details['match_score']
            if score >= 80:
                ui_class = 'match-excellent'
            elif score >= 50:
                ui_class = 'match-good'
            elif score >= 20:
                ui_class = 'match-partial'
            else:
                ui_class = 'match-low'

            recommendations.append({
                'internship': internship,
                'match_score': score,
                'matched_skills': match_details['matched_skills'],
                'missing_skills': match_details['missing_skills'],
                'category': match_details['category'],
                'ui_class': ui_class
            })

        # Sort recommendations by match_score in descending order
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations
