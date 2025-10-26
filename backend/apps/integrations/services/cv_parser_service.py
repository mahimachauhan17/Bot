import PyPDF2
import docx
import re
from django.core.files.uploadedfile import UploadedFile

class CVParserService:
    """
    Service for parsing CV files (PDF, DOCX, TXT)
    Extracts structured data from resumes
    """
    
    def parse_cv(self, cv_file):
        """
        Parse a CV file and extract structured information
        
        Args:
            cv_file: UploadedFile object
            
        Returns:
            dict: Parsed CV data
        """
        file_ext = cv_file.name.lower()[cv_file.name.rfind('.'):]
        
        # Extract text based on file type
        if file_ext == '.pdf':
            text = self._extract_text_from_pdf(cv_file)
        elif file_ext in ['.docx', '.doc']:
            text = self._extract_text_from_docx(cv_file)
        elif file_ext == '.txt':
            text = cv_file.read().decode('utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Parse the extracted text
        parsed_data = self._parse_text(text)
        
        return parsed_data
    
    def _extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    def _extract_text_from_docx(self, docx_file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")
    
    def _parse_text(self, text):
        """
        Parse extracted text to structured data
        
        This is a basic implementation. In production, you would use:
        - NLP models for better extraction
        - Named Entity Recognition (NER)
        - AI services like OpenAI for intelligent parsing
        """
        parsed_data = {
            'full_name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'location': self._extract_location(text),
            'linkedin_url': self._extract_linkedin(text),
            'summary': self._extract_summary(text),
            'technical_skills': self._extract_skills(text),
            'soft_skills': [],
            'languages': [],
            'certifications': self._extract_certifications(text),
            'work_experience': self._extract_work_experience(text),
            'education': self._extract_education(text),
            'projects': [],
            'total_experience_years': self._calculate_experience_years(text)
        }
        
        return parsed_data
    
    def _extract_name(self, text):
        """Extract candidate name (usually first line)"""
        lines = text.strip().split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 2:
                # Likely a name (short, at top)
                return line
        return "Unknown"
    
    def _extract_email(self, text):
        """Extract email address"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text):
        """Extract phone number"""
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}'
        matches = re.findall(phone_pattern, text)
        # Filter out likely false positives (too short)
        valid_phones = [m for m in matches if len(re.sub(r'[^0-9]', '', m)) >= 10]
        return valid_phones[0] if valid_phones else None
    
    def _extract_location(self, text):
        """Extract location/address"""
        # Basic pattern for city, state/country
        location_keywords = ['location', 'address', 'based in', 'residing in']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in location_keywords):
                # Next line might be the location
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        
        return None
    
    def _extract_linkedin(self, text):
        """Extract LinkedIn URL"""
        linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/in/[\w-]+'
        matches = re.findall(linkedin_pattern, text)
        return matches[0] if matches else None
    
    def _extract_summary(self, text):
        """Extract professional summary"""
        summary_keywords = ['summary', 'profile', 'objective', 'about']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Collect next few lines as summary
                summary_lines = []
                for j in range(i + 1, min(i + 6, len(lines))):
                    if lines[j].strip() and not any(kw in lines[j].lower() for kw in ['experience', 'education', 'skills']):
                        summary_lines.append(lines[j].strip())
                    else:
                        break
                return ' '.join(summary_lines) if summary_lines else None
        
        return None
    
    def _extract_skills(self, text):
        """Extract technical skills"""
        # Common technical skills (expandable)
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'spring', 'sql', 'nosql', 'mongodb', 'postgresql',
            'mysql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'ci/cd',
            'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
            'html', 'css', 'rest api', 'graphql', 'microservices', 'agile', 'scrum'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills[:15]  # Return top 15 skills found
    
    def _extract_certifications(self, text):
        """Extract certifications"""
        cert_keywords = ['certified', 'certification', 'certificate']
        lines = text.split('\n')
        
        certifications = []
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications
    
    def _extract_work_experience(self, text):
        """Extract work experience (basic)"""
        # This is a simplified version
        # In production, use NER or AI parsing
        experiences = []
        
        # Look for job titles, companies, dates
        # Placeholder structure
        experiences.append({
            'company': 'Company Name',
            'title': 'Job Title',
            'start_date': '2020-01',
            'end_date': '2023-12',
            'description': 'Job responsibilities and achievements',
            'achievements': []
        })
        
        return experiences
    
    def _extract_education(self, text):
        """Extract education history"""
        education = []
        
        # Look for degree keywords
        degree_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.tech', 'm.tech', 'mba']
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in degree_keywords):
                education.append({
                    'degree': line.strip(),
                    'institution': 'University Name',
                    'field': 'Computer Science',
                    'start_date': None,
                    'end_date': None,
                    'gpa': None
                })
        
        return education
    
    def _calculate_experience_years(self, text):
        """Calculate total years of experience"""
        # Look for phrases like "5 years experience", "5+ years"
        exp_pattern = r'(\d+)[\+]?\s*(years?|yrs?)\s*(of\s*)?(experience|exp)'
        matches = re.findall(exp_pattern, text.lower())
        
        if matches:
            years = [int(match[0]) for match in matches]
            return max(years) if years else 0
        
        return 0
