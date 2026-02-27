"""
Company Configuration
Contains company details for branding and reports
"""

COMPANY_INFO = {
    "name": "PGT International (Private) Limited",
    "address": "PGT Building, Al-Aziz Block, Pakpattan Road, Sahiwal",
    "phone": "0300-1210706",
    "email": "ceo@pgtinternational.com",
    "website": "http://www.pgtinternational.com",
    "logo_path": "static/logo.png",  # Path to company logo
    "tagline": "Excellence in Transportation & Logistics"
}

def get_company_info():
    """Returns company information dictionary"""
    return COMPANY_INFO

def get_company_header():
    """Returns formatted company header for reports"""
    return {
        "name": COMPANY_INFO["name"],
        "address": COMPANY_INFO["address"],
        "contact": f"Phone: {COMPANY_INFO['phone']} | Email: {COMPANY_INFO['email']}",
        "website": COMPANY_INFO["website"]
    }
